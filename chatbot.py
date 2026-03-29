"""
chatbot.py
----------
Logica principale del chatbot: gestione della conversazione e chiamate
all'API Anthropic.

Separato da app.py per mantenere la UI (Gradio) disaccoppiata dalla logica.
Questo rende il codice più leggibile e più facile da testare.
"""

import os
from dotenv import load_dotenv
import anthropic

from system_prompt import SYSTEM_PROMPT
from calendar_mock import book_appointment

# Carica le variabili d'ambiente da .env (in locale).
# Su Hugging Face Spaces, la variabile viene letta direttamente dai Secrets.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Inizializzazione del client Anthropic.
# ⚠️  La API key viene letta dall'ambiente — non scrivere mai la chiave nel codice.
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Modello usato. claude-3-5-haiku è veloce ed economico — adatto per un demo.
MODEL = "claude-haiku-4-5-20251001"

# Numero massimo di token nella risposta del modello.
MAX_TOKENS = 1024


def chat(user_message: str, history: list[dict]) -> tuple[str, list[dict]]:
    """
    Elabora un messaggio dell'utente e restituisce la risposta del chatbot.

    Args:
        user_message: il testo inviato dall'utente
        history: lista dei messaggi precedenti nel formato Anthropic
                 [{"role": "user"|"assistant", "content": "..."}]

    Returns:
        Tupla (risposta_del_bot, history_aggiornata)
    """
    # Aggiunge il nuovo messaggio dell'utente alla cronologia
    history = history + [{"role": "user", "content": user_message}]

    # Chiamata all'API Anthropic con l'intera cronologia della conversazione.
    # Il system prompt viene passato separatamente (non come messaggio).
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=history,
    )

    # Estrae il testo dalla risposta
    assistant_message = response.content[0].text

    # Aggiunge la risposta del bot alla cronologia
    history = history + [{"role": "assistant", "content": assistant_message}]

    return assistant_message, history


def get_initial_greeting() -> tuple[str, list[dict]]:
    """
    Genera il messaggio di benvenuto iniziale del chatbot.

    Questo approccio — chiedere al modello di generare il primo messaggio —
    garantisce che il tono e il disclaimer siano coerenti con il system prompt,
    invece di usare un testo statico hardcoded.

    Returns:
        Tupla (messaggio_iniziale, history_con_il_messaggio)
    """
    greeting_prompt = (
        "Inizia la conversazione con un saluto caloroso e presentati. "
        "Includi il disclaimer in modo naturale come indicato nelle istruzioni."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": greeting_prompt}],
    )

    greeting = response.content[0].text

    # La history inizia con il messaggio di benvenuto del bot
    # (non includiamo il prompt di trigger — non è parte della conversazione reale)
    initial_history = [{"role": "assistant", "content": greeting}]

    return greeting, initial_history
