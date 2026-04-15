TEXTS = {
    "de": {
        "app_title": "RenzForge Autohaus Manager",
        "summary_default": "Starte ein neues Spiel und lass den Bestand für dich arbeiten.",
        "selection_empty": "Kein Auto ausgewählt",
        "energy_tank": "Tank (L)",
        "timer_idle": "Neues Spiel starten, dann läuft die Uhr.",
        "timer_display_idle": "--:--",
        "market_summary_empty": "Noch kein Angebot ausgewählt",
        "market_hint_empty": "Noch kein Markt gebaut",
        "customer_summary_empty": "Noch kein Kundenangebot aktiv",
        "customer_hint_empty": "Wähle links ein eigenes Auto aus und hol dir dann ein Angebot.",
        "guide_missing": "Die Spielprinzip-Datei wurde nicht gefunden.",
        "header_subtitle": "Autohaus-Sandbox mit Tageswechsel, Verschleiß, Unfällen und Verkaufsdruck.",
        "header_tag": "Tag",
        "header_cash": "Kapital",
        "header_target_cash": "Kapitalziel",
        "header_next_day": "Nächster Tag",
        "button_new_game": "Neues Spiel",
        "button_guide": "Spielprinzip TXT",
        "menu_fill_all_fuel": "Alle tanken",
        "menu_fill_all_charge": "Alle laden",
        "menu_status": "Status",
        "menu_clear_inventory": "Bestand leeren",
        "menu_buy_offer": "Angebot kaufen",
        "menu_reject_offer": "Angebot ablehnen",
        "menu_refresh_market": "Markt auffrischen",
        "menu_request_offer": "Angebot holen",
        "menu_send_counteroffer": "Gegenangebot senden",
        "menu_accept": "Annehmen",
        "menu_reject": "Ablehnen",
        "menu_edit_large": "Groß bearbeiten",
        "menu_save": "Speichern",
        "menu_wash": "Waschen",
        "menu_service": "Warten",
        "menu_repair": "Reparieren",
        "menu_fill_up": "Voll machen",
        "menu_log": "Kurzstatus zeigen",
    }
}


def get_ui_text(language="de"):
    return TEXTS.get(language, TEXTS["de"])
