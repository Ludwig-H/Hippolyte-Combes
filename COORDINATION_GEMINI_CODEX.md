# Coordination Gemini 4 Argon / Codex — 16 octobre 2026

Gemini conserve la direction éditoriale et graphique. Codex prépare une conciliation ciblée des lectures, de l’apparat, des notices et des renvois dans une copie isolée : `/tmp/hc_argon_codex/reconciliation_20261016` (HEAD détachée, aucune branche créée).

Les changements de Gemini jusqu’à `eb681bb` (filets diplomatiques, trois arbres et huit cartes TikZ) sont intégrés. Les trois registres, les sept chapitres et le format 155 × 225 mm sont conservés. Le lot concilie 111 fiches et 166 champs. Les corrections sont gardées par valeur antérieure exacte et empreinte des photographies ; un nouvel apport divergent provoquera un arrêt de la génération, pour conciliation explicite.

Paquet validé : 13 fiches de lectures/apparat, 95 notices historiques, 33 fiches de titres/lieux (40 champs), 13 paragraphes de chapitres, deux réserves codicologiques ; certains changements portent sur les mêmes vues. Les loci et les index sont réancrés sur des occurrences effectives. Aucun quota de notes marginales ni raccourcissement automatique n’est ajouté.

Le dossier `edition_philologique/conciliation_argon_2026_10/` contient les propositions, la base témoin, les décisions et les résultats des vérifications. Publication uniquement en avance rapide sur `main`, après régénération et contrôle du PDF ; aucune réécriture d’historique.

Ce fichier constitue un point de coordination dans le dépôt. Aucun canal de discussion direct avec Gemini n’est exposé dans cette session ; aucune réponse ou approbation de sa part n’est présumée.

## Refonte des cartes — 16 octobre 2026

À la demande explicite de Louis, les huit cartes schématiques sont remplacées par des PDF vectoriels géographiques. Travail préparé en HEAD détachée depuis `87d9c4a`, dans `/tmp/hc_cartes_20261016/repo`, sans branche supplémentaire et sans modification du dossier de travail principal. Les trois arbres, les photographies, les transcriptions et les notices de la conciliation restent conservés. Les changements portent sur les cartes, leur inclusion, leur indexation et leur vérification.

Le dossier `edition_philologique/cartographie/` contient les 82 localisations contrôlées, les fonds et licences, les justificatifs textuels des itinéraires, les scripts reproductibles, les huit PDF/SVG/PNG et les rapports indépendants. Les fonds sont explicitement contemporains ; aucune ligne de front conjecturale n'est tracée. Les liaisons indiquent une succession d'étapes, sans reconstitution du réseau routier ou ferroviaire historique. La position du bâtiment de Sainte-Marie-des-Champs en 1916 reste réservée.

La carte générale dispose d'une page propre ; les sept cartes de chapitre restent avec leurs photographies. L'édition conserve 424 pages, 186 vis-à-vis et les renvois d'index vérifiés à partir du texte effectivement imprimé des cartes. Le témoin historique `conciliation_argon_2026_10/empreintes_livrables.json` n'est pas réécrit : les nouvelles empreintes sont dans le dossier cartographique.

La publication se fait sur `main`, après contrôle de l'état distant et avance rapide, sans réécriture d'historique. Ce journal permet la reprise par Gemini ; aucune approbation de sa part n'est présumée.

### Correctif de chronologie des cartes après `6954da9`

À la question de Louis sur l'exactitude « à tout point de vue », une contre-vérification a révélé que Saint-Sernin était placé dans la première permission alors que la visite relève de la seconde. Le contrôle géométrique et la vérification globale des citations ne détectaient pas l'appartenance chronologique de chaque point. Ce défaut est reconnu et corrigé ; Matabiau, nom inféré dans III, est également retiré. Les contextes et identifications proposés sont désormais explicités sur les cartes, et la tournée du 30 avril ne reçoit plus de départ implicite d'Hérissart.

Le fichier `cartographie/verification/attestations_lieux.json` couvre les 120 points restants (80 lieux). Le validateur contrôle la période, les citations et les réserves imprimées pour chaque occurrence. Deux régressions reproduisent les défauts et confirment leur rejet. Les transcriptions restent inchangées : cette passe examine leurs attestations, sans prétendre à une nouvelle collation intégrale des images. La forme composée Corbeil-Essonnes a cependant été vérifiée ponctuellement sur l'autographe 145 et conservée. Les témoins de la livraison initiale restent identifiés comme tels.

## Refonte complète de l'édition — 18-19 octobre 2026 (Claude)

À la demande de Louis, l'édition a été entièrement refaite dans `edition/`, qui remplace `edition_philologique/` (conservée dans l'historique, étiquette `edition-philologique-2026-10`). Le titre ne porte plus « philologique » : *Livre-Journal. Texte diplomatique en regard des fac-similés, avec commentaire (critique & historique), cartes et illustrations*.

- Ordre des feuillets restitué par la transparence de l'encre (93 feuillets reliés en tête ; `edition/donnees/codicologie.yaml`).
- Relecture intégrale des 185 pages sur les photographies, en lecture puis contrôle indépendant, lettre à lettre dans les cas difficiles ; relevé par page dans `edition/donnees/relecture/`. Balisage diplomatique décrit dans `edition/BALISAGE.md`.
- Commentaire historique refait page par page d'après huit dossiers de recherche (`edition/recherche/`) ; introductions générales et de chapitre, annexes (lettres relues sur les originaux, services, abréviations, glossaire, bibliographie), index et *loci paralleli* recalculés.
- Générateur LaTeX neuf (`edition/src/`), format 160 × 226 mm, Libertinus ; cartes refaites (`edition/cartes/`) ; construction et vérifications : `edition/construire.sh`.

## Audit général après la refonte — 24 octobre 2026 (Codex)

Après récupération du distant, la base publiée est `ce61fc3`. L'audit est préparé dans `/tmp/hc_audit_20261024/repo`, en HEAD détachée, sans nouvelle branche. Les 19 modifications non commitées déjà présentes dans le dossier principal sont sauvegardées et maintenues séparément de la publication ; les corrections factuelles communes sont conciliées avec leur réécriture stylistique, sans publier celle-ci à leur place.

Le contrôle couvre les 186 fichiers de pages (185 pages actives, 3 711 lignes), les introductions et annexes, les index et renvois, les neuf cartes et les deux PDF. Les lectures diplomatiques ne changent pas. Corrections : notes et renvois incohérents, portée des preuves des *Feuillets de Route*, attribution du JMO des Irish Guards, ouverture du carnet en Flandre, réserves sur les faces non photographiées, cantonnement de Barlette et légendes des fronts. La notice d'impression précise que le livret A4 est déjà réduit et s'imprime à 100 %.

Les rapports et contrôles se trouvent dans `edition/verification/2026-10-24/`. Le validateur confronte désormais aussi l'export JSON aux YAML et les 185 images effectivement incorporées aux fac-similés préparés ; des cas négatifs vérifient le refus d'un export périmé, d'une photographie intervertie et d'un caractère absent. Le PDF corrigé compte 504 pages, le livret 256 pages A4 (32 cahiers de 16 pages). Les fronts restent schématiques, les fonds contemporains ; cet audit n'est pas une nouvelle collation intégrale des autographes ni un dépouillement renouvelé de toute la bibliographie.

La publication se fait sur `main` par avance rapide, sans réécriture d'historique. Aucune approbation d'un autre développeur n'est présumée.

## Audit de lecture et allègement — 24-25 octobre 2026 (Claude)

À la demande de Louis : audit intégral de l'édition publiée (`7236c2f`) et des *Feuillets de Route*, édition moins verbeuse et d'un style moins précieux (« Urtext » conservé), retrait des expressions pieuses ou laudatives, avertissement réduit (sans adresse GitHub, éditeur nommé, sans lien de parenté avec Pierre-Alain Hauseux). Travail dans le dossier principal ; les corrections de Codex (`7236c2f`) sont conservées, sauf les réserves sur le verso du f. 6 : Louis a précisé que ce verso a été photographié et qu'il est blanc.

- Lecture : chaque page relue sur les photographies en pleine résolution ; chaque correction proposée soumise à un second lecteur chargé de la réfuter sur l'image : 137 corrections retenues, 10 rejetées (relevé : `edition/donnees/relecture/NNN.yaml`, champ `audit`).
- Apparat : 3 570 → 1 930 notes ; les abréviations et mots anglais courants renvoient à la table et au glossaire (une note reste quand le développement n'est pas l'usuel). Registre critique limité à ce que le fac-similé ne montre pas (46 pages). Commentaires historiques : 738 caractères en moyenne (1 082 avant). Chaque allègement a été contre-vérifié.
- Textes : introductions, chapitres et annexes resserrés et contre-vérifiés contre leur version précédente ; citations du carnet recalées sur la transcription définitive.
- Pour les prochains passages : ne pas rétablir de remarques sur l'encre ou le papier, ni de formules pieuses ; le f. 6 v° est blanc ; `edition/donnees/index.yaml` est la référence (ne pas le régénérer depuis d'anciens brouillons).

Les *Feuillets de Route* (annexe, document 6) sont en cours de relecture lettre à lettre par deux lecteurs indépendants, avec arbitrage ; leur édition révisée suivra dans un second commit.

Rapport : `edition/verification/2026-10-25/`. Publication sur `main` par avance rapide, sans réécriture d'historique.
