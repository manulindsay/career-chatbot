# Ici, nous faisons une demande de récupération des secteurs d'activité de nos métiers

import json
import requests
import time
from auth_api_ft import get_access_token

# API France Travail
API_URL_DETAILS = "https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/metier"

# Charger le fichier existant
with open("metiers_competences.json", "r", encoding="utf-8") as f:
    metiers_data = json.load(f)

# Fonction pour récupérer les secteurs
def get_metier_secteurs(code_metier):
    try:
        access_token = get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{API_URL_DETAILS}/{code_metier}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            secteurs = []

            if "secteursActivites" in data:
                for sec in data["secteursActivites"]:
                    if "secteurActivite" in sec and "libelle" in sec["secteurActivite"]:
                        secteurs.append(sec["secteurActivite"]["libelle"])
                    elif "libelle" in sec:
                        secteurs.append(sec["libelle"])

            return list(set(secteurs))

        else:
            print(f" Code {code_metier} — Erreur {response.status_code}")
            return []

    except Exception as e:
        print(f" Exception pour {code_metier} : {e}")
        return []

#  Parcourir les métiers et enrichir avec les secteurs
print(" Ajout des secteurs d'activité en cours...\n")

for code, infos in metiers_data.items():
    if "secteurs_activite" in infos:
        print(f" {code} déjà enrichi, on saute.")
        continue

    secteurs = get_metier_secteurs(code)
    metiers_data[code]["secteurs_activite"] = secteurs
    print(f" {infos['libelle']} ({code}) → {len(secteurs)} secteur(s)")
    time.sleep(7)

#  Sauvegarde dans le fichier original
with open("metiers_competences.json", "w", encoding="utf-8") as f:
    json.dump(metiers_data, f, ensure_ascii=False, indent=4)

print("\n Mise à jour terminée. Le fichier a été enrichi avec les secteurs d'activité.")
