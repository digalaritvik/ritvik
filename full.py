import cv2
from PIL import Image
import google.generativeai as genai
import pyttsx3
import time
import numpy as np

# Configure Gemini API
genai.configure(api_key="AIzaSyB_WwLUqtrx4Nnf73-W4wyzWhnhOc_wt_w")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-pro-vision")

# Initialize speech engines
engine = pyttsx3.init()

# Import speech recognition after other imports
import speech_recognition as sr

recognizer = sr.Recognizer()


# Speak function
def speak(text):
    print("\nRam says:", text)
    engine.say(text)
    engine.runAndWait()


# Capture image from webcam
def capture_image_from_webcam(filename="captured_image.jpg"):
    speak("Opening webcam...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        speak("Error: Webcam is not accessible.")
        return None

    speak("Capturing image in 3 seconds... Hold still.")
    time.sleep(3)  # Short pause before capture

    ret, frame = cap.read()
    if not ret:
        speak("Error: Failed to capture image.")
        cap.release()
        return None

    cv2.imwrite(filename, frame)
    speak("Image successfully captured.")
    cap.release()
    return filename


# Segment image using OpenCV
def segment_image(image_path):
    try:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            speak("Error: Could not read the image.")
            return None

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply threshold
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on original image
        result = image.copy()
        cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

        # Save segmented image
        segmented_path = "segmented_" + image_path
        cv2.imwrite(segmented_path, result)
        speak("Image segmentation completed.")
        return segmented_path
    except Exception as e:
        speak(f"Error during segmentation: {e}")
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
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)  # Increased timeout
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            speak("I didn't catch that. Can you repeat?")
        except sr.RequestError:
            speak("There was a problem with the speech recognition service.")
        return ""


# Main assistant logic
def ram_assistant():
    speak("Hello! I'm Ram. Say 'Hey Ram' or give a direct command.")

    while True:
        command = listen_command()

        # Wake word detection
        if "hey ram" in command or "ram" in command:
            speak("Yes, I'm listening. What do you need?")
            instruction = listen_command()

            if any(kw in instruction for kw in ["take a picture", "describe", "what is this", "capture"]):
                speak("Okay, capturing an image now.")
                image_path = capture_image_from_webcam()
                if image_path:
                    speak("Would you like me to segment the image?")
                    segment_command = listen_command()
                    if "yes" in segment_command or "segment" in segment_command:
                        segmented_path = segment_image(image_path)
                        if segmented_path:
                            analyze_image(segmented_path)
                    else:
                        analyze_image(image_path)

            elif any(kw in instruction for kw in ["exit", "stop", "goodbye"]):
                speak("Goodbye! Have a great day.")
                break

            else:
                speak("I didn't understand that. Can you try again?")

        # Allow direct commands without "Hey Ram"
        elif "take a picture" in command or "capture" in command:
            speak("Okay, capturing an image now.")
            image_path = capture_image_from_webcam()
            if image_path:
                speak("Would you like me to segment the image?")
                segment_command = listen_command()
                if "yes" in segment_command or "segment" in segment_command:
                    segmented_path = segment_image(image_path)
                    if segmented_path:
                        analyze_image(segmented_path)
                else:
                    analyze_image(image_path)

        elif "exit" in command or "stop" in command:
            speak("Goodbye! Have a great day.")
            break


if __name__ == "__main__":
    ram_assistant()