import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.resolve()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE = os.environ.get('DATABASE') or str(BASE_DIR / 'instance' / 'database.db')
