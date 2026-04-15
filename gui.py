import random
import tkinter as tk
from tkinter import ttk

from branding import create_logo_photo
from data import (
    ALLE_AUTOHAEUSER,
    AUTOHAUS,
    BESITZER,
    FARBEN,
    MARKEN,
    PREMIUM_AUTOHAUS,
    PREMIUM_MARKEN,
)
from models import Auto, ElektroAuto, Garage
from utils import clear_table, clearlog, gui_print

PALETTE = {
    "app_bg": "#050816",
    "card": "#0d1528",
    "card_alt": "#111c33",
    "line": "#1e2c47",
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "accent": "#7c3aed",
    "accent_two": "#06b6d4",
    "accent_soft": "#172554",
    "input_bg": "#09111f",
    "danger": "#9f1239",
    "warn": "#ea580c",
    "ok": "#0f766e",
}


class AutoGUI:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.garage = Garage("RenzForge Garage", config)
        self.tables = {}
        self.tab_frames = {}
        self.form_vars = {}
        self.stat_vars = {}
        self.header_stat_vars = {}
        self.detail_vars = {}
        self.selected_vehicle = None
        self.selected_offer = None
        self.customer_offer = None
        self.logo_image = None
        self.market_offers = []
        self.market_tree = None

        self.summary_var = tk.StringVar(
            value="Starte ein neues Spiel und lass den Bestand für dich arbeiten."
        )
        self.selection_var = tk.StringVar(value="Kein Auto ausgewählt")
        self.energy_label_var = tk.StringVar(value="Tank (L)")
        self.market_summary_var = tk.StringVar(value="Noch kein Angebot ausgewählt")
        self.market_hint_var = tk.StringVar(value="Noch kein Markt gebaut")
        self.customer_summary_var = tk.StringVar(
            value="Noch kein Kundenangebot aktiv"
        )
        self.customer_hint_var = tk.StringVar(
            value="Wähle links ein eigenes Auto aus und hol dir dann ein Angebot."
        )
        for key in ("wert", "zustand", "sauberkeit", "schaden", "letzte_fahrt"):
            self.detail_vars[key] = tk.StringVar(value="-")
        self.setup_ui()

    def setup_ui(self):
        self.root.title("RenzForge Autohaus Manager")
        self.root.geometry("1660x980")
        self.root.minsize(1360, 860)
        self.root.configure(bg=PALETTE["app_bg"])
        self.setup_style()
        self.setup_header()

        content = tk.Frame(self.root, bg=PALETTE["app_bg"])
        content.pack(fill="both", expand=True, padx=18, pady=(0, 14))

        left = self.make_card(content)
        left.pack(side="left", fill="both", expand=True)
        right = self.make_card(content, width=390)
        right.pack(side="right", fill="y", padx=(16, 0))
        right.pack_propagate(False)

        self.setup_notebook(left)
        self.setup_editor(right)
        self.setup_log()
        self.refresh_all_views()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=PALETTE["card"], borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=PALETTE["accent_soft"],
            foreground="#cbd5e1",
            padding=(18, 10),
            font=("Bahnschrift", 10, "bold"),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", PALETTE["accent"])],
            foreground=[("selected", "#ffffff")],
        )
        style.configure(
            "Forge.Treeview",
            background=PALETTE["input_bg"],
            foreground=PALETTE["text"],
            fieldbackground=PALETTE["input_bg"],
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Forge.Treeview.Heading",
            background=PALETTE["card_alt"],
            foreground=PALETTE["text"],
            relief="flat",
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Forge.Treeview",
            background=[("selected", "#243b74")],
            foreground=[("selected", "#ffffff")],
        )
        style.configure(
            "Forge.TCombobox",
            fieldbackground=PALETTE["input_bg"],
            background=PALETTE["input_bg"],
            foreground=PALETTE["text"],
            arrowcolor=PALETTE["accent_two"],
            borderwidth=0,
            padding=6,
        )

    def setup_header(self):
        hero = self.make_card(self.root, pad=0)
        hero.pack(fill="x", padx=18, pady=(18, 0))
        tk.Frame(hero, bg=PALETTE["accent"], height=3).pack(fill="x")
        inner = tk.Frame(hero, bg=PALETTE["card"])
        inner.pack(fill="x", padx=22, pady=20)

        brand = tk.Frame(inner, bg=PALETTE["card"])
        brand.pack(side="left", fill="both", expand=True)
        try:
            self.logo_image = create_logo_photo(width=500, height=102)
        except Exception:
            self.logo_image = None

        if self.logo_image is not None:
            tk.Label(brand, image=self.logo_image, bg=PALETTE["card"]).pack(anchor="w")
        else:
            tk.Label(
                brand,
                text="RENZFORGE",
                fg=PALETTE["text"],
                bg=PALETTE["card"],
                font=("Bahnschrift", 30, "bold"),
            ).pack(anchor="w")

        tk.Label(
            brand,
            text="Autohaus-Sandbox mit Tageswechsel, Verschleiß, Unfällen und Verkaufsdruck.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(6, 0))
        tk.Label(
            brand,
            textvariable=self.summary_var,
            fg="#cbd5e1",
            bg=PALETTE["card"],
            font=("Segoe UI Semibold", 10),
        ).pack(anchor="w", pady=(14, 0))

        stats = tk.Frame(inner, bg=PALETTE["card"])
        stats.pack(side="right")
        for index in range(3):
            stats.grid_columnconfigure(index, weight=1)

        stat_cards = [
            ("Tag", "tag", PALETTE["accent"]),
            ("Kasse", "cash", "#f59e0b"),
            ("Bestand", "gesamt", "#2563eb"),
            ("Premium", "premium", "#ec4899"),
            ("Elektro", "elektro", PALETTE["accent_two"]),
            ("Ziel", "goal_left", "#22c55e"),
        ]
        for idx, (title, key, color) in enumerate(stat_cards):
            self.header_stat_vars[key] = tk.StringVar(value="-")
            card = tk.Frame(
                stats,
                bg=PALETTE["card_alt"],
                highlightbackground=PALETTE["line"],
                highlightthickness=1,
                padx=14,
                pady=14,
            )
            card.grid(row=idx // 3, column=idx % 3, sticky="nsew", padx=6, pady=6)
            tk.Frame(card, bg=color, height=3).pack(fill="x", pady=(0, 10))
            tk.Label(
                card,
                text=title,
                fg=PALETTE["muted"],
                bg=PALETTE["card_alt"],
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor="w")
            tk.Label(
                card,
                textvariable=self.header_stat_vars[key],
                fg=PALETTE["text"],
                bg=PALETTE["card_alt"],
                font=("Bahnschrift", 18, "bold"),
            ).pack(anchor="w", pady=(4, 0))

        toolbar = self.make_card(self.root)
        toolbar.pack(fill="x", padx=18, pady=(14, 14))
        controls = tk.Frame(toolbar, bg=PALETTE["card"])
        controls.pack(fill="x", padx=18, pady=16)

        info = tk.Frame(controls, bg=PALETTE["card"])
        info.pack(side="left")
        tk.Label(
            info,
            text="Erst einkaufen, dann Tag für Tag managen",
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Segoe UI Semibold", 12),
        ).pack(anchor="w")
        tk.Label(
            info,
            text="Du kaufst jetzt aus Angeboten ein. Danach fahren die Autos, verlieren Wert und machen Arbeit.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        actions = tk.Frame(controls, bg=PALETTE["card"])
        actions.pack(side="right")
        tk.Label(
            actions,
            text="Angebote",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(0, 8))
        self.anzahl_entry = tk.Entry(
            actions,
            width=6,
            font=("Consolas", 12),
            justify="center",
            bg=PALETTE["input_bg"],
            fg=PALETTE["text"],
            insertbackground=PALETTE["text"],
            relief="flat",
        )
        self.anzahl_entry.insert(0, "8")
        self.anzahl_entry.pack(side="left", padx=(0, 12), ipady=6)

        toolbar_buttons = [
            ("Neues Spiel", self.generieren, PALETTE["accent"]),
            ("Nächster Tag", self.next_day, PALETTE["warn"]),
            ("Alle tanken", self.tanken_alle, "#2563eb"),
            ("Alle laden", self.laden_alle, PALETTE["accent_two"]),
            ("Status", self.status_alle, PALETTE["ok"]),
            ("Bestand leeren", self.clear_inventory, "#7f1d1d"),
        ]
        for text, command, color in toolbar_buttons:
            self.make_button(actions, text, command, color).pack(side="left", padx=4)

    def setup_notebook(self, parent):
        header = tk.Frame(parent, bg=PALETTE["card"])
        header.pack(fill="x", padx=18, pady=(18, 10))
        tk.Label(
            header,
            text="Bestand im Blick",
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Bahnschrift", 18, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Hier siehst du den ganzen Laden samt Wertverlust, Zustand und kleinen Katastrophen.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        inventory_tabs = [
            ("market", "Einkaufen"),
            ("customers", "Kunden"),
            ("all", "Alle Autos"),
            ("normal", "Normale Ecke"),
            ("premium", "Premium Ecke"),
        ]
        for key, title in inventory_tabs:
            frame = tk.Frame(self.notebook, bg=PALETTE["card"])
            self.tab_frames[key] = frame
            self.notebook.add(frame, text=title)
            if key == "market":
                self.setup_market_tab(frame)
            elif key == "customers":
                self.setup_customer_tab(frame)
            else:
                self.setup_inventory_tab(frame, key, title)
        editor_frame = tk.Frame(self.notebook, bg=PALETTE["card"])
        self.tab_frames["editor"] = editor_frame
        self.notebook.add(editor_frame, text="Bearbeiten")
        self.setup_editor_tab(editor_frame)
        stats_frame = tk.Frame(self.notebook, bg=PALETTE["card"])
        self.tab_frames["stats"] = stats_frame
        self.notebook.add(stats_frame, text="Statistiken")
        self.setup_stats_tab(stats_frame)
        self.notebook.bind("<<NotebookTabChanged>>", lambda _event: self.refresh_statistics())

    def setup_market_tab(self, parent):
        tk.Label(
            parent,
            text="Angebote am Markt",
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Segoe UI Semibold", 13),
        ).pack(anchor="w", padx=16, pady=(16, 4))
        tk.Label(
            parent,
            text="Hier kaufst du Fahrzeuge ein, bevor sie in deinem Bestand landen.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=16, pady=(0, 10))

        action_row = tk.Frame(parent, bg=PALETTE["card"])
        action_row.pack(fill="x", padx=16, pady=(0, 12))
        self.make_button(
            action_row,
            "Ausgewähltes Angebot kaufen",
            self.buy_selected_offer,
            PALETTE["accent"],
        ).pack(side="left")
        self.make_button(
            action_row,
            "Markt auffrischen",
            self.refresh_market_offers,
            PALETTE["warn"],
        ).pack(side="left", padx=(10, 0))
        self.make_button(
            action_row,
            "Angebot ablehnen",
            self.reject_selected_offer,
            "#475569",
        ).pack(side="left", padx=(10, 0))

        wrap = tk.Frame(parent, bg=PALETTE["card"])
        wrap.pack(fill="both", expand=True, padx=16, pady=(0, 10))
        shell = tk.Frame(
            wrap,
            bg=PALETTE["input_bg"],
            highlightbackground=PALETTE["line"],
            highlightthickness=1,
        )
        shell.pack(fill="both", expand=True)

        columns = (
            "ID",
            "Marke",
            "Typ",
            "Zustand",
            "Sauberkeit",
            "Schaden",
            "Ankauf",
            "Deal",
            "Standort",
        )
        widths = {
            "ID": 70,
            "Marke": 130,
            "Typ": 90,
            "Zustand": 90,
            "Sauberkeit": 95,
            "Schaden": 125,
            "Ankauf": 110,
            "Deal": 90,
            "Standort": 180,
        }
        tree = ttk.Treeview(
            shell,
            columns=columns,
            show="headings",
            style="Forge.Treeview",
            height=15,
        )
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=widths[column], anchor="center")

        tree.tag_configure("deal_good", background="#10261b")
        tree.tag_configure("deal_ok", background="#111c33")
        tree.tag_configure("deal_hard", background="#2a1722")
        tree.pack(side="left", fill="both", expand=True, padx=1, pady=1)
        tree.bind("<<TreeviewSelect>>", self.on_market_select)

        scrollbar = ttk.Scrollbar(shell, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        self.market_tree = tree

        info = tk.Frame(
            parent,
            bg=PALETTE["input_bg"],
            highlightbackground=PALETTE["line"],
            highlightthickness=1,
        )
        info.pack(fill="x", padx=16, pady=(0, 16))
        tk.Label(
            info,
            text="Aktuelles Angebot",
            fg=PALETTE["accent_two"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI Semibold", 11),
        ).pack(anchor="w", padx=14, pady=(12, 6))
        tk.Label(
            info,
            textvariable=self.market_summary_var,
            fg=PALETTE["text"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI", 10),
            wraplength=980,
            justify="left",
        ).pack(anchor="w", padx=14)
        tk.Label(
            info,
            textvariable=self.market_hint_var,
            fg=PALETTE["muted"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI", 10),
            wraplength=980,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(6, 12))

    def setup_customer_tab(self, parent):
        tk.Label(
            parent,
            text="Kundenangebote",
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Segoe UI Semibold", 13),
        ).pack(anchor="w", padx=16, pady=(16, 4))
        tk.Label(
            parent,
            text="Hier kannst du für ein ausgewähltes Bestandsauto Angebote holen und nachverhandeln.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=16, pady=(0, 10))

        action_row = tk.Frame(parent, bg=PALETTE["card"])
        action_row.pack(fill="x", padx=16, pady=(0, 12))
        buttons = [
            ("Angebot holen", self.request_customer_offer, PALETTE["accent"]),
            ("Nachverhandeln", self.negotiate_customer_offer, PALETTE["warn"]),
            ("Annehmen", self.accept_customer_offer, PALETTE["ok"]),
            ("Ablehnen", self.reject_customer_offer, "#475569"),
        ]
        for text, command, color in buttons:
            self.make_button(action_row, text, command, color).pack(
                side="left",
                padx=(0, 10),
            )

        shell = tk.Frame(
            parent,
            bg=PALETTE["input_bg"],
            highlightbackground=PALETTE["line"],
            highlightthickness=1,
        )
        shell.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        info = tk.Frame(shell, bg=PALETTE["input_bg"])
        info.pack(fill="both", expand=True, padx=16, pady=16)
        tk.Label(
            info,
            text="Aktuelle Auswahl",
            fg=PALETTE["accent_two"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI Semibold", 11),
        ).pack(anchor="w")
        tk.Label(
            info,
            textvariable=self.selection_var,
            fg=PALETTE["text"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI", 10),
            wraplength=980,
            justify="left",
        ).pack(anchor="w", pady=(6, 16))
        tk.Label(
            info,
            text="Laufendes Angebot",
            fg=PALETTE["accent_two"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI Semibold", 11),
        ).pack(anchor="w")
        tk.Label(
            info,
            textvariable=self.customer_summary_var,
            fg=PALETTE["text"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI", 10),
            wraplength=980,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))
        tk.Label(
            info,
            textvariable=self.customer_hint_var,
            fg=PALETTE["muted"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI", 10),
            wraplength=980,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

    def setup_inventory_tab(self, parent, key, title):
        tk.Label(
            parent,
            text=title,
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Segoe UI Semibold", 13),
        ).pack(anchor="w", padx=16, pady=(16, 4))
        tk.Label(
            parent,
            text="Ein Klick wählt das Auto aus. Danach kannst du rechts direkt handeln.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=16, pady=(0, 10))
        wrap = tk.Frame(parent, bg=PALETTE["card"])
        wrap.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        shell = tk.Frame(
            wrap,
            bg=PALETTE["input_bg"],
            highlightbackground=PALETTE["line"],
            highlightthickness=1,
        )
        shell.pack(fill="both", expand=True)
        columns = (
            "ID",
            "Marke",
            "Typ",
            "KM",
            "Zustand",
            "Sauberkeit",
            "Schaden",
            "Energie",
            "Wert",
            "Haus",
            "Standort",
        )
        widths = {
            "ID": 70,
            "Marke": 130,
            "Typ": 90,
            "KM": 90,
            "Zustand": 90,
            "Sauberkeit": 95,
            "Schaden": 125,
            "Energie": 85,
            "Wert": 120,
            "Haus": 85,
            "Standort": 185,
        }
        tree = ttk.Treeview(
            shell,
            columns=columns,
            show="headings",
            style="Forge.Treeview",
            height=20,
        )
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=widths[column], anchor="center")
        tree.tag_configure("normal_even", background="#0a1324")
        tree.tag_configure("normal_odd", background="#0d182c")
        tree.tag_configure("premium_even", background="#1a1432")
        tree.tag_configure("premium_odd", background="#211842")
        tree.pack(side="left", fill="both", expand=True, padx=1, pady=1)
        tree.bind(
            "<<TreeviewSelect>>",
            lambda _event, table_key=key: self.on_table_select(table_key),
        )
        scrollbar = ttk.Scrollbar(shell, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        self.tables[key] = tree

    def setup_stats_tab(self, parent):
        grid = tk.Frame(parent, bg=PALETTE["card"])
        grid.pack(fill="x", padx=16, pady=16)
        for index in range(3):
            grid.grid_columnconfigure(index, weight=1)
        cards = [
            ("Kasse", "cash", PALETTE["accent"]),
            ("Noch bis zum Ziel", "goal_left", "#f59e0b"),
            ("Verkaufte Autos", "sold_count", "#ec4899"),
            ("Schadensfälle", "accident_count", PALETTE["warn"]),
            ("Ø Zustand", "durchschnitt_zustand", "#38bdf8"),
            ("Ø Sauberkeit", "durchschnitt_sauberkeit", "#10b981"),
            ("Ø PS", "durchschnitt_ps", "#2563eb"),
            ("Bestandswert", "bestandswert", "#22c55e"),
            ("Beliebteste Marke", "haeufigste_marke", "#f97316"),
        ]
        for idx, (label, key, accent) in enumerate(cards):
            self.stat_vars[key] = tk.StringVar(value="-")
            card = tk.Frame(
                grid,
                bg=PALETTE["card_alt"],
                highlightbackground=PALETTE["line"],
                highlightthickness=1,
            )
            card.grid(row=idx // 3, column=idx % 3, sticky="nsew", padx=6, pady=6)
            tk.Frame(card, bg=accent, height=3).pack(fill="x")
            tk.Label(
                card,
                text=label,
                fg=PALETTE["muted"],
                bg=PALETTE["card_alt"],
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor="w", padx=14, pady=(14, 4))
            tk.Label(
                card,
                textvariable=self.stat_vars[key],
                fg=PALETTE["text"],
                bg=PALETTE["card_alt"],
                font=("Bahnschrift", 18, "bold"),
            ).pack(anchor="w", padx=14, pady=(0, 14))
        analysis = tk.Frame(
            parent,
            bg=PALETTE["input_bg"],
            highlightbackground=PALETTE["line"],
            highlightthickness=1,
        )
        analysis.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        tk.Label(
            analysis,
            text="Kurzer Überblick",
            fg=PALETTE["text"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI Semibold", 12),
        ).pack(anchor="w", padx=14, pady=(14, 8))
        self.stats_text = tk.Text(
            analysis,
            height=12,
            bg=PALETTE["input_bg"],
            fg=PALETTE["text"],
            insertbackground=PALETTE["text"],
            relief="flat",
            font=("Consolas", 10),
            padx=14,
            pady=10,
        )
        self.stats_text.pack(fill="both", expand=True, padx=2, pady=(0, 2))

    def setup_editor_tab(self, parent):
        header = tk.Frame(parent, bg=PALETTE["card"])
        header.pack(fill="x", padx=18, pady=(18, 10))
        tk.Label(
            header,
            text="Auto bearbeiten",
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Bahnschrift", 18, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Hier kannst du Daten anpassen und auch Spielwerte wie Zustand oder Schaden geradeziehen.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        shell = tk.Frame(parent, bg=PALETTE["card"])
        shell.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        canvas = tk.Canvas(shell, bg=PALETTE["card"], highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(shell, orient="vertical", command=canvas.yview)
        grid = tk.Frame(canvas, bg=PALETTE["card"])
        window_id = canvas.create_window((0, 0), window=grid, anchor="nw")

        def sync_scrollregion(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def sync_width(event):
            canvas.itemconfigure(window_id, width=event.width)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        grid.bind("<Configure>", sync_scrollregion)
        canvas.bind("<Configure>", sync_width)
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for column in range(4):
            grid.grid_columnconfigure(column, weight=1, uniform="editor")
        grid.grid_rowconfigure(0, weight=1)

        editor_groups = [
            (
                "Stammdaten",
                [
                    ("Fahrzeug-ID", "fahrzeug_id", "entry"),
                    ("Marke", "marke", "combo"),
                    ("Farbe", "farbe", "combo"),
                    ("Besitzer", "besitzer", "combo"),
                ],
            ),
            (
                "Handel",
                [
                    ("Kategorie", "kategorie", "combo"),
                    ("Standort", "standort", "combo"),
                    ("Basispreis (EUR)", "preis", "entry"),
                    ("Baujahr", "baujahr", "entry"),
                ],
            ),
            (
                "Technik",
                [
                    ("Typ", "typ", "combo"),
                    ("Kilometer", "km", "entry"),
                    ("PS", "ps", "entry"),
                    ("MaxSpeed", "maxspeed", "entry"),
                    ("Energie", "energie", "entry"),
                ],
            ),
            (
                "Spielzustand",
                [
                    ("Zustand (%)", "zustand", "entry"),
                    ("Sauberkeit (%)", "sauberkeit", "entry"),
                    ("Schaden (0-3)", "schaden", "combo"),
                ],
            ),
        ]

        for column, (title, fields) in enumerate(editor_groups):
            self.build_editor_group(grid, column, title, fields)

    def build_editor_group(self, parent, column, title, fields):
        shell = tk.Frame(
            parent,
            bg=PALETTE["input_bg"],
            highlightbackground=PALETTE["line"],
            highlightthickness=1,
        )
        shell.grid(row=0, column=column, sticky="nsew", padx=6, pady=6)
        tk.Label(
            shell,
            text=title,
            fg=PALETTE["accent_two"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI Semibold", 10),
        ).pack(anchor="w", padx=10, pady=(10, 6))

        content = tk.Frame(shell, bg=PALETTE["input_bg"])
        content.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        canvas = tk.Canvas(content, bg=PALETTE["input_bg"], highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        panel = tk.Frame(canvas, bg=PALETTE["input_bg"])
        window_id = canvas.create_window((0, 0), window=panel, anchor="nw")

        def sync_scrollregion(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def sync_width(event):
            canvas.itemconfigure(window_id, width=event.width)

        panel.bind("<Configure>", sync_scrollregion)
        canvas.bind("<Configure>", sync_width)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for row, (label, key, kind) in enumerate(fields):
            if key not in self.form_vars:
                self.form_vars[key] = tk.StringVar()

            if key == "energie":
                tk.Label(
                    panel,
                    textvariable=self.energy_label_var,
                    fg="#cbd5e1",
                    bg=PALETTE["input_bg"],
                    font=("Segoe UI", 9, "bold"),
                ).grid(row=row, column=0, sticky="w", pady=5)
            else:
                tk.Label(
                    panel,
                    text=label,
                    fg="#cbd5e1",
                    bg=PALETTE["input_bg"],
                    font=("Segoe UI", 9, "bold"),
                ).grid(row=row, column=0, sticky="w", pady=5)

            if kind == "combo":
                widget = ttk.Combobox(
                    panel,
                    textvariable=self.form_vars[key],
                    values=self.field_values(key),
                    style="Forge.TCombobox",
                    width=18,
                )
                widget.bind("<<ComboboxSelected>>", self.on_form_mode_change)
            else:
                widget = tk.Entry(
                    panel,
                    textvariable=self.form_vars[key],
                    bg=PALETTE["card"],
                    fg=PALETTE["text"],
                    insertbackground=PALETTE["text"],
                    relief="flat",
                    font=("Segoe UI", 9),
                    width=18,
                )

            widget.grid(row=row, column=1, sticky="w", padx=(10, 0), pady=5, ipady=3)
            if key == "fahrzeug_id":
                widget.configure(state="readonly")
            if key == "standort":
                self.standort_combo = widget

        panel.grid_columnconfigure(1, weight=1)

    def setup_editor(self, parent):
        header = tk.Frame(parent, bg=PALETTE["card"])
        header.pack(fill="x", padx=18, pady=(18, 10))
        tk.Label(
            header,
            text="Gerade ausgewählt",
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Bahnschrift", 18, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            textvariable=self.selection_var,
            fg="#c4b5fd",
            bg=PALETTE["card"],
            font=("Segoe UI Semibold", 10),
        ).pack(anchor="w", pady=(6, 0))

        actions = tk.Frame(parent, bg=PALETTE["card"])
        actions.pack(fill="x", padx=18, pady=(0, 12))
        buttons = [
            ("Groß bearbeiten", self.open_editor_tab, PALETTE["accent"]),
            ("Kundenangebot", self.request_customer_offer, "#2563eb"),
            ("Speichern", self.save_vehicle_changes, "#4f46e5"),
            ("Verkaufen", self.sell_selected_vehicle, PALETTE["warn"]),
            ("Waschen", self.wash_selected_vehicle, PALETTE["accent_two"]),
            ("Warten", self.service_selected_vehicle, PALETTE["ok"]),
            ("Reparieren", self.repair_selected_vehicle, PALETTE["danger"]),
            ("Voll machen", self.fill_selected_vehicle, "#4f46e5"),
            ("Ins Log schreiben", self.log_selected_vehicle, "#475569"),
        ]
        for text, command, color in buttons:
            self.make_button(actions, text, command, color).pack(fill="x", pady=4)

        shell = tk.Frame(
            parent,
            bg=PALETTE["input_bg"],
            highlightbackground=PALETTE["line"],
            highlightthickness=1,
        )
        shell.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        info = tk.Frame(shell, bg=PALETTE["input_bg"])
        info.pack(fill="both", expand=True, padx=14, pady=14)
        tk.Label(
            info,
            text="Das Auto im Kurzprofil",
            fg=PALETTE["accent_two"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI Semibold", 12),
        ).pack(anchor="w")
        tk.Label(
            info,
            text="Hier siehst du direkt, wie schlimm es schon um den Wagen steht und ob sich ein Verkauf lohnt.",
            fg=PALETTE["muted"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI", 10),
            wraplength=300,
            justify="left",
        ).pack(anchor="w", pady=(8, 16))

        summary = tk.Frame(
            info,
            bg=PALETTE["card"],
            highlightbackground=PALETTE["line"],
            highlightthickness=1,
        )
        summary.pack(fill="x")
        tk.Label(
            summary,
            text="Ausgewähltes Auto",
            fg="#cbd5e1",
            bg=PALETTE["card"],
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=12, pady=(12, 4))
        tk.Label(
            summary,
            textvariable=self.selection_var,
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
            wraplength=300,
            justify="left",
        ).pack(anchor="w", padx=12, pady=(0, 12))

        details = tk.Frame(summary, bg=PALETTE["card"])
        details.pack(fill="x", padx=12, pady=(0, 12))
        rows = [
            ("Verkaufswert", "wert"),
            ("Zustand", "zustand"),
            ("Sauberkeit", "sauberkeit"),
            ("Schaden", "schaden"),
            ("Letzte Fahrt", "letzte_fahrt"),
        ]
        for label, key in rows:
            row = tk.Frame(details, bg=PALETTE["card"])
            row.pack(fill="x", pady=2)
            tk.Label(
                row,
                text=label,
                fg=PALETTE["muted"],
                bg=PALETTE["card"],
                font=("Segoe UI", 9, "bold"),
            ).pack(anchor="w")
            tk.Label(
                row,
                textvariable=self.detail_vars[key],
                fg=PALETTE["text"],
                bg=PALETTE["card"],
                font=("Segoe UI", 9),
                wraplength=290,
                justify="left",
            ).pack(anchor="w", pady=(1, 4))
        self.clear_editor()

    def setup_log(self):
        shell = self.make_card(self.root)
        shell.pack(fill="x", padx=18, pady=(2, 18))
        header = tk.Frame(shell, bg=PALETTE["card"])
        header.pack(fill="x", padx=18, pady=(16, 8))
        tk.Label(
            header,
            text="Log und Tageskram",
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Bahnschrift", 16, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Hier landet alles, was im Autohaus so passiert.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))
        log_shell = tk.Frame(shell, bg=PALETTE["input_bg"], highlightbackground=PALETTE["line"], highlightthickness=1)
        log_shell.pack(fill="x", padx=18, pady=(0, 18))
        self.log = tk.Text(
            log_shell,
            height=8,
            bg=PALETTE["input_bg"],
            fg=PALETTE["text"],
            insertbackground=PALETTE["text"],
            relief="flat",
            font=("Consolas", 10),
            padx=14,
            pady=12,
        )
        self.log.pack(fill="x")
        gui_print(
            self.log,
            "App gestartet. Starte ein neues Spiel oder baue deinen Bestand direkt auf.",
        )

    def field_values(self, key):
        if key == "marke":
            return MARKEN
        if key == "farbe":
            return [name for name, _ in FARBEN]
        if key == "besitzer":
            return BESITZER
        if key == "kategorie":
            return ["Normal", "Premium"]
        if key == "typ":
            return ["Benzin", "Elektro"]
        if key == "standort":
            return ALLE_AUTOHAEUSER
        if key == "schaden":
            return ["0", "1", "2", "3"]
        return []

    def _read_offer_target(self):
        try:
            return int(self.anzahl_entry.get())
        except ValueError:
            return None

    def generieren(self):
        anzahl = self._read_offer_target()
        if anzahl is None:
            gui_print(self.log, "Bitte bei den Angeboten nur ganze Zahlen eingeben.")
            return
        if anzahl < 4 or anzahl > 20:
            gui_print(self.log, "Nimm bitte eine Zahl zwischen 4 und 20.")
            return
        self.garage.start_new_game()
        self.selected_vehicle = None
        self.selected_offer = None
        self.market_offers = []
        clearlog(self.log)
        gui_print(
            self.log,
            f"Neues Spiel gestartet. Ich habe dir {anzahl} Angebote auf den Markt gelegt.",
        )
        gui_print(
            self.log,
            (
                f"Startkapital: {self.format_currency(self.garage.cash)} | "
                f"Ziel: {self.format_currency(self.garage.target_cash)}"
            ),
        )
        self.fill_market_offers(anzahl)
        self.refresh_all_views()
        self.clear_editor()
        gui_print(
            self.log,
            "Der Bestand ist am Anfang leer. Du musst jetzt clever einkaufen.",
        )

    def create_random_vehicle(self):
        marke = random.choice(MARKEN)
        farbe, _ = random.choice(FARBEN)
        besitzer = random.choice(BESITZER)
        premium = marke in PREMIUM_MARKEN or random.random() < 0.18
        elektrisch = (
            marke in {"Tesla", "Lucid", "Rimac", "Polestar", "BYD"}
            or random.random() < 0.32
        )
        if premium:
            preis = random.randint(65000, 420000)
            ps = random.randint(220, 900)
            maxspeed = random.randint(220, 360)
            baujahr = random.randint(2018, 2026)
            standort = random.choice(PREMIUM_AUTOHAUS)
            km = random.randint(0, 95000)
        else:
            preis = random.randint(8000, 78000)
            ps = random.randint(75, 380)
            maxspeed = random.randint(150, 260)
            baujahr = random.randint(1998, 2026)
            standort = random.choice(AUTOHAUS)
            km = random.randint(0, 220000)
        zustand = random.randint(58, 100) if not premium else random.randint(68, 100)
        sauberkeit = random.randint(45, 100)
        schaden = random.choices([0, 1, 2], weights=[78, 18, 4], k=1)[0]
        if elektrisch:
            return ElektroAuto(
                config=self.config,
                marke=marke,
                farbe=farbe,
                km=km,
                ps=ps,
                maxspeed=maxspeed,
                batterie=random.randint(18, self.config.MAX_BATTERIE),
                besitzer=besitzer,
                preis=preis + random.randint(4000, 28000),
                baujahr=max(2016, baujahr),
                standort=standort,
                premium=premium,
                zustand=zustand,
                sauberkeit=sauberkeit,
                schaden=schaden,
            )

        return Auto(
            config=self.config,
            marke=marke,
            farbe=farbe,
            km=km,
            ps=ps,
            maxspeed=maxspeed,
            tank=random.randint(8, self.config.MAX_TANK),
            besitzer=besitzer,
            preis=preis,
            baujahr=baujahr,
            standort=standort,
            premium=premium,
            zustand=zustand,
            sauberkeit=sauberkeit,
            schaden=schaden,
        )

    def build_market_offer(self):
        fahrzeug = self.create_random_vehicle()

        if fahrzeug.schaden > 0 or fahrzeug.sauberkeit < 65 or fahrzeug.zustand < 72:
            faktor = random.uniform(0.72, 0.92)
        else:
            faktor = random.uniform(0.88, 1.05)

        ankauf = max(1_500, round(fahrzeug.verkaufswert * faktor))
        differenz = fahrzeug.verkaufswert - ankauf
        if differenz >= 8_000:
            deal = "Stark"
        elif differenz >= 2_000:
            deal = "Fair"
        else:
            deal = "Hart"

        return {
            "vehicle": fahrzeug,
            "ankauf": ankauf,
            "deal": deal,
            "differenz": differenz,
        }

    def fill_market_offers(self, target_count):
        while len(self.market_offers) < target_count:
            self.market_offers.append(self.build_market_offer())

    def update_market_table(self):
        if self.market_tree is None:
            return

        clear_table(self.market_tree)
        selected_id = (
            str(self.selected_offer["vehicle"].fahrzeug_id)
            if self.selected_offer is not None
            else None
        )
        for offer in self.market_offers:
            fahrzeug = offer["vehicle"]
            if offer["deal"] == "Stark":
                tag = "deal_good"
            elif offer["deal"] == "Fair":
                tag = "deal_ok"
            else:
                tag = "deal_hard"

            self.market_tree.insert(
                "",
                "end",
                iid=str(fahrzeug.fahrzeug_id),
                values=(
                    fahrzeug.fahrzeug_id,
                    fahrzeug.marke,
                    fahrzeug.typ,
                    fahrzeug.zustand_label,
                    fahrzeug.sauberkeit_label,
                    fahrzeug.schaden_label,
                    self.format_currency(offer["ankauf"]),
                    offer["deal"],
                    fahrzeug.standort,
                ),
                tags=(tag,),
            )

        if selected_id and self.market_tree.exists(selected_id):
            self.market_tree.selection_set(selected_id)
            self.market_tree.focus(selected_id)
            self.market_tree.see(selected_id)
        elif self.selected_offer is not None:
            self.selected_offer = None
            self.market_summary_var.set("Noch kein Angebot ausgewählt")
            self.market_hint_var.set("Klick im Markt auf ein Fahrzeug, um den Deal zu prüfen.")
        elif not self.market_offers:
            self.market_summary_var.set("Gerade sind keine Angebote im Markt.")
            self.market_hint_var.set("Starte ein neues Spiel oder frische den Markt auf.")
        else:
            self.market_summary_var.set("Noch kein Angebot ausgewählt")
            self.market_hint_var.set("Klick im Markt auf ein Fahrzeug, um den Deal zu prüfen.")

    def refresh_all_views(self):
        self.update_market_table()
        self.update_table("all", self.garage.alle_fahrzeuge())
        self.update_table("normal", self.garage.filter_normal())
        self.update_table("premium", self.garage.filter_premium())
        self.refresh_statistics()
        self.update_tab_titles()
        stats = self.garage.statistik()
        self.summary_var.set(
            (
                f"Tag {stats['tag']} | "
                f"Kasse {self.format_currency(stats['cash'])} | "
                f"Bestand {stats['gesamt']} Autos | "
                f"Markt {len(self.market_offers)} Angebote | "
                f"Inventarwert {self.format_currency(stats['bestandswert'])}"
            )
        )
        if self.selected_vehicle is not None:
            if self.selected_vehicle in self.garage.fahrzeuge:
                self.fill_editor(self.selected_vehicle)
            else:
                self.selected_vehicle = None
                self.clear_editor()
        if (
            self.customer_offer is not None
            and self.customer_offer["vehicle"] not in self.garage.fahrzeuge
        ):
            self.customer_offer = None
        self.refresh_customer_panel()

    def update_table(self, key, fahrzeuge):
        tree = self.tables[key]
        clear_table(tree)
        selected_id = str(self.selected_vehicle.fahrzeug_id) if self.selected_vehicle else None
        for index, fahrzeug in enumerate(fahrzeuge):
            prefix = "premium" if fahrzeug.premium else "normal"
            suffix = "even" if index % 2 == 0 else "odd"
            tree.insert(
                "",
                "end",
                iid=str(fahrzeug.fahrzeug_id),
                values=(
                    fahrzeug.fahrzeug_id,
                    fahrzeug.marke,
                    fahrzeug.typ,
                    fahrzeug.km,
                    fahrzeug.zustand_label,
                    fahrzeug.sauberkeit_label,
                    fahrzeug.schaden_label,
                    fahrzeug.energie_label,
                    fahrzeug.verkaufswert_label,
                    fahrzeug.haus_label,
                    fahrzeug.standort,
                ),
                tags=(f"{prefix}_{suffix}",),
            )
        if selected_id and tree.exists(selected_id):
            tree.selection_set(selected_id)
            tree.focus(selected_id)
            tree.see(selected_id)

    def update_tab_titles(self):
        self.notebook.tab(
            self.tab_frames["market"],
            text=f"Einkaufen ({len(self.market_offers)})",
        )
        kunden_label = "Kunden *" if self.customer_offer is not None else "Kunden"
        self.notebook.tab(self.tab_frames["customers"], text=kunden_label)
        self.notebook.tab(self.tab_frames["all"], text=f"Alle Autos ({len(self.garage.alle_fahrzeuge())})")
        self.notebook.tab(self.tab_frames["normal"], text=f"Normale ({len(self.garage.filter_normal())})")
        self.notebook.tab(self.tab_frames["premium"], text=f"Premium ({len(self.garage.filter_premium())})")

    def refresh_statistics(self):
        stats = self.garage.statistik()
        self.header_stat_vars["tag"].set(str(stats["tag"]))
        self.header_stat_vars["cash"].set(self.short_currency(stats["cash"]))
        self.header_stat_vars["gesamt"].set(str(stats["gesamt"]))
        self.header_stat_vars["premium"].set(str(stats["premium"]))
        self.header_stat_vars["elektro"].set(str(stats["elektro"]))
        self.header_stat_vars["goal_left"].set(self.short_currency(stats["goal_left"]))
        self.stat_vars["cash"].set(self.format_currency(stats["cash"]))
        self.stat_vars["goal_left"].set(self.format_currency(stats["goal_left"]))
        self.stat_vars["sold_count"].set(str(stats["sold_count"]))
        self.stat_vars["accident_count"].set(str(stats["accident_count"]))
        self.stat_vars["durchschnitt_zustand"].set(f"{stats['durchschnitt_zustand']}%")
        self.stat_vars["durchschnitt_sauberkeit"].set(f"{stats['durchschnitt_sauberkeit']}%")
        self.stat_vars["durchschnitt_ps"].set(f"{stats['durchschnitt_ps']} PS")
        self.stat_vars["bestandswert"].set(self.format_currency(stats["bestandswert"]))
        self.stat_vars["haeufigste_marke"].set(stats["haeufigste_marke"])
        teuerstes = stats["teuerstes_auto"]
        lines = [
            f"Tag: {stats['tag']}",
            f"Kasse: {self.format_currency(stats['cash'])}",
            f"Bis zum Ziel fehlen: {self.format_currency(stats['goal_left'])}",
            f"Bestand: {stats['gesamt']} Autos",
            f"Schadensfälle im Hof: {stats['schadensfaelle']}",
            f"Durchschnitt Kilometer: {stats['durchschnitt_km']}",
            f"Durchschnitt Zustand: {stats['durchschnitt_zustand']}%",
            f"Durchschnitt Sauberkeit: {stats['durchschnitt_sauberkeit']}%",
            f"Am häufigsten im Hof: {stats['haeufigste_marke']}",
        ]
        if teuerstes is not None:
            lines.append(
                f"Teuerstes Auto gerade: #{teuerstes.fahrzeug_id} "
                f"{teuerstes.marke} mit {teuerstes.verkaufswert_label}"
            )
        else:
            lines.append("Teuerstes Auto gerade: -")
        self.stats_text.configure(state="normal")
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, "\n".join(lines))
        self.stats_text.configure(state="disabled")

    def on_market_select(self, _event=None):
        if self.market_tree is None:
            return

        selection = self.market_tree.selection()
        if not selection:
            return

        fahrzeug_id = int(selection[0])
        for offer in self.market_offers:
            if offer["vehicle"].fahrzeug_id == fahrzeug_id:
                self.selected_offer = offer
                break
        else:
            return

        fahrzeug = self.selected_offer["vehicle"]
        self.market_summary_var.set(
            (
                f"#{fahrzeug.fahrzeug_id} | {fahrzeug.marke} | {fahrzeug.typ} | "
                f"Ankauf {self.format_currency(self.selected_offer['ankauf'])}"
            )
        )
        self.market_hint_var.set(
            (
                f"Deal-Eindruck: {self.selected_offer['deal']} | "
                f"Zustand {fahrzeug.zustand_label} | "
                f"Sauberkeit {fahrzeug.sauberkeit_label} | "
                f"Schaden {fahrzeug.schaden_label} | "
                f"{fahrzeug.km} km"
            )
        )

    def reject_selected_offer(self):
        if self.selected_offer is None:
            gui_print(self.log, "Bitte zuerst ein Angebot im Einkauf-Tab auswählen.")
            return

        fahrzeug = self.selected_offer["vehicle"]
        self.market_offers = [
            offer
            for offer in self.market_offers
            if offer["vehicle"].fahrzeug_id != fahrzeug.fahrzeug_id
        ]
        self.selected_offer = None
        self.refresh_all_views()
        gui_print(
            self.log,
            f"Angebot für #{fahrzeug.fahrzeug_id} {fahrzeug.marke} ausgeschlagen.",
        )

    def refresh_customer_panel(self):
        if self.customer_offer is None:
            self.customer_summary_var.set("Noch kein Kundenangebot aktiv")
            if self.selected_vehicle is None:
                self.customer_hint_var.set(
                    "Wähle links ein eigenes Auto aus und hol dir dann ein Angebot."
                )
            else:
                self.customer_hint_var.set(
                    f"Für #{self.selected_vehicle.fahrzeug_id} {self.selected_vehicle.marke} kannst du jetzt ein Angebot holen."
                )
            return

        angebot = self.customer_offer
        fahrzeug = angebot["vehicle"]
        self.customer_summary_var.set(
            (
                f"{angebot['customer']} ({angebot['profile']}) bietet dir "
                f"{self.format_currency(angebot['offer'])} für "
                f"#{fahrzeug.fahrzeug_id} {fahrzeug.marke}."
            )
        )
        self.customer_hint_var.set(
            (
                f"Runde {angebot['rounds']}/{angebot['max_rounds']} | "
                f"Stimmung: {angebot['mood']} | "
                f"Zustand {fahrzeug.zustand_label} | "
                f"Schaden {fahrzeug.schaden_label}"
            )
        )

    def on_table_select(self, table_key):
        selection = self.tables[table_key].selection()
        if not selection:
            return
        fahrzeug = self.garage.get_fahrzeug_by_id(selection[0])
        if fahrzeug is None:
            return
        for key, tree in self.tables.items():
            if key == table_key:
                continue
            for item in tree.selection():
                tree.selection_remove(item)
        self.selected_vehicle = fahrzeug
        self.fill_editor(fahrzeug)

    def fill_editor(self, fahrzeug):
        self.selection_var.set(
            f"#{fahrzeug.fahrzeug_id} | {fahrzeug.marke} | {fahrzeug.haus_label} | {fahrzeug.standort}"
        )
        values = {
            "fahrzeug_id": fahrzeug.fahrzeug_id,
            "marke": fahrzeug.marke,
            "farbe": fahrzeug.farbe,
            "besitzer": fahrzeug.besitzer,
            "kategorie": fahrzeug.haus_label,
            "typ": fahrzeug.typ,
            "standort": fahrzeug.standort,
            "preis": fahrzeug.preis,
            "baujahr": fahrzeug.baujahr,
            "km": fahrzeug.km,
            "ps": fahrzeug.ps,
            "maxspeed": fahrzeug.maxspeed,
            "energie": fahrzeug.tank,
            "zustand": fahrzeug.zustand,
            "sauberkeit": fahrzeug.sauberkeit,
            "schaden": fahrzeug.schaden,
        }
        for key, value in values.items():
            self.form_vars[key].set(str(value))

        self.detail_vars["wert"].set(fahrzeug.verkaufswert_label)
        self.detail_vars["zustand"].set(fahrzeug.zustand_label)
        self.detail_vars["sauberkeit"].set(fahrzeug.sauberkeit_label)
        self.detail_vars["schaden"].set(fahrzeug.schaden_label)
        self.detail_vars["letzte_fahrt"].set(fahrzeug.letzte_fahrt)
        self.on_form_mode_change()

    def clear_editor(self):
        self.selection_var.set("Kein Auto ausgewählt")
        defaults = {
            "fahrzeug_id": "",
            "marke": "",
            "farbe": "",
            "besitzer": "",
            "kategorie": "Normal",
            "typ": "Benzin",
            "standort": AUTOHAUS[0],
            "preis": "",
            "baujahr": "",
            "km": "",
            "ps": "",
            "maxspeed": "",
            "energie": "",
            "zustand": "",
            "sauberkeit": "",
            "schaden": "0",
        }
        for key, value in defaults.items():
            if key in self.form_vars:
                self.form_vars[key].set(value)

        for variable in self.detail_vars.values():
            variable.set("-")
        self.on_form_mode_change()

    def on_form_mode_change(self, _event=None):
        typ = self.form_vars["typ"].get() or "Benzin"
        kategorie = self.form_vars["kategorie"].get() or "Normal"
        self.energy_label_var.set("Batterie (%)" if typ == "Elektro" else "Tank (L)")
        standorte = PREMIUM_AUTOHAUS if kategorie == "Premium" else AUTOHAUS
        self.standort_combo.configure(values=standorte)
        if self.form_vars["standort"].get() not in standorte:
            self.form_vars["standort"].set(standorte[0])

    def save_vehicle_changes(self):
        if self.selected_vehicle is None:
            gui_print(self.log, "Bitte zuerst ein Fahrzeug in einer Tabelle auswählen.")
            return
        try:
            self.selected_vehicle.update_daten(
                marke=self.form_vars["marke"].get().strip() or self.selected_vehicle.marke,
                farbe=self.form_vars["farbe"].get().strip() or self.selected_vehicle.farbe,
                km=int(self.form_vars["km"].get()),
                ps=int(self.form_vars["ps"].get()),
                maxspeed=int(self.form_vars["maxspeed"].get()),
                energie=int(self.form_vars["energie"].get()),
                besitzer=self.form_vars["besitzer"].get().strip() or self.selected_vehicle.besitzer,
                preis=int(self.form_vars["preis"].get()),
                baujahr=int(self.form_vars["baujahr"].get()),
                standort=self.form_vars["standort"].get().strip() or self.selected_vehicle.standort,
                premium=self.form_vars["kategorie"].get() == "Premium",
                elektrisch=self.form_vars["typ"].get() == "Elektro",
                zustand=int(self.form_vars["zustand"].get()),
                sauberkeit=int(self.form_vars["sauberkeit"].get()),
                schaden=int(self.form_vars["schaden"].get()),
            )
        except ValueError:
            gui_print(
                self.log,
                "Preis, Baujahr, Kilometer, PS, MaxSpeed, Energie und Spielwerte brauchen gültige Zahlen.",
            )
            return
        self.refresh_all_views()
        gui_print(
            self.log,
            (
                f"Auto #{self.selected_vehicle.fahrzeug_id} gespeichert. "
                f"Neuer Verkaufswert: {self.selected_vehicle.verkaufswert_label}"
            ),
        )

    def open_editor_tab(self):
        self.notebook.select(self.tab_frames["editor"])

    def ensure_vehicle_selected(self):
        if self.selected_vehicle is None:
            gui_print(self.log, "Bitte zuerst ein Fahrzeug in einer Tabelle auswählen.")
            return False
        return True

    def refresh_market_offers(self):
        ziel = self._read_offer_target()
        if ziel is None:
            ziel = 8
        if self.market_offers:
            refresh_kosten = 750 + len(self.market_offers) * 35
            if self.garage.cash < refresh_kosten:
                gui_print(
                    self.log,
                    f"Zum Auffrischen des Markts fehlen dir {self.format_currency(refresh_kosten)}.",
                )
                return
            self.garage.cash -= refresh_kosten
            gui_print(
                self.log,
                f"Markt neu gewürfelt. Kosten: {self.format_currency(refresh_kosten)}",
            )
        else:
            gui_print(self.log, "Ich baue dir einen frischen Markt auf.")

        ziel = max(4, min(20, ziel))
        self.market_offers = []
        self.selected_offer = None
        self.fill_market_offers(ziel)
        self.refresh_all_views()

    def build_customer_offer(self, fahrzeug):
        profiles = [
            {
                "profile": "Schnäppchenjäger",
                "mood": "vorsichtig",
                "start": (0.68, 0.82),
                "max": (0.84, 0.96),
                "max_rounds": 2,
            },
            {
                "profile": "Alltagsfahrer",
                "mood": "okay drauf",
                "start": (0.78, 0.92),
                "max": (0.92, 1.02),
                "max_rounds": 3,
            },
            {
                "profile": "Markenfan",
                "mood": "ziemlich interessiert",
                "start": (0.86, 0.98),
                "max": (0.98, 1.08),
                "max_rounds": 3,
            },
        ]
        if fahrzeug.premium:
            profiles.append(
                {
                    "profile": "Sammler",
                    "mood": "heiß auf das Auto",
                    "start": (0.92, 1.02),
                    "max": (1.04, 1.16),
                    "max_rounds": 4,
                }
            )

        profil = random.choice(profiles)
        marktwert = fahrzeug.verkaufswert
        start_ratio = random.uniform(*profil["start"])
        max_ratio = random.uniform(*profil["max"])

        if fahrzeug.schaden >= 2:
            start_ratio -= 0.05
            max_ratio -= 0.06
        if fahrzeug.sauberkeit < 50:
            start_ratio -= 0.03
        if fahrzeug.zustand > 90 and fahrzeug.sauberkeit > 85:
            max_ratio += 0.02

        start_price = max(1_000, round(marktwert * max(0.55, start_ratio)))
        max_price = max(start_price, round(marktwert * max(0.68, max_ratio)))

        return {
            "vehicle": fahrzeug,
            "customer": random.choice(BESITZER),
            "profile": profil["profile"],
            "mood": profil["mood"],
            "offer": start_price,
            "max_price": max_price,
            "rounds": 0,
            "max_rounds": profil["max_rounds"],
        }

    def request_customer_offer(self):
        if not self.ensure_vehicle_selected():
            return

        self.customer_offer = self.build_customer_offer(self.selected_vehicle)
        self.notebook.select(self.tab_frames["customers"])
        self.refresh_all_views()
        angebot = self.customer_offer
        gui_print(
            self.log,
            (
                f"{angebot['customer']} möchte #{self.selected_vehicle.fahrzeug_id} "
                f"{self.selected_vehicle.marke} und startet mit "
                f"{self.format_currency(angebot['offer'])}."
            ),
        )

    def negotiate_customer_offer(self):
        if self.customer_offer is None:
            gui_print(self.log, "Es gibt gerade kein Kundenangebot zum Verhandeln.")
            return

        angebot = self.customer_offer
        fahrzeug = angebot["vehicle"]
        if angebot["rounds"] >= angebot["max_rounds"]:
            gui_print(
                self.log,
                f"{angebot['customer']} hat keine Lust mehr zu verhandeln und ist weg.",
            )
            self.customer_offer = None
            self.refresh_all_views()
            return

        gap = max(0, angebot["max_price"] - angebot["offer"])
        leave_chance = 0.12 + angebot["rounds"] * 0.14
        if gap < max(1_000, fahrzeug.verkaufswert * 0.05):
            leave_chance += 0.18

        angebot["rounds"] += 1
        if random.random() < leave_chance and gap < fahrzeug.verkaufswert * 0.14:
            gui_print(
                self.log,
                f"{angebot['customer']} findet dein Nachverhandeln zu hart und geht.",
            )
            self.customer_offer = None
            self.refresh_all_views()
            return

        erhöhung = max(250, round(gap * random.uniform(0.35, 0.7)))
        neues_angebot = min(angebot["max_price"], angebot["offer"] + erhöhung)
        delta = neues_angebot - angebot["offer"]
        angebot["offer"] = neues_angebot
        angebot["mood"] = random.choice(
            ["noch dabei", "leicht genervt", "zäh aber interessiert"]
        )
        self.refresh_all_views()
        gui_print(
            self.log,
            (
                f"{angebot['customer']} legt nach: +{self.format_currency(delta)} | "
                f"neues Angebot {self.format_currency(angebot['offer'])}"
            ),
        )

    def accept_customer_offer(self):
        if self.customer_offer is None:
            gui_print(self.log, "Es gibt gerade kein Kundenangebot zum Annehmen.")
            return

        angebot = self.customer_offer
        fahrzeug = angebot["vehicle"]
        preis = self.garage.sell_vehicle(fahrzeug, angebot["offer"])
        if self.selected_vehicle == fahrzeug:
            self.selected_vehicle = None
        self.customer_offer = None
        self.refresh_all_views()
        self.clear_editor()
        gui_print(
            self.log,
            (
                f"Deal mit {angebot['customer']} abgeschlossen. "
                f"#{fahrzeug.fahrzeug_id} verkauft für {self.format_currency(preis)}."
            ),
        )

    def reject_customer_offer(self):
        if self.customer_offer is None:
            gui_print(self.log, "Es gibt gerade kein Kundenangebot zum Ablehnen.")
            return

        kunde = self.customer_offer["customer"]
        fahrzeug = self.customer_offer["vehicle"]
        self.customer_offer = None
        self.refresh_all_views()
        gui_print(
            self.log,
            f"Angebot von {kunde} für #{fahrzeug.fahrzeug_id} {fahrzeug.marke} abgelehnt.",
        )

    def buy_selected_offer(self):
        if self.selected_offer is None:
            gui_print(self.log, "Bitte zuerst ein Angebot im Einkauf-Tab auswählen.")
            return

        fahrzeug = self.selected_offer["vehicle"]
        erfolgreich, preis = self.garage.buy_vehicle(
            fahrzeug,
            self.selected_offer["ankauf"],
        )
        if not erfolgreich:
            gui_print(
                self.log,
                f"Für #{fahrzeug.fahrzeug_id} fehlen dir {self.format_currency(preis)}.",
            )
            return

        self.market_offers = [
            offer
            for offer in self.market_offers
            if offer["vehicle"].fahrzeug_id != fahrzeug.fahrzeug_id
        ]
        self.selected_offer = None
        self.selected_vehicle = fahrzeug
        self.refresh_all_views()
        gui_print(
            self.log,
            (
                f"Auto #{fahrzeug.fahrzeug_id} eingekauft für {self.format_currency(preis)}. "
                f"Aktueller Marktwert: {fahrzeug.verkaufswert_label}"
            ),
        )

    def next_day(self):
        report = self.garage.advance_day()
        ziel = self._read_offer_target() or 8
        self.fill_market_offers(max(4, min(20, ziel)))
        self.customer_offer = None
        self.refresh_all_views()

        gui_print(
            self.log,
            (
                f"Tag {report['day']} abgeschlossen. "
                f"{report['gesamt_km']} km gefahren | "
                f"Wertverlust {self.format_currency(report['wertverlust'])} | "
                f"Unfälle {report['unfaelle']}"
            ),
        )
        if not report["events"]:
            gui_print(self.log, "Noch kein eigenes Auto auf dem Hof. Heute war nur Marktbeobachtung.")
        for event in report["events"][:6]:
            fahrzeug = event["fahrzeug"]
            line = (
                f"#{fahrzeug.fahrzeug_id} {fahrzeug.marke}: "
                f"{event['fahrt']} mit {event['km']} km, "
                f"Wertverlust {self.format_currency(event['wertverlust'])}"
            )
            if event["unfall"] is not None:
                line += f" | Unfall: {event['unfall']}"
            gui_print(self.log, line)

    def sell_selected_vehicle(self):
        if not self.ensure_vehicle_selected():
            return

        fahrzeug = self.selected_vehicle
        preis = self.garage.sell_vehicle(fahrzeug)
        self.selected_vehicle = None
        self.refresh_all_views()
        self.clear_editor()
        gui_print(
            self.log,
            (
                f"Auto #{fahrzeug.fahrzeug_id} verkauft. "
                f"Erlös: {self.format_currency(preis)}"
            ),
        )

    def wash_selected_vehicle(self):
        if not self.ensure_vehicle_selected():
            return

        erfolgreich, kosten, plus = self.garage.wash_vehicle(self.selected_vehicle)
        if not erfolgreich:
            gui_print(self.log, f"Zum Waschen fehlen dir {self.format_currency(kosten)}.")
            return

        self.refresh_all_views()
        gui_print(
            self.log,
            (
                f"Auto #{self.selected_vehicle.fahrzeug_id} gewaschen. "
                f"Sauberkeit +{plus}% | Kosten {self.format_currency(kosten)}"
            ),
        )

    def service_selected_vehicle(self):
        if not self.ensure_vehicle_selected():
            return

        erfolgreich, kosten, plus = self.garage.service_vehicle(self.selected_vehicle)
        if not erfolgreich:
            gui_print(self.log, f"Für die Wartung fehlen dir {self.format_currency(kosten)}.")
            return

        self.refresh_all_views()
        gui_print(
            self.log,
            (
                f"Auto #{self.selected_vehicle.fahrzeug_id} gewartet. "
                f"Zustand +{plus}% | Kosten {self.format_currency(kosten)}"
            ),
        )

    def repair_selected_vehicle(self):
        if not self.ensure_vehicle_selected():
            return

        erfolgreich, kosten, report = self.garage.repair_vehicle(self.selected_vehicle)
        if not erfolgreich:
            gui_print(self.log, f"Für die Reparatur fehlen dir {self.format_currency(kosten)}.")
            return

        self.refresh_all_views()
        gui_print(
            self.log,
            (
                f"Auto #{self.selected_vehicle.fahrzeug_id} repariert. "
                f"Schaden {report['schaden_vorher']} -> {report['schaden_nachher']} | "
                f"Zustand +{report['zustand_plus']}% | "
                f"Kosten {self.format_currency(kosten)}"
            ),
        )

    def fill_selected_vehicle(self):
        if not self.ensure_vehicle_selected():
            return

        erfolgreich, kosten = self.garage.refill_vehicle(self.selected_vehicle)
        if not erfolgreich:
            gui_print(self.log, f"Zum Auffüllen fehlen dir {self.format_currency(kosten)}.")
            return

        self.refresh_all_views()
        gui_print(
            self.log,
            (
                f"Auto #{self.selected_vehicle.fahrzeug_id} wurde aufgefüllt. "
                f"Kosten {self.format_currency(kosten)}"
            ),
        )

    def log_selected_vehicle(self):
        if not self.ensure_vehicle_selected():
            return
        gui_print(self.log, self.selected_vehicle.status_text())

    def clear_inventory(self):
        self.garage.clear()
        self.selected_vehicle = None
        clearlog(self.log)
        gui_print(self.log, "Der Hof ist leer. Kasse und Tag bleiben so, wie sie gerade sind.")
        self.refresh_all_views()
        self.clear_editor()

    def tanken_alle(self):
        if not self.garage.fahrzeuge:
            gui_print(self.log, "Es gibt noch keine Fahrzeuge.")
            return

        count, kosten, uebersprungen = self.garage.tanken_alle()
        self.refresh_all_views()
        gui_print(
            self.log,
            (
                f"{count} Benziner aufgefüllt | "
                f"Kosten {self.format_currency(kosten)} | "
                f"wegen Geld übersprungen: {uebersprungen}"
            ),
        )

    def laden_alle(self):
        if not self.garage.fahrzeuge:
            gui_print(self.log, "Es gibt noch keine Fahrzeuge.")
            return

        count, kosten, uebersprungen = self.garage.laden_alle()
        self.refresh_all_views()
        gui_print(
            self.log,
            (
                f"{count} Elektroautos geladen | "
                f"Kosten {self.format_currency(kosten)} | "
                f"wegen Geld übersprungen: {uebersprungen}"
            ),
        )

    def status_alle(self):
        if not self.garage.fahrzeuge:
            gui_print(self.log, "Es gibt noch keine Fahrzeuge.")
            return
        stats = self.garage.statistik()
        gui_print(
            self.log,
            (
                f"Status | Tag {stats['tag']} | "
                f"Kasse: {self.format_currency(stats['cash'])} | "
                f"Bestand: {stats['gesamt']} | "
                f"Bestandswert: {self.format_currency(stats['bestandswert'])} | "
                f"Verkäufe: {stats['sold_count']}"
            ),
        )
        for status in self.garage.status_bericht():
            gui_print(self.log, status)

    @staticmethod
    def make_card(parent, width=None, pad=18):
        return tk.Frame(parent, bg=PALETTE["card"], highlightbackground=PALETTE["line"], highlightthickness=1, width=width)

    @staticmethod
    def make_button(parent, text, command, bg):
        return tk.Button(parent, text=text, command=command, bg=bg, fg="#ffffff", activebackground=bg, activeforeground="#ffffff", relief="flat", padx=16, pady=8, cursor="hand2", font=("Segoe UI Semibold", 10))

    @staticmethod
    def format_currency(value):
        return f"{value:,.0f} EUR".replace(",", ".")

    @staticmethod
    def short_currency(value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f} Mio"
        if value >= 1_000:
            return f"{value / 1_000:.0f} Tsd"
        return str(value)
