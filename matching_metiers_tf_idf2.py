import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# === Chargement des données métiers enrichies ===
with open("metiers_competences.json", "r", encoding="utf-8") as f:
    metiers_data = json.load(f)

# === Saisie utilisateur ===
user_input = ""
while not user_input.strip():
    print(" Entrez vos compétences, séparées par des virgules (ex: soudure, élagage, tronçonneuse) :")
    user_input = input(" Vos compétences : ")
    if not user_input.strip():
        print(" Vous devez saisir au moins une compétence.\n")

texte_utilisateur = user_input.strip()

# === Préparation des données pour TF-IDF ===
codes = []
libelles = []
corpus = []

for code, infos in metiers_data.items():
    competences = infos.get("competences_cles", [])
    if not competences:
        continue
    corpus.append(", ".join(competences))
    codes.append(code)
    libelles.append(infos.get("libelle", "Inconnu"))

# Ajouter l'utilisateur au début
corpus.insert(0, texte_utilisateur)

# === TF-IDF Matching ===
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)
similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

# === Enregistrer les métiers compatibles (mais ne pas afficher) ===
matched_metiers = []
for i, score in enumerate(similarities):
    if score > 0.02:
        matched_metiers.append({
            "code": codes[i],
            "libelle": libelles[i],
            "score": round(score, 3),
            "secteurs": metiers_data[codes[i]].get("secteurs_activite", [])
        })

# Trier par score
matched_metiers.sort(key=lambda x: x["score"], reverse=True)

# === Récupérer tous les secteurs disponibles ===
tous_secteurs = set()
for metier in matched_metiers:
    tous_secteurs.update(metier["secteurs"])

# Si aucun métier trouvé
if not matched_metiers:
    print(" Aucun métier trouvé avec un score supérieur à 0.6.")
    exit()

# === Afficher les secteurs disponibles ===
if tous_secteurs:
    print("\n Voici les secteurs d'activité liés aux métiers compatibles :")
    secteurs_list = sorted(list(tous_secteurs))
    for idx, sec in enumerate(secteurs_list, 1):
        print(f"{idx}. {sec}")

    selection = input("\n Entrez les numéros des secteurs que vous préférez (ex: 1,3) ou appuyez sur Entrée pour tous les métiers : ")

    if selection.strip():
        try:
            selected_indices = [int(x.strip()) for x in selection.split(",") if x.strip().isdigit()]
            selected_secteurs = {secteurs_list[i - 1] for i in selected_indices if 1 <= i <= len(secteurs_list)}
        except Exception:
            print(" Saisie invalide. Affichage de tous les métiers.")
            selected_secteurs = set()
    else:
        selected_secteurs = set()
else:
    selected_secteurs = set()

# === Filtrer si secteurs sélectionnés ===
if selected_secteurs:
    matched_metiers = [
        m for m in matched_metiers
        if set(m["secteurs"]).intersection(selected_secteurs)
    ]

# === Affichage final ===
print("\n Métiers correspondant à vos compétences", end="")
if selected_secteurs:
    print(" ET aux secteurs choisis :\n")
else:
    print(" :\n")

for metier in matched_metiers:
    print(f" {metier['libelle']} ({metier['code']}) — Score : {metier['score']}")
    if metier['secteurs']:
        print(f"    Secteurs : {', '.join(metier['secteurs'])}")
    print("-" * 50)

if not matched_metiers:
    print(" Aucun métier trouvé pour les critères sélectionnés.")
