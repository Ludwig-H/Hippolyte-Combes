# Reprise intégrale de l’apparat critique

Base immuable : `base_edition.json`, commit `04673ef921062b4db01357cbdbff6069266947af`, SHA-256 `98c1dc916c78fac84f16896fbcd320e1a2855adf99fab963b1df3f671b000d18`. Le travail parallèle déjà livré reste conservé. Les lots de cette passe sont distincts des anciennes propositions et ne les réécrivent pas.

Chaque photographie entière est examinée à nouveau avec sa transcription, ses marges et son commentaire critique. Contrôler chaque note ancienne, sa présence réelle, son numéro de ligne et son sens dans cette phrase. Relever les omissions : contractions lexicales, reprises, ratures, ajouts, réserves, signes et changements de langue. Une marque typographique de l’ancienne édition ne démontre pas une disposition du manuscrit.

Le résultat consiste en un apparat explicitement révisé pour chaque vue, sans limite automatique du nombre de notes par ligne. Les formes à plusieurs valeurs sont développées selon le contexte : `pt` n’est pas toujours petit, `lg` n’est pas toujours longtemps, `div.` n’est pas toujours division, `propre` n’est pas toujours propriétaire. Une lettre incertaine ne reçoit pas un développement présenté comme certain. Une ellipse grammaticale n’est pas une abréviation ; un emprunt lexical se traduit selon son usage. Les noms propres restent dans le commentaire lorsqu’aucune contraction ou difficulté ne justifie de note marginale.

Les unités usuelles des comptes (`f`, `fr`, `c`), les heures (`h`, `H`, `m`, `s`) et fractions horaires sont expliquées dans les conventions générales ; une note locale est ajoutée lorsqu’une ambiguïté existe. Ne pas produire de prétendue lacune matérielle à partir d’illisible, ni de « compte en marge » à partir de crochets éditoriaux. Une rature, un ajout ou un crochet autographe ne se déclare qu’après examen du cliché.

## Format des lots

Chaque lot JSON contient `base_sha256`, `scope`, `reviews` et `patches`. Pour chaque vue, même si certaines notes sont confirmées :

```json
{
  "scan_num": 2,
  "filename": "nom_exact.jpg",
  "originals": {"marginal_notes": {}, "critique": "valeur exacte de la base"},
  "changes": {"critique": "Commentaire critique entièrement relu et corrigé"},
  "entries": [
    {"line": 1, "lemma": "Ma", "kind": "abreviation", "note": "mardi"}
  ],
  "evidence": [{"source": "scans_haute_qualite/nom_exact.jpg", "detail": "Observations précises sur les notes retirées, rétablies ou rectifiées."}]
}
```

`lemma` est une séquence **exacte et continue** de la ligne finale citée, sans numéro de ligne ajouté. Les graphies et apostrophes sont conservées. `kind` appartient à `abreviation`, `emprunt`, `rature`, `ajout`, `lecture`, `signe`, `compte`, `syntaxe`, `disposition`. `note` est du français lisible sans balises LaTeX ; les développements d’abréviation sont fléchis selon la phrase, et les réserves explicites. Plusieurs entrées peuvent porter sur une même ligne. Le rendu marginal sera construit par le coordinateur à partir de ces entrées, sans suppression des notes excédentaires.

Les `originals` doivent aussi contenir la valeur exacte de chacun des autres champs modifiés. Les clés possibles de `changes` sont `critique` et, seulement si la confrontation le justifie, `lines`, `title` ou `historique`. Une nouvelle lecture fournit le tableau complet des lignes et sa preuve ; les notes sont alors ancrées sur ces lignes finales. Les marges ne sont pas saisies deux fois : elles sont dérivées des `entries`.

Chaque `review` indique `scan_num`, `filename`, `review_level: "apparat_integral_sur_image"`, `source_sha256`, `observations`, `remaining_uncertainties`, et les lignes ou phénomènes contrôlés. Les vues 091 et 093 montrent la même page : harmoniser leurs lignes et leurs entrées. Chaque lot possède un Markdown expliquant les erreurs concrètes repérées et les difficultés restantes.

Le contrôle porte aussi sur le premier registre en bas de page (`critique`) : supprimer les descriptions périmées, les développements incompatibles et les affirmations matérielles sans preuve ; conserver les remarques étayées. Les notices historiques ne sont modifiées que pour résoudre une contradiction créée ou révélée par ce contrôle. Ne pas engager une nouvelle enquête biographique parallèle.
