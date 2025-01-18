"""
Module for interfacing with OpenAI API

Contains functions for generating volumes of each drink via natural language
processing (NLP) using the OpenAI API.

"""

from openai import OpenAI

def generate_matrix(prompt):

    client = OpenAI(
    api_key= --
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )

    print(completion.choices[0].message.content.strip())
    return(completion.choices[0].message.content.strip())


def main():
    # Step 1: Input available drinks
    drinks = ["Whiskey", "Tequila", "Aperol", "Coke", "Orange Juice", "Lime Juice"]
    print("Available drinks:", ", ".join(drinks))

    # Step 2: Await instructions
    while True:
        user_instruction = input("Enter your instruction (or type 'exit' to quit): ")
        if user_instruction.lower() == "exit":
            print("Goodbye!")
            break

        # Step 3: Pass instruction to ChatGPT
        prompt = (
            f"Available drinks: {', '.join(drinks)}. "
            f"Instruction: {user_instruction}. "
            "Generate a python list of 6 integers representing percentages of each drink containing to be dispensed to satisfy the instruction."
            "Give me just the list and nothing else."
            "The list should satisfy the following conditions:"
            "1) Each number is between 0 and 100 inclusive."
            "2) The sum of the numbers is 100."
        )
        # prompt = "make a matrix of 6 numbers"
        print("prompt: ", prompt)
        generate_matrix(prompt)

main()
