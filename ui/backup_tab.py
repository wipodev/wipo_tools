import customtkinter as ctk
from tkinter import filedialog, messagebox
from app.backup import BackupManager

class BackupTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.manager = BackupManager()
        self.dest_folder = ""

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
        # Área de lista (usa CTkTextbox como reemplazo de Listbox)
        self.textbox = ctk.CTkTextbox(parent, width=200,)
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.refresh_list()

        # Botonera
        btn_frame = ctk.CTkFrame(parent)
        btn_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        btn_frame.grid_columnconfigure((0,1,2), weight=1)
        ctk.CTkButton(btn_frame, text="Agregar Archivo", command=self.add_file).grid(row=0, column=0, sticky="ew", padx=5)
        ctk.CTkButton(btn_frame, text="Agregar Carpeta", command=self.add_folder).grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar Seleccionado", command=self.remove_selected).grid(row=0, column=2, sticky="ew", padx=5)
    
    def _ConfigFrame(self, parent):
        cf = ctk.CTkFrame(parent)
        cf.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        cf.grid_columnconfigure(0, weight=1)
        for r in range(5):
            cf.grid_rowconfigure(r, weight=0)

        ctk.CTkLabel(cf, text="Nombre del Backup:").grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
        self.backup_name_var = ctk.StringVar()
        ctk.CTkEntry(cf, textvariable=self.backup_name_var).grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

        ctk.CTkButton(cf, text="Seleccionar Carpeta de Destino", command=self.select_dest_folder).grid(row=2, column=0, sticky="ew", padx=10, pady=(0,10))
        self.dest_folder_label = ctk.CTkLabel(cf, text="Destino: No seleccionado")
        self.dest_folder_label.grid(row=3, column=0, sticky="w", padx=10, pady=(0,10))

        ctk.CTkButton(cf, text="Hacer Backup", command=self.perform_backup).grid(row=4, column=0, padx=10, sticky="ew")

    def refresh_list(self):
        self.textbox.delete("0.0", "end")
        for p in self.manager.paths_to_backup:
            self.textbox.insert("end", p + "\n")  # usa CTkTextbox :contentReference[oaicite:3]{index=3}

    def add_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.manager.add_path(path)
            self.refresh_list()

    def add_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.manager.add_path(path)
            self.refresh_list()

    def remove_selected(self):
        selected = self.listbox.curselection()
        for i in reversed(selected):
            self.manager.remove_path(i)
        self.refresh_listbox()

    def select_dest_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_folder = path
            self.dest_folder_label.configure(text=f"Destino: {path}")

    def perform_backup(self):
        if not self.dest_folder:
            messagebox.showwarning("Falta destino", "Selecciona la carpeta de destino.")
            return

        backup_name = self.backup_name_var.get().strip()
        if not backup_name:
            messagebox.showwarning("Falta nombre", "Escribe un nombre para el backup.")
            return

        try:
            result_path = self.manager.perform_backup(self.dest_folder, backup_name)
            messagebox.showinfo("Backup completado", f"Backup creado en:\n{result_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
