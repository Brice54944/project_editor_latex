import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import configparser
import subprocess
import webbrowser

from chatgpt_api import call_chatGPT_api


class LatexEditor:
    def __init__(self, root):
        self.text_editor_frame = ttk.Frame(root, padding="10")
        self.text_editor_frame.grid(row=0, column=0, sticky="nsew")

        self.text_editor = ScrolledText(self.text_editor_frame, height=20, width=80, font=("Arial", 12))
        self.text_editor.pack(fill="both", expand=True)

        default_code = r'''\documentclass{article}
\usepackage{amsmath}

 \begin{document}
    
 \end{document}'''
        self.text_editor.insert(tk.END, default_code)

    def get_code(self):
        return self.text_editor.get("1.0", tk.END)

    def insert_code(self, code):
        self.text_editor.insert("insert", code)


def process_query():
    query = text_entry.get("1.0", tk.END).strip()
    prompt = "Donne moi le code LaTex correspondant à " + query + ", uniquement le code. Utilise le format '$$' pour l'équation. Si la réponse comporte plusieurs équations donne uniquement le code correspondant à chacune. Aucunes phrases ne sont nécessaires. Formate le code avec des retours à la ligne pour que ce soit visible."
    window.update()

    response = call_chatGPT_api(prompt)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, response)

    latex_editor.insert_code(response)


def compile_latex():
    latex_code = latex_editor.get_code()
    temp_filename = "temp.tex"
    with open(temp_filename, "w") as file:
        file.write(latex_code)

    try:
        subprocess.run(["pdflatex", temp_filename], check=True)
        messagebox.showinfo("Compilation réussie", "Le code LaTeX a été compilé avec succès.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur de compilation", "La compilation du code LaTeX a échoué.")

    subprocess.run(["rm", temp_filename])


# Load API key from the configuration file
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get('API', 'key')

# Create main application window
window = tk.Tk()
window.title("Éditeur LaTeX")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

latex_editor = LatexEditor(window)

input_frame = ttk.Frame(window, padding="10")
input_frame.grid(row=1, column=0, sticky="ew")

text_entry = ScrolledText(input_frame, height=5, width=40, font=("Arial", 12))
text_entry.pack(fill="both", expand=True)

output_frame = ttk.Frame(window, padding="10")
output_frame.grid(row=2, column=0, sticky="ew")

output_text = ScrolledText(output_frame, height=5, width=40, font=("Arial", 12))
output_text.pack(fill="both", expand=True)

submit_button = ttk.Button(input_frame, text="Soumettre", command=process_query)
submit_button.pack(pady=10)

compile_button = ttk.Button(output_frame, text="Compiler", command=compile_latex)
compile_button.pack(pady=10)


window.mainloop()
