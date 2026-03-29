# Assistente Salute 🏥

**Chatbot AI di triage ortopedico in italiano — progetto portfolio**

> Sviluppato da Antonio come dimostrazione pratica di competenze in NLP
> applicato, prompt engineering e integrazione di LLM in produzione.

---

## Descrizione

Assistente Salute è un chatbot conversazionale in italiano che simula un flusso
di triage ortopedico per utenti anziani. Il bot:

1. Accoglie l'utente con un disclaimer chiaro ma non burocratico
2. Pone 2–3 domande contestuali sui sintomi muscoloscheletrici
3. Fornisce una risposta orientativa (non medica)
4. Raccomanda lo specialista più adatto
5. Gestisce la prenotazione di un appuntamento su un calendario mock

Il progetto è costruito specificamente come artefatto dimostrativo per
candidature in ruoli AI/NLP engineering. Non è un servizio medico.

---

## Stack tecnico

| Componente | Tecnologia |
|---|---|
| LLM | Anthropic Claude (claude-3-5-haiku) |
| SDK | `anthropic` Python SDK |
| UI | Gradio |
| Deploy | Hugging Face Spaces |
| Config | python-dotenv |

---

## Struttura del progetto

```
assistente-salute/
├── app.py              # Entry point Gradio
├── chatbot.py          # Logica conversazione e chiamate API
├── system_prompt.py    # System prompt (artefatto portfolio centrale)
├── calendar_mock.py    # Mock calendar con specialisti e disponibilità
├── .env                # API key locale (escluso da Git)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Come eseguire in locale

```bash
# 1. Clona il repository
git clone https://github.com/tuousername/assistente-salute
cd assistente-salute

# 2. Crea un ambiente virtuale
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Configura la API key
cp .env.example .env
# Modifica .env e inserisci la tua ANTHROPIC_API_KEY

# 5. Avvia l'app
python app.py
```

> ⚠️  **Non committare mai il file `.env`** — contiene la tua API key.
> Il `.gitignore` lo esclude automaticamente.

---

## Deploy su Hugging Face Spaces

1. Crea un nuovo Space (SDK: Gradio)
2. Carica i file del progetto (escludi `.env`)
3. Vai in **Settings > Variables and secrets**
4. Aggiungi `ANTHROPIC_API_KEY` come secret

---

## Specialisti disponibili (mock)

| Specialista | Specializzazione | Disponibilità |
|---|---|---|
| Dr. Rossi | Ortopedico generalista | Lun / Mer / Ven |
| Dr. Marino | Ortopedico colonna vertebrale | Mar / Gio |
| Dr. Ferretti | Fisiatra | Lun / Gio / Sab |

---

## Scope e limitazioni

Questo progetto è un **prototipo dimostrativo** con le seguenti limitazioni consapevoli:

- **Calendario mock**: la prenotazione è simulata in memoria. I dati non
  persistono tra le sessioni.
- **Nessuna autenticazione**: non c'è gestione di utenti o sessioni reali.
- **Solo muscoloscheletrico**: il bot è ottimizzato per sintomi ortopedici.
  Per altri ambiti, rimanda al medico di base.
- **Non è un dispositivo medico**: le risposte sono orientative. Il bot
  non sostituisce una visita medica.

---

## Miglioramenti futuri

- **Integrazione Google Calendar API**: sostituire il mock con prenotazioni
  reali su Google Calendar, inclusa gestione della disponibilità in tempo reale.
- **Autenticazione utente**: associare le prenotazioni a profili utente.
- **Streaming delle risposte**: usare `client.messages.stream()` per una UX
  più fluida su connessioni lente.
- **Espansione specialisti**: aggiungere altri ambiti (cardiologia, dermatologia)
  con routing dinamico.

---

## Note sul prompt engineering

Il file `system_prompt.py` è il cuore del progetto dal punto di vista
linguistico. Il prompt:

- Definisce tono, stile e vincoli in italiano
- Struttura il flusso conversazionale in fasi discrete
- Include regole di safety esplicite (es. sintomi urgenti → 118)
- Genera il riepilogo degli specialisti dinamicamente dal modulo calendar

Il design del prompt riflette le competenze acquisite durante il percorso in
Computational Linguistics e l'esperienza come Prompt Engineer.

---

*Antonio — MSc Computational Linguistics, Ca' Foscari Venezia*
