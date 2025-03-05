# Ici, nous faisons une demande de Token qui nous permet d'accéder à l'API de France Travail

import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv(dotenv_path="api_ft.env")

# Récupérer les identifiants API depuis .env
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = os.getenv("TOKEN_URL")
SCOPE = os.getenv("SCOPE")

def get_access_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPE
    }
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("Token récupéré avec succès !")
        return token
    else:
        raise Exception(f"Erreur {response.status_code}: {response.text}")
