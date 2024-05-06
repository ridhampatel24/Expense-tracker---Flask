"""Other module"""
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"
load_dotenv(ENV_FILE_PATH)


class Config:
    """setting config variables"""
    # for image path
    IMAGES_UPLOADS = "static/images"
    # session
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    # jwt
    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_COOKIE_NAME = "x-access-token"
    # per page item
    PER_PAGE_ITEM_VIEW = 3
