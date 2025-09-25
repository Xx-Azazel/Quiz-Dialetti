#!/usr/bin/env python3
import json, re, sys, pathlib, textwrap

PLACEHOLDER_RE = re.compile(r"^(\*+|\?+)$")

MAX_QUESTION_LEN = 300
MAX_ANSWER_LEN = 160


def load_dataset(path: pathlib.Path):
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, list):
            raise ValueError('Il file JSON deve essere una lista di domande')
        return data
    except Exception as e:
        print(f"❌ Errore caricamento dataset: {e}")
        sys.exit(1)


def validate_question(q, idx):
    errors = []
    context = f"[Domanda {idx+1}]"
    if 'question' not in q:
        errors.append(f"{context} campo 'question' mancante")
        return errors
    question_text = str(q['question']).strip()
    if not question_text:
        errors.append(f"{context} testo domanda vuoto")
    if len(question_text) > MAX_QUESTION_LEN:
        errors.append(f"{context} testo domanda troppo lungo ({len(question_text)} > {MAX_QUESTION_LEN})")
    answers = q.get('answers')
    if not isinstance(answers, list):
        errors.append(f"{context} 'answers' non è una lista")
        return errors
    if len(answers) != 4:
        errors.append(f"{context} numero risposte != 4 (trovate {len(answers)})")
    correct_flags = 0
    for i, a in enumerate(answers):
        prefix = f"{context} risposta {i+1}"
        if not isinstance(a, dict):
            errors.append(f"{prefix}: non è un oggetto JSON")
            continue
        txt = str(a.get('text', '')).strip()
        if not txt:
            errors.append(f"{prefix}: testo vuoto")
        if PLACEHOLDER_RE.match(txt):
            errors.append(f"{prefix}: placeholder non ammesso ('{txt}')")
        if len(txt) > MAX_ANSWER_LEN:
            errors.append(f"{prefix}: troppo lunga ({len(txt)} > {MAX_ANSWER_LEN})")
        if a.get('correct') is True:
            correct_flags += 1
    if correct_flags != 1:
        errors.append(f"{context} numero risposte corrette != 1 (trovate {correct_flags})")
    return errors


def main():
    path = pathlib.Path('questions.json')
    if not path.exists():
        print('❌ File questions.json non trovato')
        sys.exit(1)
    data = load_dataset(path)
    all_errors = []
    for idx, q in enumerate(data):
        all_errors.extend(validate_question(q, idx))
    if all_errors:
        print('❌ Dataset NON valido:')
        for e in all_errors:
            print('-', e)
        print(f"Totale errori: {len(all_errors)}")
        sys.exit(1)
    print(f"✅ Dataset valido. Domande: {len(data)}")

if __name__ == '__main__':
    main()
