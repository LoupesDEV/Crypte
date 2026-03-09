import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from cryptography.fernet import Fernet

from .constants import ACCENT, BG_CARD, BG_INPUT, BG_MAIN, BG_PANEL, TEXT_MUTED, TEXT_SEC
from .security import derive_key, test_decryption
from .storage import append_entry, load_encrypted_entries, save_all_entries
from .styles import apply_styles


class Crypte:
    def __init__(self, root):
        self.root = root
        self.root.title("CRYPTE")
        self.root.geometry("1100x680")
        self.root.minsize(980, 620)
        self.root.configure(bg=BG_MAIN)
        self.app_icon_image = None
        self.set_app_icon()

        self.root.attributes("-topmost", False)

        self.file_path = "vault/crypte.dat"
        self.key = None
        self.passwords_data = []
        self.show_passwords = False
        self.search_var = tk.StringVar()

        apply_styles()
        self.setup_ui()

        self.root.after(100, self.ask_master_password)

    def set_app_icon(self):
        icon_path = os.path.join("assets", "logo.png")
        if not os.path.exists(icon_path):
            return
        try:
            self.app_icon_image = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, self.app_icon_image)
        except Exception:
            self.app_icon_image = None

    def ask_master_password(self):
        pwd = simpledialog.askstring("Authentification", "Entrez le Master Password :", show="*")
        if pwd:
            self.key = Fernet(derive_key(pwd))
            if not test_decryption(self.file_path, self.key):
                messagebox.showerror("Erreur", "Mot de passe incorrect")
                self.root.destroy()
            else:
                self.load_passwords()
        else:
            self.root.destroy()

    def setup_ui(self):
        shell = tk.Frame(self.root, bg=BG_MAIN)
        shell.pack(fill="both", expand=True, padx=16, pady=16)

        sidebar = ttk.Frame(shell, style="Panel.TFrame", width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="CRYPTE", font=("Segoe UI", 28, "bold"), bg=BG_PANEL, fg=ACCENT).pack(anchor="w", padx=20, pady=(26, 8))
        tk.Label(sidebar, text="Gestion sécurisée", font=("Segoe UI", 10), bg=BG_PANEL, fg=TEXT_MUTED).pack(anchor="w", padx=20, pady=(0, 24))

        ttk.Button(sidebar, text="+ Ajouter", command=self.w_add, style="Sidebar.TButton").pack(fill="x", padx=12, pady=4)
        ttk.Button(sidebar, text="- Supprimer", command=self.delete, style="Sidebar.TButton").pack(fill="x", padx=12, pady=4)
        ttk.Button(sidebar, text="📋 Copier user", command=lambda: self.copy_selected_field("user", "Utilisateur"), style="Sidebar.TButton").pack(fill="x", padx=12, pady=4)
        ttk.Button(sidebar, text="📋 Copier mdp", command=lambda: self.copy_selected_field("password", "Mot de passe"), style="Sidebar.TButton").pack(fill="x", padx=12, pady=4)
        ttk.Button(sidebar, text="👁 Reveal/Hide mdp", command=self.toggle_password_visibility, style="Sidebar.TButton").pack(fill="x", padx=12, pady=4)

        ttk.Button(sidebar, text="Quitter", command=self.root.destroy, style="SidebarExit.TButton").pack(side="bottom", fill="x", padx=12, pady=12)

        container = ttk.Frame(shell, style="Card.TFrame")
        container.pack(side="right", fill="both", expand=True, padx=(16, 0))

        title_row = tk.Frame(container, bg=BG_CARD)
        title_row.pack(fill="x", padx=24, pady=(18, 6))

        ttk.Label(title_row, text="Mots de passe", style="Title.TLabel").pack(side="left")

        search_wrap = tk.Frame(title_row, bg=BG_CARD)
        search_wrap.pack(side="right")
        tk.Label(search_wrap, text="Recherche", bg=BG_CARD, fg=ACCENT, font=("Segoe UI", 18, "bold")).pack(side="left", padx=(0, 10))
        search_entry = tk.Entry(
            search_wrap,
            textvariable=self.search_var,
            width=20,
            bg=BG_INPUT,
            fg=ACCENT,
            insertbackground=ACCENT,
            relief="flat",
            font=("Segoe UI", 18, "bold"),
        )
        search_entry.pack(side="left", ipady=4)
        search_entry.bind("<KeyRelease>", lambda _event: self.refresh_tree())

        ttk.Label(container, text="Double-clique une ligne pour la modifier", style="Subtle.TLabel").pack(anchor="w", padx=24, pady=(0, 14))

        table_wrap = tk.Frame(container, bg=BG_CARD)
        table_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tree = ttk.Treeview(table_wrap, columns=("site", "user", "password", "note"), show="headings")
        self.tree.heading("site", text="SITE")
        self.tree.heading("user", text="NOM D'UTILISATEUR")
        self.tree.heading("password", text="MOT DE PASSE")
        self.tree.heading("note", text="NOTE")
        self.tree.column("site", width=220, anchor="w")
        self.tree.column("user", width=220, anchor="w")
        self.tree.column("password", width=180, anchor="w")
        self.tree.column("note", width=280, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        scrollbar.pack(side="right", fill="y", padx=(8, 0))
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.tag_configure("odd", background="#1A1F29")
        self.tree.tag_configure("even", background="#202633")

        self.tree.bind("<Double-1>", self.open_edit_popup)

    def load_passwords(self):
        self.passwords_data = load_encrypted_entries(self.file_path, self.key)
        self.refresh_tree()

    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        query = self.search_var.get().strip().lower()
        visible_count = 0

        for idx, data in enumerate(self.passwords_data):
            site = data.get("site", "")
            if query and query not in site.lower():
                continue

            user = data.get("user", "")
            password = data.get("password", "")
            note_preview = data.get("note", "")
            password_display = password if self.show_passwords else ("•" * max(4, len(password)))
            row_tag = "even" if visible_count % 2 else "odd"

            self.tree.insert(
                "",
                tk.END,
                iid=str(idx),
                values=(site, user, password_display, note_preview),
                tags=(row_tag,),
            )
            visible_count += 1

    def get_selected_index(self, show_warning=True):
        item = self.tree.selection()
        if not item:
            if show_warning:
                messagebox.showwarning("Sélection", "Sélectionne une ligne dans le tableau.")
            return None

        try:
            idx = int(item[0])
        except ValueError:
            return None

        if idx >= len(self.passwords_data):
            return None
        return idx

    def get_selected_data(self):
        idx = self.get_selected_index()
        if idx is None:
            return None
        return self.passwords_data[idx]

    def copy_selected_field(self, field, label):
        data = self.get_selected_data()
        if not data:
            return
        value = data.get(field, "")
        self.copy_to_clipboard(value, label)

    def toggle_password_visibility(self):
        self.show_passwords = not self.show_passwords
        self.load_passwords()

    def save_all_passwords(self):
        save_all_entries(self.file_path, self.key, self.passwords_data)

    def copy_to_clipboard(self, value, label):
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()
        messagebox.showinfo("Copie", f"{label} copié dans le presse-papiers.")

    def w_add(self):
        win = tk.Toplevel(self.root, bg=BG_CARD)
        win.title("Nouvelle entrée")
        win.geometry("460x520")
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="Nouvelle entrée", font=("Segoe UI", 14, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w", padx=30, pady=(22, 12))

        def add_entry(label, show=None):
            tk.Label(win, text=label, bg=BG_CARD, fg=TEXT_SEC).pack(anchor="w", padx=30, pady=(10, 4))
            row = tk.Frame(win, bg=BG_CARD)
            row.pack(padx=30, fill="x")

            if show is None:
                e = ttk.Entry(row, style="Rounded.TEntry")
            else:
                e = ttk.Entry(row, style="Rounded.TEntry", show=show)
            e.pack(side="left", fill="x", expand=True)
            return e

        e_site = add_entry("Site")
        e_user = add_entry("Utilisateur")
        e_pwd = add_entry("Mot de passe", show="•")

        pwd_visible = tk.BooleanVar(value=False)

        def toggle_add_password():
            if pwd_visible.get():
                e_pwd.configure(show="•")
                pwd_visible.set(False)
            else:
                e_pwd.configure(show="")
                pwd_visible.set(True)

        pwd_toggle_btn = ttk.Button(e_pwd.master, text="👁", style="Tiny.TButton", command=toggle_add_password)
        pwd_toggle_btn.pack(side="left", padx=(8, 0))
        tk.Label(win, text="Note", bg=BG_CARD, fg=TEXT_SEC).pack(anchor="w", padx=30, pady=(10, 4))
        t_note = tk.Text(win, bg=BG_INPUT, fg=ACCENT, height=5, bd=0, padx=8, pady=8, insertbackground=ACCENT)
        t_note.pack(padx=30, fill="x")

        def save():
            entry = {
                "site": e_site.get(),
                "user": e_user.get(),
                "password": e_pwd.get(),
                "note": t_note.get("1.0", tk.END).strip(),
            }
            append_entry(self.file_path, self.key, entry)
            self.load_passwords()
            win.destroy()

        ttk.Button(win, text="Enregistrer", command=save, style="Primary.TButton").pack(pady=24, padx=30, fill="x")

    def open_edit_popup(self, event=None):
        if event is not None:
            item_id = self.tree.identify_row(event.y)
            if not item_id:
                return
            self.tree.selection_set(item_id)

        idx = self.get_selected_index(show_warning=False)
        if idx is None:
            return

        data = self.passwords_data[idx]

        win = tk.Toplevel(self.root, bg=BG_CARD)
        win.title("Modifier l'entrée")
        win.geometry("460x520")
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="Modifier l'entrée", font=("Segoe UI", 14, "bold"), bg=BG_CARD, fg=ACCENT).pack(anchor="w", padx=30, pady=(22, 12))

        def add_entry(label, value="", show=None):
            tk.Label(win, text=label, bg=BG_CARD, fg=TEXT_SEC).pack(anchor="w", padx=30, pady=(10, 4))
            row = tk.Frame(win, bg=BG_CARD)
            row.pack(padx=30, fill="x")

            if show is None:
                e = ttk.Entry(row, style="Rounded.TEntry")
            else:
                e = ttk.Entry(row, style="Rounded.TEntry", show=show)
            e.pack(side="left", fill="x", expand=True)
            e.insert(0, value)
            return e

        e_site = add_entry("Site", data.get("site", ""))
        e_user = add_entry("Utilisateur", data.get("user", ""))
        e_pwd = add_entry("Mot de passe", data.get("password", ""), show="•")

        pwd_visible = tk.BooleanVar(value=False)

        def toggle_edit_password():
            if pwd_visible.get():
                e_pwd.configure(show="•")
                pwd_visible.set(False)
            else:
                e_pwd.configure(show="")
                pwd_visible.set(True)

        ttk.Button(e_pwd.master, text="👁", style="Tiny.TButton", command=toggle_edit_password).pack(side="left", padx=(8, 0))

        tk.Label(win, text="Note", bg=BG_CARD, fg=TEXT_SEC).pack(anchor="w", padx=30, pady=(10, 4))
        t_note = tk.Text(win, bg=BG_INPUT, fg=ACCENT, height=5, bd=0, padx=8, pady=8, insertbackground=ACCENT)
        t_note.pack(padx=30, fill="x")
        t_note.insert("1.0", data.get("note", ""))

        def save_changes():
            self.passwords_data[idx] = {
                "site": e_site.get(),
                "user": e_user.get(),
                "password": e_pwd.get(),
                "note": t_note.get("1.0", tk.END).strip(),
            }
            self.save_all_passwords()
            self.load_passwords()
            win.destroy()

        ttk.Button(win, text="Mettre à jour", command=save_changes, style="Primary.TButton").pack(pady=24, padx=30, fill="x")

    def delete(self):
        idx = self.get_selected_index(show_warning=False)
        if idx is None:
            return
        del self.passwords_data[idx]
        self.save_all_passwords()
        self.load_passwords()
