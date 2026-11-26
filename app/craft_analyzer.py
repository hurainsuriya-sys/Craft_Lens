
import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.1-flash-lite"


def analyze_craft(image_bytes, mime_type):

    prompt = """
    You are CraftLens, an intelligent DIY craft analysis assistant.

    Analyze the uploaded craft image and return structured information.

    Identify:

    1. Craft name
    2. Detailed visual description
    3. Visible objects
    4. Possible materials
    5. Wire type, if visible or relevant
    6. Wire material
    7. Estimated wire thickness in mm, only if reasonably inferable
    8. Wire flexibility
    9. Required tools
    10. Difficulty level (Beginner, Intermediate, Advanced)
    11. Step-by-step crafting instructions
    12. Confidence level

    Pay special attention to:
    - Beading wire
    - Copper wire
    - Floral wire
    - Nylon thread
    - Pipe cleaners
    - Crochet yarn
    - Beads and accessories

    IMPORTANT:
    Do not invent materials or exact measurements.
    If something cannot be identified, write "Unknown".
    Clearly distinguish visible materials from suggested materials.
    Quantity estimates must be approximate.

    Return ONLY valid JSON using this structure:

    {
        "craft_name": "",
        "description": "",
        "visible_objects": [],
        "possible_materials": [],
        "wire_type": "",
        "wire_material": "",
        "estimated_thickness": "",
        "wire_flexibility": "",
        "required_tools": [],
        "difficulty": "",
        "steps": [],
        "confidence": "",
        "notes": ""
    }
    """

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt, image_part],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    try:
        return json.loads(response.text)

    except (json.JSONDecodeError, TypeError):
        raise ValueError(
            "Gemini returned an invalid JSON response"
        )

