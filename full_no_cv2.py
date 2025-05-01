import os
from PIL import Image, ImageGrab
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import time

# Configure Gemini API
genai.configure(api_key="AIzaSyB_WwLUqtrx4Nnf73-W4wyzWhnhOc_wt_w")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-pro-vision")

# Initialize speech engines
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Speak function
def speak(text):
    print("\nRam says:", text)
    engine.say(text)
    engine.runAndWait()

# Capture image from screen instead of webcam
def capture_image_from_screen(filename="captured_image.jpg"):
    speak("Capturing screen image...")
    try:
        # Capture the entire screen
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        speak("Image successfully captured.")
        return filename
    except Exception as e:
        speak(f"Error capturing image: {e}")
        return None

# Analyze image with Gemini
def analyze_image(image_path):
    try:
        speak("Analyzing the image...")
        image = Image.open(image_path)
        image.thumbnail([1024, 1024], Image.Resampling.LANCZOS)

        prompt = "Describe what is in this image."
        response = model.generate_content([prompt, image])

        result = response.text.strip()
        speak(result)
    except Exception as e:
        speak(f"Error while analyzing image: {e}")

# Listen for command
def listen_command():
    with sr.Microphone() as source:
        print("\nListening for command...")
        # Adjust microphone settings for better sensitivity
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 300  # Lower value makes it more sensitive
        recognizer.pause_threshold = 0.5  # Shorter pause threshold
        
        print("Adjusting for ambient noise... Please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ready! Please speak now...")
        
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("Processing your speech...")
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio. Please speak more clearly.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

# Main assistant logic
def ram_assistant():
    print("Starting Ram Assistant...")
    speak("Hello! I'm Ram. Say 'Hey Ram' or give a direct command.")

    while True:
        print("\nWaiting for command...")
        command = listen_command()
        print(f"Received command: '{command}'")

        # Wake word detection
        if "hey ram" in command or "ram" in command:
            print("Wake word detected!")
            speak("Yes, I'm listening. What do you need?")
            instruction = listen_command()
            print(f"Received instruction: '{instruction}'")

            if any(kw in instruction for kw in ["take a picture", "describe", "what is this", "capture"]):
                print("Picture command detected!")
                speak("Okay, capturing an image now.")
                image_path = capture_image_from_screen()
                if image_path:
                    analyze_image(image_path)
                else:
                    speak("Sorry, I couldn't capture the image. Please try again.")

            elif any(kw in instruction for kw in ["exit", "stop", "goodbye"]):
                speak("Goodbye! Have a great day.")
                break

            else:
                speak("I didn't understand that. Can you try again?")

        # Allow direct commands without "Hey Ram"
        elif "take a picture" in command or "capture" in command:
            print("Direct picture command detected!")
            speak("Okay, capturing an image now.")
            image_path = capture_image_from_screen()
            if image_path:
                analyze_image(image_path)
            else:
                speak("Sorry, I couldn't capture the image. Please try again.")

        elif "exit" in command or "stop" in command:
            speak("Goodbye! Have a great day.")
            break

if __name__ == "__main__":
    print("Program starting...")
    try:
        ram_assistant()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...") 