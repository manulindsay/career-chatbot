import json
from sentence_transformers import SentenceTransformer, util

# === Chargement du fichier enrichi ===
with open("data/metiers_competences.json", "r", encoding="utf-8") as f:
    metiers_data = json.load(f)

# === Chargement du modèle optimisé SentenceCamemBERT ===
model = SentenceTransformer("dangvantuan/sentence-camembert-base")

# === Saisie utilisateur ===
user_input = ""
while not user_input.strip():
    print(" Entrez vos compétences, séparées par des virgules :")
    user_input = input(" Vos compétences : ")
    if not user_input.strip():
        print(" Vous devez saisir au moins une compétence.\n")

texte_utilisateur = user_input.strip()

# === Encodage utilisateur ===
embedding_user = model.encode(texte_utilisateur, convert_to_tensor=True)

# === Matching avec les métiers ===
matched_metiers = []
for code, infos in metiers_data.items():
    competences = infos.get("competences_cles", [])
    if not competences:
        continue

    texte_metier = ", ".join(competences)
    embedding_metier = model.encode(texte_metier, convert_to_tensor=True)
    score = util.cos_sim(embedding_user, embedding_metier).item()

    if score > 0.4:
        matched_metiers.append({
            "code": code,
            "libelle": infos.get("libelle", "Inconnu"),
            "score": round(score, 3),
            "secteurs": infos.get("secteurs_activite", [])
        })

# Trier les métiers par score décroissant
matched_metiers.sort(key=lambda x: x["score"], reverse=True)

# === Récupération de tous les secteurs liés aux métiers compatibles ===
tous_secteurs = set()
for metier in matched_metiers:
    tous_secteurs.update(metier["secteurs"])

if not matched_metiers:
    print(" Aucun métier trouvé avec un score > 0.6.")
    exit()

# === Affichage des secteurs + choix utilisateur ===
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

# === Filtrage final des métiers ===
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

if matched_metiers:
    for metier in matched_metiers:
        print(f" {metier['libelle']} ({metier['code']}) — Score : {metier['score']}")
        if metier['secteurs']:
            print(f"    Secteurs : {', '.join(metier['secteurs'])}")
        
else:
    print(" Aucun métier trouvé avec les critères choisis.")
