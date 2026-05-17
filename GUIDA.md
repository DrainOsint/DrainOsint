# 👁️ DRAIN OSINT BOT — Guida Completa
**By Drain | @fattissimo**

---

## 📁 Struttura del progetto

```
drainbot/
├── bot.py            ← Bot Telegram principale
├── sherlock_core.py  ← Motore di ricerca username
├── requirements.txt  ← Dipendenze Python
└── GUIDA.md          ← Questo file
```

---

## PASSO 1 — Crea il bot su Telegram (BotFather)

1. Apri Telegram e cerca **@BotFather**
2. Scrivi `/newbot`
3. Scegli un nome (es. `Drain OSINT Bot`)
4. Scegli uno username (es. `DrainOsintBot`)
5. Copia il **token** che ti dà (es. `123456789:AAFxxxx...`)
6. Apri `bot.py` e sostituisci:
   ```python
   BOT_TOKEN = "INSERISCI_QUI_IL_TUO_TOKEN"
   ```
   con il tuo token reale.

---

## PASSO 2 — Installazione in locale (per testare)

### Requisiti
- Python 3.9 o superiore installato

### Comandi
```bash
# Entra nella cartella
cd drainbot

# Installa le dipendenze
pip install -r requirements.txt

# Avvia il bot
python bot.py
```

Il bot è ora attivo finché il terminale rimane aperto.

---

## PASSO 3 — Deploy gratuito su Railway (consigliato)

Railway ti permette di tenere il bot attivo 24/7 gratis.

1. Vai su **https://railway.app** e registrati con GitHub
2. Clicca **"New Project"** → **"Deploy from GitHub repo"**
3. Carica il tuo codice su GitHub (o usa il drag & drop)
4. Aggiungi la variabile d'ambiente:
   - Nome: `BOT_TOKEN`
   - Valore: il tuo token di BotFather
5. (Modifica `bot.py` per leggere da env var — vedi sotto)
6. Railway avvia automaticamente il bot

### Modifica per Railway (variabile d'ambiente)
In `bot.py` sostituisci la riga del token con:
```python
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN", "INSERISCI_QUI_IL_TUO_TOKEN")
```

---

## COMANDI DEL BOT

| Comando | Descrizione |
|---|---|
| `/start` | Menu principale con bottoni |
| `/cerca <username>` | Avvia la ricerca dell'username |

---

## PERSONALIZZAZIONI RAPIDE

### Cambiare il watermark
In `bot.py`, riga:
```python
WATERMARK = "\n\n🔍 *By Drain* | @fattissimo"
```

### Aggiungere un sito alla ricerca
In `sherlock_core.py`, aggiungi una riga al dizionario `SITI`:
```python
"Nome Sito": "https://esempio.com/{}",
```
Il `{}` viene sostituito automaticamente con l'username.

### Rimuovere un sito
Cancella semplicemente la riga corrispondente in `SITI`.

---

## ⚠️ Note legali

Questo bot controlla **solo URL pubblicamente accessibili**.
Non accede a dati privati, password o informazioni riservate.
Usalo in modo responsabile e nel rispetto delle leggi vigenti.
