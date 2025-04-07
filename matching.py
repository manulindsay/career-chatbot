import json
from sentence_transformers import SentenceTransformer, util
import streamlit as st

@st.cache_resource
def load_model():
    return SentenceTransformer("dangvantuan/sentence-camembert-base")

@st.cache_data
def load_metiers(filepath="data/metiers_competences.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def trouver_metiers(texte_utilisateur, metiers_data, model, seuil_score=0.4):
    embedding_user = model.encode(texte_utilisateur, convert_to_tensor=True)

    matched = []
    for code, infos in metiers_data.items():
        competences = infos.get("competences_cles", [])
        if not competences:
            continue

        texte_metier = ", ".join(competences)
        embedding_metier = model.encode(texte_metier, convert_to_tensor=True)
        score = util.cos_sim(embedding_user, embedding_metier).item()

        if score > seuil_score:
            matched.append({
                "code": code,
                "libelle": infos.get("libelle", "Inconnu"),
                "score": round(score, 3),
                "secteurs": infos.get("secteurs_activite", [])
            })

    matched.sort(key=lambda x: x["score"], reverse=True)
    return matched