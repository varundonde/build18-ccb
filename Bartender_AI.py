"""
Module for interfacing with OpenAI API

Contains functions for generating volumes of each drink via natural language
processing (NLP) using the OpenAI API.

"""

import pyttsx3
import speech_recognition as sr
from openai import OpenAI


class Bartender_AI: 

    def __init__(self): 
        self.engine = self.initialize_tts()
        self.key = "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"
        
    # Initialize text-to-speech engine
    def initialize_tts(self):
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)  # Set speaking rate
        engine.setProperty("volume", 1.0)  # Set volume
        return engine

    # Text-to-speech function
    def speak(self, engine, text):
        engine.say(text)
        engine.runAndWait()

    # Speech-to-text function
    def get_speech_input(self, recognizer, microphone):
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
    
    def generate_list(self, prompt):
        client = OpenAI(
            api_key = self.key
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


    def generate_volume(self, user_instruction):
        # Available drinks
        drinks = ["Whiskey", "Tequila", "Aperol", "Coke", "Orange Juice", "Lime Juice"]
        print("Available drinks:", ", ".join(drinks))

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
        response = self.generate_list(prompt)
        if response != "Error":
            return True
        else:
            return False

