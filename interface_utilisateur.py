import tkinter as tk
import configparser

from chatgpt_api import call_chatGPT_api

# Charger la clé d'API à partir du fichier de configuration
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get('API', 'key')


# Fonction de traitement de la requête
def process_query():
    # Obtenir le texte saisi par l'utilisateur
    query = text_entry.get("1.0", tk.END).strip()

    # Rafraîchir l'interface utilisateur pour afficher le texte saisi
    window.update()

    # Afficher le texte saisi dans la zone de texte de sortie
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, query)

    # Appeler l'API de ChatGPT pour obtenir la réponse en LaTeX
    response = call_chatGPT_api(query)

    # Afficher le résultat dans la zone de texte de sortie
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, response)


# Créer la fenêtre principale de l'éditeur LaTeX
window = tk.Tk()
window.title("Éditeur LaTeX")

# Créer une zone de texte pour l'entrée de l'utilisateur
text_entry = tk.Text(window, height=10, width=60, font=("Arial", 12))
text_entry.pack(pady=10)

# Créer un bouton pour soumettre la requête
submit_button = tk.Button(window, text="Soumettre", command=process_query)
submit_button.pack()

# Créer une zone de texte pour afficher la sortie
output_text = tk.Text(window, height=20, width=60, font=("Arial", 12))
output_text.pack(pady=10)

# Démarrer la boucle principale de l'interface utilisateur
window.mainloop()


