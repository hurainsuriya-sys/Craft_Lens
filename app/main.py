
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from io import BytesIO

from app.ocr import extract_text
from app.craft_analyzer import analyze_craft
from app.materials import estimate_materials


app = FastAPI(
    title="CraftLens",
    description="AI-powered DIY Craft Image Analyzer",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to CraftLens",
        "status": "API is running"
    }


@app.post("/analyze-craft")
async def analyze_image(file: UploadFile = File(...)):

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="No image uploaded"
        )

    if len(image_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Image must be smaller than 5 MB"
        )

    try:
        img = Image.open(BytesIO(image_bytes))

        image_format = img.format

        allowed_formats = ["JPEG", "PNG", "WEBP"]

        if image_format not in allowed_formats:
            raise HTTPException(
                status_code=415,
                detail="Only JPG, PNG and WEBP images are allowed"
            )

        img.verify()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image"
        )

    mime_type = f"image/{image_format.lower()}"

    try:
        # OCR
        extracted_text = extract_text(
            image_bytes,
            mime_type
        )

        # Craft analysis
        craft_data = analyze_craft(
            image_bytes,
            mime_type
        )

        # Materials and wire analysis
        material_data = estimate_materials(
            craft_data
        )

        return {
            "filename": file.filename,
            "format": image_format,
            "size": len(image_bytes),
            "extracted_text": extracted_text,
            "craft_analysis": craft_data,
            "material_analysis": material_data,
            "message": "CraftLens analysis completed successfully"
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(error)}"
        )
# Code	Meaning
# UploadFile	Represents a file uploaded by the user
# File(...)	Tells FastAPI that this parameter comes from a file upload
# async def	Defines an asynchronous function
# await file.read()	Reads the uploaded file's contents
# len(image)	Calculates the size of the image data in bytes
# content_type	Tells us the file type, such as image/jpeg
# BytesIO(image)	Makes image bytes readable like a file in memory
# Image.open()	Opens the image using Pillow
# img.verify()	Checks whether the image file is valid
# HTTPException	Returns an HTTP error when something goes wrong
# 413	Request content is too large
# 400	Invalid input
