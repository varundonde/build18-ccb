"""
Module for interfacing with OpenAI API

Contains functions for generating volumes of each drink via natural language
processing (NLP) using the OpenAI API.

"""

import pyttsx3
import speech_recognition as sr
from openai import OpenAI


# Initialize text-to-speech engine
def initialize_tts():
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Set speaking rate
    engine.setProperty("volume", 1.0)  # Set volume
    return engine


# Text-to-speech function
def speak(engine, text):
    engine.say(text)
    engine.runAndWait()


# Speech-to-text function
def get_speech_input(recognizer, microphone):
    try:
        print("Listening for your instructions...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        print("Processing your input...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that. Please try again."
    except sr.RequestError as e:
        return f"Speech recognition service error: {e}"


def generate_matrix(prompt):
    client = OpenAI(
        api_key="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"
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message.content.strip())
    return (completion.choices[0].message.content.strip())


def generate_volume():
    # Initialize recognizer and microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Initialize text-to-speech engine
    tts_engine = initialize_tts()

    # Available drinks
    drinks = ["Whiskey", "Tequila", "Aperol", "Coke", "Orange Juice", "Lime Juice"]
    print("Available drinks:", ", ".join(drinks))
    speak(tts_engine, "Welcome to CCB, your Changi Chatbot Bartender!")

    while True:
        speak(tts_engine, "Please describe your flavor preferences, or say 'exit' to quit.")
        user_instruction = get_speech_input(recognizer, microphone)
        print("You said:", user_instruction)

        if user_instruction.lower() == "exit":
            speak(tts_engine, "Goodbye! Enjoy your drink!")
            break

        # Create the prompt for OpenAI API
        prompt = (
            f"Available drinks: {', '.join(drinks)}. "
            f"Instruction: {user_instruction}. "
            "Generate a python list of 6 integers representing percentages of each drink to be dispensed to satisfy the instruction. "
            "Give me just the list and nothing else. "
            "The list should satisfy the following conditions: "
            "1) Each number is between 0 and 100 inclusive. "
            "2) The sum of the numbers is 100."
        )

        print("Prompt:", prompt)

        # Generate the response from OpenAI API
        response = generate_matrix(prompt)
        if response != "Error":
            speak(tts_engine, f"I have prepared the following proportions for your drink: {response}. Enjoy!")
        else:
            speak(tts_engine, "I encountered an error while preparing your drink. Please try again.")


main()
