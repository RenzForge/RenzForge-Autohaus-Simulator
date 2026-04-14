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
        self.selected_vehicle = None
        self.logo_image = None
        self.summary_var = tk.StringVar(value="Noch kein Bestand geladen.")
        self.selection_var = tk.StringVar(value="Kein Auto ausgewählt")
        self.energy_label_var = tk.StringVar(value="Tank (L)")
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
            text="Ein kleines Tool zum Sortieren, Anschauen und Bearbeiten deiner Autos.",
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
        for index in range(2):
            stats.grid_columnconfigure(index, weight=1)

        stat_cards = [
            ("Autos", "gesamt", PALETTE["accent"]),
            ("Premium", "premium", "#f59e0b"),
            ("Elektro", "elektro", PALETTE["accent_two"]),
            ("Wert", "bestandswert", "#22c55e"),
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
            card.grid(row=idx // 2, column=idx % 2, sticky="nsew", padx=6, pady=6)
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
                font=("Bahnschrift", 20, "bold"),
            ).pack(anchor="w", pady=(4, 0))

        toolbar = self.make_card(self.root)
        toolbar.pack(fill="x", padx=18, pady=(14, 14))
        controls = tk.Frame(toolbar, bg=PALETTE["card"])
        controls.pack(fill="x", padx=18, pady=16)
        info = tk.Frame(controls, bg=PALETTE["card"])
        info.pack(side="left")
        tk.Label(
            info,
            text="Autos schnell erzeugen",
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Segoe UI Semibold", 12),
        ).pack(anchor="w")
        tk.Label(
            info,
            text="Ein Klick und der Laden ist wieder voll.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        actions = tk.Frame(controls, bg=PALETTE["card"])
        actions.pack(side="right")
        tk.Label(
            actions,
            text="Anzahl",
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
        self.anzahl_entry.insert(0, "18")
        self.anzahl_entry.pack(side="left", padx=(0, 12), ipady=6)

        toolbar_buttons = [
            ("Generieren", self.generieren, PALETTE["accent"]),
            ("Alle tanken", self.tanken_alle, "#2563eb"),
            ("Alle laden", self.laden_alle, PALETTE["accent_two"]),
            ("Status zeigen", self.status_alle, "#0f766e"),
            ("Alles leeren", self.clear_inventory, "#7f1d1d"),
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
            text="Hier siehst du alle Autos, die teuren Kisten und ein paar nützliche Zahlen dazu.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        inventory_tabs = [
            ("all", "Alle Autos"),
            ("normal", "Normale Ecke"),
            ("premium", "Premium Ecke"),
        ]
        for key, title in inventory_tabs:
            frame = tk.Frame(self.notebook, bg=PALETTE["card"])
            self.tab_frames[key] = frame
            self.notebook.add(frame, text=title)
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
            text="Klick einfach ein Auto an, dann kannst du es bearbeiten.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=16, pady=(0, 10))
        wrap = tk.Frame(parent, bg=PALETTE["card"])
        wrap.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        shell = tk.Frame(wrap, bg=PALETTE["input_bg"], highlightbackground=PALETTE["line"], highlightthickness=1)
        shell.pack(fill="both", expand=True)
        columns = ("ID", "Marke", "Typ", "Farbe", "Jahr", "PS", "KM", "Energie", "Preis", "Haus", "Standort")
        widths = {
            "ID": 70,
            "Marke": 130,
            "Typ": 90,
            "Farbe": 110,
            "Jahr": 70,
            "PS": 80,
            "KM": 95,
            "Energie": 90,
            "Preis": 120,
            "Haus": 90,
            "Standort": 180,
        }
        tree = ttk.Treeview(shell, columns=columns, show="headings", style="Forge.Treeview", height=20)
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
            ("Autos gesamt", "gesamt", PALETTE["accent"]),
            ("Normale", "normal", "#2563eb"),
            ("Premium", "premium", "#f59e0b"),
            ("Elektro", "elektro", PALETTE["accent_two"]),
            ("Benziner", "benzin", "#475569"),
            ("Durchschnitt PS", "durchschnitt_ps", "#38bdf8"),
            ("Durchschnittspreis", "durchschnitt_preis", "#10b981"),
            ("Gesamtwert", "bestandswert", "#22c55e"),
            ("Beliebteste Marke", "haeufigste_marke", "#f97316"),
        ]
        for idx, (label, key, accent) in enumerate(cards):
            self.stat_vars[key] = tk.StringVar(value="-")
            card = tk.Frame(grid, bg=PALETTE["card_alt"], highlightbackground=PALETTE["line"], highlightthickness=1)
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
        analysis = tk.Frame(parent, bg=PALETTE["input_bg"], highlightbackground=PALETTE["line"], highlightthickness=1)
        analysis.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        tk.Label(
            analysis,
            text="Kurzer Überblick",
            fg=PALETTE["text"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI Semibold", 12),
        ).pack(anchor="w", padx=14, pady=(14, 8))
        self.stats_text = tk.Text(analysis, height=12, bg=PALETTE["input_bg"], fg=PALETTE["text"], insertbackground=PALETTE["text"], relief="flat", font=("Consolas", 10), padx=14, pady=10)
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
            text="Hier kannst du das ausgewählte Auto in Ruhe anpassen, ohne dass irgendwas abgeschnitten wird.",
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

        for column in range(3):
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
                "Verkauf und Zeug",
                [
                    ("Kategorie", "kategorie", "combo"),
                    ("Standort", "standort", "combo"),
                    ("Preis (EUR)", "preis", "entry"),
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
        ]

        for column, (title, fields) in enumerate(editor_groups):
            self.build_editor_group(grid, column, title, fields)

    def build_editor_group(self, parent, column, title, fields):
        shell = tk.Frame(parent, bg=PALETTE["input_bg"], highlightbackground=PALETTE["line"], highlightthickness=1)
        shell.grid(row=0, column=column, sticky="nsew", padx=6, pady=6)
        tk.Label(shell, text=title, fg=PALETTE["accent_two"], bg=PALETTE["input_bg"], font=("Segoe UI Semibold", 10)).pack(anchor="w", padx=10, pady=(10, 6))

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
                tk.Label(panel, textvariable=self.energy_label_var, fg="#cbd5e1", bg=PALETTE["input_bg"], font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", pady=5)
            else:
                tk.Label(panel, text=label, fg="#cbd5e1", bg=PALETTE["input_bg"], font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", pady=5)

            if kind == "combo":
                widget = ttk.Combobox(panel, textvariable=self.form_vars[key], values=self.field_values(key), style="Forge.TCombobox", width=18)
                widget.bind("<<ComboboxSelected>>", self.on_form_mode_change)
            else:
                widget = tk.Entry(panel, textvariable=self.form_vars[key], bg=PALETTE["card"], fg=PALETTE["text"], insertbackground=PALETTE["text"], relief="flat", font=("Segoe UI", 9), width=18)

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
            ("Speichern", self.save_vehicle_changes, "#4f46e5"),
            ("Voll machen", self.fill_selected_vehicle, PALETTE["accent_two"]),
            ("Ins Log schreiben", self.log_selected_vehicle, "#0f766e"),
        ]
        for text, command, color in buttons:
            self.make_button(actions, text, command, color).pack(fill="x", pady=4)

        shell = tk.Frame(parent, bg=PALETTE["input_bg"], highlightbackground=PALETTE["line"], highlightthickness=1)
        shell.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        info = tk.Frame(shell, bg=PALETTE["input_bg"])
        info.pack(fill="both", expand=True, padx=14, pady=14)
        tk.Label(
            info,
            text="Bearbeiten passiert links",
            fg=PALETTE["accent_two"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI Semibold", 12),
        ).pack(anchor="w")
        tk.Label(
            info,
            text="Das ausgewählte Auto siehst du hier kurz im Blick. Für alles Größere gibt's links den Editor.",
            fg=PALETTE["muted"],
            bg=PALETTE["input_bg"],
            font=("Segoe UI", 10),
            wraplength=300,
            justify="left",
        ).pack(anchor="w", pady=(8, 16))

        summary = tk.Frame(info, bg=PALETTE["card"], highlightbackground=PALETTE["line"], highlightthickness=1)
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
        self.clear_editor()

    def setup_log(self):
        shell = self.make_card(self.root)
        shell.pack(fill="x", padx=18, pady=(2, 18))
        header = tk.Frame(shell, bg=PALETTE["card"])
        header.pack(fill="x", padx=18, pady=(16, 8))
        tk.Label(
            header,
            text="Log und Notizen",
            fg=PALETTE["text"],
            bg=PALETTE["card"],
            font=("Bahnschrift", 16, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Hier landet alles, was die App gerade so macht.",
            fg=PALETTE["muted"],
            bg=PALETTE["card"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))
        log_shell = tk.Frame(shell, bg=PALETTE["input_bg"], highlightbackground=PALETTE["line"], highlightthickness=1)
        log_shell.pack(fill="x", padx=18, pady=(0, 18))
        self.log = tk.Text(log_shell, height=7, bg=PALETTE["input_bg"], fg=PALETTE["text"], insertbackground=PALETTE["text"], relief="flat", font=("Consolas", 10), padx=14, pady=12)
        self.log.pack(fill="x")
        gui_print(self.log, "App gestartet. Du kannst jetzt Autos erzeugen oder eins aus dem Bestand anklicken.")

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
        return []

    def generieren(self):
        try:
            anzahl = int(self.anzahl_entry.get())
        except ValueError:
            gui_print(self.log, "Bitte nur ganze Zahlen eingeben.")
            return
        if anzahl <= 0 or anzahl > 250:
            gui_print(self.log, "Nimm bitte eine Zahl zwischen 1 und 250.")
            return
        self.garage.clear()
        self.selected_vehicle = None
        clearlog(self.log)
        gui_print(self.log, f"Ich baue dir gerade {anzahl} Autos zusammen...")
        for _ in range(anzahl):
            self.garage.add_auto(self.create_random_vehicle())
        self.refresh_all_views()
        self.clear_editor()
        stats = self.garage.statistik()
        gui_print(
            self.log,
            (
                f"Fertig: {stats['gesamt']} Autos im Bestand | "
                f"normal: {stats['normal']} | premium: {stats['premium']} | elektro: {stats['elektro']}"
            ),
        )

    def create_random_vehicle(self):
        marke = random.choice(MARKEN)
        farbe, _ = random.choice(FARBEN)
        besitzer = random.choice(BESITZER)
        premium = marke in PREMIUM_MARKEN or random.random() < 0.18
        elektrisch = marke in {"Tesla", "Lucid", "Rimac", "Polestar", "BYD"} or random.random() < 0.32
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
        )

    def refresh_all_views(self):
        self.update_table("all", self.garage.alle_fahrzeuge())
        self.update_table("normal", self.garage.filter_normal())
        self.update_table("premium", self.garage.filter_premium())
        self.refresh_statistics()
        self.update_tab_titles()
        stats = self.garage.statistik()
        self.summary_var.set(
            (
                f"{stats['gesamt']} Autos im Bestand | "
                f"{stats['normal']} normal | {stats['premium']} premium | {stats['elektro']} elektro"
            )
        )

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
                    fahrzeug.farbe,
                    fahrzeug.baujahr,
                    fahrzeug.ps,
                    fahrzeug.km,
                    fahrzeug.energie_label,
                    fahrzeug.preis_label,
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
        self.notebook.tab(self.tab_frames["all"], text=f"Alle Autos ({len(self.garage.alle_fahrzeuge())})")
        self.notebook.tab(self.tab_frames["normal"], text=f"Normale ({len(self.garage.filter_normal())})")
        self.notebook.tab(self.tab_frames["premium"], text=f"Premium ({len(self.garage.filter_premium())})")

    def refresh_statistics(self):
        stats = self.garage.statistik()
        self.header_stat_vars["gesamt"].set(str(stats["gesamt"]))
        self.header_stat_vars["premium"].set(str(stats["premium"]))
        self.header_stat_vars["elektro"].set(str(stats["elektro"]))
        self.header_stat_vars["bestandswert"].set(self.short_currency(stats["bestandswert"]))
        self.stat_vars["gesamt"].set(str(stats["gesamt"]))
        self.stat_vars["normal"].set(str(stats["normal"]))
        self.stat_vars["premium"].set(str(stats["premium"]))
        self.stat_vars["elektro"].set(str(stats["elektro"]))
        self.stat_vars["benzin"].set(str(stats["benzin"]))
        self.stat_vars["durchschnitt_ps"].set(f"{stats['durchschnitt_ps']} PS")
        self.stat_vars["durchschnitt_preis"].set(self.format_currency(stats["durchschnitt_preis"]))
        self.stat_vars["bestandswert"].set(self.format_currency(stats["bestandswert"]))
        self.stat_vars["haeufigste_marke"].set(stats["haeufigste_marke"])
        teuerstes = stats["teuerstes_auto"]
        lines = [
            f"Durchschnitt Kilometer: {stats['durchschnitt_km']}",
            f"Normal zu Premium: {stats['normal']} / {stats['premium']}",
            f"Elektro-Anteil: {round((stats['elektro'] / stats['gesamt']) * 100, 1) if stats['gesamt'] else 0}%",
            f"Am häufigsten steht hier: {stats['haeufigste_marke']}",
            f"Durchschnittlicher Fahrzeugwert: {self.format_currency(stats['durchschnitt_preis'])}",
        ]
        if teuerstes is not None:
            lines.append(f"Teuerstes Fahrzeug: #{teuerstes.fahrzeug_id} {teuerstes.marke} mit {teuerstes.preis_label}")
            lines.append(f"Standort des teuersten Fahrzeugs: {teuerstes.standort}")
        else:
            lines.append("Teuerstes Fahrzeug: -")
        self.stats_text.configure(state="normal")
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, "\n".join(lines))
        self.stats_text.configure(state="disabled")

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
        }
        for key, value in values.items():
            self.form_vars[key].set(str(value))
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
        }
        for key, value in defaults.items():
            if key in self.form_vars:
                self.form_vars[key].set(value)
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
            )
        except ValueError:
            gui_print(
                self.log,
                "Preis, Baujahr, Kilometer, PS, MaxSpeed und Energie brauchen gültige Zahlen.",
            )
            return
        self.refresh_all_views()
        self.fill_editor(self.selected_vehicle)
        gui_print(self.log, f"Auto #{self.selected_vehicle.fahrzeug_id} wurde gespeichert.")

    def open_editor_tab(self):
        self.notebook.select(self.tab_frames["editor"])

    def fill_selected_vehicle(self):
        if self.selected_vehicle is None:
            gui_print(self.log, "Bitte zuerst ein Fahrzeug in einer Tabelle auswählen.")
            return
        if self.selected_vehicle.elektrisch:
            self.selected_vehicle.laden()
            action = "geladen"
        else:
            self.selected_vehicle.tanken()
            action = "vollgetankt"
        self.refresh_all_views()
        self.fill_editor(self.selected_vehicle)
        gui_print(self.log, f"Auto #{self.selected_vehicle.fahrzeug_id} wurde {action}.")

    def log_selected_vehicle(self):
        if self.selected_vehicle is None:
            gui_print(self.log, "Bitte zuerst ein Fahrzeug in einer Tabelle auswählen.")
            return
        gui_print(self.log, self.selected_vehicle.status_text())

    def clear_inventory(self):
        self.garage.clear()
        self.selected_vehicle = None
        clearlog(self.log)
        gui_print(self.log, "Alles raus. Der Bestand ist jetzt leer.")
        self.refresh_all_views()
        self.clear_editor()

    def tanken_alle(self):
        if not self.garage.fahrzeuge:
            gui_print(self.log, "Es gibt noch keine Fahrzeuge.")
            return
        count = self.garage.tanken_alle()
        self.refresh_all_views()
        gui_print(self.log, f"{count} Benziner wurden aufgefüllt.")

    def laden_alle(self):
        if not self.garage.fahrzeuge:
            gui_print(self.log, "Es gibt noch keine Fahrzeuge.")
            return
        count = self.garage.laden_alle()
        self.refresh_all_views()
        gui_print(self.log, f"{count} Elektroautos wurden geladen.")

    def status_alle(self):
        if not self.garage.fahrzeuge:
            gui_print(self.log, "Es gibt noch keine Fahrzeuge.")
            return
        stats = self.garage.statistik()
        gui_print(
            self.log,
            (
                f"Status | gesamt: {stats['gesamt']} | "
                f"normal: {stats['normal']} | premium: {stats['premium']} | "
                f"elektro: {stats['elektro']} | schnitt: {self.format_currency(stats['durchschnitt_preis'])}"
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
