import streamlit as st
from matching import load_model, load_metiers, trouver_metiers

# === Chargement du modèle et des données ===
model = load_model()
metiers_data = load_metiers()

# === Interface ===
st.title("🔍 Recommandation de Métiers à partir de vos Compétences")

# === Étape 1 : Saisie des compétences ===
user_input = st.text_input(" Entrez vos compétences (séparées par des virgules) :")

if user_input.strip():
    texte_utilisateur = user_input.strip()

    # Matching fait en backend, mais pas encore affiché
    matched_metiers = trouver_metiers(texte_utilisateur, metiers_data, model)

    if matched_metiers:
        # === Étape 2 : Choix des secteurs ===
        tous_secteurs = sorted({s for m in matched_metiers for s in m["secteurs"]})
        selected_secteurs = st.multiselect(
            " Choisissez les secteurs d'activité qui vous intéressent (ou laissez vide pour tout afficher) :",
            tous_secteurs,
        )

        # === Étape 3 : Affichage conditionnel ===
        if st.button("Afficher les résultats"):
            # Filtrage si sélection
            if selected_secteurs:
                matched_metiers = [
                    m for m in matched_metiers
                    if set(m["secteurs"]).intersection(selected_secteurs)
                ]

            # Résultats
            st.subheader(" Résultats :")
            if matched_metiers:
                for m in matched_metiers:
                    st.markdown(f"**{m['libelle']}** (`{m['code']}`) — Score : {m['score']}")
                    if m['secteurs']:
                        st.markdown(f" Secteurs : {', '.join(m['secteurs'])}")
                    st.markdown("---")
            else:
                st.warning("Aucun métier trouvé avec les secteurs choisis.")
    else:
        st.warning("Aucun métier trouvé avec vos compétences.")
