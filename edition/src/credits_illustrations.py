#!/usr/bin/env python3
"""Annexe « Sources des illustrations » : relève les images citées par l'édition (ouvertures de chapitre,
textes) et écrit textes/annexe_illustrations.tex à partir des catalogues :
  illustrations/epoque/catalogue.yaml  images d'époque (auteur, source, licence)
  illustrations/famille.yaml           archives familiales
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

EDITION = Path(__file__).resolve().parents[1]


def _tex(s: str) -> str:
    s = str(s or "").strip()
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\\textit{\1}", s)
    s = s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#").replace("_", r"\_")
    s = re.sub(r"https?://\S+", lambda m: r"\url{%s}" % m.group(0).replace(r"\_", "_").replace(r"\%", "%").rstrip(".,;)"), s)
    return s


def images_citees() -> list[str]:
    vus: list[str] = []
    chap = yaml.safe_load((EDITION / "donnees" / "chapitres.yaml").read_text(encoding="utf-8"))["chapitres"]
    textes = sorted((EDITION / "textes").rglob("*.tex"))
    sources = [yaml.safe_dump(c, allow_unicode=True) for c in chap] + [t.read_text(encoding="utf-8") for t in textes]
    for s in sources:
        for m in re.finditer(r"illustrations/((?:epoque/)?[A-Za-z0-9_\-]+\.(?:jpe?g|png))", s):
            if m.group(1) not in vus:
                vus.append(m.group(1))
    return vus


def main() -> None:
    epoque = yaml.safe_load((EDITION / "illustrations" / "epoque" / "catalogue.yaml").read_text(encoding="utf-8")) or {}
    famille = yaml.safe_load((EDITION / "illustrations" / "famille.yaml").read_text(encoding="utf-8")) or {}
    lignes = []
    for img in images_citees():
        nom = img.split("/")[-1]
        if img.startswith("epoque/") and nom in epoque:
            e = epoque[nom]
            leg = e.get("lieu", "")
            date = e.get("date", "")
            credit = "%s Source : %s Licence : %s" % (_tex(e.get("auteur", "")), _tex(e.get("source", "")), _tex(e.get("licence", "")))
            lignes.append(r"\textit{%s} — %s & %s\\" % (_tex(leg).rstrip("."), _tex(str(date)).rstrip("."), credit))
        elif nom in famille:
            e = famille[nom]
            lignes.append(r"%s & Archives familiales (%s).\\" % (_tex(e.get("legende", "")), _tex(e.get("origine", ""))))
    tex = r"""\section{Sources des illustrations}\label{annexe-illustrations}

Les fac-similés reproduisent les photographies du carnet prises le 26 novembre 2025 ; les cartes ont été dessinées pour la présente édition (sources indiquées sous chacune d'elles). Les photographies et documents de famille appartiennent aux archives des descendants d'Hippolyte Combes. Les images d'époque, toutes dans le domaine public ou sous licence libre, sont reproduites avec les mentions demandées par les institutions qui les conservent.

{\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{50mm}>{\raggedright\arraybackslash}p{88mm}@{}}
\toprule
\textbf{Image} & \textbf{Auteur, source et licence}\\
\midrule\endhead
\bottomrule\endfoot
""" + "\n".join(lignes) + r"""
\end{longtable}}
"""
    (EDITION / "textes" / "annexe_illustrations.tex").write_text(tex, encoding="utf-8")
    print(f"{len(lignes)} illustrations -> textes/annexe_illustrations.tex")


if __name__ == "__main__":
    main()
