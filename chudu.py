import google.generativeai as genai
from PIL import Image

import io
import os
import requests
from io import BytesIO

GOOGLE_API_KEY="AIzaSyB_WwLUqtrx4Nnf73-W4wyzWhnhOc_wt_w"

from google import genai
from google.genai import types

client = genai.Client(api_key=GOOGLE_API_KEY)
model_name = "gemini-2.5-pro-exp-03-25" # @param ["gemini-1.5-flash-latest","gemini-2.0-flash-lite","gemini-2.0-flash","gemini-2.5-pro-exp-03-25"] {"allow-input":true}

image = "test.png" # @param ["Socks.jpg","Vegetables.jpg","Japanese_bento.png","Cupcakes.jpg","Origamis.jpg","Fruits.jpg","Cat.jpg","Pumpkins.jpg","Breakfast.jpg","Bookshelf.jpg", "Spill.jpg"] {"allow-input":true}
im = Image.open(image)

prompt = "Explain about the image"  # @param {type:"string"}

# Load and resize image
im = Image.open(BytesIO(open(image, "rb").read()))
im.thumbnail([1024,1024], Image.Resampling.LANCZOS)

# Run model to find bounding boxes
response = client.models.generate_content(
    model=model_name,
    contents=[prompt, im],
    config = types.GenerateContentConfig(
        # system_instruction=bounding_box_system_instructions,
        temperature=0.5,
        # safety_settings=safety_settings,
    )
)

# Check output
print(response.text)