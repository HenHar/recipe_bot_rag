# recipe_bot_rag

## Web crawler
* crawls all german recipes of REWE (https://www.rewe.de/rezepte/)

## VectorDB with postgreSQL and pg_vector
* use of sentence transformer to embed the recipe text into a vector
* similarity search between embedded user query and all recipes 
to obtain the semanticly most menainful recipes

## multimodal user input
* text -> embedding \
* image -> image description via VLLM -> embedding

## RAG + LLM
* Attach meaningful recipe to the user prompt via a prompt template
* Use of OpenAi LLM or a self-hosted model

## Chatbot App
* simple Streamlit App with a chat-interface
```
streamlit run chat_interface.py
```