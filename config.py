import os

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get("TRANSACT_API_CLIENT_ID")
DEVELOPER_API_KEY = os.environ.get("TRANSACT_API_DEVELOPER_API_KEY")
