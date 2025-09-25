# SISTEMA DI GESTIONE DOMANDE QUIZ - BIDIREZIONALE

## 📁 File Principali

| File | Descrizione |
|------|-------------|
| `questions.json` | Database delle domande per il quiz online |
| `ELENCO_DOMANDE_QUIZ_V2.txt` | File editabile in formato testo |
| `txt_to_json.py` | Convertitore TXT → JSON |
| `json_to_txt.py` | Convertitore JSON → TXT |

## 🔄 Workflow di Lavoro

### 1️⃣ Modifica delle Domande
```
Edita → ELENCO_DOMANDE_QUIZ_V2.txt
```
- Apri il file V2 con qualsiasi editor di testo
- Modifica le domande esistenti
- Sostituisci i "?" con nuove domande
- Segui il formato indicato nel file

### 2️⃣ Aggiornamento del Quiz
```bash
python txt_to_json.py
```
- Converte le modifiche dal TXT al JSON
- Aggiorna automaticamente il database del quiz
- Mostra un report delle domande processate

### 3️⃣ Esportazione per Revisione
```bash
python json_to_txt.py
```
- Rigenera il file TXT dal JSON attuale
- Utile per sincronizzare dopo modifiche dirette al JSON
- Mantiene il formato standard

## 📝 Formato delle Domande

```
[NUMERO]. Proverbio [REGIONE]: 
'[PROVERBIO IN DIALETTO]' 
Cosa significa?

A) [Opzione A]
B) [Opzione B] ✓
C) [Opzione C]  
D) [Opzione D]

---
```

### ⚠️ Regole Importanti:
- Usa **✓** per indicare la risposta corretta
- Mantieni le linee **---** come separatori
- Esattamente **4 opzioni** per domanda (A, B, C, D)
- I **"?"** indicano slot per nuove domande

## 🚀 Esempi di Uso

### Aggiungere una nuova domanda:
1. Apri `ELENCO_DOMANDE_QUIZ_V2.txt`
2. Trova un "?" e sostituiscilo con:
```
25. Proverbio Barese: 
'A chi time a Dio, Dio non manca mai.' 
Cosa significa?

A) Dio aiuta sempre i credenti ✓
B) La paura di Dio è sbagliata
C) Bisogna pregare molto
D) I baresi sono religiosi
```
3. Salva il file
4. Esegui: `python txt_to_json.py`

### Modificare una domanda esistente:
1. Trova la domanda in `ELENCO_DOMANDE_QUIZ_V2.txt`
2. Modifica il testo o le opzioni
3. Sposta il ✓ se necessario
4. Esegui: `python txt_to_json.py`

### Sincronizzare dal JSON:
Se qualcuno modifica direttamente `questions.json`:
```bash
python json_to_txt.py
```

## 🔧 Risoluzione Problemi

| Errore | Causa | Soluzione |
|--------|-------|-----------|
| "Domanda saltata: trovate X risposte" | Formato errato | Controlla che ci siano esattamente 4 opzioni A-D |
| "Nessuna domanda convertita" | Formato completamente errato | Verifica i separatori --- e la struttura |
| "File non trovato" | File mancante | Assicurati che i file esistano nella stessa cartella |

## 📊 Statistiche Attuali
- **50 domande** nel database
- **29 regioni/dialetti** rappresentati
- **Quiz seleziona 10 domande casuali** per partita

## 🎯 Vantaggi del Sistema
- ✅ **Editing facile** con qualsiasi editor di testo
- ✅ **Conversione automatica** bidirezionale
- ✅ **Backup sicuro** (sempre 2 formati disponibili)
- ✅ **Collaborazione semplice** (condividi il file TXT)
- ✅ **Controllo qualità** automatico durante la conversione