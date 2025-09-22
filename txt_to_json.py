#!/usr/bin/env python3
"""
Convertitore TXT → JSON per Quiz Proverbi Dialettali
Legge il file ELENCO_DOMANDE_QUIZ_V2.txt e genera questions.json
"""

import json
import re
import sys

def parse_txt_to_json(txt_file, json_file):
    """Converte il file TXT in formato JSON"""
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Dividi le domande usando i separatori ---
        sections = content.split('---')
        questions = []
        
        for section in sections:
            section = section.strip()
            
            # Salta sezioni vuote, istruzioni o che contengono solo "?"
            if not section or 'FORMATO PER' in section or 'ISTRUZIONI:' in section or section == '?':
                continue
            
            # Pattern per estrarre la domanda
            question_match = re.search(r'(\d+)\.\s*Proverbio\s+([^:]+):\s*\n\'([^\']+)\'\s*\nCosa significa\?', section)
            
            if not question_match:
                continue
            
            number = question_match.group(1)
            region = question_match.group(2).strip()
            proverb = question_match.group(3).strip()
            
            # Costruisci la domanda completa
            question_text = f"Proverbio {region}: \n'{proverb}' \nCosa significa?"
            
            # Estrai le risposte
            answers = []
            answer_pattern = r'([A-D])\)\s*([^✓\n]+)(\s*✓)?'
            answer_matches = re.findall(answer_pattern, section)
            
            for letter, text, is_correct in answer_matches:
                answers.append({
                    "text": text.strip(),
                    "correct": bool(is_correct.strip())
                })
            
            # Aggiungi solo se ci sono esattamente 4 risposte
            if len(answers) == 4:
                questions.append({
                    "question": question_text,
                    "answers": answers
                })
                print(f"✅ Domanda {number} aggiunta: {region}")
            else:
                print(f"⚠️  Domanda {number} saltata: trovate {len(answers)} risposte invece di 4")
        
        # Salva il JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=4)
        
        print(f"\n🎯 Conversione completata!")
        print(f"📄 File creato: {json_file}")
        print(f"📊 Domande convertite: {len(questions)}")
        
        return len(questions)
        
    except Exception as e:
        print(f"❌ Errore durante la conversione: {e}")
        return 0

def main():
    txt_file = "ELENCO_DOMANDE_QUIZ_V2.txt"
    json_file = "questions.json"
    
    print("🔄 Conversione TXT → JSON")
    print(f"📖 Leggo: {txt_file}")
    print(f"💾 Scrivo: {json_file}")
    print("-" * 50)
    
    count = parse_txt_to_json(txt_file, json_file)
    
    if count > 0:
        print(f"\n✅ Successo! {count} domande convertite.")
        print("🌐 Ora puoi testare il quiz aggiornato!")
    else:
        print("\n❌ Nessuna domanda convertita. Controlla il formato del file TXT.")

if __name__ == "__main__":
    main()