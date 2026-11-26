
# CraftLens 🔍

AI-powered DIY Craft Analyzer that transforms craft images into useful crafting guidance.

## Features
- Upload craft images
- Extract text using OCR
- Analyze images using Google Gemini AI
- Identify required materials and tools
- Generate step-by-step crafting instructions

## Tech Stack
- Python
- FastAPI
- Streamlit
- Google Gemini API
- OCR
- Docker

## Run with Docker

```bash
docker compose up --build
```

Frontend: http://localhost:8501

API Documentation: http://localhost:8000/docs

## Environment Setup

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
```

## Project Structure

```text
CraftLens/
├── app/
├── streamlit_app.py
├── Dockerfile
├── docker-compose.yml
├── req.txt
└── README.md
```

## Author
Hurain Suriya
