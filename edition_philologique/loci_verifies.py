# -*- coding: utf-8 -*-
"""Loci paralleli vérifiables, indépendants des commentaires et des index.

Le catalogue hérité propose des rapprochements. Seules les lignes transcrites
produisent des attestations ; les titres et les lieux éditoriaux sont exclus.
Les lemmes affichés sont les sous-chaînes exactes des lignes. Les identités
personnelles que la seule graphie ne prouve pas restent des rapprochements de
lecture. La foliotation et les pages sont rendues par la fonction injectée.

API : build_verified_loci(records, entities, reference_fn) -> {scan_num: LaTeX}.
La fonction ajoute ``loci_entries`` à chaque enregistrement. Le validateur pur
``validate_loci_entries`` contrôle les deux extrémités de chaque renvoi.
"""
from __future__ import annotations

import re
from collections import defaultdict
from typing import Callable, Iterable

# Catalogue complémentaire de motifs effectivement recherchés dans les lignes.
# Aucun rapprochement n'est produit si les deux attestations ne sont pas trouvées.
THEMATIC_ENTITIES = (
    {"id": "theme_voyage", "pattern": r"(?<!\w)(?:train|trains|gare|gares|compartiment)(?!\w)", "kind": "thematic"},
    {"id": "theme_kit", "pattern": r"(?<!\w)kit(?!\w)", "kind": "thematic"},
    {"id": "theme_mess", "pattern": r"(?<!\w)mess(?:[- ](?:room|hut))?(?!\w)", "kind": "thematic"},
    {"id": "theme_billet", "pattern": r"(?<!\w)billets?(?!\w)", "kind": "thematic"},
    {"id": "theme_room", "pattern": r"(?<!mess )(?<![\w-])(?:room|chambre|chambrette|garret)(?![\w-])", "kind": "thematic"},
    {"id": "theme_bombardement", "pattern": r"(?<!\w)(?:bombard(?:ement|emt|é|ée|és|ées)|bombardt|canonnade)(?!\w)", "kind": "thematic"},
    {"id": "theme_food", "pattern": r"(?<!\w)(?:Food|food|eggs|œufs|oeufs)(?!\w)", "kind": "thematic"},
    {"id": "theme_lait", "pattern": r"(?<!\w)lait(?!\w)", "kind": "thematic"},
    {"id": "theme_washing", "pattern": r"(?<!\w)(?:Washing|washing|darning)(?!\w)", "kind": "thematic"},
    {"id": "theme_forage", "pattern": r"(?<!\w)(?:fourrage|fourragères|forage|paille|foin|luzerne)(?!\w)", "kind": "thematic"},
)

# Les regex anciennes confondaient des entités, notamment Germaine Faure avec
# Germaine Vincens, et la cavalerie indienne avec les 17th Lancers britanniques.
# Les prénoms seuls restent des prénoms ; on n'ajoute aucun patronyme au lemme.
SAFE_OVERRIDES = {
    "marguerite": ("marguerite", r"(?<!\w)(?:Margte|Marg\.|Mte|Marguerite|Gueïte)(?!\w)", "textual"),
    "r_fusiliers": ("r_fusiliers", r"(?<!\w)(?:R\.\s*Fusrs|Royal\s+Fusiliers|R\.F\.)(?!\w)", "textual"),
    "crouzet": ("crouzet", r"(?<!\w)(?:Crouzet|Czt\.?)(?!\w)", "textual"),
    "vincens": ("vincens", r"(?<!\w)Vincens(?!\w)", "textual"),
    "jean_crouzet": ("jean_prenom", r"(?<!\w)Jean(?!\w)", "lexical"),
    "pierre_calmels": ("pierre_prenom", r"(?<!\w)Pierre(?!\w)", "lexical"),
    "lancers_17": ("lancers_17", r"(?<!\w)(?:17(?:th|e)\s*Lancers|Death\s+or\s+Glory)(?!\w)", "textual"),
    "st_michel_ternoise": ("st_michel_ternoise", r"(?<!\w)St[. -]+Michel[- ](?:s[- ]|sur[- ])Ternoise(?!\w)", "textual"),
    "st_jacques": ("rue_st_jacques", r"(?<!\w)rue\s+St[.-]Jacques(?!\w)", "textual"),
    # Les formes patronymiques divergent : un renvoi ne prouve pas leur identité.
    "lepin": ("lepin_formes", r"(?<!\w)(?:Lupin|Lépin|Liepin)(?!\w)", "lexical"),
    "houthouan": ("houtteman_formes", r"(?<!\w)(?:Houthouan|Houtteman)(?!\w)", "lexical"),
}

_CONFIDENCES = {"textual", "lexical", "uncertain"}
_KINDS = {"textual", "thematic", "material", "chronology"}


def _escape_tex(text: str) -> str:
    table = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(table.get(ch, ch) for ch in text)


def _normalise_entities(entities: Iterable) -> list[dict]:
    result = []
    seen = set()
    for raw in entities:
        if isinstance(raw, dict):
            entity = dict(raw)
            entity_id = entity.get("id", entity.get("entity"))
            pattern = entity.get("pattern")
            if not entity_id or not pattern:
                raise ValueError("Entité sans identifiant ou motif de recherche.")
            kind = entity.get("kind", "textual")
            confidence = entity.get("confidence", "textual")
        else:
            if len(raw) < 2:
                raise ValueError("Entité héritée incomplète.")
            entity_id, pattern = raw[:2]
            kind, confidence = "textual", "textual"
        if entity_id in {"forage", "bois_ribeaucourt", "solde_84", "solde_78_75", "cooking", "hair_cut"}:
            kind = "thematic"
        if entity_id in SAFE_OVERRIDES:
            entity_id, pattern, confidence = SAFE_OVERRIDES[entity_id]
        if entity_id in seen:
            raise ValueError(f"Entité répétée : {entity_id}.")
        if kind not in _KINDS - {"material", "chronology"} or confidence not in _CONFIDENCES - {"uncertain"}:
            raise ValueError(f"Type d'entité invalide : {entity_id}.")
        result.append({"id": entity_id, "pattern": pattern, "regex": re.compile(pattern), "kind": kind, "confidence": confidence})
        seen.add(entity_id)
    # Les compléments ne remplacent aucune définition fournie explicitement.
    for extra in THEMATIC_ENTITIES:
        if extra["id"] not in seen:
            result.append({**extra, "regex": re.compile(extra["pattern"]), "confidence": "textual"})
            seen.add(extra["id"])
    return result


def _question_ranges(text: str) -> list[tuple[int, int]]:
    """Crochets intérieurs seulement : le doute sur R.E. n'affecte pas Hair cut."""
    stack = []
    brackets = []
    for i, char in enumerate(text):
        if char == "[":
            stack.append(i)
        elif char == "]" and stack:
            start = stack.pop()
            brackets.append((start, i + 1))
    return [(a, b) for a, b in brackets if "?" in text[a:b] and not any(a < c < d < b and "?" in text[c:d] for c, d in brackets)]


def _is_cancelled(text: str, start: int, end: int) -> bool:
    for match in re.finditer(r"⟦[^⟧]*⟧", text):
        if match.start() <= start < end <= match.end():
            return True
    return False


def _is_uncertain(text: str, start: int, end: int) -> bool:
    if any(a <= start < end <= b for a, b in _question_ranges(text)):
        return True
    # Certains états diplomatiques placent le doute après le nom : « Bertin [?] ».
    return bool(re.match(r"\s*\[\s*\?\s*\]", text[end:]))


def collect_verified_occurrences(records: list[dict], entities: Iterable) -> list[dict]:
    """Retourne toutes les occurrences exactes, sans titres ni lieux éditoriaux.

    Le champ ``entity`` désigne un regroupement du catalogue, pas une preuve
    historique d'identité. ``confidence=lexical`` interdit cette assimilation.
    """
    definitions = _normalise_entities(entities)
    occurrences = []
    for record in records:
        n = record["scan_num"]
        for line_number, text in enumerate(record["lines"], 1):
            for entity in definitions:
                for match in entity["regex"].finditer(text):
                    if "\\hfill" in match.group(0):
                        continue
                    uncertainty = _is_uncertain(text, match.start(), match.end())
                    occurrences.append({
                        "entity": entity["id"], "kind": entity["kind"],
                        "scan_num": n, "line": line_number, "lemma": match.group(0),
                        "start": match.start(), "end": match.end(),
                        "confidence": "uncertain" if uncertainty else entity["confidence"],
                        "attestation": "autograph_text",
                        "cancelled": _is_cancelled(text, match.start(), match.end()),
                    })
    return occurrences


def _anchor(occurrence: dict) -> dict:
    return {key: occurrence[key] for key in ("scan_num", "line", "lemma", "start", "end", "confidence", "attestation", "cancelled")}


def _logical_page(scan_num: int) -> int:
    # Une même page est photographiée deux fois ; les deux vues restent citables.
    return 91 if scan_num == 93 else scan_num


def _nearest_targets(source: dict, occurrences: list[dict]) -> list[dict]:
    alternatives = [o for o in occurrences if _logical_page(o["scan_num"]) != _logical_page(source["scan_num"])]
    first_per_page = {}
    for occurrence in sorted(alternatives, key=lambda o: (o["scan_num"], o["line"], o["start"])):
        first_per_page.setdefault(_logical_page(occurrence["scan_num"]), occurrence)
    before = [o for o in first_per_page.values() if o["scan_num"] < source["scan_num"]]
    after = [o for o in first_per_page.values() if o["scan_num"] > source["scan_num"]]
    chosen = []
    if before:
        chosen.append(max(before, key=lambda o: o["scan_num"]))
    if after:
        chosen.append(min(after, key=lambda o: o["scan_num"]))
    if len(chosen) == 1:
        remaining = [o for o in first_per_page.values() if o not in chosen]
        if remaining:
            chosen.append(min(remaining, key=lambda o: abs(o["scan_num"] - source["scan_num"])))
    targets = []
    for occurrence in sorted(chosen, key=lambda o: o["scan_num"]):
        targets.append({**_anchor(occurrence), "entity": occurrence["entity"], "direction": "supra" if occurrence["scan_num"] < source["scan_num"] else "infra"})
    return targets


def _find_anchor(records_by_num: dict, scan_num: int, line_number: int, lemma: str) -> dict | None:
    record = records_by_num.get(scan_num)
    if record is None or not 1 <= line_number <= len(record["lines"]):
        return None
    text = record["lines"][line_number - 1]
    start = text.find(lemma)
    if start < 0:
        return None
    return {"scan_num": scan_num, "line": line_number, "lemma": lemma, "start": start, "end": start + len(lemma), "confidence": "uncertain" if _is_uncertain(text, start, start + len(lemma)) else "textual", "attestation": "autograph_text", "cancelled": _is_cancelled(text, start, start + len(lemma))}


def _manual_entry(records_by_num: dict, source_spec: tuple, target_spec: tuple, entity: str, kind: str, annotation: str) -> dict | None:
    source = _find_anchor(records_by_num, *source_spec)
    target = _find_anchor(records_by_num, *target_spec)
    if source is None or target is None:
        return None
    target.update({"entity": entity, "direction": "supra" if target["scan_num"] < source["scan_num"] else "infra"})
    return {"entity": entity, "kind": kind, "source": source, "targets": [target], "confidence": "textual", "annotation": annotation, "selection": "manual_relation_with_exact_anchors"}


def _special_entries(records_by_num: dict) -> dict[int, list[dict]]:
    entries = defaultdict(list)
    # Le lemme est un vrai passage commun, la nature du doublon est une note.
    for source, target in ((91, 93), (93, 91)):
        entry = _manual_entry(records_by_num, (source, 1, "Après le dîner"), (target, 1, "Après le dîner"), "duplicate_page_091_093", "material", "eadem pagina bis photographata")
        if entry:
            entries[source].append(entry)
    # Les dates sont celles des lignes réellement conservées dans chaque vue.
    for source, target in (((63, 1, "Jeudi 5"), (64, 2, "Mer. 4 Oct 16")), ((64, 2, "Mer. 4 Oct 16"), (63, 1, "Jeudi 5")), ((112, 1, "22 Ven."), (113, 1, "19 Ma.")), ((113, 1, "19 Ma."), (112, 1, "22 Ven."))):
        entry = _manual_entry(records_by_num, source, target, "chronology_photographic_order", "chronology", "de ordine chronologico")
        if entry:
            entries[source[0]].append(entry)
    for source, target, label in (((1, 3, "25 juillet 1916"), (2, 1, "25 Ma."), "terminus a quo"), ((1, 4, "30 avril 1917"), (186, 1, "30 Lundi."), "terminus ad quem")):
        entry = _manual_entry(records_by_num, source, target, "cover_date_limits", "chronology", label)
        if entry:
            entries[source[0]].append(entry)
    return entries


def _validate_anchor(anchor: dict, records_by_num: dict, label: str) -> None:
    n = anchor.get("scan_num")
    line = anchor.get("line")
    lemma = anchor.get("lemma")
    if type(n) is not int or n not in records_by_num or type(line) is not int or not 1 <= line <= len(records_by_num[n]["lines"]):
        raise ValueError(f"{label} : numéro de vue ou de ligne invalide.")
    if not isinstance(lemma, str) or not lemma or lemma not in records_by_num[n]["lines"][line - 1]:
        raise ValueError(f"{label} : lemme absent de la vue {n:03d}, ligne {line}.")
    a, b = anchor.get("start"), anchor.get("end")
    text = records_by_num[n]["lines"][line - 1]
    if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(text) or text[a:b] != lemma:
        raise ValueError(f"{label} : offsets inexacts pour {n:03d}, ligne {line}.")
    if anchor.get("confidence") not in _CONFIDENCES or anchor.get("attestation") != "autograph_text":
        raise ValueError(f"{label} : statut d'attestation absent ou invalide.")
    a = anchor.get("start", records_by_num[n]["lines"][line - 1].find(lemma))
    b = anchor.get("end", a + len(lemma))
    if anchor.get("cancelled") is not _is_cancelled(records_by_num[n]["lines"][line - 1], a, b):
        raise ValueError(f"{label} : statut de rature perdu pour {n:03d}, ligne {line}.")
    if _is_uncertain(records_by_num[n]["lines"][line - 1], a, b) and anchor["confidence"] != "uncertain":
        raise ValueError(f"{label} : doute autographe ou éditorial effacé pour {n:03d}, ligne {line}.")


def validate_loci_entries(records: list[dict], entries_by_scan: dict[int, list[dict]] | None = None) -> dict[str, int]:
    """Validation pure des ancrages et directions ; lève ValueError au défaut.

    Le contrôle ne prouve pas une identité historique : il empêche qu'un titre,
    un lieu éditorial ou un lemme normalisé se substitue à une attestation.
    """
    records_by_num = {r["scan_num"]: r for r in records}
    if len(records_by_num) != len(records):
        raise ValueError("Numéros de vues répétés.")
    entries_by_scan = entries_by_scan if entries_by_scan is not None else {r["scan_num"]: r.get("loci_entries", []) for r in records}
    if set(entries_by_scan) != set(records_by_num):
        raise ValueError("Couverture des vues incomplète pour les loci.")
    total = targets_total = 0
    for n, entries in entries_by_scan.items():
        if not isinstance(entries, list) or len(entries) > 3:
            raise ValueError(f"Vue {n:03d} : liste de loci invalide ou trop longue.")
        seen = set()
        for entry in entries:
            total += 1
            if entry.get("kind") not in _KINDS or not isinstance(entry.get("entity"), str) or not entry["entity"]:
                raise ValueError(f"Vue {n:03d} : type ou entité invalide.")
            _validate_anchor(entry.get("source", {}), records_by_num, "Source")
            if entry["source"]["scan_num"] != n:
                raise ValueError(f"Vue {n:03d} : source ancrée sur une autre vue.")
            if entry.get("confidence") not in _CONFIDENCES or not entry.get("targets"):
                raise ValueError(f"Vue {n:03d} : statut ou cibles absents.")
            key = (entry["entity"], entry["source"]["line"], entry["source"]["lemma"])
            if key in seen:
                raise ValueError(f"Vue {n:03d} : locus répété.")
            seen.add(key)
            has_uncertain_anchor = entry["source"]["confidence"] == "uncertain"
            target_keys = set()
            for target in entry["targets"]:
                targets_total += 1
                _validate_anchor(target, records_by_num, "Cible")
                s = target["scan_num"]
                if s == n or target.get("direction") != ("supra" if s < n else "infra"):
                    raise ValueError(f"Vue {n:03d} : direction du renvoi {s:03d} incorrecte.")
                if target.get("entity") != entry["entity"]:
                    raise ValueError(f"Vue {n:03d} : cible d'une autre entité.")
                if entry["kind"] not in {"material", "chronology"} and _logical_page(s) == _logical_page(n):
                    raise ValueError(f"Vue {n:03d} : le doublon photographique n'est pas un second témoin textuel.")
                target_key = (s, target["line"], target["lemma"])
                if target_key in target_keys:
                    raise ValueError(f"Vue {n:03d} : cible répétée.")
                target_keys.add(target_key)
                has_uncertain_anchor |= target["confidence"] == "uncertain"
            if has_uncertain_anchor and entry["confidence"] != "uncertain":
                raise ValueError(f"Vue {n:03d} : réserve perdue dans le rapprochement.")
    return {"scans": len(records), "entries": total, "targets": targets_total}


def _render_entry(entry: dict, reference_fn: Callable[[int], str]) -> str:
    source = entry["source"]
    head = f"\\textbf{{{source['line']}}} (\\textit{{{_escape_tex(source['lemma'])}}})"
    tags = []
    if source.get("cancelled"):
        tags.append("verba deleta")
    if entry.get("annotation"):
        tags.append(entry["annotation"])
    if entry["kind"] == "thematic":
        tags.append("de eadem re")
    if entry["confidence"] == "uncertain":
        tags.extend(("similitudo lectionis", "incertitudo nominis"))
    elif entry["confidence"] == "lexical":
        tags.append("similitudo lectionis")
    groups = []
    for direction in ("supra", "infra"):
        references = []
        for target in entry["targets"]:
            if target["direction"] != direction:
                continue
            deleted = ", del." if target.get("cancelled") else ""
            references.append(f"{reference_fn(target['scan_num'])}, l.~{target['line']} (\\textit{{{_escape_tex(target['lemma'])}}}){deleted}")
        if references:
            groups.append(direction + " " + "; ".join(references))
    annotation = " " + ", ".join(tags) if tags else ""
    return head + annotation + " cf. " + "; ".join(groups) + "."


def build_verified_loci(records: list[dict], entities: Iterable, reference_fn: Callable[[int], str]) -> dict[int, str]:
    """Construit trois rapprochements choisis au plus, avec données contrôlables.

    Les relations matérielles et chronologiques documentées ont priorité.
    Les entités nommées suivent l'ordre des lignes. Les motifs thématiques
    complètent uniquement les vues sans autre parallèle textuel disponible.
    Une page sans attestation commune reçoit une déclaration d'absence.
    """
    records_by_num = {r["scan_num"]: r for r in records}
    if len(records_by_num) != len(records):
        raise ValueError("Numéros de vues répétés.")
    occurrences = collect_verified_occurrences(records, entities)
    by_entity = defaultdict(list)
    by_scan = defaultdict(list)
    for occurrence in occurrences:
        by_entity[occurrence["entity"]].append(occurrence)
        by_scan[occurrence["scan_num"]].append(occurrence)
    specials = _special_entries(records_by_num)
    entries_by_scan = {}
    for n in records_by_num:
        entries = list(specials.get(n, []))
        candidates = []
        seen = set()
        for occurrence in sorted(by_scan[n], key=lambda o: (o["line"], o["start"], o["entity"])):
            if occurrence["entity"] in seen:
                continue
            seen.add(occurrence["entity"])
            targets = _nearest_targets(occurrence, by_entity[occurrence["entity"]])
            if not targets:
                continue
            confidence = occurrence["confidence"]
            if any(target["confidence"] == "uncertain" for target in targets):
                confidence = "uncertain"
            elif confidence != "uncertain" and any(target["confidence"] == "lexical" for target in targets):
                confidence = "lexical"
            candidates.append({"entity": occurrence["entity"], "kind": occurrence["kind"], "source": _anchor(occurrence), "targets": targets, "confidence": confidence, "selection": "exact_autograph_anchors"})
        textual = [entry for entry in candidates if entry["kind"] == "textual"]
        thematic = [entry for entry in candidates if entry["kind"] == "thematic"]
        chosen = textual if textual else thematic
        entries.extend(chosen[:max(0, 3 - len(entries))])
        entries_by_scan[n] = entries
    validate_loci_entries(records, entries_by_scan)
    result = {}
    for record in records:
        n = record["scan_num"]
        record["loci_entries"] = entries_by_scan[n]
        result[n] = " — ".join(_render_entry(entry, reference_fn) for entry in entries_by_scan[n]) or "Nullus locus parallelus certus repertus."
    return result
