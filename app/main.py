from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError
from utils import password_generator, transform_data
from schema import PasswordFields as PasswordSchema
from pathlib import Path
import os
from dotenv import load_dotenv
import requests

app = FastAPI()

BASE_DIR = Path(__file__).parent.parent.absolute()

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)
templates = Jinja2Templates(directory=BASE_DIR / "templates")

load_dotenv(".env")
movies_url = os.environ["MOVIES_URL"]
access_token = os.environ["ACCESS_TOKEN"]


@app.post("/generate-password")
async def generate_password(additionalFields: PasswordSchema):
    """
    This endpoint generates a password
    """
    try:
        password = password_generator(additionalFields)
        return JSONResponse({"generatedPassword": password, "length": len(password)})
    except ValueError as e:
        return Response({"error": str(e)})


@app.get("/third-party-api")
async def get_movies(request: Request):
    """Fetches"""
    headers = {"accept": "application/json", "Authorization": f"Bearer {access_token}"}
    response = requests.get(movies_url, headers=headers)

    movies_result = response.json()
    transformed_movie_data = transform_data(movies_result)
    return templates.TemplateResponse(
        "movies.html", {"request": request, "movie_info": transformed_movie_data[:10]}
    )
