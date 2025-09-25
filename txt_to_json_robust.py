#!/usr/bin/env python3

import json
import re
import sys

def parse_txt_to_json_robust(txt_file, json_file):
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = content.split('---')
        questions = []
        question_number = 1
        
        for section in sections:
            section = section.strip()
            
            if (not section or 
                'QUIZ PROVERBI' in section or 
                'LEGENDA:' in section or 
                'FORMATO PER' in section or 
                'ISTRUZIONI:' in section or
                len(section) < 50):
                continue
            
            question_match = re.search(r'\d+\.\s*Proverbio\s+([^:]+):\s*\n\'([^\']+)\'\s*\nCosa significa\?', section)
            
            if not question_match:
                print(f"⚠️  Sezione saltata: formato non riconosciuto")
                continue
            
            region = question_match.group(1).strip()
            proverb = question_match.group(2).strip()
            
            question_text = f"Proverbio {region}: \n'{proverb}' \nCosa significa?"
            
            answers = []
            answer_pattern = r'([A-D])\)\s*([^✓\n]+)(\s*✓)?'
            answer_matches = re.findall(answer_pattern, section)
            
            for letter, text, is_correct in answer_matches:
                answer_text = text.strip()
                # Accetta qualsiasi testo, inclusi i placeholder "?"
                if answer_text:
                    answers.append({
                        "text": answer_text,
                        "correct": bool(is_correct.strip())
                    })
            
            if len(answers) == 4:
                questions.append({
                    "question": question_text,
                    "answers": answers
                })
                print(f"✅ Domanda {question_number} aggiunta: {region}")
                question_number += 1
            else:
                print(f"⚠️  Domanda saltata ({region}): trovate {len(answers)} risposte invece di 4")
        
        # Salva il JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=4)
        
        print(f"\n🎯 Conversione completata!")
        print(f"📄 File creato: {json_file}")
        print(f"📊 Domande convertite: {len(questions)}")
        
        return len(questions)
        
    except Exception as e:
        print(f"❌ Errore durante la conversione: {e}")
        import traceback
        traceback.print_exc()
        return 0

def main():
    txt_file = "ELENCO_DOMANDE_QUIZ_V2.txt"
    json_file = "questions.json"
    
    print("🔄 Conversione TXT → JSON (VERSIONE ROBUSTA)")
    print(f"📖 Leggo: {txt_file}")
    print(f"💾 Scrivo: {json_file}")
    print("-" * 50)
    
    count = parse_txt_to_json_robust(txt_file, json_file)
    
    if count > 0:
        print(f"\n✅ Successo! {count} domande convertite.")
        print("🌐 Ora puoi testare il quiz aggiornato!")
    else:
        print("\n❌ Nessuna domanda convertita. Controlla il formato del file TXT.")

if __name__ == "__main__":
    main()