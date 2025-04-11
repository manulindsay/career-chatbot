import streamlit as st
from matching1 import (
    load_model,
    load_metiers,
    trouver_metiers,
    extraire_competences_depuis_pdf,
)

# === Chargement du modèle et des données ===
model = load_model()
metiers_data = load_metiers()

# === Titre et instructions ===
st.title("🤖 Chatbot de Recommandation de Métiers")
st.markdown("Choisissez une méthode pour obtenir vos suggestions de métiers :")

# === Choix du mode
mode = st.radio("Méthode d'analyse :", ["📝 Saisie manuelle", "📄 Dépôt de CV (PDF)"])
texte_utilisateur = ""

# === Saisie manuelle
if mode == "📝 Saisie manuelle":
    texte_utilisateur = st.text_area("Entrez vos compétences ou une description :")

# === Dépôt de CV
elif mode == "📄 Dépôt de CV (PDF)":
    uploaded_file = st.file_uploader("Déposez votre CV au format PDF", type=["pdf"])
    if uploaded_file:
        texte_utilisateur = extraire_competences_depuis_pdf(uploaded_file)
        st.success("CV analysé avec succès.")

# === Matching
if texte_utilisateur.strip():
    if (
        "matched_metiers" not in st.session_state
        or st.session_state.get("texte_source") != texte_utilisateur
    ):
        with st.spinner(" Analyse en cours..."):
            matched_metiers = trouver_metiers(texte_utilisateur, metiers_data, model)
        st.session_state["matched_metiers"] = matched_metiers
        st.session_state["texte_source"] = texte_utilisateur
        st.session_state["filtered_metiers"] = []
        st.session_state["show_results"] = False
    else:
        matched_metiers = st.session_state["matched_metiers"]

    if matched_metiers:
        tous_secteurs = sorted({s for m in matched_metiers for s in m["secteurs"]})
        selected_secteurs = st.multiselect(
            "Choisissez les secteurs d'activité (facultatif) :",
            tous_secteurs,
            key="secteurs_selection"
        )

        if st.button(" Rechercher les métiers correspondants"):
            st.session_state["show_results"] = True
            if selected_secteurs:
                st.session_state["filtered_metiers"] = [
                    m for m in matched_metiers if set(m["secteurs"]).intersection(selected_secteurs)
                ]
            else:
                st.session_state["filtered_metiers"] = matched_metiers

# === Affichage après clic
if st.session_state.get("show_results"):
    st.subheader(" Métiers recommandés :")
    if st.session_state["filtered_metiers"]:
        for m in st.session_state["filtered_metiers"]:
            st.markdown(f"**{m['libelle']}** (`{m['code']}`) — Score : {m['score']}")
            if m["secteurs"]:
                st.markdown(f" Secteurs : {', '.join(m['secteurs'])}")
            st.markdown("---")
    else:
        st.warning("Aucun métier trouvé avec les secteurs sélectionnés.")
