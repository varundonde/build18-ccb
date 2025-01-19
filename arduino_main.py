"""
This is the main file that will run the entire system. The role of this main file
is broken down into the following steps:

1. Prompts the user to enter an instruction
2. Passes the instruction to ChatGPT to generate a list of dispensing volumes 
using a separate module called openAI_methods.py (abstracted)
3. Sends the list of dispensing volumes to the Arduino using pyserial
4. The Arduino then dispenses the drinks based on the volumes received (abstracted)
"""


#--------------------IMPORTS--------------------
from Bartender_AI import *
import speech_recognition as sr


import time
import serial

#--------------------CONSTANTS--------------------

DRINKS = ["Coke", "Pepsi", "Sprite", "Fanta", "Water", "Lemonade"]
BARTENDER = Bartender_AI()
RECOGNIZER = sr.Recognizer()
MICROPHONE  = sr.Microphone()
TTS_INTRO = """Hi! I'm CCB - your Changi Chatbot Bartender, 
and I'm here to create your drink of choice. 
Just tell me what flavor profiles you want, 
and I'll prepare a wonderful drink for you! 
Enter your instruction (or type 'exit' to quit): """

#--------------------HELPERS--------------------


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

    # Initilize the serial port
    # Replace 'COM3' with your Arduino's port
    # arduino_port = "COM3"
    # baud_rate = 9600  # Match Arduino's baud rate

    # Initialize serial connection
    # ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    # time.sleep(2)  # Wait for the connection to initialize

    # Step 2: Await instructions
    while True:
        # Let Bartender introduce
        BARTENDER.speak(BARTENDER.engine, TTS_INTRO)
        user_instruction = BARTENDER.get_speech_input(RECOGNIZER, MICROPHONE)

        if user_instruction.lower() == "exit":
            print("Goodbye!")
            break

        print(user_instruction, type(user_instruction[0]))

        # Step 2: Pass instruction to ChatGPT
        # Calls the function from openAI_methods.py
        volumes_generated = BARTENDER.generate_volume(user_instruction)
        print(volumes_generated)
        # volumes_generated should be a list of ratios
        if volumes_generated: 
            BARTENDER.speak(BARTENDER.engine, "Your request is a success!")

        # For debugging
        # print("ChatGPT's response:", volumes_generated)
        
        # Step 3: Sends the list of dispensing volumes to the Arduino
        volumes_str = ",".join(map(str,volumes_generated)) + "\n"
        ser.write(volumes_str.encode('utf-8'))

        # Wait for acknowledgement from Arduino
        while True:
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                if response == "ack":
                    print("Arduino acknowledged the instruction")
                else: 
                    print("Arduino failed to acknowledge the instruction")
                break

        BARTENDER.speak(BARTENDER.engine, "Do you want to make another drink? (yes/no)")
        BARTENDER.get_speech_input(RECOGNIZER, MICROPHONE)
        if user_response.lower() == "no":
            break

main()
