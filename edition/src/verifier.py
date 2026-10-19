#!/usr/bin/env python3
"""Vérifications de l'édition : données, balisage, compilation, vis-à-vis et polices du PDF."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ICI = Path(__file__).resolve().parent
EDITION = ICI.parent
sys.path.insert(0, str(ICI))
import balisage  # noqa: E402

TYPES = {"abreviation", "emprunt", "lecture", "rature", "ajout", "surcharge", "disposition", "compte",
         "graphie", "correction", "signe", "syntaxe", "autre"}


def charger(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def verifier_donnees(erreurs: list[str]) -> list[dict]:
    codico = charger(EDITION / "donnees" / "codicologie.yaml")["cliches"]
    if len(codico) != 186:
        erreurs.append(f"codicologie : 186 clichés attendus, {len(codico)} trouvés")
    pages = [c for c in codico if c["statut"] in ("page", "couverture")]
    ordres = sorted(c["ordre"] for c in pages)
    if ordres != list(range(len(pages))):
        erreurs.append("codicologie : ordre de lecture non continu")
    feuillets = {}
    for c in pages:
        if c["statut"] == "page":
            feuillets.setdefault(c["feuillet"], []).append(c["face"])
    for f, faces in feuillets.items():
        if sorted(faces) not in (["r"], ["r", "v"]):
            erreurs.append(f"codicologie : feuillet {f} faces {faces}")
    for c in pages:
        p = EDITION / "donnees" / "pages" / f"{c['cliche']:03d}.yaml"
        if not p.exists():
            erreurs.append(f"page manquante : {p.name}")
            continue
        d = charger(p)
        try:
            rangees = balisage.analyser(d["transcription"])
        except Exception as e:  # noqa: BLE001
            erreurs.append(f"{p.name} : balisage : {e}")
            continue
        n = sum(1 for r in rangees if r.type == "texte")
        for e in d.get("apparat") or []:
            if not 1 <= int(e.get("ligne", 0)) <= n:
                erreurs.append(f"{p.name} : apparat hors limites (ligne {e.get('ligne')})")
            if e.get("type") not in TYPES:
                erreurs.append(f"{p.name} : type d'apparat inconnu {e.get('type')}")
            try:
                balisage.rendre(str(e.get("lemme", "")))
            except Exception as ex:  # noqa: BLE001
                erreurs.append(f"{p.name} : lemme mal balisé ({ex})")
        for champ in ("date", "lieux"):
            if not d.get(champ) and c["statut"] == "page":
                erreurs.append(f"{p.name} : champ {champ} vide")
    return pages


def verifier_compilation(erreurs: list[str], avertissements: list[str]) -> None:
    log = EDITION / "livre_journal.log"
    if not log.exists():
        erreurs.append("journal de compilation absent")
        return
    t = log.read_text(encoding="utf-8", errors="replace")
    if re.search(r"^! ", t, re.M):
        erreurs.append("erreur LaTeX dans le journal")
    if "There were undefined references" in t or re.search(r"Reference `[^']+' on page \d+ undefined", t):
        erreurs.append("références indéfinies")
    if "Label(s) may have changed" in t:
        avertissements.append("étiquettes modifiées : relancer la compilation")
    trop = [l for l in re.findall(r"^LJJEU (\S+) (\d+) ([\d.]+)pt ([\d.]+)pt", t, re.M) if float(l[2]) > float(l[3]) + 0.5]
    for lab, jeu, h, th in trop:
        erreurs.append(f"page de transcription {lab} trop pleine même au plus petit corps ({h} > {th} pt)")
    jeux = re.findall(r"^LJJEU \S+ (\d+)", t, re.M)
    if jeux:
        from collections import Counter
        avertissements.append("corps de transcription employés (jeu: nombre de pages) : " +
                              ", ".join(f"{k}: {v}" for k, v in sorted(Counter(jeux).items(), key=lambda x: int(x[0]))))
    over = re.findall(r"Overfull \\vbox \(([\d.]+)pt too high\)", t)
    if over:
        avertissements.append(f"{len(over)} boîtes verticales trop pleines (max {max(map(float, over)):.1f} pt)")


def verifier_pdf(pages: list[dict], erreurs: list[str], avertissements: list[str]) -> None:
    pdf = EDITION / "livre_journal.pdf"
    aux = EDITION / "livre_journal.aux"
    if not pdf.exists() or not aux.exists():
        erreurs.append("PDF ou fichier .aux absent")
        return
    lab = dict(re.findall(r"\\newlabel\{(cl\d{3}(?:-fac)?)\}\{\{[^{}]*\}\{(\d+)\}", aux.read_text(encoding="utf-8")))
    for c in pages:
        n = c["cliche"]
        a, b = lab.get(f"cl{n:03d}"), lab.get(f"cl{n:03d}-fac")
        if a is None or b is None:
            erreurs.append(f"cliché {n:03d} : étiquettes absentes")
            continue
        a, b = int(a), int(b)
        if a % 2 or b != a + 1:
            erreurs.append(f"cliché {n:03d} : vis-à-vis rompu (transcription p. {a}, fac-similé p. {b})")
    import pymupdf
    d = pymupdf.open(pdf)
    polices = set()
    for i in range(0, d.page_count, 7):
        for f in d[i].get_fonts():
            polices.add(f[3].split("+")[-1])
    if not any(p.startswith("LibertinusSerif") for p in polices):
        erreurs.append(f"Libertinus absente du PDF ({sorted(polices)[:6]})")
    w, h = d[0].rect.width / 72 * 25.4, d[0].rect.height / 72 * 25.4
    if abs(w - 160) > 0.6 or abs(h - 226) > 0.6:
        erreurs.append(f"format de page inattendu : {w:.1f} × {h:.1f} mm")
    avertissements.append(f"PDF : {d.page_count} pages, {pdf.stat().st_size / 1e6:.1f} Mo")


def main() -> int:
    erreurs, avertissements = [], []
    pages = verifier_donnees(erreurs)
    verifier_compilation(erreurs, avertissements)
    verifier_pdf(pages, erreurs, avertissements)
    for a in avertissements:
        print("note :", a)
    for e in erreurs:
        print("ERREUR :", e)
    print("vérification :", "échec" if erreurs else "réussie", f"({len(erreurs)} erreur(s))")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
