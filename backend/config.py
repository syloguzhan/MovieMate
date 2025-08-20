import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")


    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:123456789@localhost:5432/movie_mate"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "movie-mate-jwt")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)

    API_KEY = os.getenv("API_KEY")  
    BASE_URL1 = "https://api.themoviedb.org/3/movie/"
    BASE_URL2 = "https://api.themoviedb.org/3/tv/"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
