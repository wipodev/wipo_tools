import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from app.settings_manager import SettingsManager

class SettingsTab(ctk.CTkFrame):
    def __init__(self, master, config_path="config.json"):
        super().__init__(master)
        self.wiconfig = SettingsManager(config_path)
        self.config_path = os.path.abspath(config_path)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.last_clicked = False

        # Título
        ctk.CTkLabel(self, text="Configuración de la Aplicación", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(10, 20)
        )

        # Ruta del archivo de configuración
        ctk.CTkLabel(self, text="Ruta del archivo de configuración:").grid(row=1, column=0, sticky="w", padx=10)
        ctk.CTkLabel(self, text=self.config_path, text_color="gray").grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 20))

        # Botones de exportar e importar
        export_btn = ctk.CTkButton(self, text="Exportar Configuración", command=self.export_config, width=180, height=40)
        export_btn.grid(row=3, column=0, padx=(10, 5), pady=10, sticky="w")

        import_btn = ctk.CTkButton(self, text="Importar Configuración", command=self.import_config, width=180, height=40)
        import_btn.grid(row=3, column=1, padx=(5, 10), pady=10, sticky="w")

        # Selector de modo de apariencia
        ctk.CTkLabel(self, text="Modo de apariencia:").grid(row=4, column=0, sticky="w", padx=10, pady=(20, 5))
        self.appearance_option = ctk.CTkOptionMenu(
            self,
            values=["System", "Light", "Dark"],
            command=self.set_appearance_mode
        )
        self.appearance_option.set(ctk.get_appearance_mode())
        self.appearance_option.grid(row=5, column=0, sticky="w", padx=10, pady=(0, 20))

    def export_config(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("Archivos JSON", "*.json")]
        )
        if filepath:
            try:
                self.wiconfig.export_config(filepath)
                messagebox.showinfo("Exportar", "Configuración exportada exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar la configuración:\n{e}")

    def import_config(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json")]
        )
        if filepath:
            try:
                self.wiconfig.import_config(filepath)
                messagebox.showinfo("Importar", "Configuración importada exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo importar la configuración:\n{e}")

    def set_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)