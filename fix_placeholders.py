#!/usr/bin/env python3
"""
Sostituisce i "?" nel file V2 con asterischi progressivi (*,**,***)
"""

import re

def replace_placeholders_with_asterisks():
    """Sostituisce i ? con asterischi progressivi per ogni domanda"""
    
    # Leggi il file
    with open("ELENCO_DOMANDE_QUIZ_V2.txt", 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dividi le domande usando i separatori ---
    sections = content.split('---')
    modified_sections = []
    questions_modified = 0
    
    for section in sections:
        section_modified = section
        
        # Se la sezione contiene una domanda con "?" o righe vuote
        if ('Proverbio' in section and 'Cosa significa?' in section and 
            ('?' in section or re.search(r'^[A-D]\)\s*$', section, re.MULTILINE))):
            
            # Trova tutte le risposte con "?" in questa sezione
            answer_lines = []
            lines = section.split('\n')
            placeholder_count = 0
            
            for i, line in enumerate(lines):
                # Se è una riga di risposta (A), B), C), D))
                if re.match(r'^[A-D]\)', line.strip()):
                    answer_lines.append(i)
                    # Se contiene solo "?" o finisce con "?" o è completamente vuota
                    line_content = line.strip()
                    if (line_content.endswith('?') and len(line_content) <= 4) or (re.match(r'^[A-D]\)\s*$', line_content)):
                        placeholder_count += 1
            
            # Sostituisci i placeholder con asterischi progressivi
            if placeholder_count > 0:
                current_asterisk = 1
                new_lines = lines.copy()
                
                for line_idx in answer_lines:
                    line = lines[line_idx].strip()
                    # Se è un placeholder da sostituire (con "?" o completamente vuoto)
                    line_content = line.strip()
                    is_placeholder = ((line_content.endswith('?') and len(line_content) <= 4) or 
                                    (re.match(r'^[A-D]\)\s*$', line_content)))
                    
                    if is_placeholder:
                        # Estrai la lettera della risposta
                        letter_match = re.match(r'^([A-D]\))', line)
                        if letter_match:
                            letter = letter_match.group(1)
                            asterisks = '*' * current_asterisk
                            new_lines[line_idx] = f"{letter} {asterisks}"
                            current_asterisk += 1
                
                section_modified = '\n'.join(new_lines)
                questions_modified += 1
                
                # Trova il numero della domanda per il log
                question_match = re.search(r'(\d+)\.\s*Proverbio\s+([^:]+):', section)
                if question_match:
                    num, region = question_match.groups()
                    print(f"✅ Domanda {num} ({region}): sostituiti {placeholder_count} placeholder con asterischi")
        
        modified_sections.append(section_modified)
    
    # Ricomponi il file
    new_content = '---'.join(modified_sections)
    
    # Salva il file modificato
    with open("ELENCO_DOMANDE_QUIZ_V2.txt", 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n🎯 Sostituzione completata!")
    print(f"📊 Domande modificate: {questions_modified}")
    print(f"💾 File aggiornato: ELENCO_DOMANDE_QUIZ_V2.txt")
    
    return questions_modified

def main():
    print("🔄 Sostituzione placeholder ? → asterischi")
    print("-" * 50)
    
    count = replace_placeholders_with_asterisks()
    
    if count > 0:
        print(f"\n✅ Successo! {count} domande aggiornate con asterischi.")
        print("🔄 Ora puoi riconvertire con: python txt_to_json.py")
    else:
        print("\n💡 Nessun placeholder '?' trovato da sostituire.")

if __name__ == "__main__":
    main()