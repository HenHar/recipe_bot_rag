from llm import get_response
from postgreSQL import setup_db, add_recipes_from_json, add_embedding_to_all_rows, get_similar_recipes_text


def setup_table(recipe_path):
    setup_db()
    add_recipes_from_json(recipe_path)
    add_embedding_to_all_rows()

def text_query():
    text = "ich würde gerne fisch essen"
    output = get_similar_recipes_text(text)
    print(type(output))
    print(output)

def image_query():
    img_path = "test_images/red_lentils.jpg"
    response = get_response(img_path, "Liste alle Zutaten im Gericht auf.")
    output = get_similar_recipes_text(response)
    print(output)

if __name__ == '__main__':
    recipe_path = "scrape/recipes_few.json"

    #setup_table()
    image_query()
    img_path = "test_images/red_lentils.jpg"
    text = "rote linsen salat"
