#!/bin/bash
# Construction complète de l'édition : fac-similés, cartes, planche, crédits, source LaTeX, PDF, livret A4,
# exports de la transcription, vérifications.
set -euo pipefail
cd "$(dirname "$0")"
python3 src/preparer_facsimiles.py
python3 cartes/generer_cartes.py "$@"
python3 src/planche.py
python3 src/credits_illustrations.py
python3 src/generer.py
for i in 1 2 3; do
  xelatex -interaction=nonstopmode -halt-on-error livre_journal.tex > /dev/null
done
python3 src/livret.py
xelatex -interaction=nonstopmode -halt-on-error livret_A4.tex > /dev/null
python3 src/exporter.py
python3 src/verifier.py
