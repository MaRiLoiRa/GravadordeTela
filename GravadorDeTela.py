import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import pyautogui
from threading import Thread

class GravadorTela:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravador de Tela")


        style = ttk.Style()
        style.configure('TButton', padding=5, relief="flat", background="#ccc")


        self.btn_iniciar = ttk.Button(root, text="Iniciar Gravação", command=self.iniciar_gravacao)
        self.btn_iniciar.pack(pady=10)


        self.btn_parar = ttk.Button(root, text="Parar Gravação", command=self.parar_gravacao, state=tk.DISABLED)
        self.btn_parar.pack(pady=10)


        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)


        self.icon_iniciar = tk.PhotoImage(file="iconstart.png")  # Substitua pelo caminho do seu ícone
        self.icon_parar = tk.PhotoImage(file="iconstop.png")  # Substitua pelo caminho do seu ícone

        self.btn_iniciar.config(image=self.icon_iniciar, compound=tk.LEFT)
        self.btn_parar.config(image=self.icon_parar, compound=tk.LEFT)

        self.gravando = False
        self.thread_gravacao = None

    def iniciar_gravacao(self):
        self.gravando = True
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_parar.config(state=tk.NORMAL)

        self.thread_gravacao = Thread(target=self.gravar_tela)
        self.thread_gravacao.start()

    def parar_gravacao(self):
        self.gravando = False
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_parar.config(state=tk.DISABLED)

    def gravar_tela(self):
        screen_size = pyautogui.size()
        codec = cv2.VideoWriter_fourcc(*"XVID")
        output = cv2.VideoWriter("gravacao_tela.avi", codec, 20.0, screen_size)

        while self.gravando:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            output.write(frame)

            # Atualiza a tela na interface gráfica
            self.atualizar_tela(frame)

        output.release()

    def atualizar_tela(self, frame):
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = tk.PhotoImage(data=cv2.imencode('.png', frame)[1].tobytes())

        self.canvas.config(width=img.width(), height=img.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = GravadorTela(root)
    root.mainloop()
