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
    def lien(m):
        brut = m.group(0)
        url = brut.rstrip(".,;")
        # Une parenthèse de la phrase reste hors du lien ; une parenthèse
        # équilibrée appartenant à l'URL reste dans celui-ci.
        while url.endswith(")") and url.count(")") > url.count("("):
            url = url[:-1]
        ponctuation = brut[len(url):]
        url = url.replace(r"\_", "_").replace(r"\%", "%").replace(r"\&", "&").replace(r"\#", "#")
        return r"\url{%s}" % url + ponctuation
    s = re.sub(r"https?://\S+", lien, s)
    return s


MOIS = ("janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre|"
        "January|February|March|April|May|June|July|August|September|October|November|December")


def _typo(s: str) -> str:
    """Typographie de l'éditeur, hors des adresses (\\url{…}) : demi-cadratin dans les intervalles de
    nombres, n\\textsuperscript{o}, 1\\textsuperscript{er}, espaces insécables (jour et mois, sigle ou
    abréviation et numéro, nombre et unité)."""
    morceaux = re.split(r"(\\url\{[^}]*\})", s)
    for i in range(0, len(morceaux), 2):
        t = morceaux[i]
        # intervalles : 1890-1900, 1862-1914 (pas les cotes du type 224-8 ou 1/2-013396-G)
        t = re.sub(r"(?<![\w/.\-])(\d{2,4})-(\d{2,4})(?![\w/\-])", r"\1--\2", t)
        t = re.sub(r"\b1er\b", r"1\\textsuperscript{er}", t)
        t = re.sub(r"n°\s*", r"n\\textsuperscript{o}~", t)
        t = re.sub(r"\b(\d{1,2}|1\\textsuperscript\{er\}) (%s)\b" % MOIS, r"\1~\2", t)
        t = re.sub(r"\b(Q|A|C|inv\.|f\.|p\.|réf\.|Nr\.|vol\.|t\.) (\d)", r"\1~\2", t)
        t = re.sub(r"(\d) (km|ans)\b", r"\1~\2", t)
        morceaux[i] = t
    return "".join(morceaux)


def _majuscule(s: str) -> str:
    """Majuscule initiale (première lettre hors commande LaTeX)."""
    m = re.match(r"((?:\\[A-Za-z]+\{)*)([^\W\d_])", s)
    return s if not m else s[:m.end(1)] + m.group(2).upper() + s[m.end(2):]


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
            credit = "%s Source : %s ; licence : %s" % (_tex(e.get("auteur", "")), _tex(e.get("source", "")), _tex(e.get("licence", "")))
            image = r"\textit{%s} — %s" % (_tex(leg).rstrip("."), _tex(str(date)).rstrip("."))
            lignes.append(r"%s & %s\\" % (_majuscule(_typo(image)), _majuscule(_typo(credit))))
        elif nom in famille:
            e = famille[nom]
            image = _tex(e.get("legende", "")).rstrip(".")  # colonne Image : sans point final
            credit = "Archives familiales (%s)." % _tex(e.get("origine", ""))
            lignes.append(r"%s & %s\\" % (_majuscule(_typo(image)), _majuscule(_typo(credit))))
    tex = r"""\section{Sources des illustrations}\label{annexe-illustrations}

Les fac-similés reproduisent les photographies du carnet prises le 26~novembre 2025, redressées et recadrées au bord du feuillet, l'éclairage et le ton du papier égalisés d'une page à l'autre (l'écriture n'est pas retouchée), et les numérisations des pièces annexes, redressées et recadrées au bord du papier ; les cartes ont été dessinées pour la présente édition (sources indiquées sous chacune d'elles). Les photographies, lettres de guerre, notes et feuillets autographes (\textit{Feuillets de Route}) appartiennent aux archives familiales des descendants d'Hippolyte Combes, communiquées par Pierre Combes et Pierre-Alain Hauseux. Les images d'époque, toutes dans le domaine public ou sous licence libre, sont reproduites avec les mentions demandées par les institutions qui les conservent.

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
    tex = re.sub(r"«[ \t]+", "«~", re.sub(r"[ \t]+»", "~»", tex))  # guillemets insécables
    (EDITION / "textes" / "annexe_illustrations.tex").write_text(tex, encoding="utf-8")
    print(f"{len(lignes)} illustrations -> textes/annexe_illustrations.tex")


if __name__ == "__main__":
    main()
