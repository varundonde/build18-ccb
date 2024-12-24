"""
Module for interfacing with OpenAI API

Contains functions for generating volumes of each drink via natural language
processing (NLP) using the OpenAI API.

"""

import openai

# Set up OpenAI API key
openai.api_key = "insert_api_key"


# @brief Generates volumes of each drink via NLP
# Example Response: [20, 20, 20, 20, 20, 20]

# Generates volumes of each drink via NLP
def generate_volumes(prompt):
    response = openai.Completion.create(
        engine="insert_chatgpt_engine",
        prompt=prompt,
        max_tokens=100
    )
    print(response)  # To see what all is generated
    return response.choices[0].text.strip() # TODO: does this actually return a list
