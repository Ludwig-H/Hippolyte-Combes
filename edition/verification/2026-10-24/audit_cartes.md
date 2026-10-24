# Audit des cartes et de leur iconographie — 24 octobre 2026

Base examinée : `ce61fc3`, après la refonte de `edition/`. Corrections préparées dans la copie détachée `/tmp/hc_audit_20261024/repo` ; le dépôt principal et ses modifications locales sont restés intacts.

## Périmètre effectivement vérifié

Les neuf cartes (deux générales et sept de chapitre) ont été examinées dans leurs définitions, leur PDF et une planche de leurs aperçus. Les cartes III et IV corrigées ont aussi été examinées séparément à plus grande taille. Les 147 occurrences de points (121 dans la couche des lieux du carnet, 26 de contexte ; 88 identifiants distincts) se résolvent dans le catalogue. Les coordonnées des communes imprimées concordent avec le répertoire des communes archivé ; les points particuliers conservent leur source et leurs réserves propres.

Un contrôle indépendant du PDF a projeté chaque point du catalogue en Lambert-93 et l'a comparé au centre du cercle effectivement imprimé : écart maximal inférieur à 0,00004 point typographique. Les deux moitiés de chacune des neuf barres d'échelle correspondent à la distance annoncée. Aucun texte extrait ne déborde du format de la carte. Le détail numérique, les empreintes et la portée du contrôle sont dans `cartes_controles.json` ; le script de ce contrôle dans `verifier_cartes_pdf.py`, dans ce dossier. Ces résultats vérifient la conformité géométrique au catalogue, pas l'identification historique des lieux.

Les nouveaux fronts ont été confrontés à leurs dossiers de construction R4 (§2.3) et R5 (§2.D). Ces dossiers procèdent par points d'appui, localités et ouvrages approximativement localisés. Ils ne constituent pas une restitution des tranchées à une précision uniforme. L'audit ne prétend pas avoir collationné chaque sommet avec une carte d'état-major géoréférencée.

## Corrections apportées

- **Cartes générale du Nord et IV : Barlette à la place de Ribeaucourt comme cantonnement des 6–14 octobre.** Le texte de la page source 067 dit que la compagnie est cantonnée « au hameau de Barlette, près de Ribeaucourt » ; les pages 068–074 poursuivent ce séjour et datent le départ du 15 octobre. Le point de Barlette est déjà documenté dans le catalogue IGN ; il remplace effectivement le point du bourg de Ribeaucourt, y compris dans l'origine de la liaison de IV.
- **Carte IV : Bouzincourt et Hédauville portent tous deux une réserve †.** La page 077 situe le camp « 1/2 route entre Bouzincourt & Hedauville » ; le point de chaque bourg ne peut identifier ce camp. La légende le dit maintenant explicitement, sans inventer de coordonnées intermédiaires.
- **Carte II : La Croix-du-Bac † et légende du transfert du 25 août.** Le nom du cantonnement est déduit de la continuité avec le premier chapitre ; cette réserve est rétablie. La légende distingue maintenant le départ du cantonnement et le parcours ferroviaire de Bailleul à Saint-Pol, conformément au récit et au dossier R5.
- **Carte III : Purpan et Pech-David.** La visite des ruines ne prouve pas seule l'identification exacte du bâtiment ; « Purpan (ruines ?) » et la note présentent l'amphithéâtre comme proposé. Pech-David est expressément un repère du coteau. L'attribution OpenStreetMap du repère de Purpan est ajoutée au crédit. Saint-Sernin et Matabiau restent absents de cette carte : l'ancienne erreur de période n'a pas réapparu.
- **Cartes V et VII : situation du front datée du 18 novembre 1916.** L'intitulé « front de l'hiver 1916–1917 » suggérait une permanence que les opérations de janvier–février démentent. Il est remplacé par la date correspondant au tracé. Sur VII, la totalité des hachures était dite évacuée en mars alors que le polygone se prolonge à l'est de la ligne Hindenburg ; la légende décrit désormais la zone allemande à la date de référence, avant le repli.
- **Documentation des fronts : précision non établie retirée.** La promesse « 0,5 à 1 km » n'est pas justifiée par la méthode de construction. La limitation aux grands secteurs, sans restitution des tranchées ni des variations quotidiennes, est explicite. L'attribution du volume de 1938 de l'histoire officielle britannique est corrigée en Miles, conformément au dossier R5.
- **Carte générale de France : doublon de tracé supprimé.** `artois_somme_1916_11` contient déjà le tronçon de Flandre ; le redessiner séparément était redondant. Aucun secteur du front n'est retiré.
- **Carte VI : frontières actuelles signalées aussi dans son propre crédit.** Le texte introductif le précisait déjà pour l'ensemble.
- **Catalogue iconographique : Bailleul et Puchevillers.** Pour la photographie de mai 1917, les promenades de l'été 1916 ne sont plus dites « un an plus tôt », mais « l'été précédent ». La notice de Puchevillers ne localise plus le billet 220 dans ce village : le récit du 11 mars mentionne le tournant de Puchevillers, mais le paiement du porteur (page 167) est explicitement « A Herissart » et la page 168 confirme le séjour à Hérissart. La carte générale « févr.–avr. » à Hérissart est donc conservée.

Huit cartes ont été régénérées en PDF et PNG ; I n'a pas nécessité de modification. La source du générateur cartographique n'a pas été modifiée.

## Précision éditoriale signalée au responsable

`intro_cartes.tex` affirme que la première carte rassemble « l'ensemble des lieux du carnet », alors qu'elle ne porte que quinze lieux sélectionnés : remplacer par « les principaux lieux » ou « les principales étapes ». Cette correction a été intégrée par le lot de textes.

## Réserves maintenues

Le contrôle s'appuie sur la transcription actuelle et sur les référentiels archivés. Il n'est pas une nouvelle lecture intégrale des 186 photographies. Les mairies et centres des bourgs ne localisent pas les chambres, fermes ou camps de 1916–1917 ; les fonds hydrographiques et administratifs sont contemporains. Les liaisons montrent une succession d'étapes, pas les voies historiques exactes. Sercus reste une lecture réservée, Purpan une identification proposée, Pech-David un repère de coteau. Les fronts restent des schémas : leur précision cartographique apparente ne doit pas être confondue avec une exactitude parcellaire ou quotidienne. L'absence de dépassement de page n'est pas une mesure exhaustive de toutes les collisions typographiques ; le contrôle visuel des aperçus n'a pas révélé de défaut matériel nouveau.
