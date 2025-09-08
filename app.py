import pandas as pd
import streamlit as st
import duckdb as db
import numpy as np
import joblib

st.set_page_config(layout="wide")


# --- HEADER ---
st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center; gap: 20px; padding-top: 30px;">
        <img src="https://i.postimg.cc/yY1xYV0g/LE-CREUSOGRAPHE.png" width="100" style="border-radius: 15px;" />
        <h1 style="margin: 0; color: white;">Le Creusographe</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# === CHARGEMENT DU DATAFRAME PRINCIPAL df_master.csv ===
if "df" not in st.session_state:
    df = pd.read_csv("df_master.csv")
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

# === AFFICHAGE DES DÉTAILS D'UN FILM SÉLECTIONNÉ + RECOMMANDATIONS ===
if "selected_film_id" in st.session_state:
    film_id = st.session_state["selected_film_id"]
    film = df[df["movie_ID"] == film_id].iloc[0]

    st.markdown(f"## {film['frenchTitle']}")
    col1, col2 = st.columns([1, 3])
    with col1:
        image_url = (
            f"https://image.tmdb.org/t/p/w500{film['poster_path']}"
            if pd.notna(film["poster_path"])
            else "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Pas_d%27image_disponible.svg/2048px-Pas_d%27image_disponible.svg.png"
        )
        st.image(image_url, width=150)
    with col2:
        st.markdown(
            f"""
            - **Année** : {film['startYear']}  
            - **Genre(s)** : {film['genres']}  
            - **Note moyenne** : {film['averageRating']}  
            - {film['tagline']}
            """
        )

    st.markdown("---")

    # === AFFICHAGE DES RECOMMANDATIONS BASÉES SUR LE MODÈLE TF-IDF ===
    st.markdown(
        f"### Voici nos recommandations basées sur le contenu :\n**pour {film['frenchTitle']}**"
    )

    # Chargement des données pour le système de recommandation
    df_salade = pd.read_csv("df_salade.csv")
    recos = joblib.load("recos.pkl")

    # Trouver l'index du film dans df_salade
    film_index_in_salade = df_salade[df_salade["movie_ID"] == film_id].index

    if not film_index_in_salade.empty:
        film_index = film_index_in_salade[0]

        # Récupérer les indices des 8 recommandations les plus proches (en excluant le film lui-même)
        recommended_indices = recos[film_index][1:9]

        # Récupération des IDs et détails des films recommandés
        recommended_movie_ids = df_salade.iloc[recommended_indices]["movie_ID"].tolist()
        recommandations = df[df["movie_ID"].isin(recommended_movie_ids)]

        # Affichage des recommandations dans des colonnes
        cols = st.columns(len(recommandations))
        for i, (idx, row) in enumerate(recommandations.iterrows()):
            with cols[i]:
                if st.button(row["frenchTitle"], key=f"rec_film_{row['movie_ID']}"):
                    st.session_state["selected_film_id"] = row["movie_ID"]
                    st.rerun()

                image_url = (
                    f"https://image.tmdb.org/t/p/w500{row['poster_path']}"
                    if pd.notna(row["poster_path"])
                    else "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Pas_d%27image_disponible.svg/2048px-Pas_d%27image_disponible.svg.png"
                )

                st.markdown(
                    f"""
                    <div style='text-align: center;'>
                        <img src="{image_url}" style="max-width: 100%; border-radius: 8px;" />
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.warning("Aucune recommandation disponible pour ce film.")

    st.markdown("---")

    if st.button("Retour à la recherche", key="retour_resultats"):
        del st.session_state["selected_film_id"]
        st.rerun()

# === PAGE DE RECHERCHE D'UN FILM SI AUCUN FILM N'EST SÉLECTIONNÉ ===
else:
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        recherche_film = st.text_input(
            "Entrez le nom de votre film préféré :", key="film_name"
        )

        if recherche_film:
            resultats = df[
                df["frenchTitle"].str.contains(recherche_film, case=False, na=False)
            ]

            if not resultats.empty:
                st.success(f"{len(resultats)} film(s) trouvé(s) :")
                resultats_dedoublonnes = resultats.drop_duplicates(subset=["movie_ID"])

                for index, row in resultats_dedoublonnes.iterrows():
                    with st.container():
                        c1, c2 = st.columns([1, 3])
                        with c1:
                            image_url = (
                                f"https://image.tmdb.org/t/p/w500{row['poster_path']}"
                                if pd.notna(row["poster_path"])
                                else "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Pas_d%27image_disponible.svg/2048px-Pas_d%27image_disponible.svg.png"
                            )
                            st.image(image_url, width=120)
                        with c2:
                            if st.button(
                                f"{row['frenchTitle']}", key=f"film_{row['movie_ID']}"
                            ):
                                st.session_state["selected_film_id"] = row["movie_ID"]
                                st.rerun()

                            st.markdown(
                                f"""
                                - **Année** : {row['startYear']}  
                                - **Genre** : {row['genres']}  
                                - **Note** : {row['averageRating']}
                                """
                            )
                    st.markdown("---")
            else:
                st.error("Aucun film trouvé.")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 0.9em; padding: 10px 0;">
        Site réalisé par Le Creusographe (Charlotte, Eve, Jérémi et Samira) - juin 2025
    </div>
    """,
    unsafe_allow_html=True,
)
