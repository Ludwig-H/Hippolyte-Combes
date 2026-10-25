# Audit de lecture et allègement — 24-25 octobre 2026

Base : `7236c2f` (audit de Codex du 24 octobre), avec la réécriture stylistique des textes alors en cours dans le dossier principal. Demande de Louis Hauseux : auditer intégralement l'édition et les documents nouveaux (*Feuillets de Route*), rendre l'édition moins verbeuse et d'un style moins précieux (en gardant « Urtext »), retirer les expressions pieuses ou laudatives, réduire l'avertissement à quelques lignes (sans adresse GitHub, l'éditeur nommé, sans lien de parenté avec Pierre-Alain Hauseux). Louis Hauseux a précisé que le verso du f. 6 a été photographié et qu'il est blanc : les réserves de `7236c2f` sur l'état de ce verso sont donc retirées.

## Transcription

- Chaque page (185, 3 711 lignes) a été relue sur les photographies en pleine résolution, découpées en tuiles, lettre à lettre dans les cas difficiles.
- Chaque correction proposée a été soumise à un second lecteur chargé de la réfuter sur l'image : 137 corrections retenues (dont une modifiée), 10 rejetées. Les corrections retenues sont relevées page par page dans `edition/donnees/relecture/NNN.yaml`, champ `audit`.
- Lectures incertaines : 358 (351 avant), chacune justifiée par une note de lecture. Deux lectures ont été réexaminées lors de la revue finale : « 15 c » (f. 27 v°, l. 14), confirmé par comparaison avec le f. 27 r°, l. 17 ; « tea-dinner » (f. 93 r°, l. 12), désormais marqué incertain : on ne compte que quatre jambages après le *d* (« diner » possible).

## Apparat et registres

- Apparat : 3 570 → 1 930 notes. Les abréviations et les mots anglais courants (les 123 abréviations et les 34 mots anglais les plus fréquents) ne sont plus développés à chaque occurrence ; ils sont réunis dans la table des abréviations et le glossaire. Une note est gardée quand le développement n'est pas l'usuel (*pr* = *par*, *fr.* = *française*, *m.* = *minutes*) ou qu'elle justifie une lecture.
- Registre critique : limité à ce que le fac-similé ne montre pas (ordre restitué des feuillets, verso blanc du f. 6, journée continuée ou manquante, date fautive) ; 46 pages sur 185 (184 avant). Aucune remarque sur l'encre, le papier ou les soulignements.
- Commentaire historique : 738 caractères en moyenne (1 082 avant ; 887 au plus). Chaque allègement a été contre-vérifié contre la version précédente : faits, marques d'incertitude, sources, renvois de feuillets.

## Textes

- Page de titre (« Édition établie par Louis Hauseux »), avertissement en cinq lignes, colophon.
- Introductions, chapitres et annexes : style simplifié ; expressions pieuses, laudatives ou précieuses supprimées ; sections « Le carnet » des introductions de chapitre ramenées à une synthèse (environ 550 mots) ; redites entre introductions remplacées par des renvois. Chaque texte a été comparé à la version précédente par un vérificateur chargé de relever les faits perdus, altérés ou ajoutés.
- Citations du carnet recalées sur la transcription définitive (`verifier_citations_textes.py`) ; une citation inexistante a été remplacée (« Place assez semblable à celle d'Hazebrouck & de Bethune », f. 4 r°).
- Lettres (documents 1 à 5) : les remarques d'encre deviennent le fait qu'elles établissent (ajout ou correction postérieure) ; la carte postale du 12 novembre 1918 est reproduite à l'endroit.
- Index : Mme Miquel (autre lecture : Mignot) ; le capitaine « Pant » n'est pas identifié. Table des abréviations mise à jour (formes et comptes).
- Cartes : apostrophes et exposants, dates d'Albert (19 octobre – 2 novembre), légende distinguant le lieu principal (point plein) des villages cités (cercle).

Les *Feuillets de Route* (document 6) font l'objet d'une relecture séparée (deux lectures indépendantes, arbitrage, vérification) ; leur édition révisée suivra.

## Contrôles

- `controle_coherence.py` : aucune lecture incertaine sans note ; aucune remarque d'encre au registre critique ; aucun commentaire de plus de 900 caractères ; tous les renvois de feuillets existent.
- `verifier_citations_textes.py` (textes et commentaires) : signalements restants examinés, tous faux positifs (citations d'autres sources, renvois multiples).
- `chercher_expressions.py` : plus d'expression pieuse ou laudative hors citations.
- Revue finale : contrôle visuel d'environ 130 pages rendues du PDF et relecture croisée des introductions et des chapitres ; les défauts relevés ont été corrigés (ligatures historiques désactivées, guillemets insécables, en-têtes, légendes, placement des figures).
- Cohérence des identifications : pour chacune des personnes nommées en plusieurs endroits, notice d'index, commentaires des pages, chapitres et introductions confrontés ; une vingtaine de certitudes ramenées à la formule prudente justifiée par les sources (« sans doute », « peut-être »), quelques faits rectifiés d'après le carnet.
- Seconde revue visuelle des pages modifiées : en-têtes (titre de section posé avec son titre), arbres généalogiques, cartes (légende de la zone tenue par l'armée allemande, étiquettes dégagées, retour Paris–Acheux, villages des tournées), redites d'un chapitre à l'autre remplacées par des renvois.
- Construction complète (`edition/construire.sh`) : aucune référence indéfinie, aucun caractère manquant, aucune boîte trop pleine ; `verifier.py` sans erreur.
