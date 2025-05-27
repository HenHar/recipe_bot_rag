from llm import get_response
from postgreSQL import setup_db, add_recipes_from_json, add_embedding_to_all_rows, get_similar_recipes_text, \
    delete_table, get_connection
from src.utils import get_absolute_path


def setup_table(recipe_path, table_name):
    delete_table(table_name)
    setup_db()
    add_recipes_from_json(recipe_path)
    add_embedding_to_all_rows()

def text_query(query):
    output = get_similar_recipes_text(query)
    print(type(output))
    print(output)

def image_query():
    img_path = "../test_images/red_lentils.jpg"
    response = get_response(img_path, "Liste alle Zutaten im Gericht auf.")
    output = get_similar_recipes_text(response)
    print(output)

if __name__ == '__main__':
    conn = get_connection()
    recipe_path = "../scrape/recipes.json"
    recipe_path = get_absolute_path(recipe_path)
    table_name = "recipes"
    add_embedding_to_all_rows(conn)

    #img_path = "../test_images/red_lentils.jpg"
    #query = "rote linsen salat"
    #text_query(query)
