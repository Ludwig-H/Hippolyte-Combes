#!/usr/bin/env python3
"""Exports de la transcription dans l'ordre de lecture restitué.

  transcriptions/livre_journal_transcription.md    lecture courante (Markdown ; soulignés, lettres suscrites,
                                                   biffures et ajouts rendus par des balises HTML simples)
  transcriptions/livre_journal_donnees.json        données complètes de chaque page (transcription balisée,
                                                   apparat, registres, feuillet, cliché)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

import balisage

EDITION = Path(__file__).resolve().parents[1]
RACINE = EDITION.parent
SORTIE = RACINE / "transcriptions"


def charger(p: Path):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def folio(c: dict) -> str:
    if c.get("feuillet") is None:
        return "couverture"
    return "f. %d %s" % (c["feuillet"], "r°" if c["face"] == "r" else "v°")


def md_ligne(s: str) -> str:
    """Balisage diplomatique -> Markdown/HTML lisible."""
    def groupe(s, i):
        prof, j = 0, i
        while j < len(s):
            if s[j] == "{":
                prof += 1
            elif s[j] == "}":
                prof -= 1
                if prof == 0:
                    return s[i + 1:j], j + 1
            j += 1
        return s[i + 1:], len(s)
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([a-zA-Z]+)", s[i:])
            nom = m.group(1)
            i += len(m.group(0))
            if nom in ("sl", "sll", "del", "add", "addm", "inc"):
                a, i = groupe(s, i)
                a = md_ligne(a)
                out.append({"sl": "<ins>%s</ins>", "sll": "<ins><ins>%s</ins></ins>", "del": "<del>%s</del>", "add": "\\%s/",
                            "addm": "\\%s/ (en marge)", "inc": "%s [?]"}[nom] % a)
            elif nom == "sur":
                a, i = groupe(s, i)
                b, i = groupe(s, i)
                out.append("%s [sur %s]" % (md_ligne(b), md_ligne(a)))
            elif nom == "fr":
                a, i = groupe(s, i)
                b, i = groupe(s, i)
                out.append("%s/%s" % (a, b))
            elif nom == "ill":
                m2 = re.match(r"\[(\d+)\]", s[i:])
                if m2:
                    i += len(m2.group(0))
                    out.append("[%s mots illis.]" % m2.group(1))
                else:
                    out.append("[illis.]")
            elif nom == "lac":
                out.append("[lacune]")
            elif nom == "hfill":
                out.append("    ")
            elif nom == "trait":
                out.append(" ——")
        elif c == "^":
            a, i = groupe(s, i + 1)
            out.append("<sup>%s</sup>" % md_ligne(a))
        else:
            j = i
            while j < len(s) and s[j] not in "\\^":
                j += 1
            out.append(s[i:j])
            i = j
    return "".join(out)


def main() -> None:
    codico = charger(EDITION / "donnees" / "codicologie.yaml")["cliches"]
    lecture = sorted((c for c in codico if c["statut"] in ("page", "couverture")), key=lambda c: c["ordre"])
    SORTIE.mkdir(exist_ok=True)
    md = ["# Hippolyte Combes, *Livre-Journal* (25 juillet 1916 – 30 avril 1917)", "",
          "Transcription diplomatique dans l'ordre de lecture restitué (feuillets reliés en tête ; voir l'introduction de l'édition). "
          "Conventions : <ins>souligné</ins>, <sup>suscrit</sup>, <del>biffé</del>, \\ajout/, [?] lecture incertaine, [illis.] mot illisible ; "
          "les lignes du carnet sont conservées. L'apparat et les commentaires figurent dans l'édition imprimée "
          "(`edition/livre_journal.pdf`) et dans `livre_journal_donnees.json`.", ""]
    donnees = []
    for c in lecture:
        n = c["cliche"]
        p = charger(EDITION / "donnees" / "pages" / f"{n:03d}.yaml")
        md += [f"## {folio(c)} — {p.get('date', '')}", ""]
        if p.get("lieux"):
            md += [f"*{p['lieux']}*", ""]
        lignes = []
        for r in balisage.analyser(p["transcription"]):
            if r.type == "texte":
                pre = "    " * int(r.retrait) if r.retrait else ""
                lignes.append(f"{r.numero:>3}  {pre}{md_ligne(r.corps)}")
            elif r.type == "filet":
                lignes.append("     " + "—" * 12)
            else:
                lignes.append("")
        md += ["<pre>"] + lignes + ["</pre>", ""]
        donnees.append({"cliche": n, "fichier": c["fichier"], "ordre": c["ordre"], "feuillet": c.get("feuillet"),
                        "face": c.get("face"), "folio": folio(c),
                        **{k: p.get(k) for k in ("date", "mois", "lieux", "titre", "transcription", "apparat",
                                                  "critique", "historique", "sources") if p.get(k) is not None}})
    (SORTIE / "livre_journal_transcription.md").write_text("\n".join(md), encoding="utf-8")
    (SORTIE / "livre_journal_donnees.json").write_text(json.dumps(donnees, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(donnees)} pages exportées -> {SORTIE}")


if __name__ == "__main__":
    main()
