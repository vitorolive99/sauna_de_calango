import tkinter as tk

class ExperimentGUI:
    def __init__(self, master, start_program_CTmax):
        self.master = master
        self.master.title("Experiment GUI")
        self.master.geometry("400x200")  # Defina o tamanho da janela da GUI

        self.start_program_CTmax = start_program_CTmax  # Função start_program() de app.py

        self.experiment_type = tk.StringVar()  # Variável para armazenar a opção selecionada
        self.experiment_type.set("CTmax")  # Valor padrão inicial

        self.start_button = tk.Button(self.master, text="Iniciar Experimento", command=self.start_experiment)
        self.start_button.pack(pady=20)

        # Adiciona os botões de rádio
        tk.Radiobutton(self.master, text="CTmax", variable=self.experiment_type, value="CTmax").pack()
        tk.Radiobutton(self.master, text="CTmin", variable=self.experiment_type, value="CTmin").pack()

    def start_experiment(self):
        print("Iniciando experimento...")
        experiment_type = self.experiment_type.get()
        print("Tipo de experimento selecionado:", experiment_type)

        if experiment_type == "CTmax":
            self.start_program_CTmax()

def create_gui(start_program_CTmax):
    root = tk.Tk()
    gui = ExperimentGUI(root, start_program_CTmax)
    root.mainloop()
