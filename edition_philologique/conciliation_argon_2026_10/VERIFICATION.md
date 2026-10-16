# Vérifications de la conciliation

## Contrôles de l’ensemble

La génération depuis les scripts, puis deux passes XeLaTeX, aboutissent à un PDF de **424 pages** au format **155 × 225 mm**. `verifier_edition.py` réussit : 186 photographies en regard de leurs 186 transcriptions, ordre et références cohérents, trois registres conservés, trois arbres, huit cartes et deux index présents. Aucun débordement de boîte, aucun texte hors page ni renvoi LaTeX non résolu n’est détecté.

Le vérificateur compare les exports à la reconstruction, chaque vis-à-vis au source généré et l’index à son rendu. Le PDF porte l’empreinte sémantique des enregistrements dans ses métadonnées. Les empreintes des fichiers publiés sont consignées dans `empreintes_livrables.json`.

- [Résultat du vérificateur](verification_pipeline.txt).
- [12 contrôles de gardes](verification_gardes.json) : valeurs concurrentes, base et propositions modifiées, photographie divergente, champ non autorisé, preuve absente, doublon et idempotence.
- [14 contrôles négatifs des loci](verification_loci.json), sur le corpus final : lemmes absents, ligne zéro, offsets manquants ou hors ligne, direction, entité, doublon, attestation éditoriale, réserve et rature. Les 453 loci et leurs 852 cibles représentent 1 305 ancrages exacts contrôlés.
- [21 contrôles d’index](verification_index.json) : homonymes dans les arbres, prénoms seuls, mauvaises sources, positions invalides, ligne zéro, réserve et rature. [Attestations finales](attestations_index.json) : 232 vedettes examinées, 1 828 occurrences dans le texte ou les commentaires, 253 mentions documentaires.

Les caractères absents et les références non résolues sont contrôlés. XeLaTeX signale encore des substitutions de certaines formes de police ; le contrôle visuel complète donc les contrôles techniques sans leur attribuer une garantie typographique absolue.

## Contrôle visuel

Le [rapport visuel](verification_visuelle.md) précise le PDF examiné, les six vues contrôlées, les mesures et les limites. Les vérifications automatiques de toutes les pages n’équivalent pas à une nouvelle inspection visuelle des 186 images.

## Portée philologique

Les lectures et réserves sont justifiées dans les propositions. Le contrôle des ancrages prouve qu’un renvoi trouve son lemme transcrit ; il ne prouve pas à lui seul le déchiffrement de l’autographe, l’identité d’une personne ou l’exactitude d’un contexte historique. Les 47 nuances facultatives de l’audit historique restent hors du jeu des corrections appliquées. Les images et les témoins antérieurs sont conservés pour permettre la contradiction.
