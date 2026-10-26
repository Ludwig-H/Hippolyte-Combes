"""Balisage diplomatique du Livre-Journal : analyse et conversion en LaTeX.

Le balisage est décrit dans ``edition/BALISAGE.md``. Chaque ligne du champ
``transcription`` d'une page correspond à une ligne de l'autographe ; les lignes
techniques (filets, blancs) ne sont pas numérotées.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# Commandes en ligne : nom -> nombre d'arguments obligatoires
INLINE = {
    "sl": 1, "sll": 1, "del": 1, "sur": 2, "add": 1, "addm": 1, "inc": 1,
    "fr": 2,
}
SANS_ARGUMENT = {"hfill", "trait", "ill", "lac", "ind", "centre", "droite"}
MULTILIGNES = {"crochet", "crochetd", "accolade", "accoladeg", "barre", "equerre", "equerred"}
TECHNIQUES = {"filet", "blanc"}

SPECIAUX = {
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
    "~": r"\textasciitilde{}",
}

FRACTIONS = {("1", "2"): "½", ("1", "4"): "¼", ("3", "4"): "¾"}


class ErreurBalisage(ValueError):
    pass


@dataclass
class Signe:
    """Signe couvrant plusieurs lignes (crochet, accolade, barre)."""
    nom: str
    n: int
    etiquette: str = ""


@dataclass
class Rangee:
    type: str                      # texte | filet | blanc
    numero: int = 0                # numéro de ligne (texte seulement)
    latex: str = ""                # contenu LaTeX de la ligne
    source: str = ""
    corps: str = ""                # source sans les balises de début de ligne
    retrait: float = 0.0           # en unités de retrait
    alignement: str = "g"          # g | c | d
    signes: list[Signe] = field(default_factory=list)
    filet_pos: str = "g"
    filet_frac: float = 1.0
    blanc: float = 0.0
    notes_auto: list[tuple[str, str, str]] = field(default_factory=list)  # (lemme, type, note)


def _lire_groupe(s: str, i: int) -> tuple[str, int]:
    """Lit un groupe {…} à partir de s[i] == '{' ; renvoie (contenu, index après)."""
    if i >= len(s) or s[i] != "{":
        raise ErreurBalisage(f"accolade ouvrante attendue en position {i} : {s!r}")
    prof = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            prof += 1
        elif s[j] == "}":
            prof -= 1
            if prof == 0:
                return s[i + 1:j], j + 1
    raise ErreurBalisage(f"accolade non fermée : {s!r}")


def _lire_option(s: str, i: int) -> tuple[str | None, int]:
    if i < len(s) and s[i] == "[":
        j = s.index("]", i)
        return s[i + 1:j], j + 1
    return None, i


def _texte_brut(s: str) -> str:
    out = []
    for ch in s:
        out.append(SPECIAUX.get(ch, ch))
    t = "".join(out)
    # tirets autographes : conserver la forme (— et –) ; espaces insécables avant : ; ? !
    t = re.sub(r" ([:;?!])", r"~\1", t)
    return t


def rendre(s: str, notes: list | None = None) -> str:
    """Convertit le balisage en ligne en LaTeX."""
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([a-zA-Z]+)", s[i:])
            if not m:
                raise ErreurBalisage(f"barre oblique inverse isolée : {s!r}")
            nom = m.group(1)
            i += len(m.group(0))
            if nom in INLINE:
                args = []
                for _ in range(INLINE[nom]):
                    a, i = _lire_groupe(s, i)
                    args.append(a)
                out.append(_rendre_commande(nom, args, notes))
            elif nom == "ill":
                opt, i = _lire_option(s, i)
                out.append(r"\LJill{%s}" % (opt or ""))
            elif nom == "lac":
                out.append(r"\LJlac{}")
            elif nom == "hfill":
                out.append(r"\hfill{}")
                if i < len(s) and s[i] == " ":
                    i += 1
            elif nom == "trait":
                out.append(r"\LJtrait{}")
            else:
                raise ErreurBalisage(f"commande inconnue \\{nom} : {s!r}")
        elif c == "^":
            a, i = _lire_groupe(s, i + 1)
            out.append(r"\LJsup{%s}" % rendre(a, notes))
        elif c in "{}":
            raise ErreurBalisage(f"accolade isolée : {s!r}")
        else:
            j = i
            while j < len(s) and s[j] not in "\\^{}":
                j += 1
            out.append(_texte_brut(s[i:j]))
            i = j
    return "".join(out)


def _lemme(s: str) -> str:
    """Lemme automatique : sans les balises de rature, d'ajout, etc., mais avec les lettres suscrites."""
    s = re.sub(r"\^\{([^{}]*)\}", lambda m: "\x01" + m.group(1) + "\x02", s)
    s = re.sub(r"\\sur\{(?:[^{}]|\{[^{}]*\})*\}\{", "", s)  # avant les autres balises : \sur{\inc{a}}{b}
    s = re.sub(r"\\(sl|sll|del|add|addm|inc)\{", "", s)
    s = s.replace("\\hfill", " ").replace("\\ill", "[illis.]").replace("}", "")
    s = s.replace("\x01", "^{").replace("\x02", "}")
    return re.sub(r"\s+", " ", s).strip()


def _brut(s: str) -> str:
    """Forme lisible (sans balises) pour les lemmes automatiques."""
    s = re.sub(r"\\sur\{(?:[^{}]|\{[^{}]*\})*\}\{", "", s)  # avant les autres balises : \sur{\inc{a}}{b}
    s = re.sub(r"\\(sl|sll|del|add|addm|inc)\{", "", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"\1", s)
    s = s.replace("\\hfill", " ").replace("\\ill", "[illis.]").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def _rendre_commande(nom: str, args: list[str], notes: list | None) -> str:
    if nom == "sl":
        return r"\LJsl{%s}" % rendre(args[0], notes)
    if nom == "sll":
        return r"\LJsll{%s}" % rendre(args[0], notes)
    if nom == "del":
        if notes is not None:
            notes.append((_lemme(args[0]) or "[illis.]", "rature", "biffé"))
        return r"\LJdel{%s}" % rendre(args[0], notes)
    if nom == "sur":
        if notes is not None:
            notes.append((_lemme(args[1]), "surcharge", f"écrit sur {_brut(args[0])}"))
        return r"\LJsur{%s}" % rendre(args[1], notes)
    if nom == "add":
        if notes is not None:
            notes.append((_lemme(args[0]), "ajout", "ajouté dans l'interligne"))
        return r"\LJadd{%s}" % rendre(args[0], notes)
    if nom == "addm":
        if notes is not None:
            notes.append((_lemme(args[0]), "ajout", "ajouté en marge"))
        return r"\LJaddm{%s}" % rendre(args[0], notes)
    if nom == "inc":
        return r"\LJinc{%s}" % rendre(args[0], notes)
    if nom == "fr":
        f = FRACTIONS.get((args[0].strip(), args[1].strip()))
        return f if f else r"\LJfrac{%s}{%s}" % (rendre(args[0]), rendre(args[1]))
    raise ErreurBalisage(nom)


_PREFIXES = re.compile(
    r"^\\(ind|centre|droite|crochet|crochetd|accolade|accoladeg|barre|equerre|equerred)\b"
)


def analyser(transcription: str) -> list[Rangee]:
    """Découpe la transcription en rangées (texte, filet, blanc)."""
    rangees: list[Rangee] = []
    num = 0
    for brute in transcription.rstrip("\n").split("\n"):
        ligne = brute.rstrip()
        if not ligne.strip():
            raise ErreurBalisage("ligne vide (utiliser \\blanc{n} pour un espace blanc)")
        m = re.match(r"^\\filet(?:\[([gcd])\])?(?:\{([0-9.]+)\})?\s*$", ligne)
        if m:
            rangees.append(Rangee("filet", filet_pos=m.group(1) or "g",
                                  filet_frac=float(m.group(2) or 1.0), source=ligne))
            continue
        m = re.match(r"^\\blanc\{([0-9.]+)\}\s*$", ligne)
        if m:
            rangees.append(Rangee("blanc", blanc=float(m.group(1)), source=ligne))
            continue
        num += 1
        r = Rangee("texte", numero=num, source=ligne)
        reste = ligne.lstrip()
        while True:
            m = _PREFIXES.match(reste)
            if not m:
                break
            nom = m.group(1)
            reste = reste[m.end():]
            if nom == "ind":
                opt, k = _lire_option(reste, 0)
                reste = reste[k:]
                r.retrait += float(opt) if opt else 1.0
            elif nom == "centre":
                r.alignement = "c"
            elif nom == "droite":
                r.alignement = "d"
            else:
                n, k = _lire_groupe(reste, 0)
                reste = reste[k:]
                etiquette, k = _lire_option(reste, 0)
                reste = reste[k:]
                if not n.strip().isdigit() or int(n) < 1:
                    raise ErreurBalisage(f"\\{nom}{{n}} : n entier attendu : {ligne!r}")
                r.signes.append(Signe(nom, int(n), etiquette or ""))
            reste = reste.lstrip(" ")
        notes: list = []
        r.corps = reste
        r.latex = rendre(reste, notes)
        r.notes_auto = notes
        rangees.append(r)
    # contrôle des signes multilignes
    textes = [x for x in rangees if x.type == "texte"]
    for x in textes:
        for sg in x.signes:
            if x.numero + sg.n - 1 > len(textes):
                raise ErreurBalisage(f"\\{sg.nom}{{{sg.n}}} dépasse la fin de la page (ligne {x.numero})")
    return rangees


def texte_simple(transcription: str) -> list[str]:
    """Lignes de texte sans balises (pour l'indexation et les recherches)."""
    out = []
    for r in analyser(transcription):
        if r.type == "texte":
            out.append(_brut(r.corps))
    return out
