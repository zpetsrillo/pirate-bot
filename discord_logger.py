import logging
import os
from dotenv import load_dotenv

load_dotenv()
LOG_FILE = os.getenv("LOG_FILE_DISCORD")

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=LOG_FILE, encoding="utf-8")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)