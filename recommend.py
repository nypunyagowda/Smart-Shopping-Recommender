import pandas as pd

# ---------------- ECO SCORE ---------------- #

def generate_eco_score(label):

    label = str(label).lower()

    if "organic" in label:
        return 95

    elif "eco" in label:
        return 90

    elif "recycled" in label:
        return 85

    elif "sustainable" in label:
        return 75

    else:
        return 40


# ---------------- KEYWORD MATCHING ---------------- #

def extract_keywords(product_name):

    words = str(product_name).lower().split()

    ignore_words = {
        "organic",
        "eco",
        "natural",
        "sustainable",
        "recycled",
        "premium"
    }

    keywords = [
        word for word in words
        if word not in ignore_words
    ]

    return keywords


# ---------------- RECOMMEND FUNCTION ---------------- #

def get_sustainable_recommendations(df, selected_product):

    # selected product row
    selected_row = df[
        df["product_name"] == selected_product
    ]

    if selected_row.empty:
        return pd.DataFrame()

    selected_row = selected_row.iloc[0]

    selected_category = selected_row["category"]

    selected_keywords = extract_keywords(
        selected_product
    )

    # same category only
    recommendations = df[
        (df["category"] == selected_category) &
        (df["product_name"] != selected_product)
    ].copy()

    # eco score
    recommendations["eco_score"] = recommendations[
        "sustainability_label"
    ].apply(generate_eco_score)

    # keyword similarity
    def keyword_score(name):

        name_words = str(name).lower().split()

        matches = sum(
            1 for word in selected_keywords
            if word in name_words
        )

        return matches

    recommendations["keyword_score"] = recommendations[
        "product_name"
    ].apply(keyword_score)

    # prioritize similar products
    recommendations = recommendations.sort_values(
        by=["keyword_score", "eco_score", "rating"],
        ascending=[False, False, False]
    )

    # only meaningful matches first
    meaningful = recommendations[
        recommendations["keyword_score"] > 0
    ]

    # fallback if none found
    if meaningful.empty:

        meaningful = recommendations.sort_values(
            by=["eco_score", "rating"],
            ascending=[False, False]
        )

    return meaningful.head(5)