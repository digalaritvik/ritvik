import cv2
import google.generativeai as genai
from PIL import Image
import io
import numpy as np

# Set up Google API Key
GOOGLE_API_KEY = "AIzaSyB_WwLUqtrx4Nnf73-W4wyzWhnhOc_wt_w"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Capture a frame
ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Failed to capture image.")
    exit()

# Convert OpenCV image (BGR) to PIL image (RGB)
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
image = Image.fromarray(frame_rgb)

# Resize image
image.thumbnail([1024, 1024], Image.Resampling.LANCZOS)

# Set up the model
model_name = "gemini-2.5-pro-exp-03-25"
prompt = "Describe the image"

# Run model to analyze image
client = genai.GenerativeModel(model_name)
response = client.generate_content(
    contents=[prompt, image],
    generation_config={"temperature": 0.5}  # *Fixed this line*
)

# Print the output
print(response.text)