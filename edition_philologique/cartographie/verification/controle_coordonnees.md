# Vérification géographique des nouvelles cartes

Contrôle du 16 octobre 2026, effectué avant la mise en page finale.

Les **3 190 repères** de `donnees/repertoire_communes.json` correspondent exactement, pour le nom, le code INSEE et les deux coordonnées, aux mairies des réponses sauvegardées de l’API officielle des communes. Aucun centroïde territorial n’a été substitué à une mairie.

Les **25 points particuliers** ont été contrôlés : 23 correspondent à un objet précis des réponses IGN (catégorie et identifiant vérifiés) ; Purpan est le site archéologique OSM identifié par la référence monumentale PA00094494 ; Pech-David utilise un point paysager explicitement géoréférencé par le PLUi-H municipal. Les détails, empreintes et résultats sont conservés dans `controle_coordonnees.json`.

## Distinctions à conserver

- **Oppy** : hameau de Beaudricourt, point spécial `oppy`. La commune 62639, située près d’Arras, est exclue.
- **Bailleul** : 59043 (Nord), et **Varennes** : 80776 (Somme). Les homonymes 80051 et 31568 sont exclus des cartes du carnet.
- **Mont-Noir** : lieu-dit habité de Saint-Jans-Cappel, explicitement nommé comme hameau au scan 006. Le sommet voisin, distant d’environ 390 m, n’est pas utilisé.
- **Montigny** : Montigny-sur-l’Hallue, 80562, dans les tournées autour d’Hérissart.
- **Thièvres** : village partagé entre les départements, repères 62814 et 80756 distants de 133 m. Le carnet ne permet pas de déduire le côté administratif parcouru.
- **Martinsart et Le Mesnil** : deux bourgs séparés. Le point mairie de Mesnil-Martinsart représente le bourg septentrional, Le Mesnil.
- **La Boisselle** : lieu-dit habité dans Ovillers-la-Boisselle (80615), distinct du lieu-dit non habité homonyme de Contay.
- **Croix-du-Bac** : lieu-dit habité, distinct de la rue homonyme et du cimetière militaire. **Bac-Saint-Maur** : hameau distinct du pont, du château et du point exact de ravitaillement.
- **Le Quesnoy** : lieu-dit de Puchevillers, au sud-est du bourg. **Belle-Église** : ferme à l’est du centre d’Arquèves.
- **Purpan** : l’amphithéâtre romain est repéré ; l’hôpital et l’arrêt de tramway ne sont pas utilisés. **Pech-David** : repère de coteau, sans prétendre situer exactement la promenade.
- **Berguette** : le point de gare convient à la liaison ferroviaire ; le point du bourg est une alternative, pas une seconde étape.

## Contrôles d’orientation et de distance

Renescure est au nord-ouest de Lynde ; Léalvillers au sud-ouest d’Acheux ; Louvencourt au nord-ouest ; Arquèves à l’ouest. Senlis-le-Sec est au nord-est de Contay. Rubempré est au sud-ouest d’Hérissart : **environ 2,43 km à vol d’oiseau entre les repères des mairies**. Ces relations, inversées ou déformées sur les anciennes cartes, sont testées dans le rapport JSON.

Une coordonnée actuelle exacte ne prouve ni une adresse de 1916, ni une visite, ni le tracé d’une route. Les limites modernes doivent être annoncées ; les réserves autographes telles **Sercus [?]** restent visibles. La présence d’un point dans le répertoire ne suffit pas à l’ajouter à une carte : les attestations sont documentées séparément dans `audit_carnet.json`.
