import streamlit as st
import requests

API_URL = "http://backend:5000/recipes"

st.title("Simple Recipe Organizer")


st.header("All Recipes")
response = requests.get(API_URL)
if response.status_code == 200:
    recipes = response.json()
    for r in recipes:
        with st.expander(r["title"]):
            st.write("**Ingredients:**")
            st.write(", ".join(r["ingredients"]))
            st.write("**Instructions:**")
            st.write(r["instructions"])

            if st.button(f"Delete '{r['title']}'", key=f"del-{r['id']}"):
                requests.delete(f"{API_URL}/{r['id']}")
                st.rerun()
else:
    st.error("Failed to fetch recipes")


st.header("Add New Recipe")
with st.form("recipe_form"):
    title = st.text_input("Title")
    ingredients = st.text_area("Ingredients (comma separated)")
    instructions = st.text_area("Instructions")
    submitted = st.form_submit_button("Add Recipe")
    if submitted:
        new_recipe = {
            "title": title,
            "ingredients": [i.strip() for i in ingredients.split(",") if i.strip()],
            "instructions": instructions
        }
        res = requests.post(API_URL, json=new_recipe)
        if res.status_code == 201:
            st.success("Recipe added!")
            st.rerun()
        else:
            st.error("Failed to add recipe")
