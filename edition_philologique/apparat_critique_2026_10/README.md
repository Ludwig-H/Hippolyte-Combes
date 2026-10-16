# Reprise intégrale de l’apparat critique, octobre 2026

Ce dossier reprend les notes marginales et le commentaire critique des 186 photographies. La base est l’édition du commit `04673ef921062b4db01357cbdbff6069266947af`, après la seconde collation et les apports conciliés du développeur parallèle. Les états antérieurs sont conservés, avec leurs empreintes, dans [base_edition.json](base_edition.json), [base_revision.json](base_revision.json) et [base_manifest.json](base_manifest.json).

Chaque cliché entier a été rouvert et confronté aux lignes, aux notes et au commentaire. Les corrections s’appuient sur le tracé, sur les usages comparables de Combes et sur la syntaxe locale. Les contractions reçoivent un développement fléchi selon la phrase ; les locutions anglaises sont expliquées comme locutions ; les ratures, ajouts, signes et dispositions ne sont décrits que lorsqu’ils sont visibles. Les réserves demeurent explicites. Ce travail ne transforme pas une hypothèse d’identification en lecture certaine et n’établit pas une foliotation physique.

Le [registre des 186 vues](REGISTRE.md) donne les contrôles et les réserves. Les quatre lots finaux, chacun avec un compte rendu, sont [001–048](apparat_001_048.md), [049–094](apparat_049_094.md), [095–140](apparat_095_140.md) et [141–186](apparat_141_186.md). Le premier lot réunit deux sous-lots conservés comme témoins de relecture. Les contrôles ciblés ont reçu un second regard, notamment les abréviations contextuelles des premières pages, le renvoi courbe de la vue 103 et les contractions des vues 153, 163 et 185.

Le bilan comprend **2 467 entrées** (1 665 développements d’abréviation, 428 emprunts et 374 autres observations) et **neuf vues avec ajustement des lignes** : 002, 054, 098, 103, 113, 153, 163, 175 et 185. Le format du PDF passe à **185 × 270 mm** pour conserver l’apparat intégral et les commentaires sur la page en regard du scan, sans réduire les corps typographiques ni supprimer de notes.

Les entrées structurées portent un numéro de ligne, un lemme présent exactement dans cette ligne, une catégorie et une explication en texte simple. Elles remplacent entièrement les anciennes notes, dont certaines étaient limitées à deux explications par ligne. Le rendu conserve toutes les entrées et leur alignement ; aucune fusion automatique de lignes ni masquage de leur hauteur n’est appliqué à cet apparat. Les unités monétaires, horaires, de mesure et les signes usuels relèvent de conventions générales ; les emplois ambigus gardent une note locale.

La [méthode](PROTOCOLE.md), les [sources](SOURCES.md), les [contrôles de reproduction](VERIFICATION.md) et la [coordination du travail parallèle](COORDINATION.md) complètent le registre. Les propositions parallèles écartées du chemin de production restent archivées intégralement ; elles peuvent être reprises après confrontation aux clichés et à la base gardée.

Depuis la racine du dépôt :

```bash
python edition_philologique/assembler_apparat.py
python edition_philologique/parse_all_186.py
python edition_philologique/generate_edition.py
cd edition_philologique
xelatex -halt-on-error -interaction=nonstopmode carnet_hippolyte_combes.tex
xelatex -halt-on-error -interaction=nonstopmode carnet_hippolyte_combes.tex
python verifier_edition.py
```

Une modification de la base, des photographies, de la révision parente ou des lots doit être conciliée avant la régénération. Le vérificateur contrôle la cohérence des artefacts, leur provenance et la mise en page ; il ne certifie pas le déchiffrement d’une graphie incertaine.
