# Contre-vérification chronologique des cartes

La première livraison (`6954da9`) a laissé une erreur : Saint-Sernin apparaissait dans la première permission (carte III), alors que la visite est attestée au scan 134, le 29 janvier 1917, pendant la seconde. Les contrôles de géométrie, d'échelle et de concordance des citations ne suffisaient pas à assurer la période de chaque lieu imprimé.

## Reprise systématique

Les 122 occurrences de points initiales ont été examinées une à une dans la transcription. Les preuves sont conservées dans `attestations_lieux.json`, y compris les deux points retirés. La version corrigée comporte 120 points pour 80 lieux : 114 occurrences attestées dans leur période, trois contextes et trois identifications réservées.

| Carte | Correction ou précision |
|---|---|
| III | Saint-Sernin retiré : visite attestée dans VI. |
| III | Matabiau retiré : la gare est mentionnée, mais ce nom est une identification ajoutée. |
| III | Purpan : visite des ruines attestée ; identification précise à l'amphithéâtre présentée comme proposée. |
| III | Pech-David : coteau parcouru, point moderne représentatif ; pas de lieu exact de promenade revendiqué. |
| II | La Croix-du-Bac † : continuité du cantonnement depuis I, sans nouvelle mention nominale dans II. |
| IV | Ribeaucourt † et Hédauville † : repères de voisinage ; visite du bourg non attestée dans cette période. |
| IV | Canaples : arrivée personnelle attestée le 6 octobre au scan 066, avant la coupure éditoriale qui ouvre IV au scan 067 ; même journée et période affichée. |
| VII | Tournée du 30 avril : départ d'Hérissart omis car inféré ; liaison limitée à Puchevillers, Pierregot et Villers-Bocage, explicitement nommés. |

Sercus conserve sa réserve de lecture. Belle-Église a été contrôlée dans les passages personnels de décembre et janvier, en écartant les mentions biffées et les déplacements du capitaine seul. Les 34 lieux imprimés dans VI/VII disposent d'attestations personnelles dans leur période. La forme « Corbeil-Essonnes » a été contrôlée directement sur l'autographe 145 et conservée ; la seconde partie du toponyme est lisible sur cette photographie.

## Contrôles et limites

Le validateur exige une preuve pour chaque point, vérifie les citations exactes et la période, et impose une réserve visible pour les contextes et identifications incertaines. Il prend les limites des chapitres dans le générateur de l'édition ; la jonction documentée de Canaples est explicitement contrôlée. Deux cas négatifs — Saint-Sernin replacé dans III et contexte dépourvu de réserve — sont refusés (`regressions_chronologiques.json`).

Cette contre-vérification repose sur la transcription actuelle. Elle ne remplace pas une nouvelle lecture systématique des photographies autographes. La concordance d'une coordonnée avec un référentiel moderne ne prouve pas l'identité d'un bâtiment en 1916. Les mairies servent de repères des bourgs ; les contours, limites et cours d'eau sont contemporains ; les liaisons ne reconstituent pas les voies historiques. Sainte-Marie-des-Champs, les logements précis et le camp entre Bouzincourt et Hédauville restent sans localisation ponctuelle certaine.

Les résultats numériques et les empreintes courants sont dans `validation_cartes.json` et `livraison.json`. Les revues initiales sont conservées comme témoins de la première livraison, sans les présenter comme des contrôles du correctif.
