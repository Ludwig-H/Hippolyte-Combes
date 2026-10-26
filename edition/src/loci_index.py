"""Occurrences des personnes et des lieux : renvois internes (loci paralleli) et index finaux."""
from __future__ import annotations

import re
import unicodedata

from balisage import texte_simple


def _folio(c: dict) -> str:
    if c.get("feuillet") is None:
        return "couv."
    return r"f.~%d~%s" % (c["feuillet"], r"r\textsuperscript{o}" if c["face"] == "r" else r"v\textsuperscript{o}")


def _cle_tri(s: str) -> str:
    s = re.sub(r"\\[a-zA-Z]+\{?|[{}]", "", s)
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch)).lower()


def _motifs(entite: dict) -> list[re.Pattern]:
    out = []
    for f in entite.get("formes", []):
        out.append(re.compile(r"(?<![\w-])" + f + r"(?![\w])"))
    return out


def occurrences(lecture: list[dict], pages: dict[int, dict], entites: dict) -> dict:
    """{(categorie, id): [(cliche, ligne), ...]} dans l'ordre de lecture."""
    occ: dict = {}
    for cat in ("personnes", "lieux"):
        for e in entites.get(cat, []) or []:
            motifs = _motifs(e)
            liste, pos = [], {}
            for c in lecture:
                n = c["cliche"]
                p = pages.get(n)
                if not p or not p.get("transcription"):
                    continue
                for k, ligne in enumerate(texte_simple(p["transcription"]), 1):
                    trouves = [x.start() for x in (m.search(ligne) for m in motifs) if x]
                    if trouves:
                        liste.append((n, k))
                        pos[(n, k)] = min(trouves)
            # attestations ajoutées à la main (formes abrégées non repérables automatiquement)
            for n, k in e.get("attestations", []) or []:
                if (n, k) not in liste:
                    liste.append((n, k))
                    # place dans la ligne, pour l'ordre des renvois d'une même ligne : nom court, sans accents
                    lignes = texte_simple(pages[n]["transcription"]) if pages.get(n) else []
                    if 0 < k <= len(lignes):
                        i = _cle_tri(lignes[k - 1]).find(_cle_tri(e.get("court", e["nom"])))
                        if i >= 0:
                            pos[(n, k)] = i
            ordre = {c["cliche"]: c["ordre"] for c in lecture}
            liste.sort(key=lambda x: (ordre.get(x[0], 0), x[1]))
            if liste:
                occ[(cat, e["id"])] = {"entite": e, "occ": liste, "pos": pos}
    return occ


SEUIL_LOCI = 12  # au-delà de ce nombre de pages, l'entité (Marguerite, Curtis, Acheux…) n'est que dans l'index


def loci_par_page(lecture: list[dict], occ: dict, info: dict[int, dict]) -> dict[int, str]:
    """Pour chaque page : renvois vers l'occurrence précédente et suivante de chaque entité.

    Les entités omniprésentes (plus de SEUIL_LOCI pages) ne sont pas reprises : l'index y supplée."""
    par_page: dict[int, list[tuple[int, str]]] = {}
    for (cat, _), d in occ.items():
        e, liste = d["entite"], d["occ"]
        pages_vues = []
        for n, k in liste:
            if not pages_vues or pages_vues[-1][0] != n:
                pages_vues.append((n, k))
        if len(pages_vues) > SEUIL_LOCI or e.get("sans_loci"):
            continue
        for i, (n, k) in enumerate(pages_vues):
            refs = []
            if i > 0:
                m, l = pages_vues[i - 1]
                refs.append(r"supra %s, l.~%d~(p.~\pageref{cl%03d})" % (_folio(info[m]), l, m))
            if i + 1 < len(pages_vues):
                m, l = pages_vues[i + 1]
                refs.append(r"infra %s, l.~%d~(p.~\pageref{cl%03d})" % (_folio(info[m]), l, m))
            if refs:
                nom = e.get("court", e["nom"])
                par_page.setdefault(n, []).append((k, d.get("pos", {}).get((n, k), 999),
                                                   r"\textbf{%d}~%s\,] cf. %s" % (k, nom, " ; ".join(refs))))
    # même ligne : dans l'ordre d'apparition dans la ligne
    return {n: "~— ".join(t for _, _, t in sorted(v)) + "." for n, v in par_page.items()}


def index_latex(occ: dict, info: dict[int, dict], entites: dict) -> str:
    if not occ:
        return ""
    out = []
    for cat, titre in (("personnes", "Index des noms de personnes"), ("lieux", "Index des noms de lieux")):
        entrees = [(d["entite"], d["occ"]) for (c, _), d in occ.items() if c == cat]
        entrees.sort(key=lambda x: _cle_tri(x[0]["nom"]))
        out.append(r"\LJindex{%s}{%%" % titre)
        for e, liste in entrees:
            vus, refs = set(), []
            for n, k in liste:
                if n in vus:
                    continue
                vus.add(n)
                refs.append(r"%s~(p.~\pageref{cl%03d})" % (_folio(info[n]), n))
            notice = (r", \textit{%s}" % e["notice"]) if e.get("notice") else ""
            out.append(r"\LJentree{%s%s}{%s}" % (e["nom"], notice, ", ".join(refs)))
        out.append("}")
    return "\n".join(out)
