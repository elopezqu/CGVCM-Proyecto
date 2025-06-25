import customtkinter as ctk
from pages.games_selector import GameSelectionPage
from pages.abecedario import SenhaWindow
from pages.lista_senas import ListaSenasWindow

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EnSEÑA PLAY")
        self.geometry("900x600")
        self.minsize(600, 400)

        # Modo visual (opcional)
        ctk.set_appearance_mode("light")  # o "dark"
        ctk.set_default_color_theme("blue")  # azul, dark-blue, green, etc.

        # === Contenedor principal ===
        container = ctk.CTkFrame(self, corner_radius=0)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # === Páginas ===
        self.menu_page = self.create_menu(container)
        self.frames["Menu"] = self.menu_page

        game_page = GameSelectionPage(parent=container, controller=self)
        self.frames["GameSelectionPage"] = game_page
        game_page.grid(row=0, column=0, sticky="nsew")

        lista_page = ListaSenasWindow(parent=container, controller=self)
        self.frames["ListaSenasWindow"] = lista_page
        lista_page.grid(row=0, column=0, sticky="nsew")


        self.show_frame("Menu")

    def create_menu(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="#AEEEEE")  # Fondo celeste
        frame.grid(row=0, column=0, sticky="nsew")

        # Título principal
        title_label = ctk.CTkLabel(
            frame,
            text="EnSEÑA PLAY",
            font=ctk.CTkFont("Helvetica", 48, weight="bold"),
            text_color="#003366"
        )
        title_label.pack(pady=40)
        # Contenedor de botones
        buttons_frame = ctk.CTkFrame(frame, fg_color="#AEEEEE")
        buttons_frame.pack(pady=30)

        # Opciones del menú
        options = ["Jugar", "Como Jugar", "Lista de Señas", "Opciones", "Salir"]
        for option in options:
            btn = ctk.CTkButton(
                buttons_frame,
                text=option,
                font=ctk.CTkFont(size=35, weight="bold"),
                width=350,
                fg_color="#008B8B",
                hover_color="#20B2AA",
                text_color="white",
                command=lambda opt=option: self.handle_option(opt)
            )
            btn.pack(pady=10, fill="x", expand=True)

        return frame

    def handle_option(self, option):
        if option == "Salir":
            self.destroy()
        elif option == "Jugar":
            self.show_frame("GameSelectionPage")
        elif option == "Lista de Señas":
            self.show_frame("ListaSenasWindow")
        else:
            print(f"Seleccionaste: {option}")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
