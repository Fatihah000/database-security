import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://username:password@localhost/gestion_cours'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
