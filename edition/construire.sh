#!/bin/bash
# Construction complète de l'édition : fac-similés, cartes, planche, crédits, source LaTeX, PDF, livret A4,
# exports de la transcription, vérifications. Les étapes indépendantes tournent en parallèle sur tous les
# processeurs (une carte par processus) ; les trois passes de XeLaTeX restent successives.
set -euo pipefail
cd "$(dirname "$0")"
N=$(nproc)

# 1. Fac-similés, cartes, planche paléographique et crédits des illustrations, en parallèle
pids=()
python3 src/preparer_facsimiles.py & pids+=($!)
python3 -c "import yaml; print('\n'.join(c['id'] for c in yaml.safe_load(open('cartes/cartes.yaml', encoding='utf-8'))['cartes']))" |
  xargs -P "$N" -I{} python3 cartes/generer_cartes.py --seule {} "$@" & pids+=($!)
python3 src/planche.py & pids+=($!)
python3 src/credits_illustrations.py & pids+=($!)
for p in "${pids[@]}"; do wait "$p"; done

# 2. Source LaTeX et PDF
python3 src/generer.py
for i in 1 2 3; do
  xelatex -interaction=nonstopmode -halt-on-error livre_journal.tex > /dev/null
done

# 3. Livret A4 et exports, en parallèle ; puis vérifications
pids=()
(python3 src/livret.py && xelatex -interaction=nonstopmode -halt-on-error livret_A4.tex > /dev/null) & pids+=($!)
python3 src/exporter.py & pids+=($!)
for p in "${pids[@]}"; do wait "$p"; done
python3 src/verifier.py
