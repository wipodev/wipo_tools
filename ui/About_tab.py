import customtkinter as ctk

class AboutTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text="Wipo Tools", font=("Consolas", 14)).grid(row=0, column=0, pady=20)
        # aquí agregas tus widgets…
