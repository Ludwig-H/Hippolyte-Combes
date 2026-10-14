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
            "militaire auprès du 1\\textsuperscript{er} bataillon des \\textit{Irish Guards}. Après une ultime étape à Lucheux "
            "(Somme), l'unité remonte par Saint-Pol-sur-Ternoise vers la Flandre française et belge : cantonnement au "
            "pensionnat protestant abandonné d'\\textit{Ebenezer} près de Pradelles, marche vers l'abbaye trappiste du "
            "Mont-des-Cats et Poperinghe, puis séjour prolongé à Bailleul et au hameau de La Crèche (Steenwerck)."
        ),
        "intro": (
            "Lorsqu'il ouvre ce carnet à Lucheux le mardi 25 juillet 1916, Marie Lucien Hippolyte Combes (né à Millau le "
            "14 août 1876, licencié en droit et ès lettres, ancien sous-chef de gare à Brive-la-Gaillarde, résident quatre "
            "ans à Nottingham puis professeur d'anglais aux collèges de Corte, Blaye et Nogent-le-Rotrou) approche de "
            "ses quarante ans. Passé du 10\\textsuperscript{e} régiment d'artillerie à pied de Toulon à la Mission militaire "
            "française attachée à l'Armée britannique le 4 mai 1915, il partage alors le quotidien aristocratique et exigeant "
            "des officiers du 1\\textsuperscript{er} bataillon des \\textit{Irish Guards} (\\textit{1st Guards Brigade, "
            "Guards Division}).\n\n"
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
            ("illustrations/toulon_artillerie_1915.jpg", "Hippolyte Combes au 10\\textsuperscript{e} régiment d'artillerie à pied à Toulon (Saint-Jean-du-Var) au printemps 1915.", "0.44\\textwidth"),
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
            "à une unité logistique du Train de la 18\\textsuperscript{e} Division britannique — la \\textit{152nd Company, "
            "Army Service Corps} —, il rejoint le secteur nord de la bataille de la Somme (Raincheval, Acheux-en-Amiénois, "
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
            ("illustrations/hippolyte_1897.jpg", "Hippolyte Combes jeune homme en 1897 (à l'âge de vingt et un ans), étudiant à Toulouse avant son séjour de quatre ans à Nottingham.", "0.42\\textwidth"),
        ],
    },
    {
        "num": "III",
        "title": "La première permission : d'Acheux-Varennes à Paris et au Midi",
        "subtitle": "Forceville, gare d'Acheux-Varennes, Amiens, Paris, Neuilly, Toulouse, Millau et le retour en Picardie (25 septembre – 6 octobre 1916)",
        "scan_start": 50,
        "scan_end": 66,
        "summary": (
            "Ce troisième chapitre (Folios 24r à 32r, Scans \\#050 à \\#066) forme une respiration lumineuse au milieu du "
            "carnet : le récit intégral de la première permission d'Hippolyte Combes (25 septembre – 6 octobre 1916). "
            "Il s'ouvre sur le Folio 24 recto (Scan \\#050, restitué pour la première fois dans la présente édition), qui "
            "décrit le réveil à 4 h du matin le 25 septembre, la dernière corvée de \\textit{green forage} à Forceville et "
            "l'attente au \\textit{railhead} d'Acheux-Varennes. Après une escale à Paris et Neuilly (26 septembre), Hippolyte "
            "séjourne à Toulouse (27–28 septembre) puis à Millau auprès de Marguerite Calmels (29 septembre – 3 octobre), "
            "avant le voyage de retour par Toulouse, Paris et Amiens vers le hameau de Barlette près de Bernaville (Scans \\#063–\\#066)."
        ),
        "intro": (
            "L'intérêt philologique et documentaire de ce troisième chapitre est double. Sur le plan codicologique, l'examen "
            "direct des 186 clichés a permis de résoudre deux anomalies qui affectaient les transcriptions antérieures : "
            "1° la restitution intégrale du cliché \\texttt{20251126\\_103019.jpg} (Scan \\#050, Folio 24 recto : journée du "
            "lundi 25 septembre 1916 jusqu'au départ du train de 18 h 40 à Acheux-Varennes), qui avait été omis lors du premier "
            "dépouillement ; 2° le rétablissement de l'ordre exact entre les clichés \\texttt{20251126\\_103538.jpg} (Scan \\#063, "
            "5 octobre 1916) et \\texttt{20251126\\_103554.jpg} (Scan \\#064, nuit du 4 au 5 octobre 1916).\n\n"
            "Sur le plan biographique, ces pages offrent un tableau saisissant du contraste entre la boue de la Somme et "
            "la douceur de l'arrière méridional à l'automne 1916 : visite à sa cousine Mme Faure à Neuilly, liquidation "
            "partielle de ses souvenirs d'étudiant à Toulouse, journées d'intimité avec Marguerite à Millau, mais aussi "
            "mélancolie poignante de l'arrachement au départ du 4 octobre."
        ),
        "illustrations": [
            ("illustrations/marguerite_1917.jpg", "Marguerite Calmels (1892--1986), photographiée par le studio Jublin à Millau à l'époque de ses fiançailles avec Hippolyte Combes.", "0.42\\textwidth"),
            ("illustrations/maison_millau.jpg", "La demeure familiale de Millau (Aveyron), berceau de la famille Combes.", "0.46\\textwidth"),
        ],
    },
    {
        "num": "IV",
        "title": "L'automne dans la Somme : de Ribeaucourt au bivouac d'Albert et au XIIIe Corps à Acheux",
        "subtitle": "Barlette, Ribeaucourt, Bernaville, Beauval, Warloy-Baillon, Albert (Brickfield Area), La Boisselle et le détachement à Acheux (7 octobre – 30 novembre 1916)",
        "scan_start": 67,
        "scan_end": 104,
        "summary": (
            "Ce quatrième chapitre (Scans \\#067 à \\#104) couvre près de deux mois de campagne d'automne (7 octobre – "
            "30 novembre 1916) au cœur de la bataille de la Somme. De retour de permission au hameau de Barlette (Ribeaucourt) "
            "près de Bernaville (7–14 octobre), Hippolyte gagne Beauval (15 octobre) et Warloy-Baillon (16–17 octobre), puis "
            "bivouaque pendant deux semaines aux portes mêmes d'Albert (\\textit{Brickfield Area}, 18 octobre – 1\\textsuperscript{er} "
            "novembre), visitant la basilique mutilée, le grand cratère et les abris souterrains allemands de La Boisselle "
            "ainsi que le cimetière dévasté le jour de la Toussaint. Le 2 novembre 1916, sur ordre signé du colonel Grose, "
            "il est détaché à Acheux-en-Amiénois avec le lieutenant Curtis auprès du XIII\\textsuperscript{e} Corps britannique, "
            "assistant aux bombardements et aux convois de blessés et de prisonniers de la bataille de Beaumont-Hamel et de "
            "Beaucourt-sur-l'Ancre (13–18 novembre 1916)."
        ),
        "intro": (
            "Entre le début d'octobre et la fin de novembre 1916, le journal d'Hippolyte Combes offre un témoignage de premier "
            "ordre sur la phase finale de l'offensive britannique de la Somme. Au camp de Bouzincourt puis au \\textit{Brickfield "
            "Area} d'Albert (Scans \\#077 à \\#089), l'interprète vit au rythme du duel d'artillerie formidable qui fait trembler "
            "vitres et portes jour et nuit, contemple la « Vierge penchée » au sommet du clocher de briques rouges et médite "
            "devant les tombes éventrées du cimetière d'Albert et les croix blanches des soldats anglais \\textit{killed in action}.\n\n"
            "Son détachement à Acheux-en-Amiénois le 2 novembre 1916 (Scan \\#090), où il s'installe le 5 novembre dans une "
            "chambre au n\\textsuperscript{o}~1 de la route de Léalvillers chez le tailleur M. Carluvant (Scan \\#094), "
            "inaugure trois mois de courses incessantes en automobile à travers les villages boueux de l'Amiénois et de "
            "l'Artois (Bertrancourt, Arquèves, Ferme de Belle-Église, Coisy, Hérissart, Forceville, Varennes, Doullens, "
            "Frévent, Authie, Martinsart) pour acheter paille et foin au profit du XIII\\textsuperscript{e} Corps."
        ),
        "illustrations": [
            ("illustrations/fiche_matricule.jpg", "Extrait du registre matricule d'Hippolyte Combes (classe 1896, matricule 911, bureau de recrutement de Toulouse) détaillant ses services auprès de la Mission militaire française attachée à l'Armée britannique (4 mai 1915 -- 11 novembre 1918).", "0.78\\textwidth"),
        ],
    },
    {
        "num": "V",
        "title": "L'hiver 1916–1917 à Acheux : le jeune capitaine Williams, la crise de Noël et le grand gel",
        "subtitle": "L'arrivée du capitaine Williams, l'incident du « Bloody France ! », le Noël solitaire à Acheux, l'excursion à Amiens et le gel de janvier 1917 (1er décembre 1916 – 25 janvier 1917)",
        "scan_start": 105,
        "scan_end": 127,
        "summary": (
            "Ce cinquième chapitre (Scans \\#105 à \\#127) retrace la vie quotidienne d'Hippolyte Combes à Acheux-en-Amiénois "
            "du 1\\textsuperscript{er} décembre 1916 au 25 janvier 1917. Le 2 décembre (Scan \\#105), le lieutenant Curtis "
            "est remplacé par un très jeune officier de vingt ans, le capitaine Williams (ancien \\textit{office boy} à "
            "50 livres par an avant la guerre, Scan \\#107), dont le caractère présomptueux provoque de vives tensions : "
            "le 24 décembre à Louvencourt, son exclamation « \\textit{Bloody France !} » indigne Hippolyte au moment même "
            "où une lettre de Marguerite éveille des « velléités de rupture » (Scan \\#112), avant que Williams ne lui "
            "présente d'humbles excuses le 30 décembre (Scan \\#117). Janvier 1917 est marqué par une excursion à Amiens "
            "(3 janvier, Scan \\#119), une visite au collectionneur M. Renard à Auxi-le-Château (17 janvier, Scan \\#124) "
            "et l'installation d'un gel polaire qui fige l'eau dans les chambres jusqu'à la veille du départ en permission."
        ),
        "intro": (
            "Au cœur de l'hiver 1916–1917, le \\textit{Livre-Journal} atteint une intensité psychologique remarquable. "
            "La confrontation quotidienne entre l'universitaire français de quarante ans et son nouveau chef de service "
            "britannique de vingt ans (« ce gosse de Williams », Scan \\#109) culmine en deux scènes dramatiques : la "
            "crise de conscience du soir de Noël 1916 (« \\textit{Dois-je faire 1 rapport à Mission frse ? Hanté aussi "
            "par lettre de Margte du 17 ct.} », Scan \\#114) et l'explication ferme du 30 décembre à l'issue de laquelle "
            "le jeune capitaine, contrit et humilié, supplie son interprète de ne pas le quitter (Scan \\#117).\n\n"
            "Parallèlement, les tournées automobiles en voiture \\textit{Sunbeam} (jusqu'à Corbie, Marcelcave, Bayencourt, "
            "Saulty, Barly, Beauquesne et Auxi-le-Château), les concerts des \\textit{13th Corps Archie Singers} à la "
            "baraque du Y.M.C.A. d'Acheux et les paysages de neige cristallisée sous le soleil d'hiver composent une "
            "chronique d'une grande richesse documentaire et littéraire."
        ),
        "illustrations": [
            ("illustrations/camarades_ailly_1919.jpg", "Souvenir de camaraderie militaire sur le front de Picardie (carte-photo dédicacée à Hippolyte Combes, Ailly-sur-Noye, mai 1919). Collection familiale.", "0.50\\textwidth"),
        ],
    },
    {
        "num": "VI",
        "title": "La deuxième permission : par Gézaincourt, Amiens et Neuilly vers Toulouse et Millau",
        "subtitle": "Le départ dans la neige étincelante, Mme Faure à Neuilly, Marguerite à Sainte-Marie (Toulouse), le cours d'Ernest Zyromski, l'horloger Pfister et le séjour chez les Calmels à Millau (26 janvier – 7 février 1917)",
        "scan_start": 128,
        "scan_end": 146,
        "summary": (
            "Ce sixième chapitre (Scans \\#128 à \\#146) livre le récit intégral et authentique de la deuxième permission "
            "d'Hippolyte Combes (26 janvier – 7 février 1917). Parti de la gare de Varennes le 26 janvier devant les champs "
            "de neige étincelant « comme des grains de diamant », il attend six heures à Gézaincourt, passe la nuit glaciale "
            "à Amiens avec son collègue Boilly, déjeune le 27 janvier chez Mme Faure au 16 rue d'Armenonville à Neuilly et "
            "arrive à Toulouse le dimanche 28 janvier (Scan \\#132). Accueilli avec une tendresse infinie par Marguerite à "
            "Sainte-Marie (Scan \\#133), il visite avec elle les cryptes de Saint-Sernin, l'Hôtel d'Assézat et la Daurade, "
            "assiste à une conférence d'Ernest Zyromski sur Maurice de Guérin (Scan \\#135) et lui achète un remontoir en or "
            "Louis XVI de 105 francs chez Pfister (Scan \\#138). Le 3 février, les fiancés voyagent ensemble par Carcassonne, "
            "Béziers et Bédarieux jusqu'à Millau (Scan \\#139), où Hippolyte est reçu dans la demeure des parents de Marguerite "
            "avant de repartir le 5 février au soir par Saint-Flour, Brioude, Clermont-Ferrand, Paris et Amiens pour regagner "
            "Acheux le 7 février à 13 h 30 (Scan \\#146)."
        ),
        "intro": (
            "Cette deuxième permission (26 janvier – 7 février 1917) constitue le sommet affectif et autobiographique du "
            "\\textit{Livre-Journal}. Dès son arrivée à Toulouse le dimanche 28 janvier (« \\textit{En approchant de Toulouse, "
            "souvenirs jeunesse revenus en foule esprit. Cru revoir mère et sœurs, m'attendant, cme autrefois, gare} », "
            "Scan \\#132), l'accueil tendre et spontané de Marguerite à Sainte-Marie dissipe jusqu'au souvenir des nuages "
            "de décembre. Six jours durant, les fiancés parcourent Toulouse sous la neige et le soleil d'hiver, avant de "
            "gagner ensemble Millau (« \\textit{Délicieuse intimité s/ l'épaule de Mte... Impression silence profond en "
            "débarquant ville natale} », Scan \\#139).\n\n"
            "La nuit du 3 au 4 février 1917 dans la maison Calmels à Millau (Scan \\#141) et la visite des deux fiancés "
            "au cimetière le 5 février (Scan \\#143) comptent parmi les pages les plus poignantes du manuscrit : "
            "« \\textit{Silence impressionnant vallon natal. Couché depuis 1/2 h., quand souvenirs venus en foule et obsédé. "
            "Pensé à Papa, Maman, Sœurs — que j'ai tant aimés. Peu à peu, gagné par l'émotion, et sangloté.} »"
        ),
        "illustrations": [
            ("illustrations/mariage_millau_1917.jpg", "Photographie officielle du mariage d'Hippolyte Combes (en uniforme d'interprète militaire) et de Marguerite Calmels à Millau (25 octobre 1917), entourés des familles Combes et Calmels.", "0.50\\textwidth"),
            ("illustrations/menu_mariage_1917.jpg", "Menu du repas de noces d'Hippolyte Combes et Marguerite Calmels au 10 rue Alfred-Guibert à Millau (25 octobre 1917). Archives familiales.", "0.36\\textwidth"),
        ],
    },
    {
        "num": "VII",
        "title": "De l'hiver polaire au renouveau printanier : d'Hérissart à Toutencourt",
        "subtitle": "Le déménagement imprévu à Hérissart, le départ du capitaine Williams, le repli allemand sur la ligne Hindenburg, les neiges d'avril à Toutencourt et l'hymne au printemps (7 février – 30 avril 1917)",
        "scan_start": 147,
        "scan_end": 186,
        "summary": (
            "Ce septième et dernier chapitre (Folios 73v à 93r, Scans \\#147 à \\#186) conduit le \\textit{Livre-Journal} "
            "jusqu'à son dernier feuillet (7 février – 30 avril 1917). Dès son retour à Acheux le 7 février après-midi "
            "(Scan \\#147), Hippolyte apprend que le capitaine Williams a transféré le bureau à Hérissart, où il s'installe "
            "chez Mlle Octavie sous un gel polaire. Le 10 mars 1917 (Scan \\#165), le départ définitif de Williams et le "
            "retour des lieutenants Curtis et Gilbert transforment l'atmosphère du service. Installé à Toutencourt à partir "
            "du 16 mars (Scan \\#169), Hippolyte suit avec passion les nouvelles du repli allemand, de la Révolution russe, "
            "de l'entrée en guerre des États-Unis et de l'offensive d'Arras, tout en sillonnant la Picardie jusqu'à la "
            "radieuse journée printanière du lundi 30 avril 1917 (Scan \\#186)."
        ),
        "intro": (
            "Les quarante derniers clichés du manuscrit (Scans \\#147 à \\#186) offrent une chronique particulièrement "
            "dense (souvent vingt-quatre à vingt-sept lignes par page) des mois de février, mars et avril 1917 dans les "
            "villages situés entre Amiens, Albert et Doullens (Hérissart, Toutencourt, Harponville, Warloy-Baillon, "
            "Vadencourt, Contay, Villers-Bocage). Après un mois de février glacial à Hérissart, le départ du capitaine "
            "Williams le 10 mars 1917 (Scan \\#165) est accueilli comme une véritable délivrance, et l'entente cordiale "
            "avec les lieutenants Curtis et Gilbert rend les longues tournées en automobile beaucoup plus plaisantes.\n\n"
            "Le \\textit{Livre-Journal} s'achève le \\textbf{lundi 30 avril 1917} (Folio 93 recto, Scan \\#186), exactement "
            "sur la dernière page matérielle du registre, dans un véritable hymne au printemps enfin victorieux : "
            "« \\textit{Aujourd'hui encore, temps magnifique. Soleil ardent... Ciel d'un bleu pur \\& céleste. Aux arbres, "
            "bourgeons grossissent à vue d'œil... Nuit très belle, mervt éclairée, lune superbe.} »"
        ),
        "illustrations": [
            ("illustrations/andelys_ecole_militaire.jpg", "Photographie de groupe devant l'École militaire préparatoire des Andelys (où Hippolyte est nommé professeur d'anglais le 24 novembre 1918).", "0.31\\textwidth"),
            ("illustrations/famille_combes_1925.jpg", "Hippolyte et Marguerite Combes entourés de leurs enfants à Montauban / Millau vers 1925.", "0.31\\textwidth"),
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
  {\textsc{\chaptertitlename\ \Roman{chapter}}}
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
        {\large\textsc{Archives familiales de Millau, Toulouse \& du Front britannique}}\\[2mm]
        \rule{110mm}{0.6pt}\\[6mm]
        {\LARGE\textbf{HIPPOLYTE COMBES}}\\[2mm]
        {\normalsize\textsc{(Millau, 14 août 1876 — Montauban / Millau, 1970)}}\\[8mm]
        {\Huge\textbf{\textcolor{bordeaux}{LIVRE - JOURNAL}}}\\[3mm]
        {\Large\textbf{DE CAMPAGNE (1916–1917)}}\\[4mm]
        {\large\textit{Du 25 juillet 1916 au 30 avril 1917}}\\[3mm]
        {\normalsize Interprète militaire auprès de l'Armée britannique\\
        (\textit{1st Battalion Irish Guards}, \textit{152nd Company Army Service Corps} \& \textit{XIIIth Corps})}\\[7mm]
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
        {\footnotesize d'après le manuscrit original et les archives familiales Combes-Calmels de Millau et Montauban}\\[2mm]
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
  {\Large\textsc{Marie Lucien Hippolyte Combes}}\\
  {\small (1876–1970)}\\[14mm]
  {\huge\textbf{LIVRE-JOURNAL DE GUERRE}}\\[4mm]
  {\large\textit{25 juillet 1916 — 30 avril 1917}}\\[6mm]
  {\normalsize De la Somme aux Flandres et à l'Artois\\
  avec les \textit{Irish Guards} et l'\textit{Army Service Corps}}\\[20mm]
  {\Huge $\mathfrak{Urtext}$}\\[20mm]
  \rule{55mm}{0.4pt}\\[8mm]
  {\normalsize\textbf{Édition scientifique intégrale des 186 scans du manuscrit autographe}}\\[2mm]
  {\small accompagnée des lettres de guerre inédites (1916–1918), de l'état signalétique des services\\
  et d'un répertoire prosopographique, militaire et topographique}\par
  \vfill
  {\small\textsc{Collection des Sources et Manuscrits Contemporains}}\\
  {\footnotesize Millau — Toulouse — Montauban — Paris}
  \vspace*{10mm}
\end{center}
\newpage

\frontmatter
\renewcommand{\thesection}{\Roman{section}}
\tableofcontents
\cleardoublepage

% =============================================================================
% 3. PROLÉGOMÈNES SCIENTIFIQUES ET HISTORIQUES
% =============================================================================
\chapter{Prolégomènes : Hippolyte Combes (1876–1970) et son \textit{Livre-Journal} de la Grande Guerre}
\markboth{Prolégomènes}{Prolégomènes}

\section{Destin d'un universitaire rouergat et toulousain auprès de l'Armée britannique (1876–1970)}

Né le \textbf{14 août 1876} à \textbf{Millau} (Aveyron), rue des Barris (acte de naissance n\textsuperscript{o}~395 du 16 août 1876), \textbf{Marie Lucien Hippolyte Combes} est issu d'une ancienne lignée de juristes et d'artisans millavois. Son père, \textbf{François Augustin Hippolyte Combes} (1825–1899), avocat né à Millau et établi par la suite à \textbf{Toulouse} (au 47 puis au 77 rue du Taur, tout près de la basilique Saint-Sernin), avait épousé à Millau le 22 juillet 1864 sa cousine \textbf{Marie Anaïs Alric} (1838–1907). Hippolyte grandit entouré de trois sœurs aînées demeurées célibataires : \textbf{Maria} (religieuse missionnaire en Tunisie, morte de la typhoïde à Carthage le 19 novembre 1903 à vingt-huit ans), \textbf{Françoise} (entrée au Carmel de Périgueux sous le nom de \textit{Sœur Marie de la Croix}, décédée le 16 juillet 1942 à soixante et onze ans, destinataire de sa lettre confidentielle du 16 juin 1916) et \textbf{Joséphine} (qui tint son ménage de jeune professeur et mourut subitement d'une crise cardiaque à Nogent-le-Rotrou en octobre 1914 à quarante et un ans).

Après ses études secondaires à Toulouse — au Petit Séminaire de l'Esquile, au collège jésuite du Caousou (où il se lie d'amitié avec le frère Rémi Ponsonailles) puis au Lycée de Toulouse —, Hippolyte Combes obtient sa \textbf{licence en droit}, son diplôme d'avocat et sa \textbf{licence ès lettres (anglais)} à l'Université de Toulouse. À la mort de son père en 1899, il entre aux chemins de fer et devient \textbf{sous-chef de gare à Brive-la-Gaillarde}. Démissionnaire pour découvrir l'Angleterre, il séjourne quatre années à \textbf{Nottingham}, où il enseigne le français, pratique la photographie et se lie avec la famille de \textbf{Beatrice Chilcott}. Rappelé en France par la mort de sa mère en 1907, il est nommé professeur d'anglais aux collèges de \textbf{Corte} (Corse), de \textbf{Blaye} (Gironde), puis de \textbf{Nogent-le-Rotrou} (Eure-et-Loir), où il réside au \textbf{17 rue Saint-Hilaire}.

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

Exempté dans sa jeunesse pour « faiblesse générale » (\textbf{classe 1896, bureau de recrutement de Toulouse, matricule n\textsuperscript{o}~911}), Hippolyte Combes est classé « Service armé » par le conseil de révision d'Eure-et-Loir le \textbf{18 décembre 1914}. Appelé à l'activité le \textbf{20 mars 1915} et incorporé le \textbf{21 mars 1915} à la 39\textsuperscript{e} batterie du \textbf{10\textsuperscript{e} régiment d'artillerie à pied} à Toulon (Saint-Jean-du-Var), il est détaché dès le \textbf{4 mai 1915} comme interprète militaire à la \textbf{Mission militaire française attachée à l'Armée britannique} (administrativement rattaché au \textbf{19\textsuperscript{e} escadron du Train des équipages militaires} le 15 octobre 1915) :

\begin{itemize}
  \item \textbf{Mai 1915 – Août 1916 : de la 12\textsuperscript{e} Division aux \textit{1st Irish Guards}.} D'abord affecté à la 12\textsuperscript{e} Division britannique près de Béthune (mai–juillet 1915), puis à Saint-Omer et auprès de la 18\textsuperscript{e} Division (sous les ordres du lieutenant interprète Pizzi) et du \textbf{1\textsuperscript{er} bataillon des \textit{Irish Guards}} (\textit{1st Guards Brigade, Guards Division}), il accompagne ces unités en Artois, dans le saillant d'Ypres, dans les Flandres françaises (Bailleul, Steenwerck) et sur la Somme (Lucheux).
  \item \textbf{Août 1916 – Avril 1917 : avec la \textit{152nd Company, Army Service Corps} et le XIII\textsuperscript{e} Corps.} À la fin d'août 1916, en pleine bataille de la Somme, il rejoint la \textit{152nd Company A.S.C.} (Train de la 18\textsuperscript{e} Division britannique) à Raincheval, Acheux, Forceville, Bernaville, Beauval et Albert (\textit{Brickfield Area}), puis est détaché le 2 novembre 1916 à Acheux-en-Amiénois (puis Hérissart et Toutencourt) auprès du service des achats et réquisitions de fourrages (\textit{Foraging Service} / \textit{Army Purchase Board}) des XIII\textsuperscript{e} et V\textsuperscript{e} Corps britanniques, avec les lieutenants Curtis et Gilbert et le jeune capitaine Williams.
  \item \textbf{Le mariage du 25 octobre 1917 et la carrière à Montauban.} Six mois après la clôture de ce carnet, il épouse au Sacré-Cœur de Millau, le \textbf{25 octobre 1917}, \textbf{Marie Marguerite Calmels} (née à Millau le 15 avril 1892, décédée en 1986), fille du docteur \textbf{Gabriel Calmels} (1852–1921) et de \textbf{Valentine Cartairade} (1858–1943), domiciliés au 10 rue Alfred-Guibert à Millau. Nommé le \textbf{24 novembre 1918} professeur d'anglais à l'\textbf{École militaire préparatoire des Andelys} et promu caporal le 4 décembre 1918, il est démobilisé le 7 février 1919. Nommé le \textbf{24 janvier 1920} professeur d'anglais au \textbf{lycée Ingres de Montauban} (où il réside au 55 faubourg du Moustier et élève ses sept enfants : Valentine, François, Joseph, Jean, Marie-Thérèse, Pierre et Michel), il devient membre de l'\textbf{Académie de Montauban} et s'éteint en 1970 dans sa quatre-vingt-quatorzième année.
\end{itemize}

\section{Histoire matérielle, codicologie et génétique du \textit{Livre-Journal}}

Le manuscrit édité dans le présent volume est un carnet de poche de fabrication britannique, relié en toile cirée noire souple à coins arrondis, comprenant \textbf{93 folios} (soit \textbf{186 clichés numériques} avec la couverture extérieure, numérotés de \texttt{20251126\_092853.jpg} à \texttt{20251126\_111833.jpg}). Sur le plat supérieur, une étiquette octogonale porte l'intitulé autographe : \textit{Livre - Journal / Du 25 juillet 1916 / au 30 avril 1917}.

L'examen codicologique et paléographique des 186 scans met en lumière quatre caractéristiques fondamentales :
\begin{enumerate}
  \item \textbf{Structure interne de la page.} Chaque page (ou séquence journalière) obéit à un protocole invariable : en haut à gauche, le quantième et le jour de la semaine abrégé (\textit{25 Ma.}, \textit{26 Mer.}), parfois soulignés ; en haut à droite, le mois et le millésime (\textit{Juillet 1916}, \textit{Août /16}) ; au centre, la chronique rédigée à la plume et à l'encre noire ou violette (ou au crayon graphite lors des marches sous la pluie et des bivouacs d'août–septembre 1916) ; enfin, au bas du folio, isolé par un trait horizontal ou par un grand crochet droit \texttt{[ ... ]}, le relevé minutieux des menues dépenses quotidiennes (repas, blanchissage, timbres, coiffeur, pourboires aux ordonnances).
  \item \textbf{La langue hybride du carnet : syntaxe télégraphique et « franglais » du front.} Écrivant pour lui-même à la lueur d'une bougie dans des chambres paysannes glaciales, Hippolyte Combes recourt à une syntaxe elliptique supprimant articles et pronoms sujets (\textit{« Toute nuit, passée très mauvaise »}, \textit{« Rentré billet, crotté y cape ruisselante »}), fait usage des abréviations tachygraphiques \textit{1/2} (pour \textit{demi} ou \textit{milieu}), \textit{j'à} (pour \textit{jusqu'à}), \textit{=} (pour \textit{même}), et intègre spontanément le lexique militaire et quotidien anglais (\textit{breakfast, lunch, tea-dinner, mess, mess-tent, mess-hut, billet, billeting, cottage, garret, washing, darning, shift, shifting, lorry, limber G.S., refilling point, Purchase Board, green forage, straw \& hay, German dug-outs, killed in action, out riding, a whole day off, a brainless ass}).
  \item \textbf{Restitution du Folio 24 recto (Scan \#050, \texttt{20251126\_103019.jpg}).} La collation systématique des 186 scans avec le premier brouillon de transcription (\texttt{Carnet de campagne édition diplomatique.docx}, qui ne comptait que 73 notices pour les 74 premiers clichés) a révélé que le cliché \texttt{20251126\_103019.jpg} (Scan \#050, Folio 24 recto : journée du lundi 25 septembre 1916 à Forceville et au \textit{railhead} d'Acheux-Varennes) avait été omis, provoquant un décalage d'une unité à partir du Scan \#051. Nous l'avons intégralement transcrit, commenté et rétabli à sa place.
  \item \textbf{Anomalies de numérisation des Scans \#063–\#064, \#091–\#093 et \#112–\#113.} Lors de la campagne photographique du 26 novembre 2025, deux inversions recto/verso ont eu lieu (Scans \#063 et \#064 des 4–5 octobre 1916 ; Scans \#112 et \#113 des 19–24 décembre 1916) et le feuillet des 2–3 novembre 1916 a été photographié à deux reprises (Scans \#091 et \#093). Conformément aux règles de l'édition diplomatique en vis-à-vis, chaque page de gauche transcrit fidèlement le fac-similé figurant sur la page de droite en regard, tandis que le commentaire codicologique signale l'enchaînement chronologique exact.
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
          \item \textit{Niveau 2 — Commentaire historique :} contextualisation militaire précise des opérations de la \textit{British Expeditionary Force} (Somme, Flandres, Artois), identification des unités (\textit{1st Irish Guards}, \textit{Royal Scots}, \textit{Royal Fusiliers}, \textit{152nd Coy A.S.C.}, XIII\textsuperscript{e} et V\textsuperscript{e} Corps), topographie des cantonnements et prosopographie familiale.
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
\textbf{Combes, Hippolyte} (1876–1970) & Marie Lucien Hippolyte Combes, né à Millau le 14 août 1876. Licencié en droit et ès lettres (Toulouse), professeur d'anglais au collège de Nogent-le-Rotrou, interprète détaché auprès de la B.E.F. (4 mai 1915 – 11 nov. 1918), puis professeur au lycée Ingres de Montauban (1920–1938). \\
\textbf{Calmels, Marguerite} (« Marg. », « Mte », « Gueïte », 1892–1986) & Marie Marguerite Calmels, née à Millau le 15 avril 1892, fille du Dr Gabriel Calmels (1852–1921) et de Valentine Cartairade (1858–1943), domiciliés au 10 rue Alfred-Guibert à Millau. Fiancée puis épouse d'Hippolyte Combes (25 octobre 1917). \\
\textbf{Combes, François-Hippolyte} (1825–1899) \& \textbf{Marie Anaïs Alric} (1838–1907) & Parents d'Hippolyte Combes, mariés à Millau le 22 juillet 1864, établis à Toulouse (47 et 77 rue du Taur). Leur souvenir émeut profondément Hippolyte lors de ses permissions à Toulouse et Millau (Scans \#132, \#141, \#143). \\
\textbf{Maria} († 1903), \textbf{Françoise} (1871–1942) \& \textbf{Joséphine} (1873–1914) & Les trois sœurs d'Hippolyte Combes : Maria (religieuse décédée à Carthage), Françoise (\textit{Sœur Marie de la Croix}, carmélite à Périgueux, destinataire de la lettre du 16 juin 1916) et Joséphine (décédée à Nogent-le-Rotrou en octobre 1914). \\
\textbf{Faure, Mme} (Germaine, Marcel, Henri, André) & Cousine d'Hippolyte résidant au 16 rue d'Armenonville à Neuilly-sur-Seine, chez qui il déjeune lors de chacune de ses traversées de Paris (26 septembre 1916 et 27 janvier 1917, Scans \#051 et \#130–\#131). \\
\textbf{Chilcott, Beatrice} & Amie anglaise d'Hippolyte Combes à l'époque de son séjour d'avant-guerre à Nottingham, signataire du poème autographe conservé dans ses papiers (\textit{Wesley Band of Hope}). \\
\textbf{1st Battalion, Irish Guards} & Bataillon de la Garde irlandaise (\textit{1st Guards Brigade, Guards Division}). Hippolyte y sert jusqu'en août 1916 (Lucheux, Ebenezer, Bailleul, Steenwerck). \\
\textbf{152nd Company, A.S.C.} & Compagnie du Train divisionnaire de la 18\textsuperscript{e} Division britannique (\textit{18th Divisional Train, Army Service Corps}), commandée par le colonel Grose et le major Hughes. Unité d'Hippolyte d'août 1916 à avril 1917. \\
\textbf{Capt. Williams} (« Capt. W. ») & Très jeune capitaine britannique (20 ans, ancien \textit{office boy} à 50 £ par an) qui relève le lieutenant Curtis à Acheux le 2 décembre 1916 (Scan \#105) et dirige le bureau des fourrages à Acheux puis Hérissart jusqu'au 10 mars 1917 (Scan \#165). \\
\textbf{Capt. Panton} & Capitaine britannique de la \textit{152nd Coy A.S.C.}, compagnon de chevauchées d'Hippolyte en octobre 1916 à Barlette, Ribeaucourt et Beauval. \\
\textbf{Lt. Curtis, Lt. Gilbert, Lt. Walsh, Major Levy} & Officiers britanniques du service des approvisionnements (\textit{Foraging} / \textit{Army Purchase Board}) avec lesquels Hippolyte sillonne la Somme et l'Artois. \\
\textbf{Lt. Pizzi \& Cap. Huguet} & Officiers de la Mission militaire française dirigeant respectivement les bureaux de la 18\textsuperscript{e} Division (Albert) et des XIII\textsuperscript{e} / V\textsuperscript{e} Corps (Acheux). \\
\textbf{Carluvant, M. \& Mme} & Maître tailleur et propriétaire d'Hippolyte Combes au n\textsuperscript{o}~1 de la route de Léalvillers à Acheux-en-Amiénois (novembre 1916 – février 1917). \\
\bottomrule
\end{longtable}
\end{small}
"""

    body_parts = [preamble, "\n\\mainmatter\n\\renewcommand{\\thesection}{\\thechapter.\\arabic{section}}\n"]

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
\\chapter{{{ch_title}}}
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
\titleformat{\chapter}[display]
  {\normalfont\large\bfseries\color{bordeaux}}
  {\textsc{Annexe\ \Roman{chapter}}}
  {1mm}
  {\Large\color{black}}
\chapter{Correspondance de guerre inédite et pièces justificatives (1916–1918)}
\markboth{Annexe I — Correspondance de guerre}{Annexe I — Correspondance de guerre}
{\sloppy

Les archives familiales d'Hippolyte Combes conservées dans le sous-répertoire \texttt{archives\_militaires/lettres\_de\_guerre/} du dépôt renferment cinq pièces autographes majeures de la Grande Guerre qui éclairent directement la genèse et le contexte du \textit{Livre-Journal}. Nous en donnons ici l'édition diplomatique et critique fidèle d'après les originaux numérisés.

\section{Document 1 : Lettre d'Hippolyte Combes à un capitaine, ancien collègue de la Faculté de Toulouse (Au front, 25 février 1916)}
\noindent\textbf{Source :} dossier \texttt{archives\_militaires/lettres\_de\_guerre/}, fichier \texttt{lettre fev 1916 au front à un capitaine.pdf} (double feuillet autographe numéroté p.~36 et p.~37).

\begin{quote}\small
« Au front, le 25 février 1916.\\[1mm]
Mon Capitaine,\\
Permettez à un de vos anciens collègues de la Faculté de Toulouse, aujourd'hui interprète à l'armée britannique, de se rappeler à votre bon souvenir et de solliciter de votre bienveillance un renseignement qui l'intéresse au plus haut point.\\
Détaché à la Mission militaire française dès le début de mai 1915, j'ai d'abord été affecté à la 12\textsuperscript{e} Division aux environs de Béthune, puis rappelé à la Mission à Saint-Omer. Depuis le mois d'août dernier, je suis attaché à une compagnie d'\textit{Army Service Corps} relevant de la 18\textsuperscript{e} Division, sous les ordres de M. l'officier interprète Pizzi.\\
Plusieurs de mes camarades, professeurs de l'Université comme moi et entrés dans le service à la même époque, ayant été récemment proposés ou nommés interprètes stagiaires, je vous serais profondément reconnaissant de bien vouloir me faire savoir si je puis espérer faire l'objet d'une mesure semblable lors d'une prochaine promotion.\\
Veuillez agréer, mon Capitaine, l'hommage de mon très respectueux dévouement.\\[1mm]
\hfill \textbf{H. Combes}, Interprète H. C., Prof. au Collège de Nogent-le-R. »
\end{quote}

\noindent\textbf{Commentaire :} Cette lettre du 25 février 1916 retrace avec une précision parfaite les premiers mois de campagne d'Hippolyte Combes auprès de la B.E.F. depuis son arrivée le 4 mai 1915 : secteur de Béthune avec la 12\textsuperscript{e} Division (où il a connu l'interprète Cordonnier qu'il retrouve le 4 novembre 1916 au Scan \#092), passage à Saint-Omer (quartier général de Sir John French et de la Mission française), puis affectation dès août 1915 dans la Somme auprès du Train de la 18\textsuperscript{e} Division sous l'autorité du lieutenant interprète Pizzi (mentionné aux Scans \#085, \#090 et \#092).

\section{Document 2 : Rapport d'Hippolyte Combes au sous-lieutenant Ferran sur l'incident de Morlancourt (mars 1916)}
\noindent\textbf{Source :} dossier \texttt{archives\_militaires/lettres\_de\_guerre/}, fichier \texttt{lettre de l'interprete combes pour un incident.pdf} (double feuillet autographe à l'encre, numéroté p.~26 et p.~27).

\begin{quote}\small
« \textbf{L'interprète Combes au sous-lieutenant Ferran, Officier de liaison à la 18\textsuperscript{e} Division.}\\[1mm]
J'ai l'honneur de vous rendre compte d'un incident survenu le mardi 24 mars au village de Morlancourt, alors que je procédais au cantonnement avec le lieutenant May.\\
Un lieutenant du \textit{6th Liverpool Regiment} (5\textsuperscript{e} Division) prétendait occuper de force, sans billet de logement (\textit{billeting order}), la chambre d'une veuve âgée dont la maison était déjà régulièrement retenue. Sur mon observation courtoise que ce local n'était pas disponible et qu'il convenait de s'adresser au \textit{Town Major}, cet officier s'est emporté violemment contre moi devant les soldats et les habitants et m'a crié en anglais :\\
\textit{« Keep silent, or I put you under arrest ! It's all right for me, it shall be worse for you, when I report to the Captain, my interpreter. »}\\
Devant une telle attitude, je me suis abstenu de toute réplique afin d'éviter un scandale public, mais je crois de mon devoir de porter ces faits à votre connaissance pour la sauvegarde de la dignité de nos fonctions.\\[1mm]
\hfill \textbf{H. Combes}, Interprète à la 18\textsuperscript{e} Division. »
\end{quote}

\noindent\textbf{Commentaire :} Ce rapport de mars 1916 sur l'incident de Morlancourt (Somme) constitue le pendant exact des tensions que relate le \textit{Livre-Journal} en décembre 1916 avec le jeune capitaine Williams à Louvencourt et Senlis-le-Sec (Scans \#112, \#114 et \#117). Il montre la position délicate de l'interprète militaire français, dépourvu de galons d'officier mais chargé de faire respecter les règles de réquisition et de protéger les populations civiles picardes contre les abus d'autorité.

\section{Document 3 : Lettre confidentielle d'Hippolyte Combes à sa sœur Françoise au Carmel de Périgueux (Au front, vendredi 16 juin 1916)}
\noindent\textbf{Source :} dossier \texttt{archives\_militaires/lettres\_de\_guerre/}, fichier \texttt{lettre de Hippolyte à sa soeur Josephine - 16 juin 1916 - Au front.pdf} (feuillet autographe recto-verso à l'encre noire ; bien que le fichier informatique ait été nommé par erreur « à sa sœur Joséphine », celle-ci était décédée en octobre 1914 et la lettre s'adresse à sa dernière sœur survivante, Françoise, \textit{Sœur Marie de la Croix}).

\begin{quote}\small
« \textit{Brûle ce feuillet. Je ne veux pas que tu le gardes dans tes papiers.}\\[1mm]
Au front, Vendredi 16 juin 1916.\\
Ma bien chère Sœur,\\
Les lettres mettent maintenant quatre ou cinq jours pour venir du Midi jusqu'à nous... Quelle existence que la mienne depuis plus d'un an ! Je n'ai jamais aimé la campagne : maintenant je l'ai en horreur. Ces villages boueux, ces plaines monotones, cette vie errante au milieu d'étrangers dont l'esprit et les manières sont si loin des nôtres me pèsent indiciblement.\\
Hier, étant allé à Fricourt pour le service (\textit{furnishing}), j'ai rencontré quelques camarades français avec qui j'ai pu enfin échanger mes idées à cœur ouvert. Quand donc finira cet horrible cauchemar ? Toutes ces abstractions dont les journaux nous rebattent les oreilles : gloire, honneur, héroïsme, etc., quel tas de blagues ! Vu de près, ce n'est que boue, souffrance, servitude morale et misère. Par moments, le dégoût m'envahit à tel point que je ne demande que la liberté ou la mort...\\
Prie pour moi, ma bien chère Sœur ; garde pour toi seule ces tristes confidences d'une heure de cafard, et crois à toute la tendresse de ton frère.\\[1mm]
\hfill \textbf{Hippolyte}. »
\end{quote}

\noindent\textbf{Commentaire :} Document psychologique exceptionnel, écrit quinze jours avant le déclenchement de l'offensive franco-britannique de la Somme (1\textsuperscript{er} juillet 1916) alors qu'Hippolyte Combes se rend encore à Fricourt. Sous le sceau du secret fraternel (« \textit{Brûle ce feuillet} »), l'humaniste chrétien livre sans fard sa révolte intérieure contre le bourrage de crâne de l'arrière (« \textit{toutes ces abstractions : gloire, honneur, etc., quel tas de blagues !} ») et son horreur viscérale de la vie rurale des cantonnements.

\section{Document 4 : Poème anglais de Beatrice Chilcott (\textit{Wesley Band of Hope})}
\noindent\textbf{Source :} \texttt{archives\_militaires/lettres\_de\_guerre/un poeme.pdf} (copie autographe d'un poème anglais en trois strophes de huit vers, signée \textit{Beatrice Chilcott, Wesley Band of Hope}).

\begin{quote}\small
\textit{« What, love a passion ! Heaven forbid}\\
\textit{That men should call true love by such a name... »}\\[1mm]
\hfill Signé : \textbf{Beatrice Chilcott}, \textit{Wesley Band of Hope}.
\end{quote}

\noindent\textbf{Commentaire :} Conservé précieusement par Hippolyte Combes parmi ses papiers de guerre, ce poème d'inspiration méthodiste (\textit{Wesley Band of Hope}) célébrant la pureté de l'amour spirituel par opposition à la passion charnelle est un souvenir de son séjour de quatre années à Nottingham (entre 1901 et 1907) et de son amitié avec la jeune Anglaise Beatrice Chilcott.

\section{Document 5 : Lettres de l'armistice à Marguerite et à « Bonne Maman » Calmels (Paris, 25 novembre 1918 \& Les Andelys, 2 décembre 1918)}
\noindent\textbf{Sources :} \texttt{archives\_militaires/lettres\_de\_guerre/lettre à bonne maman 25 novembre 1918.jpg} et \texttt{carte 2 decembre 1918.pdf}.

Dans sa lettre écrite de Paris (Hôtel du Panthéon et Bibliothèque Sainte-Geneviève) le \textbf{25 novembre 1918}, au lendemain de sa nomination comme professeur d'anglais à l'École militaire préparatoire des Andelys, Hippolyte Combes décrit son passage à Nogent-le-Rotrou pour récupérer ses meubles et ses livres dans sa maison du \textbf{17 rue Saint-Hilaire} et évoque avec émotion sa petite fille \textbf{Valentine Combes}, née à Millau le 18 septembre 1918. La carte postale du \textbf{2 décembre 1918}, expédiée des Andelys à \textit{« Madame Combes, 10 rue Alfred-Guibert, Millau (Aveyron) »}, annonce son installation en Normandie en attendant leur réunion familiale.
\par}

\chapter{État signalétique des services et table synoptique des 186 scans}
\markboth{Annexe II — État des services et table des scans}{Annexe II — État des services et table des scans}
{\sloppy

\section{Résumé de la fiche matricule d'Hippolyte Combes (Classe 1896, Matricule 911, Bureau de recrutement de Toulouse)}

\begin{figure}[htbp]
  \centering
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=56mm,keepaspectratio]{illustrations/mariage_millau_1917.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 3.} Mariage d'Hippolyte et Marguerite à Millau (25 octobre 1917).}
  \end{minipage}\hfill
  \begin{minipage}[b]{0.46\textwidth}
    \centering
    \includegraphics[height=56mm,keepaspectratio]{illustrations/famille_combes_1925.jpg}
    \par\vspace{1mm}{\scriptsize\textit{Fig. 4.} Hippolyte et Marguerite Combes entourés de leurs enfants (vers 1925).}
  \end{minipage}
\end{figure}

D'après le registre matricule du recrutement de Toulouse (dossier \texttt{archives\_militaires/fiche\_et\_parcours/}, fichier \texttt{Fiche\_militaire\_Combes\_Hippolyte.md.docx}) et les actes d'état civil (\texttt{biographie\_et\_famille/etat\_civil\_et\_actes/}) :
\begin{itemize}
  \item \textbf{État civil :} \textbf{Marie Lucien Hippolyte Combes}, né le \textbf{14 août 1876} à \textbf{Millau} (Aveyron), rue des Barris (inscrit sous la date du 22 août 1876 sur la fiche matricule), fils de \textbf{François Augustin Hippolyte Combes} et de \textbf{Marie Anaïs Alric}, domiciliés à Toulouse (47 rue du Taur). Signalement : cheveux et sourcils châtains, yeux gris bleu, taille 1,66 m. Profession : étudiant ecclésiastique puis professeur d'anglais au collège de Nogent-le-Rotrou (Eure-et-Loir).
  \item \textbf{Parcours militaire et campagnes (1914–1919) :}
    \begin{itemize}
      \item Exempté en 1896 pour « faiblesse générale » (numéro de tirage 74, canton de Toulouse-Nord) ; classé \textbf{Service armé} par le conseil de révision d'Eure-et-Loir le \textbf{18 décembre 1914}.
      \item Appelé à l'activité le \textbf{20 mars 1915} ; arrivé au corps le \textbf{21 mars 1915} au \textbf{10\textsuperscript{e} Régiment d'Artillerie à pied} (39\textsuperscript{e} batterie) à Toulon (campagne simple à l'intérieur du 21 mars au 3 mai 1915).
      \item Détaché à la \textbf{Mission militaire française attachée à l'Armée britannique} aux armées (campagne double) du \textbf{4 mai 1915 au 11 novembre 1918} ; passé administrativement au \textbf{19\textsuperscript{e} Escadron du Train des Équipages Militaires} le \textbf{15 octobre 1915}.
      \item Affecté successivement auprès de la 12\textsuperscript{e} Division britannique (Béthune, mai–juillet 1915), de la Mission à Saint-Omer, du \textbf{1st Battalion, Irish Guards} et de la \textbf{152nd Company, Army Service Corps} (18\textsuperscript{e} Division, XIII\textsuperscript{e} et V\textsuperscript{e} Corps).
      \item Affecté le \textbf{24 novembre 1918} à l'\textbf{École militaire préparatoire des Andelys} comme professeur d'anglais ; nommé \textbf{caporal} le \textbf{4 décembre 1918}.
      \item Mis en congé illimité de démobilisation le \textbf{7 février 1919} par le dépôt démobilisateur du 103\textsuperscript{e} R.I. (se retire à Nogent-le-Rotrou, rue Saint-Hilaire). Nommé professeur au \textbf{lycée Ingres de Montauban} le \textbf{24 janvier 1920}.
    \end{itemize}
\end{itemize}

\section{Table de concordance intégrale des 186 clichés numériques}

Tous les clichés originaux sont disponibles en double résolution à la racine du dépôt :
\begin{enumerate}
  \item \texttt{scans\_haute\_qualite/} : 186 fichiers JPEG haute résolution non compressés (1,03 Go au total, env. 5,9 Mo par scan) ;
  \item \texttt{scans\_compresses/} : 186 fichiers JPEG optimisés pour la transcription automatique et l'édition électronique (31,1 Mo au total).
\end{enumerate}
\par}

\end{document}
"""

    body_parts.append(appendices_tex)
    full_tex = "".join(body_parts)

    with open(OUT_TEX, "w", encoding="utf-8") as f:
        f.write(full_tex)
    print(f"Successfully generated {OUT_TEX} ({len(full_tex)} bytes)")


if __name__ == "__main__":
    generate_full_tex()
