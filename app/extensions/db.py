""" Configure db to sqlalchemy """
import os
from pathlib import Path
from dotenv import load_dotenv
from flask_sqlalchemy import *
from app import app
import psycopg2

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"
load_dotenv(ENV_FILE_PATH)
username = os.environ.get("DATABASE_USERNAME", "postgres")
password = os.environ.get("DATABASE_PASSWORD", "postgres")
host = os.environ.get("DATABASE_HOST", "localhost")
database_name = os.environ.get("DATABASE_NAME", "EXPENSE_TRCKER")
database_port = os.environ.get("DATABASE_PORT", 5432)

# For MySQL Connection :
# app.config["SQLALCHEMY_DATABASE_URI"] = (
#     f"mysql+pymysql://{username}:{password}@{host}/{database_name}"
# )
# For Postgresql Connection :
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{username}:{password}@{host}/{database_name}"
    # "postgres://expense_tracker_k2ey_user:5g9wjJ8tS7L7Gdq9FhJ5EiEUj5xTM5kh@dpg-cnq43kq1hbls738itsk0-a/expense_tracker_k2ey"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
