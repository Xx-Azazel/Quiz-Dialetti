# SISTEMA DI GESTIONE DOMANDE QUIZ – PIPELINE REVISIONATA 2025

Questo documento descrive il flusso aggiornato per mantenere il dataset delle domande del quiz dialetti. Il vecchio doppio convertitore è stato sostituito da **un unico convertitore robusto** + **validatore**.

## 📁 File Principali

| File | Ruolo | Stato |
|------|-------|-------|
| `ELENCO_DOMANDE_QUIZ_V2.txt` | Sorgente editabile (authoring) | Attivo |
| `convert_txt_to_json.py` | Convertitore unico TXT → JSON (supporta `--dry-run`) | Attivo |
| `questions.json` | Dataset consumato dall'app web | Output |
| `validate_questions.py` | Validatore di integrità post-conversione | Attivo |
| `json_to_txt.py` | Esporta JSON → TXT (uso raro/manuale) | Legacy opzionale |
| `txt_to_json.py`, `txt_to_json_robust.py`, `fix_placeholders.py` | Vecchi script sostituiti | Deprecati |

## 🔄 Workflow Aggiornato (End‑to‑End)

1️⃣ **Modifica / Aggiunta domande** nel file `ELENCO_DOMANDE_QUIZ_V2.txt`  
2️⃣ **Dry‑run** conversione per vedere report e avvisi (nessun file scritto)  
3️⃣ **Correggi** eventuali avvisi critici nel TXT  
4️⃣ **Conversione reale** generando / sovrascrivendo `questions.json`  
5️⃣ **Validazione formale** del JSON  
6️⃣ (Opz.) **Test rapido** nel browser del quiz  
7️⃣ (Opz.) **Backup**: copia versionata del TXT e/o JSON

### Comandi (PowerShell / Windows)
```
python convert_txt_to_json.py --dry-run
python convert_txt_to_json.py
python validate_questions.py
```
Se il validatore segnala errori, correggere il TXT e ripetere dal punto 2.

## 📝 Formato Domande nel TXT

Blocchi separati da una linea contenente almeno tre trattini (---). La numerazione iniziale è **facoltativa** e ignorata dal convertitore.

Esempio completo di blocco valido:
```
12. Proverbio Barese:
'A chi time a Dìe, Dìe non mânghe maje.'
Cosa significa?

A) Dio aiuta sempre chi lo teme e rispetta ✓
B) Bisogna andare in chiesa ogni giorno
C) I baresi sono molto religiosi
D) La paura rende più forti

---
```

### Regole Sintetiche
| Aspetto | Regola |
|---------|--------|
| Intestazione | Riga che contiene `Proverbio <Regione>:` (case‑insensitive) |
| Proverbio | Riga successiva: proverbio tra apici singoli `'...'` (apici “ ” ‘ ’ vengono normalizzati) |
| Domanda | Riga che contiene esattamente `Cosa significa?` (entro 3–4 righe dopo) |
| Risposte | 4 righe con formato `A) testo`, `B) testo` … `D) testo` |
| Corretta | Aggiungere un `✓` (senza spazi dopo) alla fine della sola risposta corretta |
| Separatore | Linea con `---` (tre o più trattini) per chiudere il blocco |
| Numeri iniziali | Ignorati (possono mancare o non essere sequenziali) |
| Placeholder vietati | Niente righe fatte solo di `*`, `**`, `?` |
| Duplicati | Evitare risposte con testo identico (warning) |

### Consigli di Qualità
- Tenere le risposte concise (≤ 120–140 caratteri ideale, limite tecnico 160).
- Evitare negazioni doppie ambigue.
- Una sola risposta deve essere marcata ✓.
- Evitare di ripetere parole identiche tra tutte le opzioni (riduce discriminatività).

## ✅ Uso del Convertitore Unico

Dry‑run (nessuna scrittura):
```
python convert_txt_to_json.py --dry-run
```
Mostra: numero domande valide, sezioni scartate, avvisi (es. “Nessuna risposta marcata corretta”, “Solo 3 risposte raccolte”, “Risposte duplicate”).

Conversione reale:
```
python convert_txt_to_json.py
```
Genera / aggiorna `questions.json`. Se presenti avvisi, esegui comunque il validatore prima di usare il file in produzione.

### Tipi di Avvisi e Azioni
| Avviso | Significato | Azione consigliata |
|--------|-------------|--------------------|
| Nessuna risposta marcata corretta | Manca il ✓ | Aggiungi ✓ a UNA sola risposta |
| 2+ risposte marcate corrette | Ambiguità | Lascia ✓ solo su quella corretta |
| Solo X risposte raccolte | Mancano opzioni | Aggiungi fino a 4 risposte totali |
| Risposte duplicate | Testi identici | Varia il contenuto |

## 🔍 Validazione Finale

Esegui:
```
python validate_questions.py
```
Controlli: struttura, 4 risposte, esattamente 1 corretta, assenza placeholder, lunghezze massime.  
Esito:
- `✅ Dataset valido.` → pronto all'uso
- `❌ Dataset NON valido` → correggi il TXT e ripeti conversione

## ♻️ (Opzionale) Esportazione JSON → TXT
Se hai modificato direttamente `questions.json` (sconsigliato) e vuoi riallineare il TXT:
```
python json_to_txt.py
```
Usare solo come emergenza per recuperare un TXT coerente.

## 🧪 Checklist Prima di Pubblicare
- [ ] Dry‑run senza avvisi critici (o avvisi risolti)
- [ ] `validate_questions.py` senza errori
- [ ] Quiz caricato in browser: nessuna domanda con risposte incomplete
- [ ] Backup creato: es. `questions_YYYYMMDD.json` e/o `ELENCO_DOMANDE_QUIZ_V2_backup.txt`

## 🧯 Troubleshooting Rapido
| Problema | Causa Probabile | Soluzione |
|----------|-----------------|-----------|
| Sezioni scartate in massa | Mancano separatori `---` | Inserire `---` tra i blocchi |
| “Solo 3 risposte raccolte” | Una riga risposta manca lettera / formattazione | Assicurarsi pattern `X) ` all'inizio |
| Nessuna risposta corretta | Dimenticato ✓ | Aggiungere ✓ solo alla risposta giusta |
| Risposte duplicate | Copia/incolla non cambiato | Diversificare i testi |
| Placeholder (*, ?) nel JSON | Rimasti nel TXT | Sostituire con testo reale e riconvertire |
| Validatore: numero risposte != 4 | Troppi o troppo pochi dopo parsing | Uniformare a 4 nel TXT |

## 🗂️ Note sulla Deprecazione
I vecchi script (`txt_to_json.py`, `txt_to_json_robust.py`, `fix_placeholders.py`) restano nel repo solo per storico. Non usarli nel flusso quotidiano: potrebbero produrre dataset inconsistenti rispetto alle nuove regole.

## 🎯 Vantaggi Nuova Pipeline
- Robustezza parsing (numeri opzionali, normalizzazione Unicode)
- Dry‑run per feedback immediato
- Validazione formale separata (fail-fast)
- Eliminazione placeholder garantita
- Riduzione rischio divergenze fra formati

## 📌 Suggerito: Convenzione Backup
Creare dopo ogni pubblicazione:
```
copy questions.json questions_YYYYMMDD.json
copy ELENCO_DOMANDE_QUIZ_V2.txt ELENCO_DOMANDE_QUIZ_V2_YYYYMMDD.txt
```
(In PowerShell sostituire YYYYMMDD manualmente o usare script futuro.)

---
Per chiarimenti o estensioni (es. campo “spiegazione” post‑risposta) aggiungere una sezione proposta e aprire PR interna.