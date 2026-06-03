import pandas as pd
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# LOAD DATASET
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "featured_dataset.csv"
)

print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully.")
print(f"Total Products: {len(df)}")

# =========================================================
# CREATE COMBINED FEATURES
# =========================================================

print("\nCreating combined features...")

df['combined_features'] = (
    df['product_name'].astype(str) + " " +
    df['category'].astype(str) + " " +
    df['material'].astype(str) + " " +
    df['brand'].astype(str)
)

# =========================================================
# TF-IDF VECTORIZATION
# =========================================================

print("Performing TF-IDF vectorization...")

vectorizer = TfidfVectorizer(stop_words='english')

tfidf_matrix = vectorizer.fit_transform(
    df['combined_features']
)

# =========================================================
# COSINE SIMILARITY
# =========================================================

print("Calculating cosine similarity...")

similarity_matrix = cosine_similarity(tfidf_matrix)

print("Similarity matrix created successfully.")

# =========================================================
# TEST FUNCTION
# =========================================================

def test_product(product_name):

    print("\n" + "=" * 60)
    print(f"TESTING PRODUCT: {product_name}")
    print("=" * 60)

    # =====================================================
    # SEARCH PRODUCT
    # =====================================================

    matching_products = df[
        (
            df['product_name']
            .str.lower()
            .str.contains(product_name.lower(), na=False, regex=False)
        )
        |
        (
            df['material']
            .str.lower()
            .str.contains(product_name.lower(), na=False, regex=False)
        )
        |
        (
            df['category']
            .str.lower()
            .str.contains(product_name.lower(), na=False, regex=False)
        )
        |
        (
            df['brand']
            .str.lower()
            .str.contains(product_name.lower(), na=False, regex=False)
        )
    ]

    # =====================================================
    # TEST INVALID SEARCH
    # =====================================================

    if matching_products.empty:

        print("TEST RESULT: FAILED")
        print("Reason: Product not found.")

        return

    print("TEST RESULT: PASSED")
    print("Product found successfully.")

    # =====================================================
    # SELECT FIRST MATCH
    # =====================================================

    product_index = matching_products.index[0]

    selected_product = df.iloc[product_index]

    # =====================================================
    # DISPLAY PRODUCT DETAILS
    # =====================================================

    print("\nPRODUCT DETAILS")
    print("-" * 40)

    print(f"Product Name : {selected_product['product_name']}")
    print(f"Category     : {selected_product['category']}")
    print(f"Material     : {selected_product['material']}")
    print(f"Brand        : {selected_product['brand']}")
    print(f"Eco Score    : {selected_product['eco_score']}")
    print(f"Sustainable  : {selected_product['is_sustainable']}")

    # =====================================================
    # TEST SUSTAINABILITY
    # =====================================================

    print("\nSUSTAINABILITY ANALYSIS")
    print("-" * 40)

    if selected_product['is_sustainable'] == 1:

        print("PASS: Product is Sustainable")

    else:

        print("PASS: Product is NOT Sustainable")

    # =====================================================
    # TEST RECOMMENDATION ENGINE
    # =====================================================

    print("\nTESTING RECOMMENDATION ENGINE")
    print("-" * 40)

    similarity_scores = list(
        enumerate(similarity_matrix[product_index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    similarity_scores = similarity_scores[1:]

    recommended_products = []

    ignore_words = {
        'eco',
        'organic',
        'natural',
        'premium',
        'reusable',
        'electric',
        'head',
        'set',
        'pack'
    }

    selected_words = set(
        word
        for word in selected_product['product_name']
        .lower()
        .split()
        if word not in ignore_words
    )

    for index, similarity_score in similarity_scores:

        candidate = df.iloc[index]

        candidate_words = set(
            candidate['product_name']
            .lower()
            .split()
        )

        common_words = selected_words.intersection(
            candidate_words
        )

        if (
            candidate['is_sustainable'] == 1
            and candidate['category'] == selected_product['category']
            and len(common_words) > 0
            and candidate['eco_score'] >= selected_product['eco_score']
            and candidate['product_name'] != selected_product['product_name']
        ):

            recommended_products.append({
                'index': index,
                'eco_score': candidate['eco_score'],
                'similarity': similarity_score
            })

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    recommended_indices = []

    seen_products = set()

    for item in recommended_products:

        idx = item['index']

        product_name = df.iloc[idx]['product_name']

        if product_name not in seen_products:

            recommended_indices.append(idx)

            seen_products.add(product_name)

        if len(recommended_indices) == 5:
            break

    # =====================================================
    # DISPLAY RECOMMENDATIONS
    # =====================================================

    if len(recommended_indices) == 0:

        print("FAIL: No recommendations found.")

    else:

        print("PASS: Recommendations generated successfully.")

        print("\nRECOMMENDED PRODUCTS")
        print("-" * 40)

        for i, idx in enumerate(recommended_indices, start=1):

            product = df.iloc[idx]

            print(f"\n{i}. {product['product_name']}")

            print(f"   Category    : {product['category']}")
            print(f"   Material    : {product['material']}")
            print(f"   Brand       : {product['brand']}")
            print(f"   Eco Score   : {product['eco_score']}")
            print(f"   Sustainable : {product['is_sustainable']}")

# =========================================================
# RUN TEST CASES
# =========================================================

print("\n" + "=" * 60)
print("RUNNING TEST CASES")
print("=" * 60)

test_cases = [

    "toothbrush",
    "bamboo",
    "plastic",
    "shampoo",
    "laptop",
    "office",
    "organic",
    "nike",
    "glass bottle",
    "invalidproduct123"

]

for product in test_cases:

    test_product(product)

# =========================================================
# FINAL MESSAGE
# =========================================================

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED")
print("=" * 60)