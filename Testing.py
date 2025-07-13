import pandas as pd
from difflib import get_close_matches
from transformers import AutoTokenizer, AutoModel
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import subprocess


DB_dir = "FoodData_DB"

# Load CSV files
food_df = pd.read_csv(r"%s\food.csv" % DB_dir)
foundation_food_df = pd.read_csv(r"%s\foundation_food.csv" % DB_dir)
food_nutrient_df = pd.read_csv(r"%s\food_nutrient.csv" % DB_dir)
nutrient_df = pd.read_csv(r"%s\nutrient.csv" % DB_dir)

# Merge food and foundation_food to get descriptions with fdc_ids
foundation_foods = foundation_food_df.merge(food_df, on="fdc_id")

# Function to find best matching fdc_id(s) for an ingredient
def find_best_fdc_ids(search_term, max_matches=1):
    search_term = search_term.lower()
    matches = foundation_foods[foundation_foods['description'].str.lower().str.contains(search_term)]
    
    if matches.empty:
        print(f"❌ No match found for '{search_term}'")
        return []

    # Display top matches
    top_matches = matches[['fdc_id', 'description']].head(max_matches)
    print(f"\n🔍 Matches for '{search_term}':")
    print(top_matches.to_string(index=False))

    return top_matches['fdc_id'].tolist()

# Get user input
print("👉 Enter ingredients and their percentages (e.g., Chicken:50, Hummus:30, Olive oil:20):")
user_input = input("Ingredients: ")

# Parse input into a dict
ingredients = {}
for item in user_input.split(","):
    try:
        name, perc = item.strip().split(":")
        ingredients[name.strip().lower()] = float(perc.strip())
    except:
        print(f"⚠️ Could not parse input: {item}")
        continue

# Initialize nutrient totals
nutrient_totals = {}

# Process each ingredient
for ingredient_name, percent in ingredients.items():
    fdc_ids = find_best_fdc_ids(ingredient_name, max_matches=1)
    if not fdc_ids:
        continue

    for fdc_id in fdc_ids:
        nutrient_rows = food_nutrient_df[food_nutrient_df['fdc_id'] == fdc_id]
        merged = nutrient_rows.merge(nutrient_df, left_on="nutrient_id", right_on="id")

        for _, row in merged.iterrows():
            nutrient_name = row["name"]
            nutrient_amount = row["amount"] * (percent / 100.0)  # scaled by % in the dish
            nutrient_totals[nutrient_name] = nutrient_totals.get(nutrient_name, 0) + nutrient_amount

# Display final totals
print("\n🍽️ Nutrient Profile for Dish (per 100g):")
for nutrient, total in sorted(nutrient_totals.items()):
    print(f"{nutrient}: {round(total, 2)}")


prompt = "Why is the sky blue"


result = subprocess.run(
                ["ollama", "run", "gemma3:4b", prompt],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

print(result.stdout.strip())

query_embedding = result.stdout.strip()

 # Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_usda")
collection = client.get_or_create_collection(name="usda_foods")

# Sample document
text = "Food: Apple\nCategory: Fruit\nNutrients:\nFiber: 2.4g\nVitamin C: 8mg"
embedding = model.encode([text])[0]

# Add to collection
collection.add(
    documents=[text],
    embeddings=[embedding],
    ids=["food_apple"]
)


query = "Which foods are high in calcium?"

# TODO replace get embedding with call to ollama using subprocess with above query
#query_embedding = get_embedding(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

retrieved_context = "\n\n".join(results["documents"][0])
prompt = f"""
Context:
{retrieved_context}

Question:
{query}
"""