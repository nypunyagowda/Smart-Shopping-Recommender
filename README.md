# Smart Sustainable Shopping Recommender

A machine-learning-based shopping application that helps users explore product sustainability and discover eco-friendly alternatives. Users can select a product category and product, view its details, review sustainability indicators, and explore recommended alternatives.

## Features

- **Product Selection:** Choose a category and a product to analyze.
- **Product Details:** View available details such as category, material, brand, price, and rating.
- **Sustainability Analysis:** Display the product's sustainability classification.
- **Feature Engineering:** Use indicators including `is_eco_material`, `is_biodegradable`, `is_recyclable`, `is_reusable`, `is_plastic_free`, `is_organic`, and `is_recycled_material`.
- **Eco Score:** Use engineered sustainability features to calculate a score representing environmental friendliness.
- **Sustainability Prediction:** Use a Random Forest Classifier to predict whether a product is sustainable or not sustainable.
- **Eco-Friendly Alternatives:** Display alternative products with available details such as material, Eco Score, rating, and recyclability.

## Technology Stack

- **Python** – Application development and data processing
- **Streamlit** – Interactive web interface
- **Pandas** – Dataset handling and manipulation
- **Scikit-learn** – Random Forest classification and machine-learning utilities

## How It Works

1. **Load Product Data:** Read product details and sustainability-related attributes from the dataset.

2. **Feature Engineering:** Create sustainability indicators such as biodegradability, recyclability, reusability, and eco-friendly materials.

3. **Eco Score Calculation:** Combine engineered sustainability indicators to generate a score representing the environmental friendliness of a product.

4. **Sustainability Prediction:** Apply the trained Random Forest Classifier to predict whether a product is sustainable or not sustainable.

5. **Product Recommendation:** Identify and display eco-friendly alternatives based on product attributes and sustainability information.

6. **Interactive Visualization:** Present product details, sustainability analysis, Eco Scores, and recommended alternatives through the Streamlit interface.

## Sustainability Features

| Feature | Description |
|---|---|
| `is_eco_material` | Indicates whether the product uses an eco-friendly material |
| `is_biodegradable` | Indicates whether the product is biodegradable |
| `is_recyclable` | Indicates whether the product can be recycled |
| `is_reusable` | Indicates whether the product can be reused |
| `is_plastic_free` | Indicates whether the product is plastic-free |
| `is_organic` | Indicates whether the product is organic |
| `is_recycled_material` | Indicates whether recycled material is used |
| `eco_score` | Represents the product's sustainability based on engineered features |

## Getting Started

### Prerequisites

Make sure Python is installed on your system.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Create a Virtual Environment

It is recommended to create a virtual environment to manage project dependencies.

For Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Alternatively, use Command Prompt:

```bat
venv\Scripts\activate.bat
```

### 3. Install Dependencies

Install the required Python libraries:

```bash
pip install streamlit pandas scikit-learn
```

If a `requirements.txt` file is available, install the dependencies using:

```bash
pip install -r requirements.txt
```

### 4. Configure the Dataset

Place the product dataset in the location expected by the application.

If the dataset path is specified in `app.py`, ensure that the file path and filename match your local setup.

### 5. Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

Open the local URL provided by Streamlit in your browser. The application is typically available at:

http://localhost:8501

## Application Workflow

1. Select a product category.
2. Choose a product from the available list.
3. Click **Analyze Product**.
4. View the product details, including material, brand, price, and rating.
5. Review the sustainability classification and Eco Score.
6. Explore recommended eco-friendly alternatives.

## Project Structure

The project may follow the structure below. Update it to match your actual repository.

```text
Smart-Sustainable-Shopping/
│
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── product_dataset.csv
```

## Notes

- The application's results depend on the quality and completeness of the product dataset.
- Some product attributes may be missing, resulting in unavailable values in the interface.
- Eco Scores and model predictions are based on the project's engineered features and should be treated as estimates rather than independent environmental certifications.
- The dataset path and dependency list should match the actual project configuration.

## Future Enhancements

- Integrate additional verified product sustainability information.
- Improve the handling of missing and inconsistent product attributes.
- Provide a detailed explanation of the Eco Score calculation.
- Enhance the recommendation system to provide more relevant alternatives.
- Expand the product dataset to cover additional categories.

## Author

**K S NYPUNYA**  
MCA Student, PES University
