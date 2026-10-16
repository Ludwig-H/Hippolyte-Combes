# Audit ciblé des index, lecture seule

Les deux motifs `^\b$` concernent bien **Françoise Combes** et **Maria Combes**, et ils ne peuvent produire aucune occurrence. Cependant, le catalogue actuel perd **trois personnes** et **quatre lieux**, pas seulement ces deux sœurs. L’index peut conserver ces entrées en citant des pages réellement imprimées hors carnet, sans leur inventer un folio.

État contrôlé : fichiers du worktree détaché `/tmp/hc_argon_codex/reconciliation_20261016`, export et PDF de 423 pages. Les numéros ci-dessous sont ceux du PDF actuel ; les renvois définitifs doivent employer des labels LaTeX.

| Entrée sans renvoi dans le corpus courant | Attestation imprimée actuelle | Renvoi conseillé |
|---|---|---|
| Françoise Combes | Arbre I, p. 7 ; titre du document 3, p. 400 ; commentaire de 028 | `genealogie:combes`, `annexe:doc3` ; un motif `\bFrançoise\b` permettrait aussi de conserver la véritable mention de commentaire 028 |
| Maria Combes | Arbre I, p. 7 ; commentaire 132, p. 286 ; sœur nommée Maria au commentaire 141 | `genealogie:combes` ; éventuellement les véritables mentions de commentaire 132 et 141 avec contexte identitaire |
| Hippolyte Combes | Biographie et arbre I ; signatures et titres des annexes ; fiche matricule p. 405 | `genealogie:combes`, nouveau `annexe:matricule` ; pas les faux folios 001/135 déduits des anciennes listes explicites |
| Montauban (Tarn-et-Garonne) | Biographie, carte générale, arbre I ; démobilisation/carrière dans l’Annexe II p. 405 | nouveau `annexe:matricule`, éventuellement label de la carte générale |
| Saint-Chély-d’Apcher | Biographie, arbre I ; décès dans l’Annexe II p. 405 | nouveau `annexe:matricule` ; le motif court `St-Chély` manque les mentions pleines `Saint-Chély-d'Apcher` du commentaire |
| Domqueur | Introduction du chapitre IV p. 150 et carte IV p. 151 | nouveau `carte:IV`, jamais `fol:70` : aucune occurrence dans ce texte |
| Talmas | Carte VII p. 317 | nouveau `carte:VII`, jamais `fol:162` : aucune occurrence dans ce texte |

Le titre « Résumé de la fiche matricule » ouvre **l’Annexe II**, après le document 5 de l’Annexe I. Il n’a pas encore de label dédié. `annexe:doc5` renvoie à la correspondance de l’armistice et ne doit pas servir de page à cette fiche matricule.

## Collisions encore présentes

- **Maria, domestique Crouzet** : la mention du texte 064 est correcte ; les commentaires 132 et 141 concernent **Maria Combes, sœur de l’auteur**, et doivent être exclus de l’entrée de la domestique. Les deux entrées exigent des contextes distincts.
- **Marie** : la restriction à la vue 140 fonctionne. Les mots composés et autres Marie ne sont plus collectés dans cette entrée. Le titre prudent « personne recevant des étrennes à Toulouse » évite une identité domestique non fournie par cette seule ligne.
- **Crouzet, Émile et Élisabeth** : l’exclusion de `Oncle` / `Tante` nus évite la collision Layrals de 142. Mais le motif `Crouzet` absorbe encore **Jean Crouzet** aux commentaires 059 et 139 ; ces pages ne nomment pas Émile ou Élisabeth. Le commentaire 133 nomme à la fois Élisabeth et Jean : seule l’occurrence Élisabeth doit soutenir l’entrée parentale.
- **Calmels, Gabriel et Valentine** : le motif familial nu `Calmels` absorbe 36 occurrences de commentaire, dont 019, 056 et 057 ne nomment que Marguerite. Ce sont des attestations de la famille ou de Marguerite, pas des deux parents. Soit élargir honnêtement la vedette à « famille Calmels », soit exiger un prénom ou contexte parental précis. Les lignes 054 « dames Calmels » et 060 « Mme Calmels » ne démontrent pas à elles seules la présence de Gabriel.
- **Vincens, Fernand, Germaine et Robert** : le commentaire 168 indexe le `Fernand` de **Louis-Fernand Flutre**, sans aucun Vincens. Exclure ce prénom composé homonyme ou exiger le patronyme/contextes propres à Vincens.
- **Saint-Michel-sur-Ternoise** : le renvoi actuel est uniquement 132, dont `St-Michel` désigne un tram toulousain. Les véritables formes 032 `St. Michel-s-Ternoise` et 037 `St. Michel-sur-Ternoise` ne correspondent pas au motif. Adopter les formes complètes Ternoise, ou réserver le nom court aux contextes géographiques vérifiés.
- **Auteur Hippolyte Combes** : la seule occurrence autographe `Hippte` actuelle est 026 `St Hippte`, correctement exclue de l’auteur. Si l’entrée de l’auteur est restaurée par des références externes, supprimer de sa description la prétendue « mention nominale autographe Hippte ».
- **Denis, Baptiste** : `Denis` est attesté, mais la contraction `Bte` reste développée **Baptiste, probablement** dans l’apparat relu. La vedette de l’index devrait conserver cette réserve, par exemple « Denis (famille), Bte (Baptiste proposé) ».

## Noms uniquement dans les arbres : portée du catalogue

Les deux motifs impossibles ne constituent pas toute la question. Plusieurs personnes nommées dans l’arbre I ou II n’ont **aucune entrée de catalogue** : François Combes (1789–1855), Madeleine Fabre-Hugou, Marie Bouquié, les deux Pierre Émile Alric, les sept enfants d’Hippolyte et Marguerite, Pierre Combes fils de Joseph, Joseph Delcamps, Louis et Jean Layrals, par exemple. Une simple liste de références externes pour deux vedettes ne peut les faire apparaître.

Pour préserver l’index actuel sans étendre cette tâche à tous les noms du volume, les sept entrées absentes peuvent être réparées immédiatement. Si l’index doit couvrir **tous** les noms imprimés des arbres et des annexes, un catalogue explicite complémentaire est nécessaire : les homonymes Pierre, Jean, François ou Marie doivent être reliés à leur nœud généalogique, sans recherche globale sur ces prénoms.

## Schéma d’intégration conseillé

Conserver séparément les occurrences du texte, celles du commentaire et les références hors corpus. Les dernières ont une source et un label réel (`genealogie:combes`, `annexe:doc3`, `annexe:matricule`, `carte:IV`, `carte:VII`) ; elles n’ont aucun `scan_num` fictif. Vérifier que chaque label cité est effectivement émis une seule fois dans le TeX. Adapter la légende : double renvoi folio/page pour le carnet, renvoi à la page et au document pour les prolégomènes, cartes et annexes.
