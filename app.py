import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from search import search_by_name, search_by_ingredients, search_by_category, search_by_filters, display_recipe

# Charger les données dès l'ouverture du site
@st.cache_data
def load_data():
    df = pd.read_csv("Food_Recipe_cleaned.csv")
    df = df.dropna(subset=["image_url"])
    return df

# Load data
df = load_data()

# Interface utilisateur
st.title("🍽️ Recommandateur de Recettes")

# Barre de navigation
page = st.sidebar.selectbox("Navigation", ["Accueil", "Rechercher par nom", "What's in your kitchen?", "Popular"])

if page == "Accueil":
    st.subheader("🔥 Here's some food I recommend you")

    random_recipes = df.sample(9)

    cols = st.columns(3)
    for i, (idx, row) in enumerate(random_recipes.iterrows()):
        with cols[i % 3]:
            try:
                response = requests.get(row["image_url"], timeout=5)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content)).resize((300, 300))
                    st.image(image)
                else:
                    st.image("https://via.placeholder.com/300", caption="Image non dispo")
                    st.write(f"Erreur {response.status_code} pour {row['image_url']}")
            except Exception as e:
                st.image("https://via.placeholder.com/300", caption="Image non dispo")
                st.write(f"Erreur : {e}")
            # Display the name of the dish and total time
            st.write(f"**{row['name']}**")
            total_time = row['prep_time (in mins)'] + row['cook_time (in mins)']
            st.write(f"Temps total: {total_time} minutes")

elif page == "Rechercher par nom":
    st.header("Rechercher par nom")
    recipe_name = st.text_input("Entrez un nom de recette :", "")
    if st.button("Rechercher"):
        search_by_name(df, recipe_name)

elif page == "What's in your kitchen?":
    st.header("What's in your kitchen?")
    st.write("Find recipes based on what you already have at home!")
    ingredients = st.text_input("Enter up to 3 ingredients separated by commas:", "")
    if st.button("Find recipes"):
        search_by_ingredients(df, ingredients)

elif page == "Popular":
    st.header("Popular Recipes")
    category = st.selectbox("Choisissez une catégorie :", ["Easy Dinner", "Under 30 Minutes", "Chicken", "Breakfast", "Desserts"])
    if st.button("Rechercher"):
        search_by_category(df, category)

# Ajouter des boutons pour les filtres
st.sidebar.header("Filtres")
difficulty = st.sidebar.radio("Difficulty", ["Under 1 Hour", "Under 45 Minutes", "Under 30 Minutes"])
diets = st.sidebar.radio("Diets", ["Non Vegetarian", "Vegetarian", "Eggtarian"])
meal = st.sidebar.radio("Meal", ["Appetizer", "Breakfast", "Dessert", "Dinner", "Lunch", "Main Course", "Side Dish", "Snack"])
cuisine = st.sidebar.radio("Cuisine", ["Arab", "Asian", "Bengali", "Chinese", "European", "French", "Greek", "Indian", "Indonesian", "Italian", "Japanese", "Korean", "Malaysian", "Mexican", "Middle Eastern", "Tamil Nadun", "Thai"])
if st.sidebar.button("Appliquer les filtres"):
    search_by_filters(df, difficulty, diets, meal, cuisine)

# Ajouter du style CSS personnalisé
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF6347;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    .stTextInput>div>div>input {
        border: 2px solid #FF6347;
        border-radius: 8px;
        padding: 10px;
    }
    .stRadio>div>div>div>label {
        background-color: #FF6347;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
