Audit des loci paralleli et des index — 16 octobre 2026

Le dispositif de Gemini est conservé : commentaire critique interne, loci paralleli latins, commentaire historique, cartes et index. L’audit porte sur la fidélité des renvois aux lignes transcrites, pas sur une nouvelle interprétation historique de toutes les personnes. La copie figée de 09:53 sert de base reproductible.

Contrôles exhaustifs

| Contrôle | Résultat |
|---|---:|
| Vues contrôlées | 186 |
| Notes de loci reconstruites | 470 |
| Renvois entre vues | 1 417 |
| Renvois dont l’entité est identifiée par le moteur | 1 391 |
| Renvois ciblant uniquement titre ou lieu, sans motif dans les lignes | 136 |
| Directions supra/infra erronées | 0 |
| Lemmatisations textuelles sans correspondance exacte sur la ligne indiquée | 12 |
| Notices matérielles de doublon placées à tort dans la case du lemme | 2 |
| Sources contenant une réserve non affichée dans le rapprochement | 4 |
| Cibles contenant une réserve non affichée dans le rapprochement | 7 |
| Index des personnes : renvois / sans correspondance au motif | 302 / 65 |
| Index des lieux : renvois / sans correspondance au motif | 714 / 181 |

Les 246 références d’index sans correspondance au motif de recherche ne sont pas toutes fausses. Certaines reposent sur une expression implicite (« proprre » pour Carluvant) ou sur une graphie omise par la regex (« Mme Cuis[?] », « Capne W. », « St. Michel »). Elles ne peuvent toutefois être présentées sans distinction comme des occurrences du nom. Les tableaux `explicit_scans` fournissent actuellement des numéros sans ligne ni justification.

Les 470 loci enregistrés dans le JSON figé correspondent exactement au résultat du constructeur figé : les défauts sont reproductibles et ne proviennent pas d’un export partiel.

Ancrages sources à corriger

| Vue | Ligne | Lemme affiché | Ligne transcrite / défaut |
|---|---|---|
| 004 | 22 | 84 f. | A Hazebrouck : Solde : 84 fr. — |
| 021 | 12 | 84 f. | [ – Solde & indemnité de fonctions : 84 fr. |
| 035 | 22 | 78 f. 75 | 78 f 75c |
| 046 | 12 | 78 f. 75 | A Acheux : solde : 78 f 75 c |
| 064 | 1 | 4 au 5 Oct. | ... Mte & moi, très |
| 069 | 10 | 78 f. 75 | A Bernaville, solde & indemnité : 78 f 75 |
| 072 | 5 | forêt | derrière le grand bois de Ribeaucourt |
| 079 | 7 | 84 f. | / Albert, mission frse : 84 fr. — |
| 081 | 15 | notre Coy | Coy bivouaque, très impressionnant spectacle |
| 091 | 1--17 | eadem pagina bis photographata | Notice matérielle, non lemme |
| 093 | 1--17 | eadem pagina bis photographata | Notice matérielle, non lemme |
| 150 | 2 | Lt Croughton | Après-midi, ds l'auto du Lieutt Croughton, |
| 157 | 15 | Hair cut | 20 Mardi. — [ 1 hair cut : net : 30 c. ] |
| 181 | 12 | Lt Gilbert | Lieut. Gilbert, retour d'Abbeville, venu passer soirée |

La normalisation 84 fr. → 84 f. ou Lieutt → Lt n’est pas nécessairement une erreur d’identification. Elle devient une erreur d’ancrage quand le lemme est présenté comme une citation exacte de sa ligne. Les deux défauts les plus nets sont « 4 au 5 Oct. » (064, l. 1), qui ne figure pas dans le texte, et « notre Coy » (081, l. 15), qui réunit des mots répartis entre les lignes 14 et 15.

Cibles issues des métadonnées

Le moteur ajoute à son registre des occurrences les correspondances trouvées dans `lieu` ou `title`, même si elles sont absentes du texte. Cela produit notamment :

- Paris (051 et plusieurs autres vues) → 001 : la couverture porte le titre et les dates, pas Paris.
- Lynde (005) → 002 et 004 : Lynde n’apparaît dans les lignes de ces deux vues.
- Belle-Église (111, 113, 119) → 117 : la cible provient du lieu/titre éditorial.
- Aveluy (082 et 151) → 150 : l’ancienne compagnie sur la route d’Aveluy est décrite à 151, l. 2, pas à 150.
- Arras (032 et 182) → 178 : aucun Arras dans le texte de cette cible.

Ces rapprochements peuvent devenir des repères de contexte historique, mais ils ne sont pas des loci textuels. Le JSON joint recense les 136 arêtes concernées, avec leurs sources et cibles.

Collisions certaines et identifications à distinguer

- La Germaine déjeunant chez Mme Faure à Neuilly (131, l. 2–7) est confondue avec les Vincens à Millau. Le mot est identique, la famille est différente. Supprimer Germaine du motif général Vincens ; l’index peut retenir Germaine Faure et Germaine Vincens séparément avec preuve contextuelle.
- Quatorze renvois appartiennent à Sainte-Marie ou au P. Marie-Antoine ; un seul concerne les étrennes à Marie. Pour la domestique, ancrer exactement 140, l. 7. Créer séparément l’entrée Sainte-Marie-des-Champs et celle du P. Marie-Antoine.
- Le motif ancien assimile la cavalerie indienne aux 17th Lancers britanniques. Ici les deux sont mentionnés, mais ce sont deux groupes distincts. Cette définition n’a pas produit de faux renvoi affiché dans la copie à cause du plafond de trois loci. Restreindre le motif des 17th Lancers à leur nom et au surnom/motto explicitement adjacent ; indexer la cavalerie indienne à part.
- Le renvoi vers 092 ne nomme aucune mère ni Alric : il décrit Bertrancourt, Bus, Jamet, Cordonnier et Pizzi. Retirer 092 ; conserver ailleurs les expressions mère/Maman uniquement comme identifications contextuelles argumentées.
- Le scan 074 nomme Connelly (l. 14), mais aucun des quatre officiers indexés explicitement sur cette vue. Aucun pronom n’y permet de les distinguer. Ne pas propager une liste d’officiers à une page décrivant un déplacement collectif sans attestation personnelle.
- Arras n’apparaît ni dans le texte ni dans le lieu de 178. La canonnade au sud d’Arras est attestée à 182, l. 2–3 et 25–27. Conserver 182 comme attestation ; retirer 178 de l’index autographique.
- Les deux attestations réelles échappent au motif St-Michel parce que l’auteur emploie St. Michel. Le scan 132, l. 17, nomme le tram St-Michel à Toulouse ; un motif sans qualification confondrait les deux lieux. Reconnaître les graphies exactement attestées avec le complément Ternoise ; garder Saint-Michel toulousain distinct.

Le catalogue permet aussi à « Jean » de devenir Jean Crouzet et à « Pierre » de devenir Pierre Calmels sans porter une preuve d’identification dans la donnée. Les contextes peuvent soutenir ces identités, mais la présence autographe du seul prénom doit rester distinguée de son attribution familiale. Les graphies Lépin/Liepin/Lupin et Houthouan/Houtteman doivent conserver les réserves et variantes, même lorsqu’un rapprochement est utile.

Complétude de l’index

Les catalogues spécifiques omettent au moins les mentions nominales suivantes, pourtant attestées dans les lignes :

- Jamet : 092, l. 7 (personne).
- Cordonnier : 092, l. 11 (personne).
- Boilly : 130, l. 5 (personne).
- Colin : 052, l. 22 (personne ou enseigne).
- Charlet : 147, l. 18 (enseigne).
- Casteljau : 151, l. 13 (personne).
- Lamennais : 135, l. 12 (personne).
- Marie-Antoine : 057, l. 22 (personne).
- Montaudran : 057, l. 9 (lieu).
- Terre-Cabade : 057, l. 19 (lieu).
- Bayencourt : 107, l. 4 (lieu).
- Gommecourt : 107, l. 5 (lieu).
- Coigneux : 107, l. 6 (lieu).
- Flixecourt : 162, l. 17 (lieu).
- Gézaincourt : 128, l. 20 (lieu).
- Gien : 144, l. 19 (lieu).
- Gannat : 144, l. 13 (lieu).
- Montargis : 144, l. 19 (lieu).
- Corbeil-Essonnes : 145, l. 7 (lieu).
- Pont-à-Mousson : 130, l. 5 (lieu).
- Monts-en-Ternois : 039, l. 13 (lieu).
- Béthune : 092, l. 12 (lieu).

Les fonctions de Colin et Charlet restent à établir ; ces formes peuvent désigner une personne ou une enseigne. Une entrée neutre suffit jusqu’à documentation. Les prénoms et patronymes incertains demandent des réserves explicites.

Foliotation, doublon et sélection

Les directions supra/infra sont toutes correctes relativement à l’ordre du PDF. La formule scan // 2, recto/verso alterne est un repérage éditorial ; elle ne démontre pas une foliotation matérielle du carnet. Elle donne d’ailleurs deux numéros différents aux deux photographies d’une même page (091/093). Il faut annoncer son caractère conventionnel et préserver les numéros de vue comme identifiants stables.

091/093 doivent rester des renvois matériels « eadem pagina bis photographata » et être exclus du calcul des répétitions textuelles ordinaires : ce ne sont pas deux attestations indépendantes. 063/064 et 112/113 portent de vrais décalages entre l’ordre des photographies et l’ordre des dates. Pour 064, la date présente est « Mer. 4 Oct 16 », l. 2.

Le plafond de trois loci laisse 253 candidats du catalogue non affichés sur 81 vues. Ce nombre n’est pas un décompte de 253 lacunes philologiques : plusieurs candidats sont triviaux ou eux-mêmes issus des métadonnées. Une sélection courte reste compatible avec le dispositif de Gemini, à condition que l’index et les données structurées assurent la recherche exhaustive et que les autres registres ne soient pas tronqués par ce plafond.

Solution fournie pour intégration

Le module autonome `loci_verifies.py` construit les renvois à partir des seules lignes, avec lemmes exacts des deux côtés, offsets, types de rapprochement et réserve de lecture. Les expressions thématiques sont signalées « de eadem re » ; les variantes ou noms réservés portent « similitudo lectionis » et, si nécessaire, « incertitudo nominis ». Les ratures sont marquées `cancelled` et rendues « verba deleta » / « del. ». Les références de folios et de pages sont injectées par la fonction de Gemini.

Sur les 186 lectures validées du commit 99f5d5a, le module produit 453 loci et 852 cibles, tous ancrés dans les lignes. Les 14 contrôles comprennent les corpus négatifs sans parallèle, les faux lemmes, les faux offsets, les directions inversées, les réserves effacées, la collision Germaine Faure/Vincens, la cavalerie indienne et les 17th Lancers, ainsi que les doublons 091/093. Le rendu et les données de validation sont joints séparément.

Les renvois aux annexes restent à contrôler avec leurs lemmes documentaires. Le module ne supprime aucune annexe ; il évite simplement de reconduire une chaîne « doc. 1 et 3 » dépourvue d’ancrage cible vérifiable.

Fichiers

- `loci.json` : matrice exhaustive ancienne, cas sémantiques, lacunes de catalogue, contrat proposé.
- `loci_module_validation.json` : résultats structurés et contrôles du nouveau module.
- `loci_module_rendus.json` : rendu latin complet du nouveau module.
- `loci_verifies.py` dans le worktree de réconciliation : seul fichier de code écrit par cet agent.

Aucun fichier du dépôt principal n’a été modifié, aucune branche ni aucun commit créés par cet agent.
