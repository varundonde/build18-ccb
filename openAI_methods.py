# open ai api key methods

import openai

# Set up OpenAI API key
openai.api_key = "insert_api_key"


# Generates volumes of each drink via NLP
def generate_volumes(prompt):
    response = openai.Completion.create(
        engine="insert_chatgpt_engine",
        prompt=prompt,
        max_tokens=100
    )
    print(response)  # To see what all is generated
    return response.choices[0].text.strip()
