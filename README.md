# Hippolyte Combes (1876–1970) — *Livre-Journal* (25 juillet 1916 – 30 avril 1917)

Ce dépôt réunit les photographies du *Livre-Journal* d'Hippolyte Combes, son édition, et les archives familiales et militaires qui l'éclairent. Professeur d'anglais, Hippolyte Combes (Millau, 14 août 1876 – Saint-Chély-d'Apcher, 2 septembre 1970) servit de 1915 à 1918 comme interprète militaire auprès de l'armée britannique. Son carnet suit, du 25 juillet 1916 au 30 avril 1917, la 152nd Company de l'Army Service Corps (train de la 18th (Eastern) Division) de la Flandre à la Somme, puis le service des achats de paille et de fourrage à Acheux et à Hérissart, avec deux permissions à Paris, Toulouse et Millau.

## L'édition

**[`edition/livre_journal.pdf`](edition/livre_journal.pdf)** — Hippolyte Combes, *Livre-Journal, 25 juillet 1916 – 30 avril 1917. Urtext. Transcription diplomatique en regard du fac-similé, commentaire critique et historique, cartes et illustrations*, édition établie par Louis Hauseux, 2026 (489 pages, 160 × 226 mm, Libertinus Serif).
**[`edition/livret_A4.pdf`](edition/livret_A4.pdf)** — la même édition imposée en 31 cahiers de 16 pages, pour l'impression en livret sur feuilles A4 (taille réelle, **100 %**, recto verso, retournement sur le bord court ; les pages sont déjà réduites à environ 92,8 % dans ce PDF).

- **Introduction** : biographie d'Hippolyte Combes, avec arbres généalogiques et photographies de famille ; un interprète français dans l'armée britannique (Mission militaire française, solde, 18th Division et son train, ravitaillement, cadre militaire, météorologie du carnet) ; description matérielle du carnet (petit carnet dont les feuillets, reliés en tête, sont aujourd'hui libres) et restitution de l'ordre des feuillets ; l'écriture et la langue du carnet, avec une planche paléographique ; principes de l'édition ; cartes générales.
- **Sept chapitres** (division éditoriale), chacun ouvert par une carte en regard de son introduction (le carnet, le contexte), avec des photographies d'époque.
- **Chaque page du carnet sur une double page** : à droite, le fac-similé ; à gauche, la transcription diplomatique ligne à ligne (soulignements, lettres suscrites, traits, crochets, accolades et équerres sur plusieurs lignes, ratures, ajouts et surcharges), l'apparat critique en marge, aligné sur les lignes, et trois registres en bas de page : remarques critiques, renvois internes (*loci paralleli*, en latin), commentaire historique sourcé.
- **Annexes** : lettres et pièces de guerre (1916–1918), transcrites intégralement avec un fac-similé ; état signalétique et des services ; abréviations du carnet ; glossaire des termes anglais et militaires ; sources et bibliographie ; sources des illustrations ; concordance des feuillets et des clichés ; index des personnes (132 entrées) et des lieux (248 entrées).

Exports : [`transcriptions/livre_journal_transcription.md`](transcriptions/livre_journal_transcription.md) (transcription lisible, dans l'ordre restitué) et [`transcriptions/livre_journal_donnees.json`](transcriptions/livre_journal_donnees.json) (données complètes de chaque page : transcription balisée, apparat, registres, sources).

## Méthode

- **Codicologie.** Les 186 photographies (26 novembre 2025) ont été remises dans l'ordre de lecture par l'étude de la transparence de l'encre : les deux faces d'un feuillet se superposent par une symétrie haut-bas, preuve que les feuillets étaient reliés en tête. Le carnet compte 93 feuillets ; trois ont été photographiés verso d'abord (ff. 18, 32, 56), une page l'a été deux fois (clichés 091 et 093), six pages sont écrites en travers.
- **Lecture.** Chaque page (3 711 lignes) a été relue intégralement sur les photographies en haute définition, en deux temps : une lecture lettre à lettre, puis un contrôle par un second lecteur, qui a vérifié au zoom les passages difficiles, les noms, les chiffres et les remarques des commentateurs. La relecture apporte 2 566 changements à la transcription antérieure (mots, chiffres, ponctuation, accents, disposition). Un audit de lecture complet (octobre 2026), dont chaque correction a été contre-vérifiée sur l'image par un second lecteur, en a ajouté 137 et rejeté 10 ; 358 lectures restent signalées comme incertaines, chacune justifiée dans l'apparat. Le relevé page par page des changements, des difficultés analysées lettre à lettre et des interventions du contrôle est conservé dans [`edition/donnees/relecture/`](edition/donnees/relecture/). Le guide de l'écriture d'Hippolyte Combes établi pour cette relecture est dans [`edition/ecriture/`](edition/ecriture/).
- **Sobriété.** L'apparat ne développe plus les abréviations ni ne traduit les mots anglais courants, réunis dans la table des abréviations et le glossaire (1 930 notes au lieu de 3 570) ; le registre critique ne retient que ce que le fac-similé ne montre pas (verso blanc du f. 6, ordre restitué, journées continuées) ; les commentaires historiques et les introductions ont été resserrés, chaque allègement étant contre-vérifié.
- **Recherches.** Huit dossiers sourcés (biographie ; 18th Division et son train ; interprètes et Mission militaire française ; Somme et Ancre ; Flandre et Artois ; permissions ; personnes ; culture matérielle) fondent les introductions et le commentaire : [`edition/recherche/`](edition/recherche/).
- Ce travail a été conduit avec l'assistance de modèles d'intelligence artificielle, sous la direction de l'éditeur. Les lectures douteuses et les identifications incertaines sont signalées comme telles.

## Compiler l'édition

Prérequis : XeLaTeX (TeX Live), polices Libertinus ; Python 3 avec `pyyaml`, `pillow`, `numpy`, `matplotlib`, `shapely`, `pyproj`, `tifffile` et `imagecodecs` (cartes), `pymupdf` (vérifications).

```bash
edition/construire.sh      # fac-similés, cartes, planche, crédits, source LaTeX, PDF (3 passes), livret A4, exports, vérifications
```

Les données éditoriales sont dans [`edition/donnees/`](edition/donnees/) : une page du carnet = un fichier YAML (`pages/NNN.yaml` : transcription balisée, apparat, registres), ordre et foliotation (`codicologie.yaml`), chapitres, index. Le balisage est décrit dans [`edition/BALISAGE.md`](edition/BALISAGE.md). Le générateur et la mise en page sont dans [`edition/src/`](edition/src/), les textes (introductions, annexes) dans [`edition/textes/`](edition/textes/), les cartes dans [`edition/cartes/`](edition/cartes/), les illustrations et leurs sources dans [`edition/illustrations/`](edition/illustrations/).

## Dossiers du dépôt

- [`edition/`](edition/) : l'édition (PDF, sources, données, textes, cartes, illustrations, dossiers de recherche, guide de l'écriture).
- [`transcriptions/`](transcriptions/) : exports de la transcription ; transcriptions antérieures et itinéraire (documents Word et PDF).
- [`scans_haute_qualite/`](scans_haute_qualite/) et [`scans_compresses/`](scans_compresses/) : photographies du carnet, numérotées dans l'ordre de la prise de vue (concordance avec les feuillets dans l'édition et dans `edition/donnees/codicologie.yaml`).
- [`archives_militaires/`](archives_militaires/) : registre matricule, parcours, photographies, lettres de guerre.
- [`biographie_et_famille/`](biographie_et_famille/) : biographie par Pierre Combes, état civil, portraits, correspondance familiale.

L'audit général de la version refondue et les corrections du 24 octobre sont documentés dans [`edition/verification/2026-10-24/`](edition/verification/2026-10-24/) : apparat, textes, cartes, fac-similés incorporés, exports et livret. L'audit de lecture et l'allègement des 24-25 octobre sont décrits dans [`edition/verification/2026-10-25/`](edition/verification/2026-10-25/).

L'édition précédente (`edition_philologique/`, octobre 2026) est conservée dans l'historique du dépôt, à l'étiquette [`edition-philologique-2026-10`](../../tree/edition-philologique-2026-10).
