#!/usr/bin/env python3
"""Vérifications de l'édition : données, balisage, compilation, vis-à-vis et polices du PDF."""
from __future__ import annotations

import hashlib
import json
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
    if sorted(c["cliche"] for c in codico) != list(range(1, 187)):
        erreurs.append("codicologie : numéros de clichés manquants ou répétés")
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
        if d.get("cliche") != c["cliche"] or d.get("fichier") != c["fichier"]:
            erreurs.append(f"{p.name} : photographie différente de la concordance codicologique")
        if not (EDITION.parent / "scans_haute_qualite" / c["fichier"]).is_file():
            erreurs.append(f"{p.name} : photographie source absente")
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


def verifier_export(pages: list[dict], erreurs: list[str]) -> None:
    chemin = EDITION.parent / "transcriptions" / "livre_journal_donnees.json"
    if not chemin.exists():
        erreurs.append("export JSON absent")
        return
    export = json.loads(chemin.read_text(encoding="utf-8"))
    lecture = sorted(pages, key=lambda c: c["ordre"])
    if [p.get("cliche") for p in export] != [c["cliche"] for c in lecture]:
        erreurs.append("export JSON : pages absentes, répétées ou dans un autre ordre")
        return
    for c, p in zip(lecture, export):
        source = charger(EDITION / "donnees" / "pages" / f"{c['cliche']:03d}.yaml")
        for champ in ("fichier", "ordre", "feuillet", "face"):
            if p.get(champ) != c.get(champ):
                erreurs.append(f"export JSON {c['cliche']:03d} : {champ} périmé")
        for champ in ("date", "mois", "lieux", "titre", "transcription", "apparat", "critique", "historique", "sources"):
            if p.get(champ) != source.get(champ):
                erreurs.append(f"export JSON {c['cliche']:03d} : {champ} périmé")


def verifier_compilation(erreurs: list[str], avertissements: list[str]) -> None:
    log = EDITION / "livre_journal.log"
    if not log.exists():
        erreurs.append("journal de compilation absent")
        return
    t = log.read_text(encoding="utf-8", errors="replace")
    if re.search(r"^! ", t, re.M):
        erreurs.append("erreur LaTeX dans le journal")
    for message in set(re.findall(r"^Missing character:.*", t, re.M)):
        erreurs.append(message)
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
    lab = dict(re.findall(r"\\newlabel\{(cl\d{3}(?:-fac)?)\}\{\{[^{}]*\}\{([^{}]+)\}", aux.read_text(encoding="utf-8")))
    import pymupdf
    d = pymupdf.open(pdf)
    if not d.page_count:
        erreurs.append("PDF vide ou compilation inachevée")
        return
    # Pagination multiple (romains, arabes, romains majuscules) : rang physique de chaque étiquette de page.
    rang = {}
    for i in range(d.page_count):
        rang.setdefault(d[i].get_label() or str(i + 1), i + 1)
    for c in pages:
        n = c["cliche"]
        a, b = lab.get(f"cl{n:03d}"), lab.get(f"cl{n:03d}-fac")
        if a is None or b is None:
            erreurs.append(f"cliché {n:03d} : étiquettes absentes")
            continue
        pa, pb = rang.get(a), rang.get(b)
        if pa is None or pb is None:
            erreurs.append(f"cliché {n:03d} : page {a} ou {b} absente du PDF")
            continue
        if pa % 2 or pb != pa + 1 or not a.isdigit() or int(a) % 2:
            erreurs.append(f"cliché {n:03d} : vis-à-vis rompu (transcription p. {a}, fac-similé p. {b} ; rangs {pa}, {pb})")
        lab[f"cl{n:03d}-fac"] = str(pb)
    polices = set()
    for i, page in enumerate(d):
        for f in page.get_fonts():
            polices.add(f[3].split("+")[-1])
        w, h = page.rect.width / 72 * 25.4, page.rect.height / 72 * 25.4
        if abs(w - 160) > 0.6 or abs(h - 226) > 0.6:
            erreurs.append(f"p. {i + 1} : format inattendu : {w:.1f} × {h:.1f} mm")
        for bloc in page.get_text("dict")["blocks"]:
            for ligne in bloc.get("lines", []):
                for morceau in ligne["spans"]:
                    x0, y0, x1, y1 = morceau["bbox"]
                    if morceau["text"].strip() and (x0 < -0.5 or y0 < -0.5 or x1 > page.rect.width + 0.5 or y1 > page.rect.height + 0.5):
                        erreurs.append(f"p. {i + 1} : texte hors page : {morceau['text']!r}")
        for lien in page.get_links():
            if lien["kind"] == pymupdf.LINK_GOTO and not 0 <= lien.get("page", -1) < d.page_count:
                erreurs.append(f"p. {i + 1} : lien interne hors du PDF")
    # Vérifier l'image réellement incorporée, au-delà de la seule parité des étiquettes.
    empreintes = {}
    for c in pages:
        cible = lab.get(f"cl{c['cliche']:03d}-fac")
        if cible is None or not cible.isdigit() or not 1 <= int(cible) <= d.page_count:
            erreurs.append(f"cliché {c['cliche']:03d} : fac-similé hors du PDF")
            continue
        source = EDITION / "fac-similes" / f"{c['cliche']:03d}.jpg"
        if not source.exists():
            erreurs.append(f"fac-similé préparé absent : {source.name}")
            continue
        attendu = hashlib.sha256(source.read_bytes()).hexdigest()
        images = []
        for im in d[int(cible) - 1].get_images():
            if im[0] not in empreintes:
                empreintes[im[0]] = hashlib.sha256(d.extract_image(im[0])["image"]).hexdigest()
            images.append(empreintes[im[0]])
        if attendu not in images:
            erreurs.append(f"cliché {c['cliche']:03d} : image du fac-similé différente de celle attendue")
    if not any(p.startswith("LibertinusSerif") for p in polices):
        erreurs.append(f"Libertinus absente du PDF ({sorted(polices)[:6]})")
    avertissements.append(f"{len(pages)} vis-à-vis et images incorporées contrôlés ; export JSON confronté aux YAML")
    avertissements.append(f"PDF : {d.page_count} pages, {pdf.stat().st_size / 1e6:.1f} Mo")


def main() -> int:
    erreurs, avertissements = [], []
    pages = verifier_donnees(erreurs)
    verifier_export(pages, erreurs)
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
