import tkinter as tk
import random
import os
import subprocess

LETRA_DETECTADA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../cg-project/letra_detectada.txt"))

PALABRAS = ["AHORCADO", "PYTHON", "SEÑALES", "CAMARA", "JUEGO", "VISUAL"]

# RUTAS AJUSTADAS A TU PROYECTO
CAMARA_SCRIPT_PATH = "C:/Users/pro20/Documents/proyectos_CGVCM/Proyecto_Final/cg-project/main.py"
CAMARA_PYTHON_PATH = "C:/Users/pro20/Documents/proyectos_CGVCM/Proyecto_Final/cg-project/venv/Scripts/python.exe"
CAMARA_WORKDIR = "C:/Users/pro20/Documents/proyectos_CGVCM/Proyecto_Final/cg-project"

class AhorcadoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego del Ahorcado con Señas")
        self.root.configure(bg="#B0D6F0")
        self.root.geometry("1000x500")
        self.root.resizable(True, True)

        self.proceso_camara = None

        self.palabra = random.choice(PALABRAS)
        self.intentos = 0
        self.max_intentos = 6
        self.letras_usadas = set()
        self.correctas = set()

        # Título
        self.titulo = tk.Label(root, text="Ahorcado", font=("Comic Sans MS", 28, "bold"), bg="#778BD3", fg="black")
        self.titulo.grid(row=0, column=0, columnspan=3, sticky="we", pady=5)

        # === Sección cámara ===
        self.area_camara = tk.Frame(root, width=300, height=240, bg="#0A0A0A", relief="raised", bd=2)
        self.area_camara.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        self.status_lbl = tk.Label(self.area_camara, text="Haz la seña de una letra", bg="#0A0A0A", fg="white")
        self.status_lbl.pack(pady=10)

        self.resultado_lbl = tk.Label(self.area_camara, text="", bg="#0A0A0A", fg="lightgreen")
        self.resultado_lbl.pack()

        # === Sección dibujo ahorcado ===
        self.canvas = tk.Canvas(root, width=150, height=250, bg="white")
        self.canvas.grid(row=1, column=1, padx=10, pady=10)
        self.dibujar_base()

        # === Palabra a adivinar ===
        self.frame_palabra = tk.Frame(root, bg="#B0D6F0")
        self.frame_palabra.grid(row=2, column=0, columnspan=3, pady=10)

        self.letras_lbls = []
        for letra in self.palabra:
            lbl = tk.Label(self.frame_palabra, text="_", font=("Arial", 24), width=2, bg="#B0D6F0")
            lbl.pack(side="left", padx=3)
            self.letras_lbls.append(lbl)

        # === Teclado virtual ===
        self.frame_teclado = tk.Frame(root, bg="#B0D6F0")
        self.frame_teclado.grid(row=3, column=0, columnspan=3, pady=5)

        self.botones = {}
        for i, letra in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            btn = tk.Button(self.frame_teclado, text=letra, width=4, height=2,
                            command=lambda l=letra: self.seleccionar_letra(l))
            btn.grid(row=i // 9, column=i % 9, padx=2, pady=2)
            self.botones[letra] = btn

        self.iniciar_camara()
        self.revisar_letra_externa()
        self.root.protocol("WM_DELETE_WINDOW", self.salir)

    def iniciar_camara(self):
        try:
            self.proceso_camara = subprocess.Popen([
                CAMARA_PYTHON_PATH, CAMARA_SCRIPT_PATH
            ], cwd=CAMARA_WORKDIR)
            print("Cámara lanzada correctamente.")
        except Exception as e:
            print(f"Error al iniciar el script de cámara: {e}")

    def salir(self):
        # Terminar cámara si está activa
        if self.proceso_camara and self.proceso_camara.poll() is None:
            self.proceso_camara.terminate()

        # Limpiar archivo al salir
        try:
            open(LETRA_DETECTADA_PATH, "w").close()
            print("Archivo letra_detectada.txt limpiado.")
        except Exception as e:
            print(f"Error al limpiar letra_detectada.txt: {e}")

        self.root.destroy()

    def dibujar_base(self):
        c = self.canvas
        c.delete("all")
        c.create_line(20, 230, 130, 230, width=5)
        c.create_line(50, 230, 50, 20, width=5)
        c.create_line(50, 20, 100, 20, width=5)
        c.create_line(100, 20, 100, 40, width=5)
        if self.intentos > 0: c.create_oval(85, 40, 115, 70, width=3, outline="red")
        if self.intentos > 1: c.create_line(100, 70, 100, 120, width=3, fill="red")
        if self.intentos > 2: c.create_line(100, 80, 80, 100, width=3, fill="red")
        if self.intentos > 3: c.create_line(100, 80, 120, 100, width=3, fill="red")
        if self.intentos > 4: c.create_line(100, 120, 80, 150, width=3, fill="red")
        if self.intentos > 5: c.create_line(100, 120, 120, 150, width=3, fill="red")

    def seleccionar_letra(self, letra):
        if letra in self.letras_usadas:
            return

        self.letras_usadas.add(letra)
        self.botones[letra].config(state="disabled")

        if letra in self.palabra:
            for i, l in enumerate(self.palabra):
                if l == letra:
                    self.letras_lbls[i].config(text=letra)
                    self.correctas.add(letra)
            self.resultado_lbl.config(text=f"Letra '{letra}' acertada ✅", fg="green")
        else:
            self.intentos += 1
            self.dibujar_base()
            self.resultado_lbl.config(text=f"Letra '{letra}' incorrecta ❌", fg="red")

        self.verificar_fin()

    def verificar_fin(self):
        if self.intentos >= self.max_intentos:
            self.resultado_lbl.config(text=f"Perdiste. La palabra era {self.palabra}", fg="red")
            self.deshabilitar_teclado()
        elif set(self.palabra) == self.correctas:
            self.resultado_lbl.config(text=f"¡Ganaste! 🎉", fg="green")
            self.deshabilitar_teclado()

    def deshabilitar_teclado(self):
        for btn in self.botones.values():
            btn.config(state="disabled")

    def revisar_letra_externa(self):
        try:
            with open(LETRA_DETECTADA_PATH, "r") as f:
                letra = f.read().strip().upper()
            if letra and letra in "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ":
                self.seleccionar_letra(letra)
                open(LETRA_DETECTADA_PATH, "w").close()
        except FileNotFoundError:
            pass
        self.root.after(1000, self.revisar_letra_externa)


if __name__ == "__main__":
    root = tk.Tk()
    app = AhorcadoApp(root)
    root.mainloop()
