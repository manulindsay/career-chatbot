# Ici, nous faisons une demande de récupération des métiers et de leurs compétences clés

import requests
import time
import json
from auth_api_ft import get_access_token
from metiers import get_metiers

API_URL_DETAILS = "https://api.francetravail.io/partenaire/rome-metiers/v1/metiers/metier"

def get_metier_competences(code_metier):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(f"{API_URL_DETAILS}/{code_metier}", headers=headers)

    if response.status_code == 200:
        metiers_competences = response.json()

        competences_cles = set()

        if "competencesMobilisees" in metiers_competences:
            for comp in metiers_competences["competencesMobilisees"]:
                if "libelle" in comp:
                    competences_cles.add(comp["libelle"])

        if "appellations" in metiers_competences:
            for appellation in metiers_competences["appellations"]:
                if "competencesCles" in appellation:
                    for comp in appellation["competencesCles"]:
                        if "competence" in comp and "libelle" in comp["competence"]:
                            competences_cles.add(comp["competence"]["libelle"])

        return list(competences_cles)

    else:
        raise Exception(f"Erreur {response.status_code}: {response.text}")

if __name__ == "__main__":
    try:
        metiers = get_metiers()
        metiers_data = {}

        print("Récupération des compétences en cours...\n")

        for metier in metiers:
            code = metier['code']
            libelle = metier['libelle']

            try:
                competences_cles = get_metier_competences(code)

                metiers_data[code] = {
                    "libelle": libelle,
                    "competences_cles": competences_cles
                }

                print(f"{libelle} ({code}) enregistré avec {len(competences_cles)} compétences.")
            except Exception as e:
                print(f"Erreur pour {libelle} ({code}) : {e}")

            time.sleep(7)

        # Sauvegarde dans un fichier JSON
        with open("metiers_competences.json", "w", encoding="utf-8") as f:
            json.dump(metiers_data, f, ensure_ascii=False, indent=4)

        print("\n Sauvegarde terminée dans 'metiers_competences.json'.")

    except Exception as e:
        print(f" Une erreur générale s'est produite : {e}")
