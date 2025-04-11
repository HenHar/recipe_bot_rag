import streamlit as st
from tempfile import NamedTemporaryFile
from llm import Prompts, client, model_version, get_response
from postgreSQL import get_similar_recipes_text

st.title("Chefkoch-Bot")
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model_version

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input(accept_file= True, file_type=["png", "jpg"], placeholder = "Was möchtest du kochen?"):
    text = user_input["text"]
    image = user_input["files"]

    # just take first image
    if image:
        image = image[0]

    with st.chat_message("user"):
        if text:
            st.markdown(text)
        if image:
            st.image(image)

    with st.chat_message("assistant"):
        if image:
            with NamedTemporaryFile() as f:
                f.write(image.getbuffer())
                try:
                    response = get_response(f.name, Prompts.describe_image_prompt)
                    text = response + "\n" + text
                except Exception as e:
                    text = "Es gab ein Problem mit der Bildverarbeitung."

        urls, distances, recipes = get_similar_recipes_text(text, limit_results=3)

        recipes_text = ""
        for recipe, url in zip(recipes, urls):
            recipes_text += "\n" + recipe + "\n" + url + "\n"

        formatted_prompt = Prompts.recipe_prompt.format(recipes_text, text)
        print(formatted_prompt)
        st.session_state.messages.append({"role": "user", "content": text})
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "user", "content": formatted_prompt}
            ],
            stream=True,
            #max_tokens=1000,
            #extra_body={"stop_token_ids": [128001, 128008, 128009]}
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
