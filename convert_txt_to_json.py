#!/usr/bin/env python3
from __future__ import annotations
import re, json, argparse, sys, pathlib, textwrap
from dataclasses import dataclass

QUESTION_BLOCK_SEP = re.compile(r'^---\s*$', re.MULTILINE)
QUESTION_HEADER_LINE_RE = re.compile(r"^\s*\d+\.\s*Proverbio\s+([^:]+):\s*$", re.IGNORECASE)
ANSWER_RE = re.compile(r'^([A-D])\)\s*(.+)$')
CORRECT_MARK_RE = re.compile(r'(?:\s|\t|\u00A0)*✓\s*$')
WHITESPACE_RE = re.compile(r'\s+')
APOSTROPHE_VARIANTS = {
    '\u2019': "'",
    '\u2018': "'",
    '\u0060': "'",
    '\u00B4': "'",
}

@dataclass
class ParsedQuestion:
    region: str
    proverb: str
    answers: list
    correct_indices: list
    raw_question_text: str

    def to_json_dict(self):
        return {
            'question': f"Proverbio {self.region}: \n'{self.proverb}' \nCosa significa?",
            'answers': [
                { 'text': a['text'], 'correct': (i in self.correct_indices) }
                for i, a in enumerate(self.answers)
            ]
        }

def normalize_text(s: str) -> str:
    for k,v in APOSTROPHE_VARIANTS.items():
        s = s.replace(k,v)
    s = s.replace('\r','')
    # Normalizza spazi multipli (non dentro il proverbio originale, ma testo esterno)
    return s.strip()

def parse_section(section: str, idx_hint: int):
    original = section
    section_clean = section.replace('\r','')
    lines = [l.rstrip() for l in section_clean.split('\n')]
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return None, 'empty'

    region = None
    proverb = None
    answers_start_idx = None
    i = 0
    header_idx = None
    for j, l in enumerate(lines):
        if QUESTION_HEADER_LINE_RE.match(l):
            header_idx = j
            break
        if l.strip().startswith('---'):
            break
    if header_idx is None:
        return None, 'no_header_match'
    m = QUESTION_HEADER_LINE_RE.match(lines[header_idx])
    region = m.group(1).strip()
    i = header_idx + 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return None, 'missing_proverb_line'
    proverb_line = lines[i].strip()
    i += 1
    # Rimuovi apici/virgolette esterne se presenti
    proverb_line = proverb_line.strip("'\"“”‘’ ")
    proverb = normalize_text(proverb_line)
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return None, 'missing_question_line'
    if 'cosa significa' not in lines[i].lower():
        return None, 'missing_cosa_significa'
    i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    answers = []
    correct_indices = []
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        if line.startswith('---'):
            break
        m = ANSWER_RE.match(line)
        if not m:
            continue
        letter, text = m.groups()
        is_correct = False
        if CORRECT_MARK_RE.search(text):
            is_correct = True
            text = CORRECT_MARK_RE.sub('', text).rstrip()
        text = normalize_text(text)
        if not text:
            return None, f'empty_answer_{letter}'
        answers.append({'letter': letter, 'text': text})
        if is_correct:
            correct_indices.append(len(answers)-1)
        if len(answers) == 4:
            break

    if len(answers) != 4:
        return None, f'answers_count_{len(answers)}'
    if len(correct_indices) != 1:
        return None, f'correct_count_{len(correct_indices)}'

    pq = ParsedQuestion(region=region, proverb=proverb, answers=answers, correct_indices=correct_indices, raw_question_text=original)
    return pq, None

def convert(txt_path: pathlib.Path, json_path: pathlib.Path, dry_run: bool=False):
    content = txt_path.read_text(encoding='utf-8')
    # Split sections on --- (keep structure loose)
    raw_sections = re.split(r'\n-{3,}\n', content)
    parsed = []
    errors = []
    total_candidates = 0

    for i, sec in enumerate(raw_sections):
        sec_norm = sec.strip()
        if not sec_norm:
            continue
        # Heuristic skip header & legenda
        if (('QUIZ PROVERBI' in sec_norm and 'Proverbio' not in sec_norm) or
            sec_norm.startswith('LEGENDA:')):
            continue
        total_candidates += 1
        q, err = parse_section(sec, i+1)
        if q:
            parsed.append(q)
        else:
            errors.append((i+1, err, sec_norm[:120].replace('\n',' ')))

    if dry_run:
        print('\n=== DRY RUN REPORT ===')
        print(f'Candidati analizzati: {total_candidates}')
        print(f'Domande valide: {len(parsed)}')
        print(f'Domande scartate: {len(errors)}')
        if errors:
            print('\nDettagli scarti:')
            for idx, err, preview in errors[:30]:
                print(f' - Sezione {idx}: {err} :: {preview}')
        if errors and len(errors) > 30:
            print(f' ... ({len(errors)-30} ulteriori)')
        return 0 if parsed else 1

    # Scrittura JSON
    data_out = [p.to_json_dict() for p in parsed]
    json_path.write_text(json.dumps(data_out, ensure_ascii=False, indent=4), encoding='utf-8')
    print(f'✅ Generato {json_path} con {len(parsed)} domande valide (scartate {len(errors)}).')
    if errors:
        print('⚠️  Domande scartate:')
        for idx, err, preview in errors[:20]:
            print(f' - Sezione {idx}: {err} :: {preview}')
        if len(errors) > 20:
            print(f' ... ({len(errors)-20} ulteriori)')
    return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', '-i', default='ELENCO_DOMANDE_QUIZ_V2.txt')
    ap.add_argument('--output', '-o', default='questions.json')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    inp = pathlib.Path(args.input)
    if not inp.exists():
        print(f'File input non trovato: {inp}')
        sys.exit(1)
    outp = pathlib.Path(args.output)
    code = convert(inp, outp, dry_run=args.dry_run)
    sys.exit(code)

if __name__ == '__main__':
    main()
