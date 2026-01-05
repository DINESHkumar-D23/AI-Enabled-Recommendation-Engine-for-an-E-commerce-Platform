import streamlit as st
import pandas as pd
from preprocess_data import process_data
from rating_based_recommendation import get_top_rated_items
from content_based_filtering import content_based_recommendation
from collaborative_based_filtering import collaborative_filtering_recommendations
from hybrid_approach import hybrid_recommendation_filtering
# Page config
st.set_page_config(
    page_title="AI E-Commerce Recommender",
    page_icon="6795674-200.png",
    layout="wide"
)
st.title(" AI-Powered Recommendation System")
st.caption("Accessible • User-friendly • Hybrid AI engine")
# Load & preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("clean_data.csv")
    return process_data(df)
data = load_data()
# Sidebar controls
with st.sidebar:
    st.header("Controls")

    algo = st.radio(
        "Choose recommendation strategy",
        (
            "Top Rated",
            "Content Based",
            "Collaborative",
            "Hybrid"
        )
    )
    top_n = st.slider("Number of recommendations", 1, 20, 8)
def recommendation_reason(strategy):
    if strategy == "Top Rated":
        return "**Recommended because it has high overall ratings**"
    elif strategy == "Content Based":
        return "**Recommended due to similar product description and tags**"
    elif strategy == "Collaborative":
        return "**Recommended because similar users liked this product**"
    elif strategy == "Hybrid":
        return "**Recommended using both product similarity and user behavior**"
    else:
        return "**Recommended for you**"
# Inputs
product_names = sorted(data["Name"].unique())
user_ids = sorted(data["ID"].unique())

selected_product = None
selected_user = None

if algo in ("Content Based", "Hybrid"):
    selected_product = st.selectbox("Select product", product_names)

if algo in ("Collaborative", "Hybrid"):
    selected_user = st.selectbox("Select user ID", user_ids)
# Recommendation logic
if st.button("Get Recommendations"):

    with st.spinner("Generating recommendations..."):

        try:
            if algo == "Top Rated":
                result = get_top_rated_items(data, top_n)

            elif algo == "Content Based":
                result = content_based_recommendation(
                    data, selected_product, top_n
                )

            elif algo == "Collaborative":
                result = collaborative_filtering_recommendations(
                    data, selected_user, top_n
                )

            elif algo == "Hybrid":
                result = hybrid_recommendation_filtering(
                    data, selected_product, selected_user, top_n
                )

            if result is None or result.empty:
                st.warning("No recommendations found. Showing top rated items.")
                result = get_top_rated_items(data, top_n)

        except Exception as e:
            st.error("Something went wrong. Falling back to Top Rated.")
            st.exception(e)
            result = get_top_rated_items(data, top_n)
    # --------------------------------------------------
    # Display results
    st.subheader("Recommended Products")

    cols = st.columns(4)
    for idx, (_, row) in enumerate(result.iterrows()):
        with cols[idx % 4]:
            if "ImageURL" in row and isinstance(row["ImageURL"], str):
                if isinstance(row.get("ImageURL"), str) and row["ImageURL"].startswith("http" or "https"):
                    st.image(row["ImageURL"], width=250)
                else:
                    st.markdown("*Image not available*")
            st.markdown(f"**{row['Name']}**")
            st.caption(f"Brand: {row.get('Brand', 'N/A')}")
            st.caption(f"Rating: {round(row.get('Rating', 0), 2)}")
            st.caption(recommendation_reason(algo))

