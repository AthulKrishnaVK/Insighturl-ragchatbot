
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise Exception("SUPABASE_URL missing in backend/.env")

if not SUPABASE_KEY:
    raise Exception("SUPABASE_KEY missing in backend/.env")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)