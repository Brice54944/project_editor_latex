#chatgpt_api.py

import configparser
import requests


# Charger la clé d'API à partir du fichier de configuration
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get('API', 'key')

# Fonction d'appel à l'API de ChatGPT
#def call_chatGPT_api(prompt):
    #url = "https://api.openai.com/v1/chat/completions"
    #headers = {
    #    "Authorization": f"Bearer {api_key}",
     #   "Content-Type": "application/json"
    #}
    #data = {
    #    "prompt": prompt,
    #    "max_tokens": 100
    #}
    #response = requests.post(url, headers=headers, json=data)
    #return response.json()["choices"][0]["text"].strip()

    
def call_chatGPT_api(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }
    response = requests.post(url, headers=headers, json=data)
    
    # Afficher la réponse complète de l'API dans la console
    print(response.json())
    
    response_data = response.json()
    if "choices" in response_data and len(response_data["choices"]) > 0:
        return response_data["choices"][0]["message"]["content"].strip()
    else:
        return "Erreur : Réponse inattendue de l'API"




