#!/usr/bin/env python3
"""Vérifie que les défauts d'export, de fac-similé et de police sont refusés.

Les altérations restent dans un répertoire temporaire ; les sources et PDF
publiés ne sont jamais modifiés.
"""
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

ICI = Path(__file__).resolve().parent
EDITION = ICI.parents[1]
sys.path.insert(0, str(EDITION / "src"))
import verifier
from credits_illustrations import _tex


def main():
    erreurs = []
    pages = verifier.verifier_donnees(erreurs)
    assert not erreurs, erreurs
    resultats = []
    origine = verifier.EDITION
    try:
        with TemporaryDirectory(prefix="hc-regressions-") as dossier:
            racine = Path(dossier)
            temporaire = racine / "edition"
            temporaire.mkdir()
            (temporaire / "donnees").symlink_to(origine / "donnees", target_is_directory=True)
            for nom in ("livre_journal.pdf", "livre_journal.aux"):
                (temporaire / nom).symlink_to(origine / nom)
            (racine / "transcriptions").mkdir()
            export = json.loads((origine.parent / "transcriptions/livre_journal_donnees.json").read_text())
            export[0]["historique"] = "Texte périmé de la fixture de contrôle."
            (racine / "transcriptions/livre_journal_donnees.json").write_text(json.dumps(export))
            verifier.EDITION = temporaire
            erreurs = []
            verifier.verifier_export(pages, erreurs)
            assert any("001 : historique périmé" in e for e in erreurs), erreurs
            resultats.append({"cas": "export JSON divergent", "refuse": True, "diagnostics": erreurs})

            (temporaire / "fac-similes").mkdir()
            for image in (origine / "fac-similes").glob("*.jpg"):
                cible = origine / "fac-similes/002.jpg" if image.name == "001.jpg" else image
                (temporaire / "fac-similes" / image.name).symlink_to(cible)
            erreurs = []
            verifier.verifier_pdf(pages, erreurs, [])
            assert any("001 : image du fac-similé différente" in e for e in erreurs), erreurs
            resultats.append({"cas": "photographie intervertie", "refuse": True, "diagnostics": erreurs})

            journal = (origine / "livre_journal.log").read_text()
            (temporaire / "livre_journal.log").write_text(journal + "\nMissing character: There is no X in font Test!\n")
            erreurs = []
            verifier.verifier_compilation(erreurs, [])
            assert any(e.startswith("Missing character:") for e in erreurs), erreurs
            resultats.append({"cas": "glyphe absent", "refuse": True, "diagnostics": erreurs})
    finally:
        verifier.EDITION = origine

    for source, attendu in [
        ("Notice (https://example.org/a_b).", r"Notice (\url{https://example.org/a_b})."),
        ("Voir https://example.org/A_(B).", r"Voir \url{https://example.org/A_(B)}."),
        ("https://example.org/?a=1&b=2#c", r"\url{https://example.org/?a=1&b=2#c}"),
    ]:
        assert _tex(source) == attendu, (_tex(source), attendu)
    resultats.append({"cas": "ponctuation et contenu des liens", "trois_cas_conformes": True})
    (ICI / "regressions.json").write_text(json.dumps(resultats, ensure_ascii=False, indent=2) + "\n")
    print("Trois défauts refusés ; trois cas de liens conformes.")


if __name__ == "__main__":
    main()
