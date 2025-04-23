import customtkinter as ctk

class TabManager(ctk.CTkFrame):
    def __init__(self, master, tabs: list[tuple[str, type]] = None):
        super().__init__(master)
        # configura grid en este frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # crea el CTkTabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # usa grid :contentReference[oaicite:1]{index=1}

        self.tabs = {}
        if tabs:
            self.add_tabs(tabs)

    def add_tabs(self, tabs):
        for title, widget_class in tabs:
            self.add_tab(title, widget_class)

    def add_tab(self, title: str, widget_class: type):
        # añade nueva pestaña (es un CTkFrame)
        tab_frame = self.tabview.add(title)  # devuelve CTkFrame :contentReference[oaicite:2]{index=2}
        # configura grid en la pestaña
        tab_frame.grid_rowconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)
        # instancia y coloca el contenido
        content = widget_class(tab_frame)
        content.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.tabs[title] = content

    def get_tabview(self):
        return self.tabview

    def get_tab(self, title: str):
        return self.tabs.get(title)