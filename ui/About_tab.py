import customtkinter as ctk
import webbrowser
from app import __version__

class AboutTab(ctk.CTkFrame):
    """
    Pestaña "Acerca de" que muestra información de la aplicación.
    """
    def __init__(self, master):
        super().__init__(master)
        # Configuración de grid
        self.grid_rowconfigure((1, 2, 3, 4), weight=0)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Título de la sección
        ctk.CTkLabel(
            self,
            text="Wipo Tools",
            font=("Consolas", 18, "bold")
        ).grid(row=0, column=0, pady=(20, 10))

        # Descripción breve
        ctk.CTkLabel(
            self,
            text="Herramienta modular para gestión de backups y utilidades.",
            font=("Consolas", 12)
        ).grid(row=1, column=0, padx=20, pady=(0, 10))

        # Versión
        ctk.CTkLabel(
            self,
            text=__version__,
            font=("Consolas", 12)
        ).grid(row=2, column=0, padx=20, pady=(0, 10))

        # Autor / Contacto
        ctk.CTkLabel(
            self,
            text="Desarrollado por: WipoDev",
            font=("Consolas", 12)
        ).grid(row=3, column=0, padx=20, pady=(0, 10))

        # Botón para abrir repositorio
        repo_button = ctk.CTkButton(
            self,
            text="Ver en GitHub",
            command=lambda: webbrowser.open("https://github.com/wipodev/wipo_tools")
        )
        repo_button.grid(row=4, column=0, pady=(0, 20))

        # Espacio flexible para empujar contenido arriba
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.grid(row=5, column=0, sticky="nsew")

        # Licencia (en footer)
        ctk.CTkLabel(
            self,
            text="© 2025 WipoDev. Licencia MIT.",
            font=("Consolas", 10),
            text_color="#888888"
        ).grid(row=6, column=0, pady=(0, 10))
