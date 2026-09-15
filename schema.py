import os

from dotenv import load_dotenv

load_dotenv()

# Supply the actual database schema through environment configuration.
schema = os.getenv("DB_SCHEMA", "")
