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


def main():
    # Step 1: Input available drinks
    drinks = ["Coke", "Pepsi", "Sprite", "Fanta", "Water", "Lemonade"]
    print("Available drinks:", ", ".join(drinks))

    # Step 2: Await instructions
    while True:
        user_instruction = input("Hi! I'm CCB - your Changi Cocktail Bartender, and I'm here to create your drink of "
                                 "choice. Just tell me what flavor profiles you want, and I'll prepare a wonderful "
                                 "drink for you! Enter your instruction (or type 'exit' to quit): ")
        if user_instruction.lower() == "exit":
            print("Goodbye!")
            break

        # Step 3: Pass instruction to ChatGPT
        prompt = (
            f"Available drinks: {', '.join(drinks)}. "
            f"Instruction: {user_instruction}. "
            "Generate an array of 6 integers representing dispensing volumes for each drink. "
            "The array should satisfy the following conditions: "
            "1) Each number is between 0 and 100 inclusive. "
            "2) The sum of the numbers is 100."
        )

        volumes_generated = generate_volumes(prompt)
        print("ChatGPT's response:", volumes_generated)

        # # Step 4: Parse response into an array (assuming ChatGPT gives a comma-separated list)
        # try:
        #     dispensing_volumes = list(map(int, volumes_generated.split(",")))
        #     if sum(dispensing_volumes) == 100 and all(0 <= x <= 100 for x in dispensing_volumes):
        #         print("Dispensing Volumes:", dispensing_volumes)
        #     else:
        #         print("Invalid response from ChatGPT. Please try again.")
        # except ValueError:
        #     print("Could not parse ChatGPT's response. Please try again.")


main()
