"""Keep index attestations distinct from identifications in printed commentary."""
from __future__ import annotations
import re
from loci_verifies import _is_uncertain, _is_cancelled


def _identity_context(headword, lemma, scan_num, explicit, text, start):
    # Bare kinship terms and first names cannot establish a particular family.
    if headword == 'Maria':
        return scan_num == 64
    if headword.startswith('Combes, Maria'):
        return scan_num in (132, 141)
    if headword.startswith('Vincens,') and lemma in ('Fernand', 'Robert'):
        return scan_num in explicit
    if headword == 'Marie':
        return scan_num == 140 and not (start and text[start-1] == '-') and not text[start+len(lemma):].startswith('-')
    if headword.startswith('Crouzet, Émile') and lemma in ('Oncle', 'Tante'):
        return False
    if headword.startswith('Crouzet, Abbé Jean') and lemma == 'Jean':
        return scan_num in explicit
    if headword.startswith('Calmels, Pierre') and lemma == 'Pierre':
        return scan_num in explicit
    if headword.startswith('Faure,') and lemma in ('Marcel', 'André', 'Germaine'):
        return scan_num in explicit
    if headword.startswith('Huguet,') and not lemma.startswith('Huguet'):
        return False
    if headword.startswith('Combes, Marie Lucien') and re.search(r'St\.?\s*$', text[:start]):
        return False
    return True



def _document_identity_rule(headword, pattern):
    """A documentary match must identify the indexed person, not a namesake.

    Family diagrams contain several Jean, Pierre, Madeleine and Marie. Bare
    forenames and a household servant's name do not establish a documentary
    identity. The reference remains an editorial/documentary attestation.
    """
    if headword in ('Maria', 'Marie'):
        return frozenset(), None
    full_names = (
        ('Combes, Françoise', r'(?<!\w)Françoise\s+Combes(?!\w)'),
        ('Combes, Maria', r'(?<!\w)Maria\s+Combes(?!\w)'),
        ('Combes, Marie Lucien', r'(?<!\w)Marie\s+Lucien\s+Hippolyte\s+Combes(?!\w)'),
        ('Calmels, Madeleine', r'(?<!\w)Madeleine\s+Calmels(?!\w)'),
        ('Calmels, Pierre', r'(?<!\w)Pierre\s+Calmels(?!\w)'),
        ('Crouzet, Abbé Jean', r'(?<!\w)Jean\s+Crouzet(?!\w)'),
        ('Crouzet, Émile', r'(?<!\w)Émile\s+Crouzet(?!\w)'),
    )
    for prefix, complete_name in full_names:
        if headword.startswith(prefix):
            return None, complete_name
    if headword.startswith('Vincens,'):
        # P. Vincens in the Combes descent is another person. The shared
        # forename Germaine also occurs in the Faure branch of the same tree.
        return frozenset({'genealogie_calmels'}), r'(?<!\w)Fernand\s+Vincens(?!\w)'
    if headword.startswith('Faure,'):
        # The family surname is needed; Marcel or André alone are insufficient.
        return None, r'(?<!\w)Faure(?!\w)'
    return None, pattern


def _printed_document(source):
    """Offsets refer to this exact text, with LaTeX comments removed."""
    return re.sub(r'(?<!\\)%[^\n]*', '', source['text'])


def _document_matches(headword, pattern, source):
    allowed_ids, document_pattern = _document_identity_rule(headword, pattern)
    if document_pattern is None or allowed_ids is not None and source['id'] not in allowed_ids:
        return []
    return list(re.finditer(document_pattern, _printed_document(source)))


def collect_index_entries(records, catalog, kind, document_sources=()):
    """Return exact occurrences. Explicit scan lists alone never create a hit."""
    result = []
    for headword, description, pattern, explicit in catalog:
        if headword.startswith("Combes, Maria"):
            pattern = r"\bMaria\b"
        expression = re.compile(pattern)
        direct, commentary = [], []
        for record in records:
            n = record['scan_num']
            for field, texts in [('lines', record['lines']), ('critique', [record.get('critique', '')]), ('historique', [record.get('historique', '')])]:
                for line, text in enumerate(texts, 1):
                    for match in expression.finditer(text):
                        if not _identity_context(headword, match.group(), n, explicit, text, match.start()):
                            continue
                        occurrence = {'scan_num': n, 'field': field, 'line': line if field == 'lines' else None,
                                      'lemma': match.group(), 'start': match.start(), 'end': match.end(),
                                      'uncertain': _is_uncertain(text, match.start(), match.end()),
                                      'cancelled': _is_cancelled(text, match.start(), match.end())}
                        (direct if field == 'lines' else commentary).append(occurrence)
        documents = []
        for source in document_sources:
            matches = _document_matches(headword, pattern, source)
            if matches:
                match = matches[0]
                documents.append({'source_id': source['id'], 'lemma': match.group(),
                                  'start': match.start(), 'end': match.end(),
                                  'reference': source['reference']})
        result.append({'kind': kind, 'headword': headword, 'description': description,
                       'pattern': pattern, 'explicit_scans': list(explicit),
                       'direct': direct, 'commentary': commentary, 'documents': documents})
    return result


def validate_index_entries(records, entries, document_sources=()):
    """Validate exact anchors, documentary identities and preserved reserves."""
    by_num = {r['scan_num']: r for r in records}
    if len(by_num) != len(records):
        raise ValueError('Index : numéros de vues répétés.')
    sources = {s['id']: s for s in document_sources}
    if len(sources) != len(document_sources):
        raise ValueError('Index : identifiants documentaires répétés.')
    total = 0
    for entry in entries:
        headword = entry.get('headword')
        pattern = entry.get('pattern')
        explicit = entry.get('explicit_scans')
        if not isinstance(headword, str) or not headword or not isinstance(pattern, str) or not isinstance(explicit, list):
            raise ValueError('Index : règle d’identité absente.')
        expression = re.compile(pattern)
        for mention in entry.get('documents', []):
            if mention.get('source_id') not in sources:
                raise ValueError('Index : source documentaire absente.')
            source = sources[mention['source_id']]
            printed = _printed_document(source)
            a, b = mention.get('start'), mention.get('end')
            lemma = mention.get('lemma')
            if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(printed) or not isinstance(lemma, str) or not lemma or printed[a:b] != lemma:
                raise ValueError('Index : position documentaire ou lemme non attesté.')
            if mention.get('reference') != source['reference']:
                raise ValueError('Index : référence documentaire différente de sa source.')
            if not any(m.start() == a and m.end() == b for m in _document_matches(headword, pattern, source)):
                raise ValueError('Index : identité documentaire non établie pour cette vedette.')
        for group in ('direct', 'commentary'):
            for occurrence in entry[group]:
                n = occurrence.get('scan_num')
                if type(n) is not int or n not in by_num:
                    raise ValueError('Index : vue source absente.')
                record = by_num[n]
                field = occurrence.get('field')
                if group == 'direct' and field != 'lines' or group == 'commentary' and field not in ('critique', 'historique'):
                    raise ValueError('Index : nature de l’attestation incorrecte.')
                if field == 'lines' and (type(occurrence.get('line')) is not int or not 1 <= occurrence['line'] <= len(record['lines'])):
                    raise ValueError('Index : ligne hors texte.')
                if field != 'lines' and occurrence.get('line') is not None:
                    raise ValueError('Index : ligne de commentaire indûment numérotée.')
                text = record['lines'][occurrence['line']-1] if field == 'lines' else record[field]
                a, b = occurrence.get('start'), occurrence.get('end')
                lemma = occurrence.get('lemma')
                if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(text) or not isinstance(lemma, str) or not lemma or text[a:b] != lemma:
                    raise ValueError('Index : lemme ou position absent de son texte.')
                if not any(m.start() == a and m.end() == b for m in expression.finditer(text)) or not _identity_context(headword, lemma, n, explicit, text, a):
                    raise ValueError('Index : identité textuelle non établie pour cette vedette.')
                if type(occurrence.get('uncertain')) is not bool or type(occurrence.get('cancelled')) is not bool or occurrence['uncertain'] != _is_uncertain(text, a, b) or occurrence['cancelled'] != _is_cancelled(text, a, b):
                    raise ValueError('Index : réserve ou rature effacée.')
                total += 1
    return total


def index_reference_text(entry, reference_fn):
    """A numeral with (?) marks a doubtful name; comm. is a separate register."""
    def group_refs(occurrences):
        first = {}
        for o in occurrences:
            first.setdefault(o['scan_num'], []).append(o)
        refs = []
        for n, row in sorted(first.items()):
            # A secure non-deleted occurrence on the page supports a secure ref.
            secure = any(not o['uncertain'] and not o['cancelled'] for o in row)
            suffix = '' if secure else r' \textit{(lect. inc.)}' if any(o['uncertain'] for o in row) else r' \textit{(del.)}'
            refs.append(reference_fn(n) + suffix)
        return refs
    direct = group_refs(entry['direct'])
    direct_ids = {o['scan_num'] for o in entry['direct']}
    comments = group_refs([o for o in entry['commentary'] if o['scan_num'] not in direct_ids])
    pieces = []
    if direct:
        pieces.append(', '.join(direct))
    if comments:
        pieces.append(r'\textit{Comm. :} ' + ', '.join(comments))
    if entry.get('documents'):
        pieces.append(' ; '.join(d['reference'] for d in entry['documents']))
    return ' ; '.join(pieces)
