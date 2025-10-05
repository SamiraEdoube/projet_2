import pandas as pd
import streamlit as st
import joblib

# ============================================
# CONFIGURATION DE LA PAGE
# ============================================
st.set_page_config(
    page_title="Le Creusographe - Cinéma de la Creuse",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================
# STYLES CSS VINTAGE
# ============================================
st.markdown(
    """
<style>
    /* Import de police vintage */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
    
    /* Couleurs vintage */
    :root {
        --vintage-gold: #d4af37;
        --vintage-dark-gold: #aa8c2c;
        --vintage-red: #8B0000;
        --vintage-dark-red: #5c0000;
        --vintage-cream: #f5e6d3;
        --vintage-dark: #2c1810;
        --vintage-gray: #4a4a4a;
    }
    
    /* Background global */
    .stApp {
        background: linear-gradient(to bottom, #f5e6d3 0%, #e8d5bd 100%);
    }
    
    /* Cache le menu Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* HEADER VINTAGE */
    .vintage-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #8B0000 0%, #5c0000 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 40px rgba(44, 24, 16, 0.4);
        border: 4px solid #d4af37;
        position: relative;
    }
    
    .vintage-header::before {
        content: '';
        position: absolute;
        top: 10px;
        left: 10px;
        right: 10px;
        bottom: 10px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 15px;
        pointer-events: none;
    }
    
    .vintage-header h1 {
        font-family: 'Cinzel', serif;
        color: #d4af37;
        font-size: 3.5rem;
        margin: 0;
        font-weight: 700;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        letter-spacing: 4px;
    }
    
    .vintage-header p {
        font-family: 'Crimson Text', serif;
        color: #f5e6d3;
        font-size: 1.3rem;
        margin-top: 0.8rem;
        font-style: italic;
        letter-spacing: 2px;
    }
    
    .vintage-badge {
        display: inline-block;
        margin-top: 1rem;
        padding: 0.5rem 1.5rem;
        background: transparent;
        border: 2px solid #d4af37;
        border-radius: 25px;
        color: #d4af37;
        font-family: 'Cinzel', serif;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 2px;
    }
    
    /* CARTES DE FILMS VINTAGE */
    .film-card {
        background: linear-gradient(135deg, #f5e6d3 0%, #e8d5bd 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        transition: all 0.4s ease;
        border: 3px solid #d4af37;
        box-shadow: 0 8px 20px rgba(44, 24, 16, 0.2);
        position: relative;
    }
    
    .film-card::before {
        content: '';
        position: absolute;
        top: 8px;
        left: 8px;
        right: 8px;
        bottom: 8px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        pointer-events: none;
    }
    
    .film-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(139, 0, 0, 0.3);
        border-color: #8B0000;
    }
    
    /* BADGES VINTAGE */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 5px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-right: 0.8rem;
        margin-bottom: 0.5rem;
        font-family: 'Crimson Text', serif;
        letter-spacing: 1px;
    }
    
    .badge-year {
        background: linear-gradient(135deg, #8B0000 0%, #5c0000 100%);
        color: #d4af37;
        border: 1px solid #d4af37;
    }
    
    .badge-rating {
        background: linear-gradient(135deg, #d4af37 0%, #aa8c2c 100%);
        color: #2c1810;
        border: 1px solid #aa8c2c;
    }
    
    /* BOUTONS VINTAGE */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #8B0000 0%, #5c0000 100%);
        color: #d4af37;
        border: 2px solid #d4af37;
        padding: 0.8rem;
        font-weight: 700;
        font-family: 'Cinzel', serif;
        letter-spacing: 2px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5c0000 0%, #8B0000 100%);
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(139, 0, 0, 0.5);
        color: #f5e6d3;
    }
    
    /* SECTION RECOMMANDATIONS */
    .reco-section {
        background: linear-gradient(135deg, rgba(139, 0, 0, 0.1) 0%, rgba(92, 0, 0, 0.05) 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        border: 3px solid #8B0000;
        box-shadow: 0 10px 30px rgba(44, 24, 16, 0.2);
        position: relative;
    }
    
    .reco-section::before {
        content: '★';
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 2rem;
        color: #d4af37;
        background: #f5e6d3;
        padding: 0 1rem;
    }
    
    .reco-title {
        color: #8B0000;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-align: center;
        font-family: 'Cinzel', serif;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    /* IMAGES VINTAGE */
    img {
        border-radius: 8px;
        box-shadow: 0 8px 20px rgba(44, 24, 16, 0.4);
        transition: all 0.3s ease;
        border: 3px solid #d4af37;
    }
    
    img:hover {
        transform: scale(1.08);
        box-shadow: 0 12px 30px rgba(139, 0, 0, 0.4);
    }
    
    /* INPUT DE RECHERCHE VINTAGE */
    .stTextInput > div > div > input {
        background: #f5e6d3;
        border: 2px solid #d4af37;
        border-radius: 10px;
        color: #2c1810;
        font-family: 'Crimson Text', serif;
        font-size: 1.1rem;
        padding: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8B0000;
        box-shadow: 0 0 15px rgba(139, 0, 0, 0.3);
    }
    
    /* TITRES DE FILMS */
    h3 {
        font-family: 'Cinzel', serif;
        color: #8B0000;
        letter-spacing: 2px;
    }
    
    /* MESSAGES */
    .stSuccess {
        background: rgba(212, 175, 55, 0.2);
        border: 2px solid #d4af37;
        border-radius: 10px;
        color: #2c1810;
        font-family: 'Crimson Text', serif;
    }
    
    .stError {
        background: rgba(139, 0, 0, 0.1);
        border: 2px solid #8B0000;
        border-radius: 10px;
        color: #8B0000;
        font-family: 'Crimson Text', serif;
    }
    
    .stWarning {
        background: rgba(170, 140, 44, 0.1);
        border: 2px solid #aa8c2c;
        border-radius: 10px;
        color: #2c1810;
        font-family: 'Crimson Text', serif;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(245, 230, 211, 0.8) 0%, rgba(232, 213, 189, 0.8) 100%);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 1.5rem;
        color: #2c1810;
        font-family: 'Crimson Text', serif;
        font-size: 1.1rem;
    }
    
    /* LIGNE SÉPARATRICE VINTAGE */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #d4af37, transparent);
        margin: 2rem 0;
    }
    
    /* FOOTER VINTAGE */
    .footer {
        text-align: center;
        padding: 2.5rem;
        margin-top: 3rem;
        color: #2c1810;
        border-top: 3px double #d4af37;
        font-family: 'Crimson Text', serif;
        background: rgba(245, 230, 211, 0.5);
        border-radius: 15px;
    }
    
    .footer-ornament {
        font-size: 1.5rem;
        color: #d4af37;
        margin: 0.5rem 0;
    }
    
    /* ORNEMENTS DÉCORATIFS */
    .ornament {
        text-align: center;
        color: #d4af37;
        font-size: 1.5rem;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ============================================
# CHARGEMENT DES DONNÉES
# ============================================
@st.cache_data
def load_data():
    """Charge les données avec mise en cache"""
    df = pd.read_csv("df_master.csv")
    df_salade = pd.read_csv("df_salade.csv")
    return df, df_salade


@st.cache_resource
def load_model():
    """Charge le modèle de recommandation"""
    return joblib.load("recos.pkl")


# Chargement
df, df_salade = load_data()
recos = load_model()

# ============================================
# HEADER VINTAGE
# ============================================
st.markdown(
    """
<div class="vintage-header">
    <h1>🎞️ LE CREUSOGRAPHE 🎞️</h1>
    <p>Cinéma de la Creuse - Depuis 1925</p>
    <div class="vintage-badge">DÉPARTEMENT 23</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="ornament">❦ ❦ ❦</div>', unsafe_allow_html=True)


# ============================================
# FONCTION AFFICHAGE FILM
# ============================================
def afficher_film_card(row, key_prefix=""):
    """Affiche une carte de film style vintage"""
    col1, col2 = st.columns([1, 3])

    with col1:
        image_url = (
            f"https://image.tmdb.org/t/p/w500{row['poster_path']}"
            if pd.notna(row["poster_path"])
            else "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Pas_d%27image_disponible.svg/2048px-Pas_d%27image_disponible.svg.png"
        )
        st.image(image_url, use_container_width=True)

    with col2:
        st.markdown(f"### {row['frenchTitle']}")

        # Badges vintage
        annee = int(row["startYear"]) if pd.notna(row["startYear"]) else "N/A"
        st.markdown(
            f"""
        <div>
            <span class="badge badge-year">📅 {annee}</span>
            <span class="badge badge-rating">⭐ {row['averageRating']}/10</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(f"**Genres :** {row['genres']}")

        if pd.notna(row.get("tagline")) and row["tagline"]:
            st.markdown(f"*« {row['tagline']} »*")

        # Bouton recommandations
        if st.button(
            f"🎬 Découvrir les recommandations", key=f"{key_prefix}{row['movie_ID']}"
        ):
            st.session_state["selected_film_id"] = row["movie_ID"]
            st.rerun()


# ============================================
# PAGE : DÉTAILS + RECOMMANDATIONS
# ============================================
if "selected_film_id" in st.session_state:
    film_id = st.session_state["selected_film_id"]
    film = df[df["movie_ID"] == film_id].iloc[0]

    # Bouton retour
    col_retour, col_spacer = st.columns([1, 4])
    with col_retour:
        if st.button("← Retour à la recherche", key="btn_retour"):
            del st.session_state["selected_film_id"]
            st.rerun()

    st.markdown("---")

    # Film sélectionné
    st.markdown("## 🎬 Film sélectionné")
    afficher_film_card(film, key_prefix="selected_")

    st.markdown("---")
    st.markdown('<div class="ornament">❦ ❦ ❦</div>', unsafe_allow_html=True)

    # ============================================
    # RECOMMANDATIONS
    # ============================================
    st.markdown('<div class="reco-section">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="reco-title">Films similaires</div>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p style="text-align: center; font-family: \'Crimson Text\', serif; font-size: 1.2rem; color: #2c1810; font-style: italic;">Basé sur « {film["frenchTitle"]} »</p>',
        unsafe_allow_html=True,
    )

    # Trouver les recommandations
    film_index_in_salade = df_salade[df_salade["movie_ID"] == film_id].index

    if not film_index_in_salade.empty:
        film_index = film_index_in_salade[0]

        # Les 8 recommandations
        recommended_indices = recos[film_index][1:9]
        recommended_movie_ids = df_salade.iloc[recommended_indices]["movie_ID"].tolist()
        recommandations = df[df["movie_ID"].isin(recommended_movie_ids)]

        # Affichage en grille 4 colonnes
        cols = st.columns(4)
        for i, (idx, row) in enumerate(recommandations.iterrows()):
            with cols[i % 4]:
                image_url = (
                    f"https://image.tmdb.org/t/p/w500{row['poster_path']}"
                    if pd.notna(row["poster_path"])
                    else "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Pas_d%27image_disponible.svg/2048px-Pas_d%27image_disponible.svg.png"
                )

                st.image(image_url, use_container_width=True)

                titre = (
                    row["frenchTitle"][:30] + "..."
                    if len(row["frenchTitle"]) > 30
                    else row["frenchTitle"]
                )
                st.markdown(
                    f"<p style='text-align: center; font-family: \"Cinzel\", serif; font-weight: 600; color: #2c1810;'>{titre}</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<p style='text-align: center; color: #8B0000;'>⭐ {row['averageRating']}/10</p>",
                    unsafe_allow_html=True,
                )

                if st.button("Voir ce film", key=f"rec_{row['movie_ID']}"):
                    st.session_state["selected_film_id"] = row["movie_ID"]
                    st.rerun()
    else:
        st.warning("😕 Aucune recommandation disponible pour ce film.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# PAGE : RECHERCHE
# ============================================
else:
    st.markdown("## 🔍 Recherche de films")
    st.markdown('<div class="ornament">❦</div>', unsafe_allow_html=True)

    # Barre de recherche
    recherche_film = st.text_input(
        "",
        placeholder="Entrez le titre d'un film (ex : Le Parrain, Titanic, Matrix...)",
        key="film_name",
        label_visibility="collapsed",
    )

    # Résultats de recherche
    if recherche_film:
        resultats = df[
            df["frenchTitle"].str.contains(recherche_film, case=False, na=False)
        ]

        if not resultats.empty:
            resultats_dedoublonnes = resultats.drop_duplicates(subset=["movie_ID"])

            st.success(
                f"✨ {len(resultats_dedoublonnes)} film(s) trouvé(s) dans notre catalogue"
            )
            st.markdown("---")

            # Affichage des résultats
            for index, row in resultats_dedoublonnes.iterrows():
                st.markdown('<div class="film-card">', unsafe_allow_html=True)
                afficher_film_card(row, key_prefix=f"search_{index}_")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("😕 Aucun film trouvé. Essayez avec un autre titre !")

    else:
        # Message d'accueil
        st.info(
            """
        🎭 **Bienvenue au Creusographe !**
        
        Entrez le nom d'un film que vous appréciez dans la barre de recherche ci-dessus.
        Notre système vous proposera des recommandations personnalisées basées sur vos goûts cinématographiques.
        
        💡 *Astuce : Vous pouvez rechercher par titre français ou original*
        """
        )

        st.markdown('<div class="ornament">❦ ❦ ❦</div>', unsafe_allow_html=True)

        # Films populaires
        st.markdown("### 🎬 Sélection de films populaires")
        st.markdown(
            "<p style=\"text-align: center; font-family: 'Crimson Text', serif; font-style: italic; color: #2c1810;\">Nos meilleures recommandations</p>",
            unsafe_allow_html=True,
        )

        films_populaires = df.nlargest(8, "averageRating").drop_duplicates(
            subset=["movie_ID"]
        )

        cols = st.columns(4)
        for i, (idx, row) in enumerate(films_populaires.iterrows()):
            with cols[i % 4]:
                image_url = (
                    f"https://image.tmdb.org/t/p/w500{row['poster_path']}"
                    if pd.notna(row["poster_path"])
                    else "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Pas_d%27image_disponible.svg/2048px-Pas_d%27image_disponible.svg.png"
                )

                st.image(image_url, use_container_width=True)

                titre = (
                    row["frenchTitle"][:25] + "..."
                    if len(row["frenchTitle"]) > 25
                    else row["frenchTitle"]
                )
                st.markdown(
                    f"<p style='text-align: center; font-family: \"Cinzel\", serif; font-weight: 600; color: #2c1810;'>{titre}</p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<p style='text-align: center; color: #8B0000;'>⭐ {row['averageRating']}/10</p>",
                    unsafe_allow_html=True,
                )

                if st.button("Explorer", key=f"pop_{row['movie_ID']}"):
                    st.session_state["selected_film_id"] = row["movie_ID"]
                    st.rerun()

# ============================================
# FOOTER VINTAGE
# ============================================
st.markdown("---")
st.markdown(
    """
<div class="footer">
    <div class="footer-ornament">❦ ❦ ❦</div>
    <p style="font-size: 1.3rem; font-weight: 600; font-family: 'Cinzel', serif; letter-spacing: 2px; color: #8B0000;">
        LE CREUSOGRAPHE
    </p>
    <p style="font-size: 1.1rem; font-style: italic;">
        Cinéma de la Creuse - Département 23
    </p>
    <p style="font-size: 0.95rem; margin-top: 1rem;">
        Projet réalisé dans le cadre d'une formation en Data Science
    </p>
    <p style="font-size: 0.85rem; color: #aa8c2c; margin-top: 0.8rem;">
        Données : IMDb & TMDB | Algorithme : TF-IDF Content-Based Filtering
    </p>
    <div class="footer-ornament">★</div>
</div>
""",
    unsafe_allow_html=True,
)
