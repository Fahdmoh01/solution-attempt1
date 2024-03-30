import smtplib, ssl
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError
from utils import password_generator, transform_data, store_as_csv
from schema import PasswordFields as PasswordSchema
import os
from dotenv import load_dotenv
import requests

app = FastAPI()

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
async def get_movies():
    """Gets data to themoviedb, transforms and stores them as csv files"""
    headers = {"accept": "application/json", "Authorization": f"Bearer {access_token}"}
    response = requests.get(movies_url, headers=headers)

    movies_result = response.json()
    transformed_data = transform_data(movies_result)
    store_as_csv(transformed_data)

    return JSONResponse({"data": transformed_data})
