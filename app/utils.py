from pathlib import Path
import os
import random
import pandas as pd
from schema import PasswordFields as PasswordSchema

# from datetime import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = lowercase.upper()
digits = "0123456789"
symbols = "!@#$%^&*()-_=+[]{};':\",./<>?"


def password_generator(fields: PasswordSchema) -> str:
    """
    Generates passwords based on field options provided
    """
    password = ""
    if fields.lowercase:
        password += lowercase
    if fields.uppercase:
        password += uppercase
    if fields.digits:
        password += digits
    if fields.symbols:
        password += symbols

    if not password:
        raise ValueError(
            "One of (lowercase, uppercase, digits, or symbols) must be enabled"
        )
    return "".join(random.choice(password) for _ in range(fields.length))


def transform_data(movies_result):
    movie_list = []
    for data in movies_result["results"]:
        movie_id = data["id"]
        movie_title = data["title"]
        movie_overview = data["overview"]
        movie_ratings = data["vote_average"]
        movie_release_date = data["release_date"]
        movie_poplarity = data["popularity"]
        movie_poster = data["poster_path"]
        movie_element = {
            "moive_id": movie_id,
            "movie_title": movie_title,
            "movie_poster": movie_poster,
            "movie_overview": movie_overview,
            "movie_ratings": movie_ratings,
            "movie_release_date": movie_release_date,
            "movie_poplarity": movie_poplarity,
        }
        movie_list.append(movie_element)
    return movie_list


# def store_as_csv(transformed_data):
#     movie_df = pd.DataFrame.from_dict(transformed_data)
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     filename = "movies_transformed_" + str(datetime.now()) + ".csv"
#     storage_path = Path(os.path.join(base_dir, "transformed_data", filename))
#     movie_df.to_csv(storage_path, index=False)
