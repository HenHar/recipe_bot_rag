from sentence_transformers import SentenceTransformer

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_text_embedding(text):
    sentence_embedding = model.encode(text)
    return sentence_embedding

def recipe_json_to_text(json_data: dict) -> str:
    """ creates a string from a recipe json"""
    recipe_text = ""
    recipe_text += f"Name: {json_data["name"]}\n"
    recipe_text += f"Beschreibung: {json_data["description"]}\n"
    recipe_text += f"Zutaten: {", ".join(json_data["recipeIngredient"])}\n"
    recipe_text += f"Anleitung\n"
    for instruction in json_data["recipeInstructions"]:
        recipe_text += f"{instruction["name"]}: {instruction["text"]}\n"

    if 'keywords' in json_data:
        recipe_text += f"Schlagworte: {json_data["keywords"]}\n"
    return recipe_text
