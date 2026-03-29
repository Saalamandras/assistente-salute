"""
calendar_mock.py
----------------
Mock calendar con specialisti ortopedici e disponibilità settimanale.

In un sistema reale, questo modulo verrebbe sostituito da un'integrazione
con Google Calendar API (vedi README per dettagli sul miglioramento futuro).
"""

# Dizionario degli specialisti disponibili.
# Ogni specialista ha: nome, specializzazione, giorni disponibili.
SPECIALISTS = {
    "rossi": {
        "nome": "Dr. Rossi",
        "specializzazione": "Ortopedico generalista",
        "disponibilita": ["Lunedì", "Mercoledì", "Venerdì"],
        "descrizione": "Ideale per dolori articolari generali, ginocchio, anca, spalla.",
    },
    "marino": {
        "nome": "Dr. Marino",
        "specializzazione": "Ortopedico colonna vertebrale",
        "disponibilita": ["Martedì", "Giovedì"],
        "descrizione": "Specializzato in mal di schiena, ernie del disco, cervicale.",
    },
    "ferretti": {
        "nome": "Dr. Ferretti",
        "specializzazione": "Fisiatra",
        "disponibilita": ["Lunedì", "Giovedì", "Sabato"],
        "descrizione": "Esperto in riabilitazione, fisioterapia, dolori muscolari cronici.",
    },
}

# Orari disponibili per ogni slot (uguali per tutti gli specialisti nel mock)
ORARI_DISPONIBILI = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]


def get_specialist_info(specialist_key: str) -> dict | None:
    """
    Restituisce le informazioni di uno specialista dato il suo identificatore.
    Restituisce None se lo specialista non esiste.
    """
    return SPECIALISTS.get(specialist_key.lower())


def get_all_specialists_summary() -> str:
    """
    Genera un riepilogo testuale di tutti gli specialisti,
    usato dal chatbot per informare l'utente sulle opzioni disponibili.
    """
    lines = []
    for spec in SPECIALISTS.values():
        giorni = ", ".join(spec["disponibilita"])
        lines.append(
            f"• {spec['nome']} ({spec['specializzazione']}) — disponibile {giorni}"
        )
    return "\n".join(lines)


def book_appointment(specialist_key: str, giorno: str, orario: str) -> dict:
    """
    Registra (in memoria) un appuntamento mock.

    Args:
        specialist_key: identificatore dello specialista (es. "rossi")
        giorno: giorno della settimana scelto (es. "Lunedì")
        orario: orario scelto (es. "10:00")

    Returns:
        Dizionario con i dettagli della prenotazione o un messaggio di errore.
    """
    spec = get_specialist_info(specialist_key)

    if not spec:
        return {"successo": False, "errore": "Specialista non trovato."}

    if giorno not in spec["disponibilita"]:
        giorni_ok = ", ".join(spec["disponibilita"])
        return {
            "successo": False,
            "errore": f"{spec['nome']} non è disponibile il {giorno}. "
                      f"Giorni disponibili: {giorni_ok}.",
        }

    if orario not in ORARI_DISPONIBILI:
        return {"successo": False, "errore": f"Orario {orario} non disponibile."}

    # In un sistema reale: chiamata a Google Calendar API qui.
    return {
        "successo": True,
        "specialista": spec["nome"],
        "specializzazione": spec["specializzazione"],
        "giorno": giorno,
        "orario": orario,
        "messaggio": (
            f"Appuntamento confermato con {spec['nome']} "
            f"({spec['specializzazione']}) "
            f"il {giorno} alle {orario}."
        ),
    }
