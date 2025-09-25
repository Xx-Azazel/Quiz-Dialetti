#!/usr/bin/env python3

import re

def debug_parse_txt():
    try:
        with open("ELENCO_DOMANDE_QUIZ_V2.txt", 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = content.split('---')
        question_count = 0
        
        for i, section in enumerate(sections):
            section = section.strip()
            
            if not section or 'QUIZ PROVERBI' in section or 'LEGENDA:' in section or len(section) < 50:
                continue
            
            question_count += 1
            
            question_match = re.search(r'(\d+)\.\s*Proverbio\s+([^:]+):\s*\n\'([^\']+)\'\s*\nCosa significa\?', section)
            
            if question_match:
                number = question_match.group(1)
                region = question_match.group(2).strip()
                proverb = question_match.group(3).strip()
                print(f"\n📋 Domanda {number} ({region}):")
                print(f"   Proverbio: '{proverb[:50]}...'")
                
                # Conta le risposte
                answer_pattern = r'([A-D])\)\s*([^✓\n]+)(\s*✓)?'
                answer_matches = re.findall(answer_pattern, section)
                
                print(f"   Risposte trovate: {len(answer_matches)}")
                for j, (letter, text, is_correct) in enumerate(answer_matches):
                    status = "✓" if is_correct.strip() else " "
                    print(f"   {letter}) {text.strip()[:40]}... {status}")
                
                if len(answer_matches) != 4:
                    print(f"   ❌ PROBLEMA: Servono 4 risposte, trovate {len(answer_matches)}")
                else:
                    print(f"   ✅ OK: 4 risposte complete")
            else:
                print(f"\n❌ Sezione {i+1}: Formato domanda non riconosciuto")
                print(f"   Primi 100 caratteri: {section[:100]}...")
            
            # Mostra solo le prime 10 per non riempire lo schermo
            if question_count >= 10:
                print(f"\n... (mostro solo le prime 10 domande per debug)")
                break
        
        print(f"\n📊 Totale sezioni analizzate: {question_count}")
        
    except Exception as e:
        print(f"❌ Errore durante l'analisi: {e}")

if __name__ == "__main__":
    debug_parse_txt()