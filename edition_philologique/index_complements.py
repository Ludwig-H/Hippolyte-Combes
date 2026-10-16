# -*- coding: utf-8 -*-
"""Compléments attestés aux catalogues des index de Gemini.

Chaque tuple suit le format (vedette, description, regex, vues explicites).
Les listes explicites restent vides : seules les lignes autographes transcrites
peuvent fournir les occurrences. Les descriptions exposent ce que dit le carnet,
sans compléter les prénoms, grades ou biographies par une identification externe.
Colin reste indéterminé ; Charlet est un café, classé parmi les lieux.
"""

EXTRA_PERSONS = [
    (
        "Boilly",
        "interprète dit professeur à Pont-à-Mousson dans le carnet",
        r"(?<!\w)Boilly(?!\w)",
        [],
    ),
    (
        "Casteljau (Cap. de)",
        "officier rencontré au bureau de la mission française du 2e corps",
        r"(?<!\w)Casteljau(?!\w)",
        [],
    ),
    (
        "Colin (mention « Chez Colin »)",
        "mention d'une personne ou d'une enseigne à la fin d'un itinéraire parisien",
        r"(?<!\w)Colin(?!\w)",
        [],
    ),
    (
        "Cordonnier",
        "interprète mentionné avec « R.F.A. », revu au bureau de la mission de la 2e division",
        r"(?<!\w)Cordonnier(?!\w)",
        [],
    ),
    (
        "Jamet",
        "interprète recherché au sujet d'une question de pétrole",
        r"(?<!\w)Jamet(?!\w)",
        [],
    ),
    (
        "Lamennais",
        "nom cité à propos d'une influence sur Maurice de Guérin, dans une conférence de M. Zyromski",
        r"(?<!\w)Lamennais(?!\w)",
        [],
    ),
    (
        "Marie-Antoine (P.)",
        "religieux dont le caveau est visité au cimetière de Terre-Cabade",
        r"(?<!\w)Marie-Antoine(?!\w)",
        [],
    ),
]

EXTRA_PLACES = [
    (
        "Bayencourt",
        "village donné dans le récit comme voisin d'Hébuterne et de Gommecourt",
        r"(?<!\w)Bayencourt(?!\w)",
        [],
    ),
    (
        "Béthune",
        "lieu où l'auteur dit avoir connu l'interprète Cordonnier",
        r"(?<!\w)Béthune(?!\w)",
        [],
    ),
    (
        "Charlet (café)",
        "café au premier étage duquel l'auteur est logé à son arrivée à Hérissart",
        r"(?<!\w)Charlet(?!\w)",
        [],
    ),
    (
        "Coigneux",
        "village décrit avec des toits squelettiques et des maisons privées de tuiles",
        r"(?<!\w)Coigneux(?!\w)",
        [],
    ),
    (
        "Corbeil-Essonnes",
        "étape ferroviaire mentionnée avant l'arrivée à Paris",
        r"(?<!\w)Corbeil-Essonnes(?!\w)",
        [],
    ),
    (
        "Flixecourt",
        "destination d'une promenade du capitaine et de son ami",
        r"(?<!\w)Flixecourt(?!\w)",
        [],
    ),
    (
        "Gannat",
        "étape ferroviaire citée pendant le retour de permission",
        r"(?<!\w)Gannat(?!\w)",
        [],
    ),
    (
        "Gézaincourt",
        "gare où l'auteur attend longuement une correspondance",
        r"(?<!\w)Gézaincourt(?!\w)",
        [],
    ),
    (
        "Gien",
        "étape ferroviaire citée pendant le retour de permission",
        r"(?<!\w)Gien(?!\w)",
        [],
    ),
    (
        "Gommecourt",
        "localité signalée avec la parenthèse « Boches » près de Bayencourt",
        r"(?<!\w)Gommecourt(?!\w)",
        [],
    ),
    (
        "Montaudran",
        "village visité à pied, avec arrêt dans l'église et montée au clocher",
        r"(?<!\w)Montaudran(?!\w)",
        [],
    ),
    (
        "Montargis",
        "étape ferroviaire citée pendant le retour de permission",
        r"(?<!\w)Montargis(?!\w)",
        [],
    ),
    (
        "Monts-en-Ternois",
        "étape de cantonnement appelée « hameau » dans le carnet",
        r"(?<!\w)Monts-en-Ternois(?!\w)",
        [],
    ),
    (
        "Pont-à-Mousson",
        "ville où Boilly est dit professeur dans le carnet",
        r"(?<!\w)Pont-à-Mousson(?!\w)",
        [],
    ),
    (
        "Terre-Cabade (cimetière)",
        "cimetière où l'auteur s'arrête devant les caveaux des Pères Jésuites et du P. Marie-Antoine",
        r"(?<!\w)Terre-Cabade(?!\w)",
        [],
    ),
]
