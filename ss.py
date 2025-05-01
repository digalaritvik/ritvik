import speech_recognition as sr
import pyttsx3
from google import genai
from google.genai import types

# Initialize TTS engine
engine = pyttsx3.init()

# Function: Text to Speech using Gemini
def text_to_speech():
    prompt = input("Enter your prompt for Gemini (e.g., 'How to cook pasta?'): ")

    try:
        client = genai.Client(
            api_key="AIzaSyB_WwLUqtrx4Nnf73-W4wyzWhnhOc_wt_w",  # Replace this with your real API key
        )

        model = "gemini-2.5-pro-exp-03-25"
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
        )

        result_text = ""

        print("\nGemini response:\n")
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            print(chunk.text, end="")
            result_text += chunk.text

        # Speak the generated text
        print("\n\nSpeaking the response...")
        engine.say(result_text)
        engine.runAndWait()

    except Exception as e:
        print("An error occurred in text-to-speech:", str(e))


# Function: Speech to Text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio")
    except sr.RequestError:
        print("Error connecting to Google API")


# Main menu
def main():
    print("Choose an option:")
    print("1. text to speech")
    print("2. speech to text")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        text_to_speech()
    elif choice == "2":
        speech_to_text()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()