# import streamlit as st
# import pandas as pd
# from preprocess_data import process_data
# from rating_based_recommendation import get_top_rated_items
# from content_based_filtering import content_based_recommendation
# from collaborative_based_filtering import collaborative_filtering_recommendations
# from hybrid_approach import hybrid_recommendation_filtering
# # Page config
# st.set_page_config(
#     page_title="AI E-Commerce Recommender",
#     page_icon="6795674-200.png",
#     layout="wide"
# )
# st.title(" AI-Powered Recommendation System")
# st.caption("Accessible • User-friendly • Hybrid AI engine")
# # Load & preprocess data
# @st.cache_data
# def load_data():
#     df = pd.read_csv("clean_data.csv")
#     return process_data(df)
# data = load_data()
# # Sidebar controls
# with st.sidebar:
#     st.header("Controls")

#     algo = st.radio(
#         "Choose recommendation strategy",
#         (
#             "Top Rated",
#             "Content Based",
#             "Collaborative",
#             "Hybrid"
#         )
#     )
#     top_n = st.slider("Number of recommendations", 1, 20, 8)
# def recommendation_reason(strategy):
#     if strategy == "Top Rated":
#         return "**Recommended because it has high overall ratings**"
#     elif strategy == "Content Based":
#         return "**Recommended due to similar product description and tags**"
#     elif strategy == "Collaborative":
#         return "**Recommended because similar users liked this product**"
#     elif strategy == "Hybrid":
#         return "**Recommended using both product similarity and user behavior**"
#     else:
#         return "**Recommended for you**"
# # Inputs
# product_placeholder = "Select a product..."
# user_placeholder = "Select user ID..."

# product_names = [product_placeholder] + sorted(data["Name"].unique())
# user_ids = [user_placeholder] + sorted(data["ID"].unique())

# selected_product = None
# selected_user = None

# if algo in ("Content Based", "Hybrid"):
#     selected_product = st.selectbox("Select product", product_names)

# if algo in ("Collaborative", "Hybrid"):
#     selected_user = st.selectbox("Select user ID", user_ids)
# # Recommendation logic
# if st.button("Get Recommendations"):

#     # Validate selections
#     if algo in ("Content Based", "Hybrid") and (selected_product == product_placeholder):
#         st.warning("Please select a product before getting recommendations.")
#         result = get_top_rated_items(data, top_n)
#     elif algo in ("Collaborative", "Hybrid") and (selected_user == user_placeholder):
#         st.warning("Please select a user ID before getting recommendations.")
#         result = get_top_rated_items(data, top_n)
#     else:
#         with st.spinner("Generating recommendations..."):

#             try:
#                 if algo == "Top Rated":
#                     result = get_top_rated_items(data, top_n)

#                 elif algo == "Content Based":
#                     result = content_based_recommendation(
#                         data, selected_product, top_n
#                     )

#                 elif algo == "Collaborative":
#                     result = collaborative_filtering_recommendations(
#                         data, selected_user, top_n
#                     )

#                 elif algo == "Hybrid":
#                     result = hybrid_recommendation_filtering(
#                         data, selected_product, selected_user, top_n
#                     )

#                 if result is None or result.empty:
#                     st.warning("No recommendations found. Showing top rated items.")
#                     result = get_top_rated_items(data, top_n)

#             except Exception as e:
#                 st.error("Something went wrong. Falling back to Top Rated.")
#                 st.exception(e)
#                 result = get_top_rated_items(data, top_n)
#     # --------------------------------------------------
#     # Display results
#     st.subheader("Recommended Products")

#     cols = st.columns(4)
#     for idx, (_, row) in enumerate(result.iterrows()):
#         with cols[idx % 4]:
#             if "ImageURL" in row and isinstance(row["ImageURL"], str):
#                 if isinstance(row.get("ImageURL"), str) and row["ImageURL"].startswith("http" or "https"):
#                     st.image(row["ImageURL"], width=250)
#                 else:
#                     st.markdown("*Image not available*")
#             st.markdown(f"**{row['Name']}**")
#             st.caption(f"Brand: {row.get('Brand', 'N/A')}")
#             st.caption(f"Rating: {round(row.get('Rating', 0), 2)}")
#             st.caption(recommendation_reason(algo))

import streamlit as st
import pandas as pd

from preprocess_data import process_data
from rating_based_recommendation import get_top_rated_items
from content_based_filtering import content_based_recommendation
from collaborative_based_filtering import collaborative_filtering_recommendations
from hybrid_approach import hybrid_recommendation_filtering


# ------------------------------------------------------
# Page config
# ------------------------------------------------------
st.set_page_config(
    page_title="AI E-Commerce Recommender",
    page_icon="6795674-200.png",
    layout="wide"
)

st.markdown("""
<style>
/* 1. Load Inter explicitly */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* 2. Force font everywhere */
html, body, [data-testid="stApp"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    
}
html, body, [data-testid="stApp"] {
    background: linear-gradient(90deg, #0f172a, #020617);
}
/* 3. Force heading weights (important) */
h1, h2, h3 {
    font-weight: 700 !important;
}

.navbar h1 {
    font-weight: 700 !important;
}

.navbar span {
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# Load & preprocess data
# ------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clean_data.csv")
    return process_data(df)

data = load_data()


# ======================================================
# ROW 1 → OPTIONS (Top control bar)
# ======================================================
st.markdown("""
<style>
.navbar {
    width: 100%;
    padding: 2rem 2.5rem;
    background: linear-gradient(90deg, #0f172a, #020617);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    margin-bottom: 2.5rem;
    border: 1px solid #1e293b;
    box-shadow: 0 12px 40px rgba(0,0,0,0.45);
    transition: box-shadow 0.35s ease, transform 0.35s ease;
}

.navbar:hover {
    box-shadow: 0 18px 55px rgba(15,23,42,0.9),
                0 0 30px rgba(56,189,248,1.0);
    transform: translateY(-2px);
}

.navbar h1 {
    color: white;
    font-size: 2rem;
    margin: 0;
    letter-spacing: 0.6px;
    text-align: center;
}

.navbar span {
    color: #94a3b8;
    font-size: 1rem;
    margin-top: 0.4rem;
    text-align: center;
}
</style>

<div class="navbar">
    <h1>AI-Powered Recommendation System</h1>
    <span>Smart • Personalized • AI-Driven</span>
</div>
""", unsafe_allow_html=True)


col1, col2 = st.columns([3, 2])

with col1:
    algo = st.radio(
        "Choose recommendation strategy",
        (
            "Top Rated",
            "Content Based",
            "Collaborative",
            "Hybrid"
        ),
        horizontal=True
    )

with col2:
    top_n = st.radio(
        "Number of recommendations",
        [5, 10, 20, 30, 40, 50],
        horizontal=True
    )

st.divider()


# ======================================================
# ROW 2 → APP NAME (Header)
# ======================================================
st.markdown("""
<style>
.section-title {
    margin-bottom: 1.5rem;
}

.section-title h2 {
    color: white;
    font-size: 2.2rem;
    margin-bottom: 0.3rem;
}
.section-title p {
    color: #94a3b8;
    font-size: 1rem;
    margin-top: 0rem;
}
</style>

<div class="section-title">
    <h2>Your Recommendation Dashboard</h2>
    <p>Explore personalized product suggestions tailored just for you</p>
</div>
""", unsafe_allow_html=True)



# ======================================================
# Helper functions
# ======================================================
def recommendation_reason(strategy):
    if strategy == "Top Rated":
        return "**Recommended because it has high overall ratings**"
    elif strategy == "Content Based":
        return "**Recommended due to similar product description and tags**"
    elif strategy == "Collaborative":
        return "**Recommended because similar users liked this product**"
    elif strategy == "Hybrid":
        return "**Recommended using both product similarity and user behavior**"
    return "**Recommended for you**"


def resolve_product_name(typed_name, product_list):
    if not typed_name:
        return None

    typed_name = typed_name.lower().strip()
    matches = [p for p in product_list if typed_name in p.lower()]
    return matches[0] if matches else None


# ======================================================
# ROW 3 → INPUTS + OUTPUT
# ======================================================
user_placeholder = "Select user ID..."
user_ids = [user_placeholder] + sorted(data["ID"].unique())

selected_user = None
typed_product = None
selected_product = None

input_col, info_col = st.columns([3, 1])

with input_col:

    if algo in ("Content Based", "Hybrid"):
        st.subheader("Product Input")
        typed_product = st.text_input(
            "Type product name",
            placeholder="e.g. iPhone, shoes, laptop..."
        )

    if algo in ("Collaborative", "Hybrid"):
        st.subheader("User Input")
        selected_user = st.selectbox("Select user ID", user_ids)

    run = st.button("Get Recommendations", use_container_width=True)


with info_col:
    st.markdown("""
    <style>
    .info-box {  
        box-shadow: 0 12px 40px rgba(0,0,0,0.45);
        transition: box-shadow 0.35s ease, transform 0.35s ease;
    }
    .info-box:hover {
        box-shadow: 0 18px 55px rgba(15,23,42,0.9),
                    0 0 30px rgba(56,189,248,1.0);
        transform: translateY(-2px);   
    } 
    </style> 
    <div class=info-box style="
        background:#020617;
        padding:1.75rem;
        margin-top:1.1rem;        
        border-radius:12px;
        border:1px solid #1e293b;
    ">
    <h4 style="color:white;">How it works</h4>
    <p style="color:#94a3b8;font-size:0.9rem;">
    The App is a algorithm-based recommendation engine for an e-commerce platform. 
    It delivers personalized product suggestions using user behavior, product features, and ratings.
    Content-based, collaborative, and hybrid approaches are implemented to demonstrate how different recommendation strategies work individually and together.
    </p>
    </div>
    """, unsafe_allow_html=True)


# ======================================================
# Recommendation logic
# ======================================================
if run:

    resolved_product = None

    if algo in ("Content Based", "Hybrid"):
        resolved_product = resolve_product_name(
            typed_product,
            data["Name"].unique()
        )
        if resolved_product:
            selected_product = resolved_product

    if algo in ("Content Based", "Hybrid") and not selected_product:
        st.warning("Please type a valid product name.")
        result = get_top_rated_items(data, top_n)

    elif algo in ("Collaborative", "Hybrid") and (
        not selected_user or selected_user == user_placeholder
    ):
        st.warning("Please select a user ID.")
        result = get_top_rated_items(data, top_n)

    else:
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
                    result = get_top_rated_items(data, top_n)

            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)
                result = get_top_rated_items(data, top_n)

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------
    if resolved_product:
        st.success(f"Showing recommendations for: **{resolved_product}**")

    st.subheader("Recommended Products")

    cols = st.columns(4)
    for idx, (_, row) in enumerate(result.iterrows()):
        with cols[idx % 4]:
            if "ImageURL" in row and isinstance(row["ImageURL"], str):
                if row["ImageURL"].startswith(("http://", "https://")):
                    st.image(row["ImageURL"], use_container_width=True)
                else:
                    st.markdown("*Image not available*")

            st.markdown(f"**{row['Name']}**")
            st.caption(f"Brand: {row.get('Brand', 'N/A')}")
            st.caption(f"Rating: {round(row.get('Rating', 0), 2)}")
            st.caption(recommendation_reason(algo))
