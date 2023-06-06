import tkinter as tk
from tkinter import messagebox
import subprocess
import re

class LatexEditor:
    def __init__(self, root):
        self.text_editor_frame = tk.Frame(root)
        self.text_editor_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.root = root 

        self.text_editor = tk.Text(self.text_editor_frame, height=20, width=80, font=("Arial", 12))
        self.text_editor.pack()

        default_code = r'''\documentclass{article}
\usepackage{amsmath}

 \begin{document}
    
 \end{document}'''
        self.text_editor.insert(tk.END, default_code)

        self.compile_button = tk.Button(self.text_editor_frame, text="Compiler", command=self.compile_latex)
        self.compile_button.pack()
    
    def get_code(self):
        return self.text_editor.get("1.0", tk.END)

    def insert_code(self, code):
        self.text_editor.insert("insert", code)

    def compile_latex(self):
        # Récupérer le code LaTeX saisi
        latex_code = self.get_code()

        # Sauvegarder le code LaTeX dans un fichier temporaire
        temp_filename = "temp.tex"
        with open(temp_filename, "w") as file:
            file.write(latex_code)

        try:
            # Exécuter la commande pdflatex pour compiler le code LaTeX
            subprocess.run(["pdflatex", temp_filename], check=True)

            # Afficher le message de réussite
            messagebox.showinfo("Compilation réussie", "Le code LaTeX a été compilé avec succès.")

            # Ouvrir le fichier PDF généré
            subprocess.run(["open", "temp.pdf"])

        except subprocess.CalledProcessError as e:
            # Afficher le message d'erreur en cas d'échec de la compilation
            messagebox.showerror("Erreur de compilation", "La compilation du code LaTeX a échoué.")

        # Supprimer le fichier temporaire
        subprocess.run(["rm", temp_filename])
