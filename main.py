#main.py

import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import configparser
import subprocess
import re

from chatgpt_api import call_chatGPT_api



class TextLineNumber(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.config(bg="#f0f0f0", relief="flat", state="disabled", width=4)
        self._update_line_numbers()

    def _update_line_numbers(self, *args):
        self.config(state="normal")
        self.delete("1.0", tk.END)
        line_count = self.index(tk.END).split(".")[0]
        for i in range(1, int(line_count) + 1):
            self.insert(tk.END, str(i) + "\n")
        self.config(state="disabled")


class LatexEditor:
    def __init__(self, root):
        self.text_editor_frame = tk.Frame(root)
        self.text_editor_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.text_editor = ScrolledText(self.text_editor_frame, height=20, width=80, font=("Arial", 12))
        self.text_editor.pack(fill="both", expand=True)

        self.line_numbers = TextLineNumber(self.text_editor_frame, width=4, bg="#f0f0f0")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_editor.config(yscrollcommand=self._scroll_editor_yview)
        self.line_numbers.config(yscrollcommand=self._scroll_line_numbers_yview)

        self.text_editor.bind("<Key>", self._on_key_press)

        default_code = r'''\documentclass{article}
\usepackage{amsmath}

\begin{document}

\end{document}'''
        self.text_editor.insert(tk.END, default_code)
        self.line_numbers._update_line_numbers()

    def _on_key_press(self, event):
        self.line_numbers._update_line_numbers()
        self._scroll_editor_yview(event)

    def _scroll_editor_yview(self, *args):
        self.line_numbers.yview_moveto(*args[0])
        self.text_editor.yview_moveto(*args[0])

    def _scroll_line_numbers_yview(self, *args):
        self.line_numbers.yview_moveto(*args[0])
        self.text_editor.yview_moveto(*args[0])

    def get_code(self):
        return self.text_editor.get("1.0", tk.END)

    def insert_code(self, code):
        self.text_editor.insert("1.0", code)
        self.line_numbers._update_line_numbers()


def process_query():
    query = text_entry.get("1.0", tk.END).strip()
    prompt = "Donne moi le code LaTex correspondant à " + query + ", uniquement le code. Utilise le format '$$' pour l'équation. Si la réponse comporte plusieurs équations donne uniquement le code correspondant à chacune. Aucunes phrases ne sont nécessaires. Formate le code avec des retours à la ligne pour que ce soit visible."
    window.update()

    response = call_chatGPT_api(prompt)
    output_text.insert("insert", response)

    code = extract_latex_code(response)
    latex_editor.insert_code(code)


def extract_latex_code(response):
    # Extraire le code LaTeX de la réponse de l'API
    code = re.findall(r"\$\$.*?\$\$", response, re.DOTALL)
    code = "\n".join(code)
    return code


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

input_frame = tk.Frame(window)
input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

text_entry = ScrolledText(input_frame, height=5, width=40, font=("Arial", 12))
text_entry.pack(fill="both", expand=True)

output_frame = tk.Frame(window)
output_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

output_text = ScrolledText(output_frame, height=5, width=40, font=("Arial", 12))
output_text.pack(fill="both", expand=True)

submit_button = tk.Button(input_frame, text="Soumettre", command=process_query)
submit_button.pack(pady=10)

compile_button = tk.Button(output_frame, text="Compiler", command=compile_latex)
compile_button.pack(pady=10)

window.mainloop()


