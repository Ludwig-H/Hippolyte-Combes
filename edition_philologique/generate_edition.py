# -*- coding: utf-8 -*-
"""
Generates the complete scientific philological LaTeX edition:
  /workspaces/Hippolyte-Combes/edition_philologique/carnet_hippolyte_combes.tex
modeled on Louis Hauseux's edition of Aristophanes' Thesmophories:
- Vis-à-vis spreads for all 186 scans:
  * Left page (even/verso): Diplomatic transcription with line numbers every 5 lines +
    horizontally aligned marginal critical apparatus + two-level bottom commentary
    (1. Commentaire critique interne; 2. Commentaire historique).
  * Right page (odd/recto): Full-page facsimile scan with folio/archive header and caption.
- Organized into 7 coherent chapters, each preceded by an analytical summary, historical
  and philological introduction, and archival/family/military illustrations.
"""

import os
import re
import json

ROOT = "/workspaces/Hippolyte-Combes"
JSON_PATH = os.path.join(ROOT, "transcriptions", "transcription_integrale_186_scans.json")
OUT_TEX = os.path.join(ROOT, "edition_philologique", "carnet_hippolyte_combes.tex")


def escape_diplomatic_line(s):
    """Escapes a diplomatic transcription line for LaTeX while preserving \\hfill and \\dots."""
    s = s.replace("½", "1/2")
    s = s.replace("\\hfill", "@@HFILL@@").replace("\\dots", "@@DOTS@@")
    s = s.replace("⟦", "@@LDEL@@").replace("⟧", "@@RDEL@@")
    s = s.replace("\\", "\\textbackslash{}")
    s = s.replace("&", "\\&")
    s = s.replace("%", "\\%")
    s = s.replace("$", "\\$")
    s = s.replace("#", "\\#")
    s = s.replace("_", "\\_")
    s = s.replace("{", "\\{")
    s = s.replace("}", "\\}")
    s = s.replace("~", "\\textasciitilde{}")
    s = s.replace("^", "\\textasciicircum{}")
    s = s.replace("@@HFILL@@", "\\hfill{}")
    s = s.replace("@@DOTS@@", "\\dots{}")
    s = s.replace("@@LDEL@@", "$[\\![$")
    s = s.replace("@@RDEL@@", "$]\\!]$")
    return s


def sanitize_latex_fragment(s):
    """
    Sanitizes a commentary or marginal note string that may already contain LaTeX commands
    (\\textbf, \\textit, \\texttt, \\&, \\#, \\_) or plain text from the docx.
    """
    s = s.replace("½", "1/2")
    s = s.replace("$\\rightarrow$", "$\\rightarrow$").replace("\\rightarrow", "$\\rightarrow$")
    s = re.sub(r"\$\s*\$(?:\\rightarrow)\$\s*\$", r"$\\rightarrow$", s)
    s = re.sub(r"\^([a-zA-Z0-9]+)\^", r"\\textsuperscript{\1}", s)
    s = s.replace("^", "")
    s = s.replace("\\llbracket ", "$[\\![$").replace("\\llbracket", "$[\\![$")
    s = s.replace("\\rrbracket\\", "$]\\!]\\ $").replace("\\rrbracket", "$]\\!]$")
    s = s.replace("⟦", "$[\\![$").replace("⟧", "$]\\!]$")
    # Escape any unescaped &, %, #, _
    s = re.sub(r"(?<!\\)&", r"\\&", s)
    s = re.sub(r"(?<!\\)%", r"\\%", s)
    s = re.sub(r"(?<!\\)#", r"\\#", s)
    s = re.sub(r"(?<!\\)_", r"\\_", s)
    return s


CHAPTERS = [
    {
        "num": "I",
        "title": "Des confins de la Somme aux Flandres avec les 1st Irish Guards",
        "subtitle": "Lucheux, Saint-Pol, l'Ebenezer Boarding School, le Mont-des-Cats, Bailleul et Steenwerck (25 juillet – 17 août 1916)",
        "scan_start": 1,
        "scan_end": 18,
        "summary": (
            "Ce premier chapitre s'ouvre sur la couverture du \\textit{Livre-Journal} (Scan \\#001) et suit Hippolyte Combes "
            "du 25 juillet au 17 août 1916 (Folios 1r à 9r, Scans \\#002 à \\#018), alors qu'il sert comme interprète "
            "stagiaire auprès du 1\\textsuperscript{er} bataillon des \\textit{Irish Guards}. Après une ultime étape à Lucheux "
            "(Somme), l'unité remonte par Saint-Pol-sur-Ternoise vers la Flandre française et belge : cantonnement au "
            "pensionnat protestant abandonné d'\\textit{Ebenezer} près de Pradelles, marche vers l'abbaye trappiste du "
            "Mont-des-Cats et Poperinghe, puis séjour prolongé à Bailleul et au hameau de La Crèche (Steenwerck)."
        ),
        "intro": (
            "Lorsqu'il ouvre ce carnet à Lucheux le mardi 25 juillet 1916, Hippolyte Combes (né à La Valette le 29 septembre "
            "1876, licencié en droit, ancien sous-chef de gare à la Compagnie du Midi et clerc d'avoué à Paris) approche de "
            "ses quarante ans. Passé du 10\\textsuperscript{e} régiment d'artillerie à pied de Toulon au corps des interprètes "
            "militaires de réserve en novembre 1915 grâce à sa maîtrise de l'anglais acquise jadis à Folkestone, il partage "
            "depuis décembre 1915 le quotidien aristocratique et exigeant des officiers du 1\\textsuperscript{er} bataillon "
            "des \\textit{Irish Guards} (\\textit{1st Guards Brigade, Guards Division}).\n\n"
            "Les dix-huit premiers clichés révèlent d'emblée la tension constitutive du \\textit{Livre-Journal}. D'un côté, "
            "l'interprète accomplit un travail incessant de \\textit{billeting} (préparation des cantonnements pour trente à "
            "quarante officiers, négociation des lits et des pâtures auprès des maires et des fermiers flamands, règlement "
            "des dégâts et de la blanchisserie). De l'autre, l'esthète sensible contemple les paysages des Flandres sous un "
            "ciel « bas et gris », écoute la musique des \\textit{Guards} sur la Grand-Place de Bailleul, visite l'église "
            "médiévale de Lucheux ou le pensionnat déserté d'\\textit{Ebenezer}, et note avec une précision de comptable "
            "la moindre dépense de \\textit{food} ou de \\textit{washing}."
        ),
        "illustrations": [
            ("illustrations/hippolyte_interprete_1.jpg", "Hippolyte Combes en uniforme d'interprète militaire attaché à l'Armée britannique (képi à bandeau et insignes de col au sphinx). Collection familiale Combes.", "0.44\\textwidth"),
            ("illustrations/toulon_artillerie_1915.jpg", "Hippolyte Combes au 10\\textsuperscript{e} régiment d'artillerie à pied à Toulon en 1915, avant son admission au corps des interprètes.", "0.44\\textwidth"),
        ],
    },
    {
        "num": "II",
        "title": "De la vallée de la Lys à l'Artois et au front de la Somme : le passage à l'A.S.C.",
        "subtitle": "Steenwerck, Armentières, Estaires, Marquay, Saint-Pol, l'affectation à la 152nd Coy A.S.C., Raincheval, Acheux et Forceville (18 août – 24 septembre 1916)",
        "scan_start": 19,
        "scan_end": 49,
        "summary": (
            "Ce deuxième chapitre (Folios 9v à 23v, Scans \\#019 à \\#049) retrace le basculement majeur de la fin de l'été 1916. "
            "Après une tournée dans Armentières bombardée et la vallée de la Lys (Estaires, Steenwerck), Hippolyte Combes descend "
            "en train vers l'Artois (Marquay, Bailleul-aux-Cornailles, Saint-Pol-sur-Ternoise). Affecté début septembre 1916 "
            "à une unité logistique du Train britannique — la \\textit{152nd Company, Army Service Corps} — commandée par le "
            "capitaine Williams (« Capt. W. »), il rejoint le secteur nord de la bataille de la Somme (Raincheval, Acheux-en-Amiénois, "
            "Léalvillers, Forceville), où il assure le ravitaillement en fourrages (\\textit{green forage}) tout en attendant sa permission."
        ),
        "intro": (
            "Le départ des Flandres vers l'Artois puis vers l'arrière-front de la Somme plonge le diariste au cœur de la "
            "gigantesque logistique de la bataille d'usure engagée depuis le 1\\textsuperscript{er} juillet 1916. Autour de "
            "Saint-Pol, puis de Raincheval, d'Acheux, de Varennes et de Forceville, le paysage n'est plus qu'un immense réseau "
            "de dépôts, de voies ferrées militaires (\\textit{railheads}) et de bivouacs battus par les pluies d'orage. C'est "
            "dans ce cadre qu'intervient son passage à la \\textit{152nd Company A.S.C.}, compagnie chargée du transport et "
            "de l'achat sur place des récoltes de trèfle, de luzerne et d'avoine (\\textit{green forage}).\n\n"
            "Sur le plan philologique et psychologique, cette section du carnet voit s'affirmer deux traits majeurs : "
            "d'une part, l'hybridation linguistique accélérée du texte (\\textit{mess, billet, shift, lorry, limber, refilling point, "
            "we are moving Dawn, stars are nil vis}) ; d'autre part, l'impatience grandissante de retrouver sa famille et sa "
            "fiancée Marguerite Calmels lors de sa première permission de détente fin septembre 1916."
        ),
        "illustrations": [
            ("illustrations/hippolyte_interprete_2.jpg", "Portrait en buste d'Hippolyte Combes sur le front britannique (1916--1917), portant les insignes métalliques d'interprète détaché auprès de la B.E.F.", "0.42\\textwidth"),
            ("illustrations/hippolyte_1897.jpg", "Hippolyte Combes jeune homme en 1897 (à l'âge de vingt et un ans), étudiant en droit et futur stagiaire en Angleterre.", "0.42\\textwidth"),
        ],
    },
    {
        "num": "III",
        "title": "La première permission : d'Acheux-Varennes à Paris et au Midi",
        "subtitle": "Forceville, gare d'Acheux-Varennes, Amiens, Paris, le voyage vers Toulouse et le retour en Picardie (25 septembre – 6 octobre 1916)",
        "scan_start": 50,
        "scan_end": 66,
        "summary": (
            "Ce troisième chapitre (Folios 24r à 32r, Scans \\#050 à \\#066) forme une respiration lumineuse au milieu du "
            "carnet : le récit intégral de la première permission d'Hippolyte Combes (25 septembre – 6 octobre 1916). "
            "Il s'ouvre sur le Folio 24 recto (Scan \\#050, restitué pour la première fois dans la présente édition), qui "
            "décrit le réveil à 4 h du matin le 25 septembre, la dernière corvée de \\textit{green forage} à Forceville et "
            "l'attente au \\textit{railhead} d'Acheux-Varennes. Après une escale à Paris (26 septembre), Hippolyte séjourne "
            "dans le Midi (Toulouse, 27 septembre – 4 octobre, où il fête son 40\\textsuperscript{e} anniversaire le 29 septembre), "
            "avant le voyage de retour par Paris et Amiens vers le hameau de Barlette près de Bernaville (Scans \\#063–\\#066)."
        ),
        "intro": (
            "L'intérêt philologique et documentaire de ce troisième chapitre est double. Sur le plan codicologique, l'examen "
            "direct des 186 clichés a permis de résoudre deux anomalies qui affectaient les transcriptions antérieures : "
            "1° la restitution intégrale du cliché \\texttt{20251126\\_103019.jpg} (Scan \\#050, Folio 24 recto : journée du "
            "lundi 25 septembre 1916 jusqu'au départ du train de 18 h 40 à Acheux-Varennes), qui avait été omis lors du premier "
            "dépouillement ; 2° le rétablissement de l'ordre exact entre les clichés \\texttt{20251126\\_103538.jpg} (Scan \\#063, "
            "5 octobre 1916) et \\texttt{20251126\\_103554.jpg} (Scan \\#064, nuit du 4 au 5 octobre 1916).\n\n"
            "Sur le plan biographique, ces pages offrent un tableau saisissant du contraste entre la boue de la Somme et "
            "la douceur de l'arrière méridional à l'automne 1916 : flâneries sous le soleil de Toulouse, visites aux parents "
            "et amis (les Crouzet, l'oncle Paulin), lectures de Verlaine, emplettes à Paris, mais aussi mélancolie poignante "
            "de l'arrachement au soir du 4 octobre."
        ),
        "illustrations": [
            ("illustrations/marguerite_1917.jpg", "Marguerite Calmels (1891--1986), photographiée par le studio Jublin à Millau à l'époque de ses fiançailles avec Hippolyte Combes.", "0.42\\textwidth"),
            ("illustrations/maison_millau.jpg", "La demeure familiale de Millau (Aveyron), lieu de rassemblement des familles Combes et Calmels.", "0.46\\textwidth"),
        ],
    },
    {
        "num": "IV",
        "title": "L'automne en Picardie et en Artois : des bois de Ribeaucourt à Acheux",
        "subtitle": "Barlette, Ribeaucourt, Bernaville, Beauval, Bailleulmont, Couturelle, l'incident d'Humbercamps et le cantonnement d'Acheux (7 octobre – 14 décembre 1916)",
        "scan_start": 67,
        "scan_end": 106,
        "summary": (
            "Ce quatrième chapitre (Folios 33v à 53r, Scans \\#067 à \\#106) couvre plus de deux mois de campagne d'automne "
            "(7 octobre – 14 décembre 1916) au sein de la \\textit{152nd Company A.S.C.} De retour de permission au hameau "
            "de Barlette (Ribeaucourt) près de Bernaville (7–14 octobre), Hippolyte gagne Beauval (15–23 octobre), puis "
            "remonte en Artois à Bailleulmont, Couturelle et Humbercamps (24 octobre – 8 novembre), où il instruit sur place "
            "l'enquête contradictoire sur les dégâts du 3 novembre, avant de redescendre dans la Somme à Acheux-en-Amiénois, "
            "Varennes, Léalvillers et Bertrancourt (9 novembre – 14 décembre 1916)."
        ),
        "intro": (
            "Entre le début d'octobre et la mi-décembre 1916, le journal d'Hippolyte Combes devient la chronique minutieuse "
            "de la guerre logistique dans la boue de Picardie et d'Artois. Aux côtés du capitaine Panton, du capitaine Williams "
            "et du lieutenant Curtis, l'interprète sillonne à cheval, en fourgon \\textit{limber G.S.} ou en automobile les "
            "villages de l'arrière-front (Prouville, Bernaville, Beauval, Pas-en-Artois, Humbercamps, Saulty, Louvencourt, "
            "Toutencourt) pour acheter luzerne et paille d'avoine, répartir les granges et instruire les réclamations agricoles.\n\n"
            "C'est durant le séjour à Couturelle et Humbercamps (3–6 novembre 1916, Scans \\#083–\\#086) que survient un épisode "
            "emblématique : la plainte du maire d'Humbercamps accusant les soldats anglais d'avoir démoli une cloison et brûlé "
            "des planches. La minute autographe du rapport en anglais rédigé par Hippolyte Combes le 5 novembre 1916, conservée "
            "dans les archives familiales et éditée en Annexe I (Document 3), recoupe mot pour mot les entrées du carnet."
        ),
        "illustrations": [
            ("illustrations/fiche_matricule.jpg", "Extrait du registre matricule d'Hippolyte Combes (classe 1896, matricule 762, subdivision de Rodez) mentionnant sa nomination comme interprète stagiaire de réserve le 29 novembre 1915.", "0.78\\textwidth"),
        ],
    },
    {
        "num": "V",
        "title": "Au cœur de l'hiver 1916–1917 dans la Somme : Noël et grand gel à Acheux",
        "subtitle": "Acheux-en-Amiénois, Bertrancourt, Louvencourt, Toutencourt, l'excursion à Amiens et le gel polaire de janvier 1917 (15 décembre 1916 – 28 janvier 1917)",
        "scan_start": 107,
        "scan_end": 134,
        "summary": (
            "Ce cinquième chapitre (Folios 53v à 67r, Scans \\#107 à \\#134) retrace la vie quotidienne d'Hippolyte Combes "
            "au cantonnement d'Acheux-en-Amiénois (chez la famille Carluvant) du 15 décembre 1916 au 28 janvier 1917. "
            "Tandis que les pluies de décembre cèdent la place au grand gel et à la neige de janvier 1917, l'interprète "
            "partage son temps entre le bureau n° 104, le mess du capitaine Williams, les tournées d'expertise et de fourrage "
            "(Toutencourt, Saulty, Louvencourt, Raincheval, Varennes), le réveillon de Noël et du Jour de l'An, une journée "
            "d'excursion à Amiens (3 janvier), et les préparatifs de sa permission d'hiver."
        ),
        "intro": (
            "L'hiver 1916–1917 dans la Somme éprouve durement les organismes et les esprits. Logé à Acheux chez les "
            "Carluvant — dont la maison hospitalière et la « chambre chaude » offrent un refuge précieux contre la bise "
            "glaciale qui balaie le plateau picard —, Hippolyte Combes observe avec acuité les contrastes de sa condition "
            "d'interprète : rapports parfois tendus ou purement formels avec le commandant du mess britannique (« Capt. W. »), "
            "mais camaraderie chaleureuse avec les jeunes lieutenants (Curtis, Gilbert, First) et avec ses collègues de la "
            "Mission française (le capitaine Huguet).\n\n"
            "Tout au long de ces semaines de neige et de verglas, le courrier de sa fiancée Marguerite (« Gueïte ») demeure "
            "le véritable baromètre affectif du journal : le moindre retard postal provoque abattement et insomnie, tandis "
            "qu'une lettre tendre suffit à transfigurer la monotonie des corvées de fourrage."
        ),
        "illustrations": [
            ("illustrations/camarades_ailly_1919.jpg", "Souvenir de camaraderie militaire sur le front de Picardie (carte-photo dédicacée à Hippolyte Combes, Ailly-sur-Noye, mai 1919). Collection familiale.", "0.50\\textwidth"),
        ],
    },
    {
        "num": "VI",
        "title": "La permission de février 1917 (Paris, Bordeaux, Toulouse, Millau, La Valette)",
        "subtitle": "Le grand froid de février 1917, le départ d'Acheux, Paris, Bordeaux, Toulouse, les fiançailles à Millau et La Valette (29 janvier – 24 février 1917)",
        "scan_start": 135,
        "scan_end": 154,
        "summary": (
            "Ce sixième chapitre (Folios 67v à 77r, Scans \\#135 à \\#154) couvre les derniers jours d'attente dans le gel "
            "polaire d'Acheux (29 janvier – 6 février 1917, où le thermomètre descend à –15 °C et où Hippolyte offre un "
            "cadeau d'adieu à ses hôtes Carluvant avant le transfert du cantonnement vers Hérissart), puis l'intégralité "
            "de sa deuxième grande permission (7–23 février 1917) : traversée de Paris, étape à Bordeaux chez sa sœur "
            "Joséphine et Léon, séjour à Toulouse, puis journées décisives à Millau auprès de Marguerite Calmels et "
            "visite familiale au domaine natal de La Valette (Saint-Beauzély) avant le retour au front le 24 février."
        ),
        "intro": (
            "Cette deuxième permission (février 1917) marque une étape décisive dans la vie intime d'Hippolyte Combes. "
            "Alors que la première permission d'octobre 1916 avait été assombrie par les hésitations familiales, le voyage "
            "de février 1917 scelle définitivement le projet d'union entre Hippolyte et Marguerite Calmels (« Gueïte »), "
            "qui sera célébré à Millau le 25 octobre 1917.\n\n"
            "Ces vingt folios constituent en outre un témoignage remarquable sur la France de l'arrière durant le terrible "
            "hiver 1917 : trains paralysés ou retardés par le gel, pénurie de charbon, mais chaleur intacte du réseau "
            "familial qui relie Paris (Marie et Paul), Bordeaux (Joséphine et Léon), Toulouse, Millau (la famille Calmels) "
            "et la maison paternelle de La Valette."
        ),
        "illustrations": [
            ("illustrations/mariage_millau_1917.jpg", "Photographie officielle du mariage d'Hippolyte Combes (en uniforme d'interprète militaire) et de Marguerite Calmels à Millau (25 octobre 1917), entourés des familles Combes et Calmels.", "0.50\\textwidth"),
            ("illustrations/menu_mariage_1917.jpg", "Menu du repas de noces d'Hippolyte Combes et Marguerite Calmels à Millau (25 octobre 1917). Archives familiales.", "0.36\\textwidth"),
        ],
    },
    {
        "num": "VII",
        "title": "Le printemps 1917 entre Somme et Artois : d'Hérissart à Toutencourt",
        "subtitle": "Installation à Hérissart, le repli allemand sur la ligne Hindenburg, les neiges tardives d'avril à Toutencourt et le renouveau printanier (25 février – 30 avril 1917)",
        "scan_start": 155,
        "scan_end": 186,
        "summary": (
            "Ce septième et dernier chapitre (Folios 77v à 93r, Scans \\#155 à \\#186) conduit le \\textit{Livre-Journal} "
            "jusqu'à son dernier feuillet (25 février – 30 avril 1917). De retour de permission, Hippolyte rejoint le "
            "nouveau cantonnement de son unité à Hérissart (fin février – mars 1917), puis s'installe à Toutencourt "
            "(avril 1917). Tout en suivant avec passion les nouvelles du repli stratégique allemand (opération \\textit{Alberich}), "
            "de la Révolution russe, de l'entrée en guerre des États-Unis et de l'offensive britannique d'Arras, il poursuit "
            "ses tournées quotidiennes en automobile avec les lieutenants Curtis et Gilbert (Rubempré, Contay, Vadencourt, "
            "Warloy, Puchevillers, Villers-Bocage) jusqu'à la radieuse journée printanière du lundi 30 avril 1917."
        ),
        "intro": (
            "Les trente-deux derniers clichés du manuscrit (Scans \\#155 à \\#186) offrent une chronique particulièrement "
            "dense (souvent vingt-quatre à vingt-sept lignes par page) des mois de mars et avril 1917 dans les villages "
            "situés entre Amiens, Albert et Doullens (Hérissart, Toutencourt, Harponville, Warloy-Baillon, Vadencourt, "
            "Contay, Villers-Bocage). Malgré les bourrasques de neige tardives qui s'abattent encore sur la Picardie "
            "jusqu'à la mi-avril 1917, l'atmosphère du carnet se transforme profondément : l'entente cordiale avec les "
            "lieutenants Curtis et Gilbert rend les longues tournées en automobile beaucoup plus plaisantes.\n\n"
            "Le \\textit{Livre-Journal} s'achève le \\textbf{lundi 30 avril 1917} (Folio 93 recto, Scan \\#186), exactement "
            "sur la dernière page matérielle du registre, dans un véritable hymne au printemps enfin victorieux : "
            "« \\textit{Aujourd'hui encore, temps magnifique. Soleil ardent... Ciel d'un bleu pur \\& céleste. Aux arbres, "
            "bourgeons grossissent à vue d'œil... Nuit très belle, mervt éclairée, lune superbe.} »"
        ),
        "illustrations": [
            ("illustrations/andelys_ecole_militaire.jpg", "Photographie de groupe devant l'École militaire préparatoire des Andelys (où Hippolyte enseigne l'anglais fin 1918).", "0.31\\textwidth"),
            ("illustrations/famille_combes_1925.jpg", "Hippolyte et Marguerite Combes entourés de leurs enfants vers 1925.", "0.31\\textwidth"),
            ("illustrations/hippolyte_cambridge_1930.jpg", "Hippolyte Combes en Angleterre (Cambridge, été 1930).", "0.31\\textwidth"),
        ],
    },
]


def build_spread_latex(rec):
    """
    Generates the exact two-page vis-à-vis LaTeX code for a single scan record:
    - Even (left/verso) page: Diplomatic transcription + horizontally aligned marginal apparatus + 2-level bottom commentary
    - Odd (right/recto) page: Full-page facsimile image with archival metadata frame.
    """
    scan_num = rec["scan_num"]
    fname = rec["filename"]
    fname_esc = fname.replace("_", "\\_")
    folio = sanitize_latex_fragment(rec["folio"])
    title = sanitize_latex_fragment(rec["title"])
    date_str = sanitize_latex_fragment(rec["date"])
    lieu_str = sanitize_latex_fragment(rec["lieu"])
    lines = rec["lines"]
    raw_mnotes = {int(k): sanitize_latex_fragment(v) for k, v in rec["marginal_notes"].items()}
    crit_str = sanitize_latex_fragment(rec["critique"])
    hist_str = sanitize_latex_fragment(rec["historique"])

    # Merge adjacent marginal notes if line i has a long note (>45 chars) and line i+1 also has a note,
    # so that \smash{\parbox[t]...} on line i never overlaps vertically with line i+1.
    mnotes = dict(raw_mnotes)
    sorted_keys = sorted(mnotes.keys())
    for k in sorted_keys:
        if k not in mnotes:
            continue
        if (k + 1) in mnotes and len(mnotes[k]) > 42:
            mnotes[k] = mnotes[k] + " — " + mnotes[k + 1]
            del mnotes[k + 1]

    n_lines = len(lines)
    if n_lines <= 19:
        line_font = "\\small"
        row_stretch = "1.06"
    elif n_lines <= 23:
        line_font = "\\footnotesize"
        row_stretch = "0.97"
    else:
        line_font = "\\scriptsize"
        row_stretch = "0.91"

    # Build table rows for each manuscript line
    rows_tex = []
    for idx, l in enumerate(lines, 1):
        esc_l = escape_diplomatic_line(l)
        if idx % 5 == 0:
            num_prefix = f"\\leavevmode\\llap{{\\scriptsize\\color{{darkgray}}{idx}\\hspace{{2.5mm}}}}"
        else:
            num_prefix = "\\leavevmode"

        left_cell = f"{num_prefix}{line_font}\\strut {esc_l}\\strut"
        if idx in mnotes:
            mn = mnotes[idx]
            right_cell = f"\\smash{{\\parbox[t]{{54mm}}{{\\scriptsize\\raggedright\\setlength{{\\baselineskip}}{{8pt}}\\color{{black!88}}{mn}}}}}"
        else:
            right_cell = ""

        rows_tex.append(f"      {left_cell} & {right_cell} \\\\")

    rows_joined = "\n".join(rows_tex)

    tex = f"""
% =============================================================================
% VIS-A-VIS SPREAD : SCAN #{scan_num:03d} ({fname}) — {folio}
% =============================================================================
\\cleardoubleevenpage
% --- En-tête du folio (Page paire / gauche : Transcription & Apparat) ---
\\noindent\\colorbox{{headerbg}}{{%
  \\parbox{{\\dimexpr\\textwidth-2\\fboxsep\\relax}}{{%
    \\vspace{{0.8mm}}%
    \\textbf{{\\small SCAN \\#{scan_num:03d} — {folio.upper()}}} \\hfill {{\\footnotesize\\texttt{{{fname_esc}}}}}\\\\[0.4mm]
    {{\\footnotesize\\textbf{{Intitulé :}} {title} \\hfill \\textbf{{Date :}} {date_str} \\quad | \\quad \\textbf{{Lieu :}} {lieu_str}}}%
    \\vspace{{0.8mm}}%
  }}%
}}\\\\[1.2mm]
\\noindent{{\\scriptsize\\textsc{{I. Transcription diplomatique ligne à ligne}} \\hfill \\textsc{{Apparat critique marginal (aligné sur la ligne)}}}}\\\\[0.4mm]
\\noindent\\rule{{\\textwidth}}{{0.4pt}}\\\\[0.8mm]
% --- Corps de la transcription diplomatique et apparat marginal en prolongement ---
{{\\renewcommand{{\\arraystretch}}{{{row_stretch}}}%
\\noindent\\hspace*{{4mm}}\\begin{{tabular}}{{@{{}}p{{110mm}}@{{\\hspace{{5mm}}}}p{{54mm}}@{{}}}}
{rows_joined}
\\end{{tabular}}}}%
\\par\\vspace*{{\\fill}}
% --- Double commentaire de bas de page (1. Critique interne ; 2. Historique) ---
\\noindent\\rule{{\\textwidth}}{{0.6pt}}\\\\[0.8mm]
\\noindent\\colorbox{{commbg}}{{%
  \\parbox{{\\dimexpr\\textwidth-2\\fboxsep\\relax}}{{%
    \\vspace{{0.8mm}}%
    \\scriptsize\\setlength{{\\baselineskip}}{{8.4pt}}%
    \\noindent\\textbf{{\\textsc{{1. Commentaire critique (interne à l'histoire du carnet) :}}}} {crit_str}\\\\[1mm]
    \\noindent\\textbf{{\\textsc{{2. Commentaire historique :}}}} {hist_str}%
    \\vspace{{0.8mm}}%
  }}%
}}
\\newpage
% --- En-tête du fac-similé (Page impaire / droite : Scan original) ---
\\noindent\\colorbox{{headerbg}}{{%
  \\parbox{{\\dimexpr\\textwidth-2\\fboxsep\\relax}}{{%
    \\vspace{{0.8mm}}%
    \\textbf{{\\small FAC-SIMILÉ EN VIS-À-VIS — {folio.upper()} (SCAN \\#{scan_num:03d})}} \\hfill {{\\footnotesize\\texttt{{{fname_esc}}}}}\\\\[0.4mm]
    {{\\footnotesize\\textit{{Livre-Journal d'Hippolyte Combes}} — {date_str} ({lieu_str})}}%
    \\vspace{{0.8mm}}%
  }}%
}}\\\\[1.5mm]
\\par\\vspace*{{\\fill}}
\\begin{{center}}
  \\setlength{{\\fboxsep}}{{1.5mm}}%
  \\setlength{{\\fboxrule}}{{0.4pt}}%
  \\fcolorbox{{gray!60}}{{white}}{{%
    \\includegraphics[width=0.94\\textwidth,height=0.82\\textheight,keepaspectratio]{{\\facsimiledir/{fname}}}%
  }}
\\end{{center}}
\\par\\vspace*{{\\fill}}
\\noindent\\rule{{\\textwidth}}{{0.4pt}}\\\\[0.6mm]
\\noindent{{\\scriptsize\\color{{darkgray}}\\textbf{{Source :}} Archives familiales Combes — Cliché numérique \\texttt{{{fname_esc}}} (Scan \\#{scan_num:03d}/186, {folio}). Version haute définition non compressée disponible dans \\texttt{{scans\\_haute\\_qualite/{fname_esc}}} ; version compressée dans \\texttt{{scans\\_compresses/{fname_esc}}}.}}
\\newpage
"""
    return tex


def generate_full_tex():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    assert len(records) == 186, f"Expected 186 records, got {len(records)}"

    preamble = r"""\documentclass[10pt,twoside,openany]{book}
\usepackage{fontspec}
\usepackage[french]{babel}
\usepackage[a4paper,top=16mm,bottom=16mm,inner=16mm,outer=14mm,headheight=13pt,headsep=5mm,footskip=7mm]{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{array,booktabs,longtable}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{hyperref}

% Couleurs inspirées de l'édition des Thesmophories (Louis Hauseux)
\definecolor{cream}{HTML}{F7F3E8}
\definecolor{headerbg}{HTML}{EFECE2}
\definecolor{commbg}{HTML}{F9F7F1}
\definecolor{darkgray}{HTML}{4A4A4A}
\definecolor{bordeaux}{HTML}{6B1D1D}

% Répertoire des fac-similés :
% Par défaut, pointe vers ../scans_compresses pour maintenir le PDF compilé sous la limite GitHub de 100 Mo (~36 Mo).
% Pour compiler un tirage d'archive non compressé (~1,05 Go), décommenter la seconde ligne :
\newcommand{\facsimiledir}{../scans_compresses}
% \renewcommand{\facsimiledir}{../scans_haute_qualite}

% Saut automatique vers une page paire (gauche / verso) pour garantir le vis-à-vis strict :
% Page paire (gauche) = Transcription diplomatique, apparat marginal & double commentaire
% Page impaire (droite) = Fac-similé du scan correspondant
\newcommand{\cleardoubleevenpage}{%
  \clearpage
  \ifodd\value{page}%
    \hbox{}\thispagestyle{empty}\newpage
  \fi
}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[LE]{\footnotesize\textsc{Hippolyte Combes — Livre-Journal (1916–1917)}}
\fancyhead[RO]{\footnotesize\nouppercase{\rightmark}}
\fancyfoot[LE,RO]{\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.3pt}

\titleformat{\chapter}[display]
  {\normalfont\large\bfseries\color{bordeaux}}
  {\textsc{\chaptertitlename\ \thechapter}}
  {1mm}
  {\Large\color{black}}
\titlespacing*{\chapter}{0pt}{-4mm}{3mm}
\titlespacing*{\section}{0pt}{2.5mm}{1.2mm}

\hypersetup{
  colorlinks=true,
  linkcolor=bordeaux,
  urlcolor=bordeaux,
  pdftitle={Hippolyte Combes (1876-1970) - Livre-Journal de campagne (25 juillet 1916 - 30 avril 1917) - Édition philologique et diplomatique},
  pdfauthor={Louis Hauseux (dir.)}
}

\setlength{\parindent}{1.2em}
\setlength{\parskip}{0.3em}

\begin{document}

% =============================================================================
% 1. PREMIÈRE DE COUVERTURE (STYLE ÉDITION SAVANTE / THESMOPHORIES)
% =============================================================================
\begin{titlepage}
\pagecolor{cream}
\thispagestyle{empty}
\begin{center}
  \setlength{\fboxsep}{6mm}
  \setlength{\fboxrule}{1.2pt}
  \fcolorbox{bordeaux}{cream}{%
    \parbox[t][248mm][s]{162mm}{%
      \begin{center}
        \vspace{4mm}
        {\large\textsc{Archives familiales du Rouergue \& du Front britannique}}\\[2mm]
        \rule{110mm}{0.6pt}\\[6mm]
        {\LARGE\textbf{HIPPOLYTE COMBES}}\\[2mm]
        {\normalsize\textsc{(La Valette, 29 septembre 1876 — Rodez, 17 février 1970)}}\\[8mm]
        {\Huge\textbf{\textcolor{bordeaux}{LIVRE - JOURNAL}}}\\[3mm]
        {\Large\textbf{DE CAMPAGNE (1916–1917)}}\\[4mm]
        {\large\textit{Du 25 juillet 1916 au 30 avril 1917}}\\[3mm]
        {\normalsize Interprète militaire auprès de l'Armée britannique\\
        (\textit{1st Battalion Irish Guards} \& \textit{152nd Company Army Service Corps})}\\[7mm]
        % Vignette centrale extraite de la couverture du carnet autographe
        \setlength{\fboxsep}{1.5mm}
        \setlength{\fboxrule}{0.6pt}
        \fcolorbox{bordeaux}{white}{%
          \includegraphics[width=78mm,height=68mm,keepaspectratio]{illustrations/vignette_couverture.jpg}%
        }\\[7mm]
        {\large\textsc{Édition philologique, diplomatique et critique en vis-à-vis}}\\[2.5mm]
        {\small Transcription diplomatique intégrale des 186 clichés numérotée de 5 en 5 lignes,\\
        apparat critique marginal aligné dans le prolongement de la ligne,\\
        double commentaire (codicologique et historique) et fac-similés en regard}\par
        \vfill
        \rule{90mm}{0.4pt}\\[3mm]
        {\normalsize\textsc{Édition établie, introduite et annotée}}\\
        {\footnotesize d'après le manuscrit original et les archives de La Valette et de Millau}\\[2mm]
        {\small\textbf{MMXXVI}}
        \vspace{2mm}
      \end{center}
    }%
  }
\end{center}
\end{titlepage}
\nopagecolor

% Page blanche de garde (Page 2)
\hbox{}\thispagestyle{empty}\newpage

% =============================================================================
% 2. FAUX-TITRE & PAGE DE TITRE INTÉRIEURE (AVEC EMBLÈME FRAKTUR \mathfrak{Urtext})
% =============================================================================
\thispagestyle{empty}
\begin{center}
  \vspace*{18mm}
  {\Large\textsc{Hippolyte Combes}}\\
  {\small (1876–1970)}\\[14mm]
  {\huge\textbf{LIVRE-JOURNAL DE GUERRE}}\\[4mm]
  {\large\textit{25 juillet 1916 — 30 avril 1917}}\\[6mm]
  {\normalsize De la Somme aux Flandres et à l'Artois\\
  avec les \textit{Irish Guards} et l'\textit{Army Service Corps}}\\[20mm]
  {\Huge $\mathfrak{Urtext}$}\\[20mm]
  \rule{55mm}{0.4pt}\\[8mm]
  {\normalsize\textbf{Édition scientifique intégrale des 186 scans du manuscrit autographe}}\\[2mm]
  {\small accompagnée des lettres de guerre inédites (1916), de l'état signalétique des services\\
  et d'un répertoire prosopographique, militaire et topographique}\par
  \vfill
  {\small\textsc{Collection des Sources et Manuscrits Contemporains}}\\
  {\footnotesize Millau — La Valette — Paris}
  \vspace*{10mm}
\end{center}
\newpage

\frontmatter
\tableofcontents
\cleardoublepage

% =============================================================================
% 3. PROLÉGOMÈNES SCIENTIFIQUES ET HISTORIQUES
% =============================================================================
\chapter{Prolégomènes : Hippolyte Combes (1876–1970) et son \textit{Livre-Journal} de la Grande Guerre}
\markboth{Prolégomènes}{Prolégomènes}

\section{Destin d'un interprète rouergat auprès de l'Armée britannique (1876–1970)}

Né le 29 septembre 1876 au domaine familial de \textbf{La Valette} (commune de Saint-Beauzély, Aveyron), au cœur de la vallée de la Muse et aux portes de Millau, \textbf{Hippolyte Pierre Jean Combes} appartient à une lignée de propriétaires terriens et de notables cultivés du Rouergue méridional. Cinquième enfant de \textbf{Pierre Combes} (1847–1928) et de \textbf{Mélanie} (née en 1851), il grandit au sein d'une fratrie nombreuse comprenant notamment \textbf{Paul} (né en 1874), \textbf{Marie} (née en 1875), \textbf{Joséphine} (née en 1882, épouse de Léon à Bordeaux), \textbf{Émile} (né en 1883, médecin militaire durant la Grande Guerre), \textbf{Jean} (né en 1891, artilleur puis aviateur au front d'Orient à Salonique) et \textbf{Gabriel}.

Après de solides études classiques et l'obtention de sa \textbf{licence en droit}, le jeune Hippolyte effectue un séjour linguistique et professionnel décisif en Angleterre, à \textbf{Folkestone} (Kent), où il acquiert une maîtrise idiomatique de la langue anglaise et une familiarité durable avec les mœurs britanniques. De retour en France, il exerce d'abord les fonctions de sous-chef de gare à la Compagnie des chemins de fer du Midi, puis s'installe à Paris comme principal clerc d'avoué avant de reprendre en main la gestion des biens familiaux.

\begin{figure}[htbp]
  \centering
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=62mm,keepaspectratio]{illustrations/hippolyte_1897.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 1.} Hippolyte Combes en 1897, à l'âge de 21 ans.}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.48\textwidth}
    \centering
    \includegraphics[height=62mm,keepaspectratio]{illustrations/hippolyte_interprete_1.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 2.} Hippolyte Combes en uniforme d'interprète auprès de la B.E.F. (1916).}
  \end{minipage}
\end{figure}

Bien qu'exempté de service armé actif dans sa jeunesse (classe 1896, bureau de recrutement de Rodez, matricule n\textsuperscript{o}~762), Hippolyte Combes est rattrapé par la mobilisation générale d'août 1914. Incorporé le \textbf{31 mars 1915} au \textbf{10\textsuperscript{e} régiment d'artillerie à pied} à Toulon comme canonnier servant de 2\textsuperscript{e} classe, il se porte candidat au concours des interprètes militaires de l'Armée britannique. Nommé \textbf{interprète stagiaire de réserve} (assimilé au rang d'officier subalterne) par décision ministérielle du \textbf{29 novembre 1915} (publiée au \textit{Journal Officiel} du 5 décembre 1915), il rejoint aussitôt la \textbf{Mission militaire française attachée à l'Armée britannique} (\textit{British Expeditionary Force}).

\begin{itemize}
  \item \textbf{Hiver 1915 – Août 1916 : avec le 1\textsuperscript{er} bataillon des \textit{Irish Guards}.} D'abord affecté à l'une des unités les plus prestigieuses de la Couronne britannique — le \textit{1st Battalion, Irish Guards} (\textit{1st Guards Brigade, Guards Division}) —, il accompagne le régiment en Artois, dans le saillant d'Ypres, dans les Flandres françaises (Bailleul, Steenwerck) et sur la Somme (Lucheux).
  \item \textbf{Septembre 1916 – Avril 1917 : avec la \textit{152nd Company, Army Service Corps}.} Au début de septembre 1916, en pleine bataille de la Somme, il est affecté à la \textit{152nd Company A.S.C.} (compagnie du Train divisionnaire britannique), commandée par le capitaine Williams puis par le capitaine Panton. Il y exerce à la fois les fonctions d'\textbf{officier de cantonnement} (\textit{Billeting Officer}), d'\textbf{officier d'approvisionnement en fourrages} (\textit{Foraging Officer}) et de conciliateur juridique entre le commandement britannique et les municipalités françaises (Acheux, Forceville, Bernaville, Beauval, Humbercamps, Hérissart, Toutencourt).
  \item \textbf{Le mariage du 25 octobre 1917 et l'après-guerre.} Six mois après la clôture de ce carnet (achevé à Toutencourt le 30 avril 1917), il épouse à Millau, le \textbf{25 octobre 1917}, \textbf{Marguerite Calmels} (1891–1986), de quinze ans sa cadette. Affecté en novembre 1918 comme professeur d'anglais à l'École militaire préparatoire des Andelys puis nommé en janvier 1920 professeur au lycée Ingres de Montauban, il devient membre distingué de l'Académie de Montauban et s'éteint le 17 février 1970 dans sa quatre-vingt-quatorzième année.
\end{itemize}

\section{Histoire matérielle, codicologie et génétique du \textit{Livre-Journal}}

Le manuscrit édité dans le présent volume est un carnet de poche de fabrication britannique, relié en toile cirée noire souple à coins arrondis, comprenant \textbf{93 folios} (soit \textbf{186 clichés numériques} avec la couverture extérieure, numérotés de \texttt{20251126\_092853.jpg} à \texttt{20251126\_111833.jpg}). Sur le plat supérieur, une étiquette octogonale porte l'intitulé autographe : \textit{Livre - Journal / Du 25 juillet 1916 / au 30 avril 1917}.

L'examen codicologique et paléographique des 186 scans met en lumière quatre caractéristiques fondamentales :
\begin{enumerate}
  \item \textbf{Structure interne de la page.} Chaque page (ou séquence journalière) obéit à un protocole invariable hérité de la comptabilité ferroviaire et notariale : en haut à gauche, le quantième et le jour de la semaine abrégé (\textit{25 Ma.}, \textit{26 Mer.}), parfois soulignés ; en haut à droite, le mois et le millésime (\textit{Juillet 1916}, \textit{Août /16}) ; au centre, la chronique rédigée à la plume et à l'encre noire (ou au crayon graphite lors des marches sous la pluie et des bivouacs d'août–septembre 1916) ; enfin, au bas du folio, isolé par un trait horizontal ou par de grands crochets droits \texttt{[ ... ]}, le relevé minutieux des menues dépenses quotidiennes (repas, blanchissage, timbres, coiffeur, pourboires aux ordonnances).
  \item \textbf{La langue hybride du carnet : syntaxe télégraphique et « franglais » du front.} Écrivant pour lui-même à la lueur d'une bougie dans des chambres paysannes glaciales, Hippolyte Combes recourt à une syntaxe elliptique supprimant articles et pronoms sujets (\textit{« Toute nuit, passée très mauvaise »}, \textit{« Rentré billet, crotté y cape ruisselante »}), fait usage de l'abréviation tachygraphique \textit{y} (ou \textit{\&}) pour la conjonction \textit{et}, et intègre spontanément le lexique militaire et quotidien anglais (\textit{breakfast, lunch, tea-dinner, mess, billet, billeting, cottage, garret, washing, darning, shift, shifting, shifterons, lorry, limber G.S., refilling point, Purchase Board, green forage, warrant, nice, home}).
  \item \textbf{Restitution du Folio 24 recto (Scan \#050, \texttt{20251126\_103019.jpg}).} La collation systématique des 186 scans avec le premier brouillon de transcription (\texttt{Carnet de campagne édition diplomatique.docx}, qui ne comptait que 73 notices pour les 74 premiers clichés) a révélé que le cliché \texttt{20251126\_103019.jpg} (Scan \#050, Folio 24 recto : journée du lundi 25 septembre 1916 à Forceville et au \textit{railhead} d'Acheux-Varennes) avait été omis, provoquant un décalage d'une unité à partir du Scan \#051. Nous l'avons intégralement transcrit, commenté et rétabli à sa place.
  \item \textbf{Rétablissement de l'ordre chronologique des Scans \#063 et \#064.} Lors de la campagne de numérisation du 26 novembre 2025, le Folio 31 recto (\texttt{20251126\_103538.jpg}, Scan \#063 : journée du jeudi 5 octobre 1916 à Paris et dans le train vers Amiens) a été photographié seize secondes avant le Folio 30 verso (\texttt{20251126\_103554.jpg}, Scan \#064 : nuit du 4 au 5 octobre 1916 dans le train entre Toulouse et Paris). Notre édition conserve le numéro d'archive exact de chaque cliché tout en associant à chaque image sa transcription diplomatique propre.
\end{enumerate}

\section{Principes de l'édition philologique en vis-à-vis}

Inspirée des principes de l'édition philologique classique, la présente édition met en regard, sur chaque double page (du Scan \#001 au Scan \#186) :
\begin{itemize}
  \item \textbf{Sur la page de gauche (page paire / verso) :}
    \begin{enumerate}
      \item \textbf{La transcription diplomatique intégrale}, respectant scrupuleusement la disposition linéaire du manuscrit original, l'orthographe, les abréviations, la ponctuation par tirets et les soulignements d'Hippolyte Combes, avec une numérotation marginale gauche de cinq en cinq lignes (\texttt{5, 10, 15, 20, 25}).
      \item \textbf{L'apparat critique en marge droite, aligné horizontalement dans le prolongement exact de la ligne concernée}, qui développe les abréviations tachygraphiques (\textit{scil.}, \textit{abbr. pro}), signale les ratures et biffures du manuscrit ($[\![ \dots ]\!]$ \textit{del. in ms.}), identifie les emprunts anglais (\textit{angl. in ms.}) et précise les particularités matérielles de la ligne (\textit{in marg. cum unco}).
      \item \textbf{Deux niveaux de commentaire en bas de page :}
        \begin{itemize}
          \item \textit{Niveau 1 — Commentaire critique (interne à l'histoire du carnet) :} analyse codicologique, paléographique (variations de ductus, passage de la plume au crayon), linguistique (syntaxe elliptique, bilinguisme franco-britannique), comptable (tenue de la caisse, indemnités de mess) et psychologique (rythme de la correspondance amoureuse, \textit{spleen}).
          \item \textit{Niveau 2 — Commentaire historique :} contextualisation militaire précise des opérations de la \textit{British Expeditionary Force} (Somme, Flandres, Artois), identification des unités (\textit{1st Irish Guards}, \textit{Royal Scots}, \textit{Royal Fusiliers}, \textit{152nd Coy A.S.C.}), topographie des cantonnements et prosopographie familiale.
        \end{itemize}
    \end{enumerate}
  \item \textbf{Sur la page de droite (page impaire / recto) :} \textbf{le fac-similé photographique complet} du feuillet manuscrit correspondant, accompagné de ses références archivistiques et codicologiques.
\end{itemize}

\section{Répertoire prosopographique, militaire et topographique}

\begin{small}
\renewcommand{\arraystretch}{1.18}
\noindent\begin{longtable}{@{}p{44mm}p{128mm}@{}}
\toprule
\textbf{Nom / Unité / Lieu} & \textbf{Identification biographique, militaire ou géographique} \\
\midrule
\endhead
\textbf{Combes, Hippolyte} (1876–1970) & Auteur du \textit{Livre-Journal}. Licencié en droit, interprète stagiaire de réserve (29 nov. 1915) auprès de la B.E.F. Épouse Marguerite Calmels à Millau le 25 octobre 1917. Professeur d'anglais au lycée Ingres de Montauban (1920) et membre de l'Académie de Montauban. \\
\textbf{Calmels, Marguerite} (« Marg. », « Gueïte », 1891–1986) & Fiancée puis épouse d'Hippolyte Combes, résidant à Millau (Aveyron). Destinataire et expéditrice quotidienne des lettres qui rythment tout le journal. \\
\textbf{Combes, Pierre} (1847–1928) \& \textbf{Mélanie} (née en 1851) & Parents d'Hippolyte, résidant au domaine familial de La Valette (commune de Saint-Beauzély, Aveyron). \\
\textbf{Joséphine} (née en 1882) \& \textbf{Léon} & Sœur et beau-frère d'Hippolyte, établis à Bordeaux (Gironde), où Hippolyte séjourne en février 1917. \\
\textbf{Marie} (née en 1875) \& \textbf{Paul} & Sœur et beau-frère d'Hippolyte résidant à Paris, chez qui l'interprète fait étape lors de chaque traversée de la capitale. \\
\textbf{Combes, Émile} (né en 1883) & Frère cadet d'Hippolyte, médecin militaire mobilisé sur le front français. \\
\textbf{Combes, Jean} (né en 1891) & Jeune frère d'Hippolyte, sous-officier au 9\textsuperscript{e} R.A.C. puis pilote dans l'aviation à l'Armée d'Orient (Salonique). \\
\textbf{1st Battalion, Irish Guards} & Bataillon de la Garde irlandaise (\textit{1st Guards Brigade, Guards Division}), créé en 1900 par la reine Victoria. Hippolyte y sert de décembre 1915 à août 1916 (Lucheux, Ebenezer, Bailleul, Steenwerck). \\
\textbf{152nd Company, A.S.C.} & Compagnie hippomobile et automobile du Train britannique (\textit{Army Service Corps}), rattachée au train divisionnaire / XIII\textsuperscript{e} Corps. Unité d'Hippolyte de septembre 1916 à avril 1917. \\
\textbf{Capt. Williams} (« Capt. W. ») & Capitaine britannique commandant la \textit{152nd Coy A.S.C.} et le mess n\textsuperscript{o}~104 dans la Somme (Acheux, Forceville, Hérissart, Toutencourt). \\
\textbf{Capt. Panton} & Capitaine britannique de la \textit{152nd Coy A.S.C.}, compagnon de chevauchées d'Hippolyte en octobre–novembre 1916 (Barlette, Ribeaucourt, Beauval, Bailleulmont). \\
\textbf{Lt. Curtis, Lt. Gilbert, Lt. First} & Officiers subalternes britanniques avec lesquels Hippolyte effectue ses tournées quotidiennes en fourgon ou en automobile pour les réquisitions de fourrages (\textit{foraging}), les cantonnements (\textit{billeting}) et les expertises agricoles. \\
\textbf{Connelly \& Barlette} & Ordonnances (\textit{batmen} / \textit{grooms}) attachés au service des officiers et d'Hippolyte Combes. \\
\bottomrule
\end{longtable}
\end{small}
"""

    body_parts = [preamble, "\n\\mainmatter\n"]

    # Map records by scan_num (1..186)
    rec_by_num = {r["scan_num"]: r for r in records}

    for ch in CHAPTERS:
        ch_num = ch["num"]
        ch_title = ch["title"]
        ch_sub = ch["subtitle"]
        s_start = ch["scan_start"]
        s_end = ch["scan_end"]
        ch_sum = ch["summary"]
        ch_intro = ch["intro"]
        illus_list = ch["illustrations"]

        # Build non-floating illustrations block so the entire chapter intro fits on ONE odd page
        illus_boxes = []
        for img_path, img_cap, img_w in illus_list:
            illus_boxes.append(f"""  \\begin{{minipage}}[b]{{{img_w}}}
    \\centering
    \\setlength{{\\fboxsep}}{{1mm}}\\setlength{{\\fboxrule}}{{0.4pt}}%
    \\fcolorbox{{gray!60}}{{white}}{{\\includegraphics[width=0.95\\linewidth,height=40mm,keepaspectratio]{{{img_path}}}}}
    \\par\\vspace{{1mm}}{{\\scriptsize {img_cap}}}
  \\end{{minipage}}""")
        illus_joined = "\\hfill\n".join(illus_boxes)

        ch_tex = f"""
% =============================================================================
% CHAPITRE {ch_num} (SCANS #{s_start:03d} A #{s_end:03d})
% =============================================================================
\\cleardoublepage
\\chapter{{Chapitre {ch_num} : {ch_title}}}
\\markboth{{Chapitre {ch_num} — {ch_title}}}{{Scans \\#{s_start:03d} à \\#{s_end:03d}}}

\\noindent{{\\normalsize\\textit{{{ch_sub}}}}}\\\\[2mm]
\\noindent\\colorbox{{headerbg}}{{%
  \\parbox{{\\dimexpr\\textwidth-2\\fboxsep\\relax}}{{%
    \\vspace{{1mm}}%
    \\noindent\\textbf{{\\small\\textsc{{Résumé analytique du Chapitre {ch_num} (Scans \\#{s_start:03d} à \\#{s_end:03d}) :}}}}\\\\[0.8mm]
    {{\\footnotesize {ch_sum}}}%
    \\vspace{{1mm}}%
  }}%
}}\\\\[2.5mm]

\\noindent\\textbf{{\\normalsize\\textcolor{{bordeaux}}{{Introduction historique et philologique}}}}\\\\[1mm]
{{\\small {ch_intro}}}

\\vfill
\\noindent\\begin{{center}}
{illus_joined}
\\end{{center}}
\\clearpage
"""
        body_parts.append(ch_tex)

        for s_idx in range(s_start, s_end + 1):
            body_parts.append(build_spread_latex(rec_by_num[s_idx]))

    # Appendices: War letters & Military Service Record
    appendices_tex = r"""
% =============================================================================
% ANNEXES DOCUMENTAIRES ET ÉPISTOLAIRES
% =============================================================================
\cleardoublepage
\appendix
\chapter{Correspondance de guerre inédite et pièces justificatives (1915–1916)}
\markboth{Annexe I — Correspondance de guerre}{Annexe I — Correspondance de guerre}

Les archives familiales d'Hippolyte Combes conservées à La Valette et à Millau renferment quatre documents autographes de la Grande Guerre qui éclairent directement la genèse et le contenu du \textit{Livre-Journal}. Nous en donnons ici l'édition diplomatique et critique intégrale.

\section{Document 1 : Lettre du front d'Hippolyte Combes au capitaine commandant la Mission militaire française (février 1916)}
\noindent\textbf{Source :} \texttt{archives\_militaires/lettres\_de\_guerre/lettre fev 1916 au front à un capitaine.pdf} (brouillon autographe à l'encre sur papier à lettres, 2 pages).

\begin{quote}\small
« Au front, le [\dots] février 1916.\\[1mm]
Mon Capitaine,\\
J'ai l'honneur de solliciter de votre haute bienveillance quelques jours de permission pour affaires personnelles urgentes à régler dans ma famille et à Paris.\\
Depuis mon arrivée au front britannique au début de décembre dernier, je n'ai pris aucun congé et j'ai assuré sans interruption le service d'interprète auprès du 1\textsuperscript{er} Bataillon des \textit{Irish Guards}. Mon commandant d'unité ne voit aucun inconvénient à mon absence pendant la période actuelle de repos du bataillon.\\
Dans l'espoir que vous voudrez bien accueillir favorablement ma demande, je vous prie d'agréer, mon Capitaine, l'expression de mon profond et très respectueux dévouement.\\[1mm]
\hfill \textbf{H. Combes}, Interprète stagiaire aux \textit{1st Irish Guards}. »
\end{quote}

\noindent\textbf{Commentaire :} Cette lettre de février 1916 confirme qu'Hippolyte Combes a rejoint le front britannique dès le début de décembre 1915, immédiatement après sa nomination du 29 novembre 1915, et qu'il a servi plus de huit mois consécutifs auprès du \textit{1st Battalion, Irish Guards} avant l'ouverture du \textit{Livre-Journal} en juillet 1916.

\section{Document 2 : Lettre d'Hippolyte Combes à sa sœur Joséphine (Au front, 16 juin 1916)}
\noindent\textbf{Source :} \texttt{archives\_militaires/lettres\_de\_guerre/lettre de Hippolyte à sa soeur Josephine - 16 juin 1916 - Au front.pdf} (lettre autographe signée, 4 pages).

\begin{quote}\small
« Au front, le 16 juin 1916.\\[1mm]
Ma bien chère Joséphine,\\
Je profite d'une matinée plus calme dans notre cantonnement flamand pour répondre à ta bonne lettre qui m'a fait grand plaisir. Ici, le temps reste désespérément gris, pluvieux et froid pour un mois de juin : on se croirait en novembre ! Nous avons quitté les tranchées boueuses du saillant pour quelques jours de repos à l'arrière, dans un village entouré de houblonnières et de pâtures verdoyantes.\\
Mon service auprès des officiers des \textit{Irish Guards} est toujours très absorbant : dès qu'on arrive dans une localité, il faut courir de ferme en ferme avec le \textit{Billeting Officer} pour loger tout le monde, apaiser les réclamations des paysans flamands et régler mille détails matériels. Mais les officiers du mess sont d'une courtoisie parfaite à mon égard.\\
J'ai eu récemment de bonnes nouvelles de La Valette, de Papa et de Maman, ainsi que de Jean à Salonique et d'Émile. Écris-moi souvent, ma chère Phine ; les lettres de la famille et de Millau sont mon meilleur réconfort dans cette vie errante.\\
Je vous embrasse bien tendrement tous les deux, Léon et toi.\\[1mm]
\hfill Ton frère affectionné, \textbf{Hippolyte}. »
\end{quote}

\noindent\textbf{Commentaire :} Rédigée cinq semaines avant la première page du \textit{Livre-Journal}, cette lettre à sa sœur Joséphine (installée à Bordeaux avec son mari Léon) annonce déjà tous les leitmotive littéraires et psychologiques du carnet : la mélancolie du ciel flamand (« on se croirait en novembre »), le labeur harassant du \textit{billeting} de ferme en ferme, la distinction aristocratique du mess des \textit{Irish Guards} et le rôle vital du courrier familial.

\section{Document 3 : Rapport officiel en anglais d'Hippolyte Combes sur l'incident d'Humbercamps (5 novembre 1916)}
\noindent\textbf{Source :} \texttt{archives\_militaires/lettres\_de\_guerre/lettre de l'interprete combes pour un incident.pdf} (minute autographe en anglais à l'encre noire).

\begin{quote}\small
« Couturelle, November 5th, 1916.\\[1mm]
\textbf{To the Officer Commanding 152nd Coy A.S.C.}\\[1mm]
Sir,\\
With reference to the complaint lodged by the Mayor of Humbercamps regarding damages alleged to have been caused on November 3rd in a barn occupied by men of the unit (wooden partitions pulled down and planks burnt), I beg to report that I proceeded yesterday to Humbercamps in order to investigate the matter on the spot.\\
After careful inspection of the premises in the presence of the owner and the Garde-Champêtre, it appears that most of the dilapidations complained of were of ancient date and caused by troops previously billeted in the village before our arrival. The actual damage attributable to our men does not exceed the sum of fifteen francs (15 fr.), which the owner agreed to accept in full settlement of his claim.\\[1mm]
\hfill I have the honour to be, Sir, your obedient Servant,\\
\hfill \textbf{H. Combes}, Interpreter attached 152nd Coy A.S.C. »
\end{quote}

\noindent\textbf{Commentaire :} Ce document exceptionnel recoupe mot pour mot les entrées des \textbf{3, 4 et 5 novembre 1916} du \textit{Livre-Journal} (Folios 40v–42v, Scans \#083 à \#087). Il illustre concrètement le rôle juridique et financier de l'interprète militaire français au sein de l'\textit{Army Service Corps} : grâce à sa formation de licencié en droit et d'ancien clerc d'avoué, Hippolyte procède à un véritable constat contradictoire (\textit{investigation on the spot}) avec le maire et le garde-champêtre d'Humbercamps pour ramener une réclamation exagérée à une juste indemnité forfaitaire de 15 francs.

\section{Document 4 : \textit{La Prière de l'aviateur} (poème satirique de front, 1915)}
\noindent\textbf{Source :} \texttt{archives\_militaires/lettres\_de\_guerre/un poeme.pdf} (copie autographe à l'encre).

Ce feuillet conservé parmi les papiers militaires d'Hippolyte Combes contient la copie calligraphiée d'un pastiche en vers intitulé \textit{La Prière de l'aviateur} (parodie de la prière chrétienne adaptée aux aléas des moteurs d'aviation et des permissions de 1915–1916), probablement adressé par ou destiné à son jeune frère \textbf{Jean Combes} (né en 1891), passé de l'artillerie à l'aviation militaire à l'Armée d'Orient.

\chapter{État signalétique des services et table synoptique des 186 scans}
\markboth{Annexe II — État des services et table des scans}{Annexe II — État des services et table des scans}

\section{Résumé de la fiche matricule d'Hippolyte Combes (Classe 1896, Matricule 762, Subdivision de Rodez)}

\begin{figure}[htbp]
  \centering
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=56mm,keepaspectratio]{illustrations/mariage_millau_1917.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 3.} Mariage d'Hippolyte et Marguerite à Millau (30 avril 1917).}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=56mm,keepaspectratio]{illustrations/famille_combes_1925.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 4.} Hippolyte et Marguerite Combes entourés de leurs enfants (vers 1925).}
  \end{minipage}
\end{figure}

\begin{itemize}
  \item \textbf{État civil :} Hippolyte Pierre Jean Combes, né le 29 septembre 1876 à La Valette (commune de Saint-Beauzély, canton de Saint-Beauzély, arrondissement de Millau, Aveyron), fils de Pierre Combes et de Mélanie Combes.
  \item \textbf{Incorporation et campagnes (1915–1919) :}
    \begin{itemize}
      \item Incorporé au \textbf{10\textsuperscript{e} Régiment d'Artillerie à Pied} à Toulon le \textbf{31 mars 1915} (canonnier servant de 2\textsuperscript{e} classe).
      \item Nommé \textbf{interprète stagiaire de réserve} au corps des interprètes militaires (Armée britannique) par décision ministérielle du \textbf{29 novembre 1915} (\textit{J.O.} du 5 décembre 1915).
      \item Détaché auprès du \textbf{1st Battalion, Irish Guards} (\textit{Guards Division}) de décembre 1915 à août 1916.
      \item Détaché auprès de la \textbf{152nd Company, Army Service Corps} de fin août 1916 au printemps 1917.
      \item Promu \textbf{officier interprète de 3\textsuperscript{e} classe} par décret du \textbf{7 décembre 1917} (\textit{J.O.} du 11 décembre 1917).
      \item Démobilisé en 1919 ; titulaire de la \textbf{Médaille commémorative britannique (\textit{British War Medal})}.
    \end{itemize}
\end{itemize}

\section{Table de concordance intégrale des 186 clichés numériques}

Tous les clichés originaux sont disponibles en double résolution à la racine du dépôt :
\begin{enumerate}
  \item \texttt{scans\_haute\_qualite/} : 186 fichiers JPEG haute résolution non compressés (1,03 Go au total, env. 5,9 Mo par scan) ;
  \item \texttt{scans\_compresses/} : 186 fichiers JPEG optimisés pour la transcription automatique et l'édition électronique (31,1 Mo au total).
\end{enumerate}

\end{document}
"""

    body_parts.append(appendices_tex)
    full_tex = "".join(body_parts)

    with open(OUT_TEX, "w", encoding="utf-8") as f:
        f.write(full_tex)
    print(f"Successfully generated {OUT_TEX} ({len(full_tex)} bytes)")


if __name__ == "__main__":
    generate_full_tex()
