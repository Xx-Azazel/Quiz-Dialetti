#!/usr/bin/env python3

import json
import re

def parse_json_to_txt(json_file, txt_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        
        content = []
        content.append("QUIZ PROVERBI DIALETTALI ITALIANI - VERSIONE EDITABILE V2")
        content.append("=" * 60)
        content.append("")
        
        for i, question_data in enumerate(questions, 1):
            question = question_data['question']
            answers = question_data['answers']
            
            match = re.search(r'Proverbio\s+([^:]+):\s*\n\'([^\']+)\'', question)
            if match:
                region = match.group(1).strip()
                proverb = match.group(2).strip()
            else:
                region = "Sconosciuto"
                proverb = "Proverbio non riconosciuto"
            
            content.append(f"{i}. Proverbio {region}: ")
            content.append(f"'{proverb}' ")
            content.append("Cosa significa?")
            content.append("")
            
            letters = ['A', 'B', 'C', 'D']
            for j, answer in enumerate(answers[:4]):  # Massimo 4 risposte
                letter = letters[j]
                text = answer['text']
                correct_mark = " ✓" if answer.get('correct', False) else ""
                content.append(f"{letter}) {text}{correct_mark}")
            
            content.append("")
            content.append("---")
            content.append("")
        
        content.extend([
            "NUOVE DOMANDE DA AGGIUNGERE:",
            "=" * 30,
            "",
            "?. ?",
            "",
            "---",
            "",
            "FORMATO PER NUOVE DOMANDE:",
            "=" * 30,
            "",
            "[NUMERO]. Proverbio [REGIONE]: ",
            "'[PROVERBIO IN DIALETTO]' ",
            "Cosa significa?",
            "",
            "A) [Opzione A]",
            "B) [Opzione B] ✓",
            "C) [Opzione C]",
            "D) [Opzione D]",
            "",
            "---",
            "",
            "ISTRUZIONI:",
            "=" * 15,
            "- Usa ✓ per indicare la risposta corretta",
            "- Mantieni il formato con le linee --- come separatori", 
            "- I '?' indicano spazi per nuove domande",
            "- Per convertire in JSON usa: python txt_to_json.py",
            "- Per aggiornare da JSON usa: python json_to_txt.py"
        ])
        
        # Salva il file
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        print(f"✅ Conversione completata!")
        print(f"📄 File creato: {txt_file}")
        print(f"📊 Domande esportate: {len(questions)}")
        
        return len(questions)
        
    except Exception as e:
        print(f"❌ Errore durante la conversione: {e}")
        return 0

def main():
    json_file = "questions.json"
    txt_file = "ELENCO_DOMANDE_QUIZ_V2.txt"
    
    print("🔄 Conversione JSON → TXT")
    print(f"📖 Leggo: {json_file}")
    print(f"💾 Scrivo: {txt_file}")
    print("-" * 50)
    
    count = parse_json_to_txt(json_file, txt_file)
    
    if count > 0:
        print(f"\n✅ Successo! {count} domande esportate.")
        print("📝 Ora puoi modificare il file TXT e riconvertirlo con txt_to_json.py")
    else:
        print("\n❌ Errore nella conversione. Controlla il file JSON.")

if __name__ == "__main__":
    main()