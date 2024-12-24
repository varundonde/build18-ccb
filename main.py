"""
i. process speech request via OpenAI Wrapper
ii. Translate into an array
iii. Call the actual RBP dispensing instruction (eg. stop —> dispense —> delay)
"""

# TODO : correct actual pin assignment once hardware is assembled


#--------------------IMPORTS--------------------
from openAI_methods import *
from dispense import *

from machine import RBP, Pin
import time

#--------------------CONSTANTS--------------------
DRINKS = ["Coke", "Pepsi", "Sprite", "Fanta", "Water", "Lemonade"]
# Pin 1: Coke, Pin 2: Pepsi, Pin 3: Sprite, Pin 4: Fanta, Pin 5: Water, Pin 6: Lemonade
NUM_PINS = 6 
PIN_PUMPS = [Pin(i, Pin.OUT) for i in range(NUM_PINS)]

#--------------------HELPERS--------------------

# are these really required?
def process_speech_request():
    pass


def convert_to_array():
    pass


def handle_gpt_response(volumes_generated):
    try:
        dispensing_volumes = list(map(int, volumes_generated.split(",")))
        if sum(dispensing_volumes) == 100 and all(0 <= x <= 100 for x in dispensing_volumes):
            print("Dispensing Volumes:", dispensing_volumes)
        else:
            print("Invalid response from ChatGPT. Please try again.")
    except ValueError:
        print("Could not parse ChatGPT's response. Please try again.")


#--------------------MAIN--------------------
def main():
    # Display available drinks
    print("Available drinks:", ", ".join(DRINKS))

    # Step 2: Await instructions
    while True:
        user_instruction = input("Hi! I'm CCB - your Changi Chatbot Bartender, and I'm here to create your drink of "
                                 "choice. Just tell me what flavor profiles you want, and I'll prepare a wonderful "
                                 "drink for you! Enter your instruction (or type 'exit' to quit): ")

        if user_instruction.lower() == "exit":
            print("Goodbye!")
            break

        # Step 3: Pass instruction to ChatGPT
        prompt = (
            f"Available drinks: {', '.join(DRINKS)}. "
            f"Instruction: {user_instruction}. "
            "Generate an comma separated list of 6 integers representing dispensing volumes for each drink, based on the instruction provided by the user. "
            "The array should satisfy the following conditions: "
            "1) Each number is between 0 and 100 inclusive. "
            "2) The sum of the numbers is 100."
        )

        volumes_generated = generate_volumes(prompt) # --> does this return an list for sure? 
        print("ChatGPT's response:", volumes_generated)
        # TODO: call parser if type mismatch --> handle_gpt_response
        # handle_gpt_response(volumes_generated)
        dispense(volumes_generated)
        user_response = input("Drink is prepared, Hope you enjoyed! Would you like to order another drink? (yes/no): ")
        if user_response.lower() == "no":
            break

main()
