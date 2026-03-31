"""
app.py
------
Entry point dell'applicazione Assistente Salute.
Configura e lancia l'interfaccia Gradio.
"""

import gradio as gr
from chatbot import chat, get_initial_greeting


def respond(user_message: str, history: list):
    """
    Funzione chiamata da Gradio ad ogni messaggio dell'utente.
    gr.ChatInterface passa la history automaticamente nel formato
    [(user, bot), ...] — la convertiamo nel formato Anthropic.
    """
    # Converte la history da formato Gradio a formato Anthropic
    anthropic_history = []
    for user_msg, bot_msg in history:
        if user_msg:
            anthropic_history.append({"role": "user", "content": user_msg})
        if bot_msg:
            anthropic_history.append({"role": "assistant", "content": bot_msg})

    bot_response, _ = chat(user_message, anthropic_history)
    return bot_response


# Genera il messaggio di benvenuto iniziale
greeting, _ = get_initial_greeting()

demo = gr.ChatInterface(
    fn=respond,
    title="🏥 Assistente Salute",
    description="Supporto AI per sintomi muscoloscheletrici e prenotazione specialisti",
    examples=["Ho mal di schiena da qualche giorno", "Mi fa male il ginocchio"],
)

if __name__ == "__main__":
    demo.launch()