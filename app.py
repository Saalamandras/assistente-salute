"""
app.py
------
Entry point dell'applicazione Assistente Salute.
Configura e lancia l'interfaccia Gradio.

Kept minimal by design: la logica è in chatbot.py, la UI è qui.
"""

import gradio as gr
from chatbot import chat, get_initial_greeting


def respond(user_message: str, history: list[dict], chatbot_state: list[dict]):
    """
    Funzione chiamata da Gradio ad ogni messaggio dell'utente.

    Args:
        user_message: testo dell'utente
        history: history nel formato Gradio (per la visualizzazione)
        chatbot_state: history nel formato Anthropic (per le chiamate API)

    Returns:
        Tupla aggiornata per Gradio: (chatbot_display, chatbot_state)
    """
    if not user_message.strip():
        return history, chatbot_state

    bot_response, updated_state = chat(user_message, chatbot_state)

    # Gradio usa il formato [(user, bot), ...] per la visualizzazione
    updated_history = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": bot_response},
    ]

    return updated_history, updated_state


def initialize():
    """
    Carica il messaggio di benvenuto all'avvio dell'interfaccia.
    Restituisce la history Gradio e lo stato API iniziali.
    """
    greeting, initial_state = get_initial_greeting()
    # Il primo messaggio è solo del bot (None come utente)
    initial_display = [{"role": "assistant", "content": greeting}]
    return initial_display, initial_state


# ── Interfaccia Gradio ────────────────────────────────────────────────────────

with gr.Blocks(title="Assistente Salute") as demo:

    gr.Markdown(
        """
        # 🏥 Assistente Salute
        *Supporto AI per sintomi muscoloscheletrici e prenotazione specialisti*
        """
    )

    # Componente chat principale
    chatbot_display = gr.Chatbot(
        label="Conversazione",
        height=500,
    )

    # Stato interno: mantiene la history nel formato Anthropic tra un turno e l'altro
    # gr.State è invisibile all'utente ma persiste durante la sessione
    chatbot_state = gr.State([])

    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Scrivi qui il tuo messaggio...",
            label="",
            scale=4,
            autofocus=True,
        )
        send_btn = gr.Button("Invia", variant="primary", scale=1)

    gr.Markdown(
        """
        ---
        *Assistente Salute è un prototipo dimostrativo sviluppato da Antonio
        come progetto portfolio. Non è un servizio medico reale.*
        """
    )

    # ── Event handlers ────────────────────────────────────────────────────────

    # Carica il saluto iniziale quando la pagina si apre
    demo.load(
        fn=initialize,
        outputs=[chatbot_display, chatbot_state],
    )

    # Invia con il pulsante
    send_btn.click(
        fn=respond,
        inputs=[user_input, chatbot_display, chatbot_state],
        outputs=[chatbot_display, chatbot_state],
    ).then(
        fn=lambda: "",  # Svuota il campo di testo dopo l'invio
        outputs=user_input,
    )

    # Invia premendo Invio
    user_input.submit(
        fn=respond,
        inputs=[user_input, chatbot_display, chatbot_state],
        outputs=[chatbot_display, chatbot_state],
    ).then(
        fn=lambda: "",
        outputs=user_input,
    )


if __name__ == "__main__":
    demo.launch()
