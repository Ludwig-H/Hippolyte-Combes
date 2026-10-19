# Guide paléographique : l'écriture d'Hippolyte Combes (*Livre-Journal*, 1916–1917)

Synthèse des études E1 (clichés 002–060), E2 (066–131) et E3 (abréviations, lectures suspectes) ; à lire avec
`BALISAGE.md`, `ABREVIATIONS.md`, `LEXIQUE.md` ; 24 extraits types vérifiés : `planche.yaml`. Renvoi « 049
[.19 .843 .345 .89] dormi » = cliché, rectangle x0 y0 x1 y1 relatif à la photographie entière (074–079 : image telle
qu'enregistrée), mot ; « l. » = ligne de l'état antérieur. Afficher :
`python3 /workspaces/hc_work/scripts/vue.py zoom 49 .19 .843 .345 .89 2` (ajouter `1` pour rehausser l'encre).

## 1. Ductus

- Cursive liée, **penchée à droite (25–35°)**, plume souple (pleins appuyés, déliés fins). Œil ≈ 1/60 de la hauteur
  du cliché ; interligne ≈ 0,045 ; 16 à 25 lignes par page.
- **Hampes et jambages longs de 2–3 œils** (f, p, q, g, j, ſ, z, 9) : ils entrent dans les lignes voisines. Une boucle
  isolée au-dessus d'un mot vient souvent de la ligne précédente ; au-dessous, de la suivante.
- **Barres de t, points et accents posés après coup, décalés vers la droite** : accent = court tiret au-dessus de la
  lettre suivante ; point du i jusqu'au-dessus du mot suivant ; barre de t couvrant tout le mot (tt, tte).
- Finales prolongées en **long délié** horizontal ou plongeant (e, s, t, n) ; un délié sans boucle peut valoir -e.
- **Minimes** (i, u, n, m, r, v, w) souvent indistinctes : compter les attaques ; u et v se confondent.
- **Encres** : violette (002–004, 045–097, 131–184), noire virée au brun ou gris-noir (007–041, 103–124), crayon
  (003 comptes ; 166). Un changement d'encre dans la page signale un ajout postérieur (027 colonne de droite ; 117
  total) : le dire dans `critique`. La **transparence du verso** (031, 038) donne des fantômes inversés.

## 2. Méthode de lecture lettre à lettre

1. **Isoler la ligne** : suivre sa ligne de base ; rendre à leur ligne les hampes, jambages et points intrus.
2. **Placer les repères** : majuscules, d en ∂, lettres descendantes (g, q, p, f, ſ, z, j), t barré, x en croix,
   signes (&, s/, +) ; puis **compter les minimes** entre deux repères (m = 3, n = 2, u = 2, i = 1 + point).
3. **Formuler le mot** et contrôler que *chaque tracé est employé* et *chaque lettre proposée visible*. Lettre absente :
   abréviation (`ABREVIATIONS.md`) ou délié final ; tracé sans emploi : lettre ou signe oublié (090 l. 14, un « 5 »).
4. **Comparer** avec la même lettre ou le même mot sur la page (même encre, même module), puis avec `LEXIQUE.md`.
5. **Transcrire l'image, non la langue** : accents absents (ecrit, Chateau, Aout), initiale minuscule (162 matin, ciel), ponctuation telle quelle. L'état antérieur n'est qu'une
   hypothèse (§ 8).
6. **Doute persistant** : `\inc{…}` + entrée `difficultes` (analyse lettre à lettre, alternatives) ; zoom ×2–×3.

## 3. Disposition type des pages

- **En-tête (l. 1)** : à gauche quantième + jour, dans les deux ordres (« 25 Ma. », « Dim. 30. », « 18 Lundi. »),
  **souligné** d'un trait appuyé souvent prolongé et terminé en crosse ; à droite mois + millésime (« Juillet 1916 »,
  « Sept^{bre} /16 ») souligné : `\sl{25 Ma.} \hfill \sl{Juillet 1916}`. Ne souligner que ce que le trait couvre
  (007 : seul 1916). Une note brève (« Levé dès 8^{h} m. », « Chaleur accablante ») est sur la l. 1 entre les deux
  *ou* sur une ligne propre en retrait sous la date (014, 019, 060) : vérifier.
- **Nouvelle journée dans la page** : `\filet` droit, oblique ou ondulé (007 y≈.565 ; 097 [0 .38 1 .47]), puis
  date soulignée en tête de ligne, sans le mois.
- **Corps** : marge gauche nulle ; alinéa = retrait de 0,08–0,15 de la largeur (`\ind`, `\ind[2]`) ; trait de
  remplissage en fin de phrase ou de journée (`\trait`, 071 [.74 .80 .92 .835]) ; blancs (`\blanc{n}`).
- **Comptes** : en fin de journée, après un filet ou intercalés et précédés d'un tiret (007 l. 16–17) ; souvent en
  deux colonnes (`\hfill`) ; montant rejeté à droite ou sur la ligne suivante (`\droite`, 021 l. 12). Signe
  d'ouverture : **grand crochet** `\crochet{n}`, haste verticale à deux pieds (041 [0 .872 .40 1.0], trois lignes ;
  le pied fixe n), **équerre** ⌜ `\equerre{n}` (010 [0 .49 .32 .57] ; 100 l. 25 ⌜…⌝ `\equerred`),
  **barre** `\barre{n}` (079 l. 6–7). Aucune accolade relevée : n'en pas inventer.
- **Ajouts** : interlinéaires écrits petit (`\add{…}`, 041 « des postes » sous la l. 11), dans un blanc à droite
  (117 « (déprimé) »), en marge (`\addm{…}`, 014 l. 9).
- **Pages en travers 074–079** : même module, lignes de 50–60 signes.

## 4. Minuscules

| | Forme(s) | Confusion → critère | Exemples |
|---|---|---|---|
| a | panse ovale fermée + court jambage qui la ferme et lie à droite | a/o : o fermé et lié **par le haut**, sans jambage ; à : a + accent détaché, parfois queue descendante (aspect ą) | 049 [.35 .055 .60 .105] brouillard |
| b | (1) haste non bouclée + arche ouverte (aspect h) ; (2) boucle haute + panse fermée (aspect lo) | b/h : la panse du b se referme sur la ligne | 057 [.55 .075 .715 .13] Labarthe |
| c | petit crochet ; à l'initiale, attaque montant de sous la ligne (faux ç) | vraie cédille = petite queue attachée au bas du c | 041 [.15 .93 .33 .98] cartes |
| d | panse + haste rejetée en arrière, bouclée à gauche (∂), à l'initiale comme en finale | panse noyée → aspect l (d'aubépine) ; boucle ouverte → cl, ol | 049 [.19 .843 .345 .89] dormi |
| e | petite boucle souvent pleine d'encre ; finale en long délié | délié final ≠ tiret ou `\trait` (aucune levée de plume) | 060 [.49 .078 .625 .108] messe |
| f | tête bouclée haute + jambage très long sans boucle inférieure | f/ſ : la tête du f dépasse les hampes ; f/5/7 dans les comptes : contexte | 071 [.02 .755 .31 .885] firmament |
| g | panse + jambage refermé en boucle | g/q : q sans boucle de retour ; g/8/9 | 057 [.54 .295 .70 .36] l'église |
| h, k | haste bouclée + arche ; k : petit nœud à mi-hauteur | h/k ; « très » réduit à « hu » | 007 [.18 .125 .37 .165] breakfast |
| i, j | point décalé à droite, en tiret ou virgule couchée ; j à longue descente | un point isolé appartient au i le plus proche à gauche, non à la ponctuation | 066 [.155 .118 .30 .175] petit |
| m, n, u | jambages anguleux ; mm et finales écrasés en trait ; n final parfois plongeant | compter les attaques ; av/au | 071 [.145 .605 .31 .66] Comme |
| p | haste droite très longue sans boucle, attaque parfois haute (aspect f) | p/f : f a une boucle de tête | 045 [.19 .20 .28 .245] par |
| q | petite panse + haste droite (aspect J, y) ; qq = deux hastes parallèles | q/g ; qq/44/yy | 071 [.455 .465 .57 .535] que |
| r | pointe ou petite bosse, souvent un simple jambage ; à l'initiale, grande boucle d'attaque (aspect 2, l) | r/i ; r/s final ; r initial/2 | 049 [.015 .528 .135 .585] retiré |
| s | (1) initial ou médian **montant** en haute boucle (aspect l, b, h) ; (2) **ſ long** descendant ; (3) final **plongeant** en ʒ ; (4) final réduit à un crochet ou à un trait vertical précédé d'un point d'attaque (aspect 1) | ss = « ll » ou « ff » ; s/l ; ſ/f/p ; s final/1 | 060 [.49 .078 .625 .108] messe ; 057 [.54 .295 .70 .36] église ; 057 [.845 .40 1.0 .465] Lauraguais ; 083 [.60 .47 .75 .53] frs |
| t | sans boucle (initial parfois bouclé, aspect l) ; barre longue tracée en dernier ; tt, tte sous une barre commune | barre longue ≠ rature (qui a ses propres extrémités) ; t/+ | 076 [.365 .59 .475 .668] ds tt |
| x | grande croix, second trait long et appuyé, recoupant le délié | x/+ | 071 [.04 .80 .33 .885] gde paix |
| y | tête en **V ouvert**, descente terminée **vers la gauche** (crochet ou boucle) | y/& (§ 7) ; y/g | 041 [.86 .595 .93 .655] y |
| z | ʒ plongeant sous la ligne | z/g/y/3 ; chz | 057 [.48 .485 .68 .53] horizon |

## 5. Majuscules

- **A** : (1) pointu « en 4 » (jambe gauche fine, droite épaisse, barre débordant à gauche) 002 [.09 .55 .20 .60] ;
  (2) a agrandi (ɑ) sans pointe 049 [.02 .185 .185 .23]. Souvent au module d'une minuscule : A seulement si la
  forme ou la taille l'imposent.
- **B** = b agrandi (aspect ℓo) 002 [.22 .21 .37 .255]. **C** : petite boucle de tête puis grand arc ouvert 049
  [.03 .765 .22 .80]. **D** en ∂ (049 [0 .275 .42 .34] Ds) ou en J, fût descendant (083 [.02 .008 .36 .08]).
  **E** bouclé (aspect ∂, ℰ, &) 007 [.03 .185 .15 .23]. **F** : boucle d'attaque, barre de tête ondulée, barre
  médiane, descend sous la ligne 049 [.015 .333 .225 .395]. **H** : deux hastes et traverse, ou une haste traversée
  (ɫ) 045 [.03 .50 .35 .54]. **J** : grande boucle inférieure fermée vers la gauche 002 [.565 0 .99 .088].
- **L** en £ ou ℒ (boucle haute, descente, boucle basse, trait de base portant la lettre suivante) 066 [.30 .41 .365 .46].
  **S** en ſ ou en L bouclé (trait montant de la gauche, boucle en tête, longue retombée) 097 [.01 .462 .18 .507] ;
  **S/L** : confusion majeure (Sam., Solde, Séparés).
- **M**, **N** : long délié d'attaque puis jambages anguleux (aspect ///, ʎu) 002 [0 .015 .31 .098]. **P**, **R** :
  haste + boucle haute ; R ajoute une jambe (oblique dans les sigles : 083 [.85 .43 1.0 .48]). **T** : haste + barre
  de tête réduite à un crochet 045 [.03 .45 .36 .50]. **V** : long délié d'attaque, premier jambage épais (aspect 1,
  K) 066 [.045 .005 .235 .05]. **Y** = y agrandi (« Y gd calme » = il y a) 010 [.60 .775 .67 .84]. **Z** en ʒ 053
  [.02 .72 .30 .78].

## 6. Chiffres

| | Forme(s) | Confusion → critère | Exemples |
|---|---|---|---|
| 1 | haste simple, souvent précédée d'un long trait d'attaque (aspect ʌ, 7 sans barre) | 1/7 : le 7 a barre de tête **et** barre médiane ; « 1 » = un, une (1 peu, d'1) | 002 [.785 .015 .925 .075] 1916 |
| 2 | (a) « à nœud » (juillet 1916) ; (b) bouclé : tête ronde, boucle fermée à la base, pied horizontal (aspect ℓ, ℒ) | 2/L/t ; 2 bouclé/& | 002 [0 .015 .31 .098] 25 |
| 3 | à deux panses ; en ʒ (une panse descendante) ; réduit à un trait en J | 3/5 : le 5 a un drapeau ; 3 réduit : contexte | 019 [.04 .005 .11 .055] ; 007 [.17 .005 .24 .05] |
| 4 | (a) fermé (aspect d) ; (b) ouvert en h ou k | 4/h/d/& : position devant une unité, aucune liaison | 010 [.02 .01 .065 .06] ; 053 [.55 .73 .61 .765] |
| 5 | (a) en ſ : longue haste, drapeau en tête ; (b) en ℓ : haute boucle fermée ; (c) drapeau + panse ouverte (ʒ, S) | 5/f : f monétaire petit et haut, 5 sur la ligne suivi d'un chiffre ou de c ; « 50 » lu ſo, lo | 002 [.045 .02 .095 .09] ; 053 [.22 .672 .335 .722] 12^{f} 50 |
| 6 | boucle basse fermée + haste montante incurvée | 6/0 ; 6/b | 004 [.84 .845 .935 .89] 60 c |
| 7 | barre de tête courte ou crochue (ʔ), diagonale sous la ligne, **barre médiane** (constante en 1917) | 7/1 ; 7/f ; 7 final à pied bouclé (aspect 2 : 131 « 1917 ») | 004 [.065 .012 .105 .065] ; 124 [.855 0 1.0 .05] |
| 8 | un seul tracé : petite boucle haute (parfois ouverte), grande boucle basse | 8/g ; 8/3 | 045 [0 0 .10 .05] |
| 9 | boucle fermée en haut + haste droite (longue dans les dates) | 9/g/y/q ; 9/4 | 014 [.55 .30 .66 .35] 9^{H} |
| 0 | petit ovale penché à hauteur d'œil, parfois ouvert en haut (aspect u) | 0/o ; 0/6 | 053 [.515 .605 .59 .64] 10 c |

- **Fractions** : ½ empilé (1 en haut, petite barre, 2 en ℓ couché ; aspect ʒ, 3, tz) → `\fr{1}{2}` (049
  [.295 0 .495 .058] ; 100 [0 .13 .14 .19]) ; à barre oblique → `1/2` (006 [.08 .055 .55 .095]) ; 2/3 oblique (083).
- **Millésime** : « 1916 », « /16 » ou « 16 ». La barre du t de « Sept » prolongée n'est pas « / » ; la barre de
  « /16 », plus longue et plus inclinée, n'est pas un 1 (090 [.64 0 .92 .08] : non « 116 »).
- **Montants** : `1^{f} 50`, `75c`, `84 fr.` ; décimale à point (`78.75 c`, 046 ; `0.05`) ; total `= 88 fr. —`.

## 7. Signes

- **Esperluette &** (jamais typographique) : (1) **« 4 »** : petite boucle fermée à gauche à hauteur d'œil, haste qui
  monte à droite puis descend sous la ligne (014 [.308 .852 .352 .893]) ; (2) **ρ / ℓ** : boucle fermée en haut à
  droite, haste oblique vers la gauche, parfois boucle géante (023 [.435 .215 .48 .27] ; 131 [.75 .14 .90 .22]) ;
  (3) **ƒ** : drapeau en tête, haste épaisse sans boucle (007 [.78 .505 .82 .555]) ; (4) **« t bouclé »** : petite
  boucle pleine en bas à gauche, haste coupée d'une barre (090 [.603 .718 .955 .79]) ; (5) **Y à pied droit** (031
  [.18 .295 .23 .35]). **Critères** dans l'ordre : (1) tête fermée ou barre = &, V ouvert = y ; (2) fin de descente vers la droite = &, vers la gauche = y ; (3) & relie deux termes de même
  nature (Matin & après-midi), y précède un verbe ou suit « il » ; (4) 2 bouclé : bouton de tête, boucle basse, pied,
  devant un nom compté (023 [.86 .945 .99 .995]) ; (5) « à » : a en ɔ + long accent (097 l. 18 a la forme du &). Le
  « et » en toutes lettres coexiste (071 [.36 .52 .45 .565]) : ne pas normaliser.
- **+** croix droite détachée = plus (comptes ; « de + en + », « + tot ») 071 [.015 .525 .31 .59] ; ≠ t (aucune
  liaison). **=** deux traits superposés = même (« moi-= », 012 [.08 .12 .30 .16]) ou total (117 « = 88 fr. — »).
- **Tirets** : – court (après le jour abrégé, entre postes), — long (fin de phrase, après un montant ; souvent épais,
  en massue) ; suites « – — » telles quelles. Point abréviatif réduit à un trait bas : le décrire (007 « Dim – 30. »).
  `\trait` = trait tiré jusqu'à la marge ou délié final prolongé (090 [.30 .445 .58 .505]) ; filet partiel
  `\filet[g]{0.15}` (047 l. 16).
- **Barres obliques** : **s/** = ſ + barre parallèle (« sur », 007 [.39 .03 .535 .076]), parfois aspect « 1/ » ou
  « // » (110 [.84 .16 1.0 .21]) ; ≠ fraction ; ≠ « /16 ».
- **Parenthèses** hautes, fines, souvent non refermées (031 « (boqueteau ») : ne pas les fermer ; fermante couvrant deux lignes (034 [.74 .40 .92 .52]). Une finale recourbée vers le bas (023 « amené »)
  n'est pas une parenthèse.
- **Lettres suscrites** `^{…}` : base au-dessus de la ligne de base (ligne de tête ou plus haut), module réduit. f
  monétaire après le chiffre (petite boucle ou crochet, parfois au-dessus du chiffre suivant : 117 [.84 .37 1.0 .44]) ;
  h des heures (petit H à deux hastes et traverse, aspect « lt », « 14 », « U », « + » : 049 [.295 0 .495 .058]) ; finales de contraction (002 [.71 .10 .87 .165] Marg^{te} ; 097 [.165 .805 .315 .865]
  C^{tes} p^{les}). Baliser seulement si la surélévation est nette : Lt, St, Mlle (060), « 9 H s. » (083
  [.52 .665 .70 .725]) restent à la ligne. Finale réduite à une ondulation (068 Oct^{bre}, 117 Dec^{bre}) : `^{bre}` +
  apparat.
- **Soulignements** : dates (§ 3), parfois tirés sous la ligne suivante (110). Mots soulignés dans le texte (060 « ensemble » ; 124 [.40 .80 1.0 .89]) : `\sl{}` après avoir écarté une
  barre de t ou un délié de la ligne inférieure.
- **Ponctuation** : point rond appuyé, en coin ou en petit trait ; deux-points nets ; virgule = trait vertical long
  (aspect 1) ; apostrophe = trait vertical, parfois à point (aspect « ! », 007 [.03 .095 .28 .13]) ; `"` = idem.

## 8. Les 30 pièges principaux (état antérieur → lecture sur l'image)

1. **bcp → bp** : b + p liés, aucun c, dans toutes les occurrences contrôlées (017 [.20 .315 .29 .355] ; 112).
2. **lgt, lgts → lgs** le plus souvent : l + g + s descendant, sans barre (082 [.03 .64 .15 .69]) ; vrais lgt en
   006 l. 12, 016 l. 14 ; longt en 006, 103.
3. **tjrs, Tjrs** jamais vu sur l'image : **Tjours** si des jambages suivent le j (085 [.29 .595 .46 .645]), **tjs** sinon
   (076 [.16 .79 .215 .88]).
4. **av. / avec** : une seule forme cursive (a + v arrondi + e réduit + délié), sans point : `avec` si quatre
   éléments, `av` si le mot s'arrête au v (058 [.38 .835 .45 .865]).
5. **Lettres suscrites** jamais marquées par l'état antérieur (heures, francs, finales) : contrôler chaque cas.
6. **Fractions** : `1/2` oblique ou `\fr{1}{2}` empilé selon l'image ; l'empilé a été lu 3, « t. », [illis.] (047 l. 2).
7. **f monétaire fantôme** : un 5 à haste ou à crochet lu f (046 [.40 .82 .78 .89] `78.75 c` ; 059 l. 19 `1.25`) ;
   inversement, le f suscrit a souvent été omis.
8. **& / y / à** : critères § 7 ; 097 [.03 .735 .36 .82] « Soir, à repas » porte la forme du &.
9. **2 bouclé lu &** : 023 l. 23 « & eggs) » a plutôt la forme du 2 (« 2 eggs ») [.86 .945 .99 .995].
10. **chez → chz** (c-h-z, z plongeant : 007 [0 .70 .45 .745]) ; ch. (suspension) est une autre forme.
11. **moi-m. → moi-=** (signe = pour « même » : 012 [.08 .12 .30 .16]).
12. **j. à, j'à → j-à, j-au** : trait d'union court (021 [0 .18 .30 .225]).
13. **pr / par / et** : pr = p + bosse + délié ; par = p + a fermé + r (118 [.55 .76 .98 .805]) ; 042 l. 23 « pr 1ère fois » = « et 1^{ère} fois » [.30 .885 .75 .94].
14. **ts / tt** : même tracé (deux hampes, barre commune) ; la syntaxe seule tranche (100 [.20 .465 .32 .52]).
15. **à / ds** : 059 l. 12 « à mon appartt » → `\inc{ds}` (haste haute, aucun accent) [.02 .595 .30 .645].
16. **Faux illisibles** : 023 l. 6 [illis.] = C^{tis} [.52 .17 .80 .215] ; 090 l. 15 [verbe illis.] = juché.
17. **Découpage des lignes** : « des postes » (041) est un ajout de la l. 11, non une ligne ; 162 l. 2–3 : la ligne
    s'arrête après « brouillard » [0 .04 1.0 .11]. Une ligne de texte = une ligne manuscrite.
18. **Note de tête** (014 « Chaleur accablante », 002 « Bien reposé ») : l. 1 ou ligne propre, selon l'image.
19. **Signes d'ouverture des comptes** omis ou rendus par « [ » : `\crochet{n}` (compter n au pied : 041 = 3),
    `\equerre{n}` (010, 100, 112), `\barre{n}` (079).
20. **Tracés de la ligne voisine** pris pour des lettres (071 [.80 .44 .99 .53] ; 007 l. 11 : g de « grenier »
    devant « ecrit ») ; points d'i de la ligne inférieure pris pour une ponctuation (007 l. 7).
21. **Barre de t prolongée** lue rature, soulignement ou « / » du millésime.
22. **Barre de « /16 »** lue 1 (090 [.64 0 .92 .08], « Nov^{bre} /16 »).
23. **Pâtés, reprises d'encre** (066 [.03 .405 .26 .475]) pris pour des ratures ; mot noyé →
    `\inc{}` (046 l. 4 « ce » ; 114 l. 3 « Tjours »).
24. **Majuscules** : S lu L et inversement ; D en J ; A réduit au module d'un a ; V lu 1 ou K ; initiales réellement
    minuscules (162 matin, ciel ; 079 merc.).
25. **Normalisations** de l'état antérieur : accents ajoutés (ecrit, Chateau),
    ponctuation ajoutée (007 l. 7) ou omise (015 l. 3 « Bien, reposé ») : suivre l'image.
26. **H suscrit ou à la ligne** : comparer la base de l'H à celle du chiffre (066 [.62 .315 .725 .372] 7^{H} 25 ;
    083 « 9 H s. ») ; le s. du soir peut se réduire à un 1 (131 [0 .30 .20 .36]).
27. **Adverbes en -t** : ext^{t}, extrêm^{t} (117, circonflexe visible), admirab^{t}, magnif^{t}, merv^{t} (060
    [.345 .035 .465 .08]) ; « lamentables » ou `lamentabl^{t}` (110 l. 9 et l. 20) à décider sur l'image.
28. **Noms propres** : Lupin/Lépin (023, 085, 090), Steenwerck/Steenwerk (023 l. 22), « Bertin » = V-a… (104
    [.84 .145 1.0 .195]), « Cap. W. » = cap. W^{m} (112 l. 18), « Bne Maman » = Bonn… (059 [.79 .88 1.0 .995]),
    relire lettre à lettre.
29. **Chiffre isolé omis** : 090 [.20 .53 .62 .60] « billet 5 & ts mes » ; le « 1 » article (1 peu, d'1 gde) se
    transcrit en chiffre.
30. **Instruments** : montants au crayon (003 [.25 .79 .99 .89]), total ajouté à l'encre violette (117
    [.45 .855 1.0 .96]), colonne ajoutée (027) : décrire dans `critique` ou l'apparat.
