import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EnSEÑA PLAY")
        self.geometry("800x600")
        self.minsize(600, 400)

        # Frame de fondo que se adapta al tamaño
        self.bg_frame = tk.Frame(self, bg="#AEEEEE")  # Fondo celeste
        self.bg_frame.pack(fill="both", expand=True)

        # Título principal
        title_label = tk.Label(
            self.bg_frame,
            text="EnSEÑA PLAY",
            font=("Helvetica", 32, "bold"),
            bg="#AEEEEE",
            fg="#003366"
        )
        title_label.pack(pady=40)

        # Contenedor para los botones
        buttons_frame = tk.Frame(self.bg_frame, bg="#AEEEEE")
        buttons_frame.pack(pady=20)

        # Opciones del menú
        options = ["Jugar", "Como Jugar", "Lista de Señas", "Opciones", "Salir"]
        for option in options:
            btn = tk.Button(
                buttons_frame,
                text=option,
                font=("Helvetica", 16, "bold"),
                width=20,
                pady=10,
                bg="#008B8B",
                fg="white",
                activebackground="#20B2AA",
                activeforeground="white",
                bd=0,
                relief="flat",
                command=lambda opt=option: self.handle_option(opt)
            )
            btn.pack(pady=10, fill="x", expand=True)

    def handle_option(self, option):
        if option == "Salir":
            self.destroy()  # Cierra la aplicación
        if option == "Lista de Señas":
            self.withdraw()  # Ocultar ventana principal
            from lista_senas import ListaSenasWindow
            ListaSenasWindow(self)
        else:
            print(f"Seleccionaste: {option}")
            # Aquí luego puedes usar self.show_frame("TrainingPage"), etc.

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
