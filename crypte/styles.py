from tkinter import ttk

from .constants import (
    ACCENT,
    BG_CARD,
    BG_INPUT,
    BG_MAIN,
    BG_PANEL,
    BTN_MAIN,
    BTN_MAIN_HOVER,
    HL_COLOR,
    TEXT_MUTED,
    TEXT_SEC,
)


def apply_styles() -> None:
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(".", background=BG_MAIN, foreground=ACCENT, font=("Segoe UI", 10))
    style.configure("Panel.TFrame", background=BG_PANEL)
    style.configure("Card.TFrame", background=BG_CARD)
    style.configure("Title.TLabel", background=BG_CARD, foreground=ACCENT, font=("Segoe UI", 18, "bold"))
    style.configure("Subtle.TLabel", background=BG_CARD, foreground=TEXT_MUTED, font=("Segoe UI", 10))

    style.configure(
        "Treeview",
        background=BG_CARD,
        foreground=ACCENT,
        fieldbackground=BG_CARD,
        rowheight=36,
        borderwidth=0,
        relief="flat",
        font=("Segoe UI", 10),
    )

    style.configure(
        "Treeview.Heading",
        background=BG_PANEL,
        foreground=ACCENT,
        relief="flat",
        borderwidth=0,
        padding=(10, 10),
        font=("Segoe UI", 10, "bold"),
    )
    style.map("Treeview.Heading", background=[("active", BG_PANEL)])

    style.configure(
        "Vertical.TScrollbar",
        gripcount=0,
        background=BG_PANEL,
        darkcolor=BG_PANEL,
        lightcolor=BG_PANEL,
        troughcolor=BG_MAIN,
        bordercolor=BG_MAIN,
        arrowcolor=TEXT_SEC,
    )

    style.configure(
        "Rounded.TEntry",
        fieldbackground=BG_INPUT,
        foreground=ACCENT,
        bordercolor=HL_COLOR,
        lightcolor=HL_COLOR,
        darkcolor=HL_COLOR,
        padding=9,
    )
    style.map(
        "Rounded.TEntry",
        bordercolor=[("focus", BTN_MAIN)],
        lightcolor=[("focus", BTN_MAIN)],
        darkcolor=[("focus", BTN_MAIN)],
    )

    style.configure(
        "Sidebar.TButton",
        background=BG_PANEL,
        foreground=TEXT_SEC,
        borderwidth=0,
        padding=(14, 10),
        anchor="w",
        font=("Segoe UI", 11),
    )
    style.map(
        "Sidebar.TButton",
        background=[("active", BG_CARD), ("pressed", BG_CARD)],
        foreground=[("active", ACCENT), ("pressed", ACCENT)],
    )

    style.configure(
        "SidebarExit.TButton",
        background=BG_PANEL,
        foreground=ACCENT,
        borderwidth=0,
        padding=(14, 12),
        anchor="center",
        font=("Segoe UI", 13, "bold"),
    )
    style.map(
        "SidebarExit.TButton",
        background=[("active", BG_CARD), ("pressed", BG_CARD)],
        foreground=[("active", ACCENT), ("pressed", ACCENT)],
    )

    style.configure(
        "Primary.TButton",
        background=BTN_MAIN,
        foreground="#FFFFFF",
        borderwidth=0,
        padding=(14, 10),
        font=("Segoe UI", 10, "bold"),
    )
    style.map("Primary.TButton", background=[("active", BTN_MAIN_HOVER), ("pressed", BTN_MAIN_HOVER)])

    style.configure(
        "Ghost.TButton",
        background=BG_INPUT,
        foreground=ACCENT,
        borderwidth=0,
        padding=(12, 8),
        font=("Segoe UI", 10, "bold"),
    )
    style.map("Ghost.TButton", background=[("active", HL_COLOR), ("pressed", HL_COLOR)])

    style.configure(
        "Tiny.TButton",
        background=BG_INPUT,
        foreground=ACCENT,
        borderwidth=0,
        padding=(8, 6),
        font=("Segoe UI", 9, "bold"),
    )
    style.map("Tiny.TButton", background=[("active", HL_COLOR), ("pressed", HL_COLOR)])

    style.map("Treeview", background=[("selected", BTN_MAIN)], foreground=[("selected", "#FFFFFF")])
