#Ici, nous faisons une demande de récupération d'un métier en fonction des compétences de l'utilisateur

import requests
from auth_api_ft import get_access_token

# URL de l'API pour récupérer les métiers
API_URL = "https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/metier" 

def get_metiers():

    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(API_URL, headers=headers)

    if response.status_code == 200:
        metiers = response.json()
        if isinstance(metiers, list):
            return metiers
        else:
            raise ValueError("La réponse de l'API n'est pas une liste.")
    else:
        raise Exception(f"Erreur {response.status_code}: {response.text}")

