# Audit général du 24 octobre 2026

Base publiée : `ce61fc3`, après les neuf commits de refonte et de correction depuis `d269852`. La refonte remplace l'ancien générateur et l'ancienne édition par `edition/` ; elle réordonne les feuillets, renouvelle les transcriptions et l'apparat, ajoute les *Feuillets de Route* et propose neuf cartes. L'audit a été conduit sur cette nouvelle architecture, sans rétablir les anciennes lectures ou la présentation précédente.

## Résultat

Le livre corrigé compte **504 pages**, avec **185 vis-à-vis** (couverture comprise ; la seconde photographie du f. 46 r° n'est pas éditée deux fois). Il conserve les **3 711 lignes** de transcription, les sept chapitres, les annexes, les 132 entrées de personnes et les 248 entrées de lieux. Les 186 champs `transcription` des fichiers YAML sont identiques à ceux de la base ; l'export Markdown est également inchangé.

Les modifications sont ciblées : incohérences de notes et de renvois, assertions allant au-delà de la pièce disponible, légendes géographiques et instructions d'impression. Les principales corrections et leurs preuves sont décrites dans les trois rapports :

- [Apparat, index et renvois](audit_apparat.md) : six fichiers de pages et deux notices d'index ; 1 207 attestations manuelles et 568 renvois complets contrôlés.
- [Introductions, annexes et bibliographie](audit_textes.md) : lieu d'ouverture du carnet, attribution du JMO des Irish Guards, portée des *Feuillets de Route*, transmission familiale, versos non photographiés, retenue différée de solde et références des pièces.
- [Cartographie et iconographie](audit_cartes.md) : neuf cartes, 147 points imprimés ; Barlette, repères du camp, réserves de Purpan et Pech-David, dates des fronts et sens des hachures.

Les trois parenthèses manquantes des notices d'illustrations provenaient du générateur de liens. Celui-ci conserve désormais la ponctuation extérieure et les parenthèses appartenant à l'URL. Le fichier d'annexe a été régénéré.

## Vérification des livrables

- Génération des fac-similés et de la planche paléographique ; régénération des huit cartes modifiées (I inchangée), des crédits, du LaTeX et des exports ; compilation du livre jusqu'à stabilisation des renvois, puis du livret.
- **Aucun renvoi LaTeX indéfini, aucun caractère manquant, aucune boîte `Overfull`, aucun texte extrait hors page.** Les avertissements de `fancyhdr` sur un pied de page nul subsistent ; l'édition n'utilise pas de pied et aucun débordement n'est constaté.
- Les 185 paires ont leur transcription à gauche et leur fac-similé sur la page suivante. Les octets JPEG extraits du PDF sont comparés par SHA-256 aux 185 images préparées attendues. Ce contrôle prouve l'identité de l'image incorporée ; il ne constitue pas une preuve supplémentaire de la foliotation proposée.
- L'export JSON est confronté aux métadonnées codicologiques et à tous les champs éditoriaux des YAML.
- Les neuf cartes passent un contrôle indépendant des positions imprimées, des échelles et des limites de page : [résultats](cartes_controles.json), [script](verifier_cartes_pdf.py).
- Le livret contient **256 faces A4**, soit **32 cahiers de 16 pages**, avec huit emplacements blancs. Chacune de ses 512 demi-pages a été comparée, par ses caractères extraits, à la page attendue de l'édition ; formats et ordre conformes : [résultats](livret_controles.json). **Imprimer à taille réelle (100 %), recto verso, retournement sur le bord court** ; la réduction à environ 92,8 % est déjà effectuée dans le PDF.
- Trois défauts introduits uniquement dans des copies temporaires sont refusés : export périmé, photographie intervertie, caractère absent. Trois cas de liens vérifient la conservation de la ponctuation : [résultats](regressions.json), [script](verifier_regressions.py).

Le compte rendu du validateur est dans [validation_edition.txt](validation_edition.txt) ; les empreintes des fichiers livrés sont dans `livraison.json`.

### Examen visuel

Vue d'ensemble de toutes les pages de l'introduction et des annexes de la version de départ, examen des neuf cartes et des pages corrigées de l'édition finale (notamment pp. 2, 9, 14, 27, 31, 96, 110, 250, 300, 396 et 442). Les pages du corps ont toutes été contrôlées numériquement ; les photographies autographes n'ont été rouvertes que pour les points explicitement indiqués dans les rapports. Les vues d'ensemble ne valent pas une lecture intégrale des petits caractères à taille d'impression.

## Coordination et limites

Le dossier principal comportait déjà dix-neuf modifications non commitées, dont une réécriture stylistique des textes et un PDF de travail. Elles ont été sauvegardées avant intervention et ne sont pas publiées dans ce lot ; la copie d'audit est une HEAD détachée, sans branche supplémentaire. Les modifications factuelles communes sont conciliées pour préserver cette réécriture dans le dossier local. Le PDF local de travail ne constitue donc pas le témoin publié de cet audit.

Cet audit vérifie la cohérence générale, les preuves des corrections retenues et la production matérielle. Il ne remplace ni une nouvelle collation intégrale des autographes, ni un examen de l'objet matériel, ni une consultation nouvelle de chacune des références bibliographiques. Les identifications expressément incertaines restent réservées. Les fronts sont schématiques et les fonds géographiques contemporains ; les coordonnées des bourgs ne désignent pas les logements de 1916.
