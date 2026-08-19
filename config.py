import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

if not TOKEN:
    raise RuntimeError("TOKEN .env faylida ko'rsatilmagan!")
