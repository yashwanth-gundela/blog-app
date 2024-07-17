import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or '--insert--your--dbconnectivity--here--' ## postgresql://username:Password@localhost/db-name
    SQLALCHEMY_TRACK_MODIFICATIONS = False
