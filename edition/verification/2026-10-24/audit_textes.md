# Audit des introductions, annexes et renvois — 24 octobre 2026

Base examinée : `ce61fc3`, nouvelle édition publiée ; corrections dans une copie de travail détachée. Les retouches stylistiques déjà présentes dans le dossier principal n'ont pas été incorporées au présent lot. Aucun texte diplomatique du carnet ou des lettres n'est modifié dans ce lot.

## Corrections établies

| Texte | Défaut corrigé | Preuve et portée |
|---|---|---|
| Introduction biographique | La découverte des *Feuillets de Route* confirmait indistinctement le service auprès des Irish Guards et le rôle personnel auprès du prince de Galles. | Le sommaire autographe contient « Avec les 1st Irish. Guards » ; aucune mention du prince dans ces titres. Le premier point est confirmé, le second demeure une tradition familiale explicitement attribuée. |
| Introduction biographique | WO 95/1216/1 était présenté comme le journal de l'état-major de la Guards Division. | Chemise photographiée, vue 6 de `archives_militaires/1st_Irish_Guards/WO-95-1216-1_01.pdf` : « 1st Gds Bde / 1st Batt. Irish Gds / Aug 1915 — Jan 1919 ». Correction en journal du bataillon. La bibliographie donnait déjà la bonne unité. |
| Biographie, description, annexe des lettres | Le feuillet « Journal 1915–1916 » devenait la preuve d'un carnet antérieur perdu et d'une suite matérielle déterminée. | Un titre de projet n'établit pas qu'un cahier correspondant a réellement été rédigé. Les notes antérieures sont suggérées ; l'existence et les dates d'un premier carnet restent ouvertes. La datation du projet, non daté, est également maintenue comme probable (« vers 1916 »). |
| Description du carnet | L'ouverture du carnet le 25 juillet 1916 était située à La Chaussée-Tirancourt, dans la Somme. | F. 1 r° (donnée 002) : « ciel de Flandre », visite de Sercus ; contexte de Lynde développé au chapitre I et f. 2 v°. Correction : environs de Lynde, en Flandre. |
| Description du carnet | Versos des ff. 6 et 93 implicitement réputés blancs alors qu'ils n'ont pas été photographiés. | `codicologie.yaml` ne dit que « Seule face photographiée de ce feuillet ». Le script de restitution original emploie `None` pour « face non photographiée » ; les dossiers de relecture ne produisent pas de constat du verso. Aucune attestation contraire repérée dans les courriels DOCX locaux recherchés. Formulation limitée aux rectos photographiés, sans modifier la foliotation ni supposer une lacune de texte. |
| Annexe des lettres | Papier du poème et des *Feuillets* déclaré exactement identique, suffisant à lever « tout doute » sur la provenance. | Les reproductions permettent un rapprochement de réglure et d'usage, non une preuve de provenance d'un même cahier. La copie du poème pendant la guerre est donnée comme possibilité, faute de date. Les analyses de main et les transcriptions sont conservées. |
| Annexe des services | Reconstitution de « toute la suite » des affectations, identification ferme de l'attaque de mai 1915 à Festubert. | Le titre autographe ne précise que mai 1915. La réserve déjà apportée dans l'annexe des lettres est harmonisée : principales étapes, rapprochement probable avec Festubert. |
| Bibliographie | Lettre de juin encore attribuée à Joséphine ; renvois aux documents 2 et 3 inversés ; lettre de février comptée comme trois pages. | La notice du document 3 identifie Françoise comme destinataire très probable. Le PDF de février contient trois vues, mais les deux premières reproduisent le même recto ; le verso est la troisième vue : deux pages écrites. Vérification directe des trois images. Les six notices renvoient désormais aux documents 1–6 avec pagination calculée. |
| Bibliographie | Étude familiale de 64 « pages » citée jusqu'à la p. 114. | La numérisation comporte des vues contenant deux pages de la pagination originale (ex. vue 26 : p. 47–48). Distinction entre 64 vues et pagination originale. |
| Chapitre VI | « L'interprète n'est pas payé moins pendant l'absence », suivi de la retenue de 35 F. | F. 74 r° (donnée 148) : versement de 78 F 75 au retour ; f. 81 r° (donnée 162), 3 mars : 43 F 75 et retenue de 35 F pour sept jours. La retenue est différée. |
| Introduction aux cartes | La carte générale était présentée comme rassemblant tous les lieux du carnet. | Elle ne retient que les principales étapes (15 points, contrôle du lot cartographique). Formulation corrigée. |
| Avertissement et description | Maurice pouvait être compris comme un second fils d'Hippolyte dans le récit de transmission. | Harmonisation avec l'arbre et la biographie : Maurice est fils de François. La correction minimale de l'avertissement est indépendante de la réécriture stylistique locale déjà en cours. |

## Contrôles transversaux

- Les 473 renvois explicites simples aux feuillets, relevés dans tous les fichiers `edition/textes/**/*.tex`, désignent des faces présentes dans le modèle codicologique. Ce contrôle de destination ne prétend pas valider automatiquement le contenu de chaque citation.
- Les 50 appels `ref`/`pageref` relevés dans ces fichiers trouvent une étiquette connue parmi les textes (ou le dispositif généré). Aucun appel d'annexe non résolu n'a été trouvé.
- Concordance vérifiée directement pour l'ouverture du 25 juillet, les deux versements de solde et les documents bibliographiques corrigés.
- Les fichiers corrigés sont `intro_biographie.tex`, `intro_description.tex`, `annexe_lettres.tex`, `annexe_bibliographie.tex`, `annexe_services.tex`, `chapitres/VI.tex`, `liminaires.tex` et `intro_cartes.tex`.
- `git diff --check -- edition/textes` ne signale pas d'erreur d'espacement.

## Limites

Cet audit porte sur les contradictions internes, la portée des preuves et les renvois de la nouvelle édition, avec examen direct des pièces citées ci-dessus. Il ne constitue ni une nouvelle collation intégrale de tous les autographes ni une nouvelle consultation de chaque ouvrage cité dans la bibliographie. Les hypothèses biographiques déjà expressément réservées ne sont pas transformées en faits acquis.

Les fichiers rédigés sont examinés séparément des sources de cartographie et du contrôle matériel du PDF, confiés aux autres lots. Les parenthèses de notices d'illustrations et les instructions d'impression sont traitées par le lot de génération ; elles ne sont pas comptées ici comme vérifications achevées.
