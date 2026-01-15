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

st.title("AI-Powered Recommendation System")
st.caption("Accessible • User-friendly • Hybrid AI engine")


# ------------------------------------------------------
# Load & preprocess data
# ------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clean_data.csv")
    return process_data(df)

data = load_data()


# ------------------------------------------------------
# Sidebar controls
# ------------------------------------------------------
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


# ------------------------------------------------------
# Helper functions
# ------------------------------------------------------
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


def resolve_product_name(typed_name, product_list):
    """
    Match typed product name to actual product name (partial match).
    """
    if not typed_name:
        return None

    typed_name = typed_name.lower().strip()
    matches = [
        p for p in product_list
        if typed_name in p.lower()
    ]

    return matches[0] if matches else None


# ------------------------------------------------------
# Inputs
# ------------------------------------------------------
# product_placeholder = "Select a product..."
user_placeholder = "Select user ID..."

# product_names = [product_placeholder] + sorted(data["Name"].unique())
user_ids = [user_placeholder] + sorted(data["ID"].unique())

# selected_product = None
selected_user = None
typed_product = None


# Product input (text + dropdown)
if algo in ("Content Based", "Hybrid"):
    st.subheader("Product Input")

    typed_product = st.text_input(
        "Type product name (recommended)",
        placeholder="e.g. iPhone, shoes, laptop..."
    )

    # selected_product = st.selectbox(
    #     "Or select product from list",
    #     product_names
    # )


# User input
if algo in ("Collaborative", "Hybrid"):
    st.subheader("User Input")
    selected_user = st.selectbox("Select user ID", user_ids)


# ------------------------------------------------------
# Recommendation logic
# ------------------------------------------------------
if st.button("Get Recommendations"):

    resolved_product = None

    if algo in ("Content Based", "Hybrid"):
        resolved_product = resolve_product_name(
            typed_product,
            data["Name"].unique()
        )

        # Typed product has higher priority
        if resolved_product:
            selected_product = resolved_product

    # ---------------- Validation ----------------
    if algo in ("Content Based", "Hybrid") and not selected_product:
        st.warning("Please type or select a product.")
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
                    st.warning("No recommendations found. Showing top rated items.")
                    result = get_top_rated_items(data, top_n)

            except Exception as e:
                st.error("Something went wrong. Falling back to Top Rated.")
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
                    st.image(row["ImageURL"], width=250)
                else:
                    st.markdown("*Image not available*")

            st.markdown(f"**{row['Name']}**")
            st.caption(f"Brand: {row.get('Brand', 'N/A')}")
            st.caption(f"Rating: {round(row.get('Rating', 0), 2)}")
            st.caption(recommendation_reason(algo))
