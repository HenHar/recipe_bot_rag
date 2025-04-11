import json
import psycopg2
import os
from PIL import Image
from io import BytesIO
import requests
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv, find_dotenv
from embedding import  get_text_embedding

load_dotenv(find_dotenv())

DB_NAME = os.getenv("DB_NAME")
HOST_IP = os.getenv("HOST_IP")
DB_USER = os.getenv('DB_USER')
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")

conn = psycopg2.connect(database=DB_NAME,
                                host=HOST_IP,
                                user=DB_USER,
                                password=PASSWORD,
                                port=PORT)
TEXT_VECTOR_SIZE = 384



def setup_db():
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()

    # Register the vector type with psycopg2
    register_vector(conn)

    # Create table to store embeddings and json_data
    table_create_command = f"""
    CREATE TABLE IF NOT EXISTS recipe (
                url text primary key, 
                json_schema jsonb,
                text_embedding vector({TEXT_VECTOR_SIZE})
                );
                """

    cur.execute(table_create_command)
    cur.execute("SELECT COUNT(*) from recipe;")
    conn.commit()
    cur.close()

def delete_table(table_name):
    cur = conn.cursor()
    query = f"""
    DROP TABLE IF EXISTS {table_name};
    """
    cur.execute(query)
    cur.close()


def get_similar_recipes_text(user_query, text_format = False, limit_results = 1):
    query_embedding = get_text_embedding(user_query)
    query_embedding = query_embedding.tolist()
    cur = conn.cursor()
    # Get the most similar documents using the KNN <=> operator
    cur.execute(
        "SELECT url, text_embedding <-> %s::vector AS distance , json_schema FROM recipe ORDER BY text_embedding <=> %s::vector LIMIT %s",
        (query_embedding, query_embedding, limit_results),
    )
    top_docs = cur.fetchall()
    distances = []
    urls = []
    texts = []

    for row in top_docs:
        distances.append(row[1])
        recipe_text = str(row[2]) + "\n\n"
        if text_format:
            recipe_text = recipe_json_to_text(row[2]["mainEntity"]) + "\n\n"
        urls.append(row[0])
        texts.append(recipe_text)

    return urls, distances, texts

def add_recipes_from_json(path):
    # read recipes line by line
    counter = 0
    with open(path, "r") as read_recipes:
        for line in read_recipes:
            print(line[:-2])
            recipe_data = json.loads(line[:-2])
            add_recipe(recipe_data)
            counter += 1

def add_recipe(recipe_data):
    # insert json_data to db
    cur = conn.cursor()
    url = recipe_data["url"]
    recipe_data = recipe_data["recipe_schema"]
    insert_sql = "INSERT INTO recipe (url, json_schema) VALUES (%s, %s) ON CONFLICT (url) DO UPDATE SET json_schema = EXCLUDED.json_schema"
    insert_data = (
        url,
        recipe_data,
    )
    cur.execute(insert_sql, insert_data)
    conn.commit()
    cur.close()

def add_embedding_to_all_rows():
    cur = conn.cursor()
    update_cur = conn.cursor()
    query = "SELECT url, json_schema FROM recipe;"
    cur.execute(query)
    counter = 0
    while True:
        rows = cur.fetchmany(100)
        if not rows:
            break

        for row in rows:
            print(counter)
            add_text_embedding(update_cur, row)
            #add_image_embedding(update_cur, row)
            counter += 1
    cur.close()
    update_cur.close()

def add_text_embedding(update_cur, row):
    url = row[0]
    data = row[1]["mainEntity"]
    text = recipe_json_to_text(data)
    text_embedding = get_text_embedding(text)
    query = """
            UPDATE recipe
            SET text_embedding = %s
            WHERE url = %s
            """
    update_cur.execute(query, (text_embedding, url))
    conn.commit()

def get_image(json_data):
    image_url = json_data["mainEntity"]["image"][0]
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img

