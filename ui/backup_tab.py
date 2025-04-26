import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from app.settings_manager import SettingsManager
from utils.resize_handler_mixin import ResizeHandlerMixin

class BackupTab(ctk.CTkFrame, ResizeHandlerMixin):
    def __init__(self, master):
        super().__init__(master)
        self.wiconfig = SettingsManager()
        self.dest_folder = ""
        self.setup_resize_listener(self.refresh_all)

        # grid principal de este frame
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text="Gestor de Backups", font=("Consolas", 16)).grid(row=0, column=0, pady=(0,10))

        # Body
        body_frame = ctk.CTkFrame(self)
        body_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        body_frame.grid_columnconfigure(0, weight=1)
        body_frame.grid_columnconfigure(1, weight=1)
        body_frame.grid_rowconfigure(0, weight=1)

        self._list_to_backup(body_frame)

        self._ConfigFrame(body_frame)

    def _list_to_backup(self, parent):
        self.scroll = ctk.CTkScrollableFrame(parent, width=200)
        self.scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.refresh_list()

        # Botonera
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=(5, 0), pady=(0, 10), sticky="w")
        btn_frame.grid_columnconfigure((0,1), weight=1)
        ctk.CTkButton(btn_frame, text="Agregar Archivo", width= 220, command=self.add_file).grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkButton(btn_frame, text="Agregar Carpeta", width= 220, command=self.add_folder).grid(row=0, column=1, sticky="w", padx=5)
    
    def _ConfigFrame(self, parent):
        cf = ctk.CTkFrame(parent)
        cf.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        cf.grid_columnconfigure(0, weight=1)
        for r in range(5):
            cf.grid_rowconfigure(r, weight=0)

        ctk.CTkLabel(cf, text="Nombre del Backup:").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        self.backup_name_var = ctk.StringVar(value=self.wiconfig.backup_name)
        ctk.CTkEntry(cf, textvariable=self.backup_name_var).grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

        ctk.CTkButton(cf, text="Seleccionar Carpeta", command=self.select_dest_folder).grid(row=3, column=0, sticky="w", padx=10, pady=(0,10))
        self.dest_folder_label = ctk.CTkLabel(cf, text="Destino: No seleccionado")
        self.dest_folder_label.grid(row=2, column=0, sticky="w", padx=10, pady=(20,10))

        ctk.CTkButton(cf, text="Hacer Backup", width=200, height=40, command=self.perform_backup, fg_color="#27ae60",
    hover_color="#219150", text_color="black", font=("Segoe UI", 14, "bold")).grid(row=4, column=0, padx=10, pady=(20, 0))

    def refresh_list(self):
        for child in self.scroll.winfo_children():
            child.destroy()

        width = self.scroll.winfo_width()
        max_chars = max(int(width / 7), 40)
        for i, route in enumerate(self.wiconfig.get_paths()):
            item_frame = ctk.CTkFrame(self.scroll)
            item_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)
            item_frame.grid_columnconfigure(0, weight=0)

            # Etiqueta con la ruta cortada
            route_closed = self.cut_route(route, max_chars)

            # Etiqueta con la ruta
            label = ctk.CTkLabel(item_frame, text=route_closed, anchor="e")
            label.grid(row=0, column=1, sticky="ew", padx=(0, 10))

            # Botón eliminar
            delete_button = ctk.CTkButton(
                item_frame,
                text="x",
                width=22,
                height=22,
                fg_color="#e74c3c", hover_color="#c0392b",
                text_color="white",
                command=lambda r=route: self.remove_item(r)
            )
            delete_button.grid(row=0, column=0, padx=(0, 5))

    def cut_route(self, route, max_chars = 50):
        if len(route) <= max_chars:
            return route
        visible_part = max_chars // 2 - 2
        return route[:visible_part] + "..." + route[-visible_part:]

    def refresh_all(self):
        self.refresh_list()
        self.update_dest_folder_label()

    def add_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.wiconfig.add_path(path)
            self.refresh_list()

    def add_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.wiconfig.add_path(path)
            self.refresh_list()

    def remove_item(self, route):
        if route in self.wiconfig.get_paths():
          self.wiconfig.remove_path(route)
          self.refresh_list()

    def select_dest_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_folder = path
            self.update_dest_folder_label()

    def update_dest_folder_label(self):
        if not self.dest_folder:
            self.dest_folder_label.configure(text="Destino: No seleccionado")
        else:
            label_width = self.dest_folder_label.winfo_width()
            if (label_width - 10) < len(self.dest_folder):
              folder_name = os.path.basename(self.dest_folder)
              self.dest_folder_label.configure(text=f"Destino: {folder_name}")
            else:
              self.dest_folder_label.configure(text=f"Destino: {self.dest_folder}")

    def perform_backup(self):
        if not self.dest_folder:
            messagebox.showwarning("Falta destino", "Selecciona la carpeta de destino.")
            return

        backup_name = self.backup_name_var.get().strip()
        if not backup_name:
            messagebox.showwarning("Falta nombre", "Escribe un nombre para el backup.")
            return

        try:
            result_path = self.wiconfig.perform_backup(self.dest_folder, backup_name)
            messagebox.showinfo("Backup completado", f"Backup creado en:\n{result_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
