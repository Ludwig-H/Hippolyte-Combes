"""Mise en page d'une double page : transcription et apparat (page paire), fac-similé (page impaire)."""
from __future__ import annotations

import re

from balisage import Rangee, _brut, analyser, rendre

HAUTEUR = {"texte": 1.0, "filet": 0.5}
LIGNE_DE_BASE = 0.76  # position de la ligne de base dans une rangée de texte (en interlignes)


def echapper(s: str) -> str:
    """Échappe un texte éditorial ordinaire (pas de balisage diplomatique)."""
    if s is None:
        return ""
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%")
             .replace("#", r"\#").replace("_", r"\_").replace("$", r"\$"))


_DIPLO = {"sll": r"\LJsll", "sl": r"\LJsl", "del": r"\LJdel", "addm": r"\LJaddm", "add": r"\LJadd",
          "inc": r"\LJinc", "fr": r"\LJfrac"}


def date_ed(s: str) -> str:
    """Date éditoriale (en-tête, concordance) : « 1er » avec l'exposant."""
    return re.sub(r"\b1er\b", r"1\\textsuperscript{er}", editorial(s))


def editorial(s: str) -> str:
    """Texte éditorial en LaTeX simple (en-tête, registres critique et historique).

    Convertit le balisage diplomatique qui y est cité (^{te}, \\sl{…}, \\inc{…}, \\ill…) et échappe
    les & % # laissés nus ; le reste (\\textit{}, « », etc.) passe tel quel."""
    if not s:
        return ""
    s = str(s).strip()
    s = re.sub(r"\\(sll|sl|del|addm|add|inc|fr)\{", lambda m: _DIPLO[m.group(1)] + "{", s)
    s = re.sub(r"\\sur\{([^{}]*)\}\{([^{}]*)\}", r"\2", s)
    s = re.sub(r"\\ill\[(\d+)\]", r"\\LJill{\1}", s)
    s = re.sub(r"\\ill(?![a-zA-Z{])", r"\\LJill{}", s)
    s = re.sub(r"(?<![\\\w{])(\d+)--(\d+)(?!\w)", r"\\mbox{\1--\2}", s)  # intervalle jamais coupé
    s = re.sub(r"\\lac(?![a-zA-Z])", r"\\LJlac{}", s)
    s = re.sub(r"\\trait(?![a-zA-Z])", "—", s)
    s = re.sub(r"\\hfill(?![a-zA-Z])\s*", " ", s)
    s = re.sub(r"«[ \t]+", "«~", s)
    s = re.sub(r"[ \t]+»", "~»", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"\\textsuperscript{\1}", s)
    s = re.sub(r"\^([A-Za-z0-9])", r"\\textsuperscript{\1}", s)
    s = re.sub(r"(?<!\\)([&%#])", r"\\\1", s)
    return s


def _hauteur(r: Rangee) -> float:
    if r.type == "blanc":
        return r.blanc
    return HAUTEUR[r.type]


def _signes_latex(rangees: list[Rangee], i: int) -> str:
    r = rangees[i]
    out = []
    for sg in r.signes:
        # hauteur couverte : de la rangée i jusqu'à la n-ième ligne de texte comprise
        h, vus, j = 0.0, 0, i
        while j < len(rangees):
            h += _hauteur(rangees[j])
            if rangees[j].type == "texte":
                vus += 1
                if vus == sg.n:
                    break
            j += 1
        if sg.nom == "accolade":
            out.append(r"\LJaccolade{%.3f}{%s}" % (h, rendre(sg.etiquette)))
        else:
            out.append(r"\LJ%s{%.3f}" % (sg.nom, h))
    return "".join(out)


def colonne_transcription(rangees: list[Rangee]) -> tuple[str, dict[int, float]]:
    """Renvoie le LaTeX des rangées et la position (ligne de base, en interlignes) de chaque ligne."""
    lignes, positions, y = [], {}, 0.0
    for i, r in enumerate(rangees):
        if r.type == "texte":
            positions[r.numero] = y + LIGNE_DE_BASE
            num = str(r.numero) if r.numero % 5 == 0 else ""
            # trait de l'auteur : au milieu de la ligne, longueur fixe ; en fin de ligne, jusqu'au bout de la colonne
            latex = re.sub(r"\\LJtrait\{\}(?=\s*[^\s}])", r"\\LJtraitc{}", r.latex)
            pleine = r"\hfill" in latex or (r"\LJtrait{}" in latex and r.alignement == "g")
            macro = r"\LJtp" if pleine else r"\LJt"
            lignes.append("%s{%s}{%g}{%s}{%s}{%s}" % (
                macro, num, 1.2 * r.retrait, r.alignement, _signes_latex(rangees, i), latex))
        elif r.type == "filet":
            lignes.append(r"\LJf{%s}{%g}" % (r.filet_pos, r.filet_frac))
        else:
            lignes.append(r"\LJb{%g}" % r.blanc)
        y += _hauteur(r)
    return "\n".join(lignes), positions


TYPES_IMPRIMES = None  # tous les types d'entrées sont imprimés


def _langue(note: str) -> str:
    """Langue d'un emprunt : latin si la note le dit, anglais sinon."""
    return "lat." if re.search(r"\blatin\b|^lat\.", note) else "angl."


def _sans_langue(note: str, lemme: str) -> str:
    """Retire de la note d'un emprunt la mention de langue, que l'apparat imprime déjà (« angl. », « lat. »)."""
    n = re.sub(r"^\s*(angl\.|anglais|lat\.|latin)\s*:?\s*", "", note)
    n = re.sub(r"^\(latin\)\s*|\s*\(latin\)", "", n)
    l = re.escape(re.sub(r"\\[a-z]+\{([^{}]*)\}", r"\1", str(lemme)).strip())
    n = re.sub(r"\s*\((?:anglais|angl\.)\s+%s\)" % l, "", n, flags=re.I) if l else n
    n = re.sub(r"^(?:angl\.|anglais)\s+%s\s*:\s*" % l, "", n, flags=re.I) if l else n
    return n.strip()


def _note(e: dict) -> str:
    lemme = e.get("lemme", "")
    lemme = "" if lemme is None else str(lemme)
    note = e.get("note", "")
    note = "" if note is None else str(note)
    t = e.get("type", "")
    lemme = re.sub(r"\s*\\hfill\s*", " … ", lemme)  # un blanc de la ligne ne s'imprime pas dans le lemme
    lem = rendre(lemme) if lemme else ""
    if t == "emprunt":
        corps = r"\textit{%s} " % _langue(note) + _angl(editorial(_sans_langue(note, lemme))) if note else ""
    elif t == "abreviation":
        # le développement en italique ; un commentaire (après « ; », « : » ou entre parenthèses) en romain
        m = re.search(r" ; | : | \(", note)
        dev, sep, reste = (note[:m.start()], m.group(0), note[m.end():]) if m else (note, "", "")
        corps = r"\textit{%s}" % editorial(dev) + (sep + _angl(editorial(reste)) if sep else "")
    else:
        corps = _angl(editorial(note))
    # « [illis.] » des notes automatiques : « illis. » en italique, comme dans la transcription (\LJill)
    lem, corps = (x.replace("[illis.]", r"[\textit{illis.}]") for x in (lem, corps))
    if lem:
        # lemme court : jamais coupé en fin de ligne
        if len(_brut(lemme)) <= 24:
            lem = r"\mbox{%s}" % lem
        return r"{\LJpolice %s}\,]\enspace %s" % (lem, corps)
    return corps


def _angl(s: str) -> str:
    """« angl. » écrit dans une remarque de l'éditeur : en italique, comme dans les notes d'emprunt ; l'autre
    lecture proposée reste sur la ligne de « lecture : »."""
    s = re.sub(r"(lectures? :) ", r"\1~", s)
    return re.sub(r"(?<![\\\w{])angl\.", r"\\textit{angl.}", s)


def colonne_apparat(apparat: list[dict], positions: dict[int, float], notes_auto: dict[int, list],
                    textes: dict[int, str] | None = None) -> str:
    """Regroupe les entrées par ligne, dans l'ordre où leurs lemmes figurent sur la ligne, et produit les
    appels \\LJapp."""
    textes = textes or {}
    par_ligne: dict[int, list[tuple[int, int, str]]] = {}

    def ajouter(n, lemme, e):
        lig = textes.get(n, "")
        brut = _brut(str(lemme or "")).strip()
        pos = lig.find(brut) if brut and lig else -1
        liste = par_ligne.setdefault(n, [])
        liste.append((pos if pos >= 0 else 10 ** 6, len(liste), _note(e)))

    def cle(x) -> str:
        return re.sub(r"[\s?.,;:«»()'’-]+", " ", _brut(str(x or ""))).strip().lower()

    # une note automatique (rature, ajout, surcharge tirées du balisage) sur le même mot qu'une note de l'éditeur
    # est fondue avec elle, ou omise si la note de l'éditeur la contient déjà
    manuelles = {}
    for e in apparat:
        manuelles.setdefault((int(e.get("ligne", 0)), cle(e.get("lemme", ""))), []).append(e)
    fusion: dict[int, dict] = {}
    for n, liste in notes_auto.items():
        for lemme, t, note in liste:
            cible = manuelles.get((n, cle(lemme)))
            if cible:
                e = fusion.setdefault(id(cible[0]), dict(cible[0]))
                if cle(note) not in cle(e.get("note", "")):
                    if e.get("type") in ("abreviation", "emprunt"):
                        e["note"] = f'{e.get("note", "")} ; {note}'
                    else:
                        e["note"] = f'{note} ; {e.get("note", "")}'
                continue
            ajouter(n, lemme, {"lemme": lemme, "type": t, "note": note})
    for e in apparat:
        ajouter(int(e.get("ligne", 0)), e.get("lemme", ""), fusion.get(id(e), e))
    out = []
    for n in sorted(par_ligne):
        if n not in positions:
            raise ValueError(f"note d'apparat sur une ligne inexistante : {n}")
        txt = r"~\textbar\ ".join(x[2] for x in sorted(par_ligne[n]))
        out.append(r"\LJapp{%.3f}{\textbf{\LJchiffres %d}\enspace %s}" % (positions[n], n, txt))
    return "\n".join(out)


def double_page(page: dict, meta: dict) -> str:
    """LaTeX de la double page. ``meta`` : feuillet, cliché, mois, image, légende, label."""
    rangees = analyser(page["transcription"])
    trans, positions = colonne_transcription(rangees)
    auto = {r.numero: r.notes_auto for r in rangees if r.type == "texte" and r.notes_auto}
    textes = {r.numero: _brut(r.corps) for r in rangees if r.type == "texte"}
    app = colonne_apparat(page.get("apparat", []), positions, auto, textes)
    blocs = []
    if page.get("critique"):
        blocs.append(r"\LJregcritique{%s}" % editorial(page["critique"]))
    if meta.get("loci"):
        blocs.append(r"\LJregloci{%s}" % meta["loci"])
    if page.get("historique"):
        blocs.append(r"\LJreghistoire{%s}" % editorial(page["historique"]))
    registres = [r"\LJdebutreg"] if blocs else []
    for k, b in enumerate(blocs):
        if k:
            registres.append(r"\LJsepreg{%s}" % ("22mm" if k == 1 else "38mm"))
        registres.append(b)
    entete = r"\LJentete{%s}{%s}{%s}{%s}{%s}" % (
        meta["feuillet"], meta["cliche"], date_ed(page.get("date", "")),
        editorial(page.get("lieux", "")), editorial(page.get("titre", "")))
    return "\n".join([
        "%% ---- %s (cliché %s) ----" % (meta["feuillet"], meta["cliche"]),
        r"\LJpagepaire",
        r"\renewcommand{\LJmois}{%s}" % meta["mois"],
        r"\phantomsection\label{%s}\renewcommand{\LJlabelcourant}{%s}" % (meta["label"], meta["label"]),
        r"\LJpagetranscription{%s}{%%" % entete,
        trans + "}{%",
        app + "}{%",
        "\n".join(registres) + "}",
        r"\renewcommand{\LJfolio}{%s}" % meta["legende"],
        r"\phantomsection\label{%s-fac}" % meta["label"],
        (r"\LJfacsimilepaysage{%s}" if meta.get("paysage") else r"\LJfacsimile{%s}") % meta["image"],
    ])
