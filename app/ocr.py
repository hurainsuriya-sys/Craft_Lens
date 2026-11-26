import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-3.1-flash-lite"
# os → accesses environment variables.



# load_dotenv() → loads the API key from your .env file.



# genai → imports Google's AI SDK.



# genai.Client() → creates a connection with Gemini.



# MODEL_NAME → stores the model name so we can reuse it.

from google.genai import types


def extract_text(image_bytes, mime_type):

    prompt = """
    Extract all readable text from this image.

    Preserve the original wording.
    Keep the text organized and readable.
    Do not summarize or explain.
    If no text is found, return 'No text detected'.
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=[
            prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            )
        ]
    )

    return response.text

# extract_text() receives the uploaded image.



# image_bytes contains the image data.



# mime_type tells Gemini whether it's a JPEG, PNG, etc.



# generate_content() sends both prompt and image to Gemini.



# response.text returns the extracted text.
