# Balisage de la transcription diplomatique (spécification v1)

But : restituer le plus fidèlement possible chaque page du *Livre-Journal* (lignes, soulignements, lettres suscrites,
traits, crochets et accolades couvrant plusieurs lignes, ratures, ajouts, blancs), de façon à ce que LaTeX
reproduise la disposition de l'autographe. Le texte est transcrit tel qu'il est écrit : graphie, accents (présents
ou absents), majuscules, ponctuation, abréviations NON développées (le développement va dans l'apparat).

## 1. Unités

- Le champ `transcription` contient **une ligne de texte par ligne manuscrite**, de haut en bas.
- Les lignes « techniques » (filets, blancs) occupent leur propre ligne et **ne sont pas numérotées**.
- Les numéros de ligne de l'apparat (`ligne:`) comptent **uniquement les lignes de texte** (1, 2, 3…), filets et blancs exclus.
- Une ligne manuscrite écrite en deux colonnes (ex. « Food : 60 c. —— Washing : 1 f. ») reste UNE ligne ; on sépare les colonnes par `\hfill`.

## 2. Balises en ligne

| Balise | Sens | Exemple |
|---|---|---|
| `\sl{…}` | souligné simple | `\sl{25 Ma.}` |
| `\sll{…}` | souligné double | `\sll{Total}` |
| `^{…}` | lettres ou chiffres suscrits (en exposant) | `M^{me}`, `8^{h}`, `lieu^{t}`, `1^{er}`, `M^{gte}` |
| `\del{…}` | mot(s) biffé(s), lisible(s) | `\del{venu}` |
| `\del{\ill}` | biffure illisible | |
| `\sur{a}{b}` | surcharge : *b* écrit par-dessus *a* | `\sur{5}{6}` |
| `\add{…}` | ajout interlinéaire (au-dessus de la ligne), placé à l'endroit où il s'insère | `ciel \add{très} bleu` |
| `\addm{…}` | ajout en marge (à gauche ou à droite) rattaché à la ligne | |
| `\inc{…}` | lecture incertaine (le mot est proposé) | `\inc{Sercus}` |
| `\ill` | un mot illisible ; `\ill[3]` = environ trois mots | |
| `\lac` | lacune matérielle (papier manquant, tache masquant le texte) | |
| `\hfill` | la suite de la ligne est rejetée à droite (date de mois, montant, 2e colonne) | `\sl{25 Ma.} \hfill \sl{Juillet 1916}` |
| `\trait` | trait horizontal tiré jusqu'au bout de la ligne après un mot (remplissage) | `gde paix épandue \trait` |
| `\fr{1}{2}` | fraction à barre horizontale (empilée) ; si Hippolyte Combes écrit `1/2` avec une barre oblique, écrire `1/2` | `7^{h} \fr{1}{2}` |

Signes autographes transcrits tels quels : `&` (esperluette), `+`, `=`, `—` (tiret long), `–` (tiret court), `/`,
`"` (guillemets ou signe de répétition « idem »), `[` et `]` lorsqu'ils tiennent sur une seule ligne, `(` `)`.
Ne jamais utiliser `[ ]` pour une intervention éditoriale : utiliser `\inc`, `\ill`, `\lac` ou l'apparat.

## 3. Balises de début de ligne (disposition)

| Balise | Sens |
|---|---|
| `\ind ` | la ligne commence en retrait (alinéa) |
| `\ind[2] ` | retrait plus marqué (environ 2 unités) |
| `\centre ` | ligne centrée |
| `\droite ` | ligne entièrement rejetée à droite |

## 4. Lignes techniques (sur une ligne propre, non numérotées)

| Balise | Sens |
|---|---|
| `\filet` | trait horizontal sur toute la largeur (séparation de journées, au-dessus des comptes) |
| `\filet[g]{0.5}` | trait partiel : position g (gauche), c (centre), d (droite) ; fraction de la largeur |
| `\blanc{n}` | espace laissé blanc, d'environ n lignes d'écriture |

## 5. Signes couvrant plusieurs lignes

Placer la balise **au début de la première ligne concernée** ; `n` = nombre de lignes de texte couvertes (y compris celle-ci).

| Balise | Sens |
|---|---|
| `\crochet{n}` | grand crochet ouvrant `[` à gauche, haut de n lignes (fréquent devant les blocs de dépenses) |
| `\crochetd{n}` | grand crochet fermant `]` à droite, haut de n lignes |
| `\accolade{n}` | accolade fermante `}` à droite regroupant n lignes (éventuellement suivie d'un total : `\accolade{3}[= 2 f 50]`) |
| `\accoladeg{n}` | accolade ouvrante `{` à gauche |
| `\barre{n}` | trait vertical en marge gauche sur n lignes |
| `\equerre{n}` | équerre ouvrante ⌜ (trait horizontal en tête puis trait vertical à gauche) sur n lignes, devant les comptes |
| `\equerred{n}` | équerre fermante ⌝ à droite sur n lignes |

Si un crochet ouvrant `[` ne couvre qu'une ligne, l'écrire simplement dans le texte.

## 6. Exemple

```
\sl{25 Ma.} Levé \inc{dès} 8^{H} m. Bien reposé \hfill \sl{Juillet 1916}
Courte nuit, pensé très vivement à Marg^{te} —
...
\filet
\crochet{2}A M^{me} \inc{Backer}, pour repas d'hier & 4 oeufs : 1 f 75
Varia : 75 c
```

## 7. Règles de fidélité

- Les variantes de forme des lettres (s long, r ou d bouclés, etc.) ne sont pas reproduites : « s » s'écrit s. Le chiffre « 1 » mis pour « un, une » reste un chiffre.

- Ne pas corriger l'orthographe, ni restituer d'accents absents (« Aout », « chateau » restent tels quels), ni ajouter de ponctuation.
- Abréviations : transcrire la forme abrégée exacte (lettres suscrites comprises) ; le développement va dans l'apparat.
- Mots anglais : tels qu'écrits ; traduction dans l'apparat.
- Chiffres et montants : exactement comme écrits (`1 f 75`, `0.50 c`, `2^{f}`).
- Lorsqu'un mot reste douteux, `\inc{…}` + entrée d'apparat donnant l'analyse lettre à lettre et les autres lectures possibles.
