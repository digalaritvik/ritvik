import base64
import os
from google import genai
from google.genai import types
import pyttsx3
engine = pyttsx3.init()

def generate():
    f=""
    client = genai.Client(
        api_key="AIzaSyB_WwLUqtrx4Nnf73-W4wyzWhnhOc_wt_w",
    )

    model = "gemini-2.5-pro-exp-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="how to dance"),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
        f+=chunk.text
    engine.say(f)
    engine.runAndWait()
if __name__ == "__main__":
    generate()