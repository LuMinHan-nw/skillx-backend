import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()


APP_NAME = os.getenv("APP_NAME", "SkillX Backend")
APP_ENV = os.getenv("APP_ENV", "development")
APP_DEBUG = os.getenv("APP_DEBUG", "True").lower() == "true"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "skillx_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", ""))

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_this_secret_key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "120")
)

CERTIFICATE_SESSION_TARGET = int(os.getenv("CERTIFICATE_SESSION_TARGET", "5"))
PASSWORD_RESET_WINDOW_MINUTES = int(os.getenv("PASSWORD_RESET_WINDOW_MINUTES", "10"))

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
