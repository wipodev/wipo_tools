import customtkinter as ctk

from ui.tab_manager import TabManager
from ui.backup_tab import BackupTab
from ui.settings_tab import SettingsTab
from ui.about_tab import AboutTab

class WipoToolsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wipo Tools")
        self.geometry("800x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Crea pestañas principales
        manager = TabManager(self, tabs=[
            ("Backup", BackupTab),
            ("Configuración", SettingsTab),
            ("Acerca de", AboutTab)
        ])
        manager.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = WipoToolsApp()
    app.mainloop()
