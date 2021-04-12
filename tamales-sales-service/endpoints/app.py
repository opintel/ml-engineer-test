import google.cloud.logging
from dotenv import load_dotenv
from fastapi import FastAPI

from . import products

load_dotenv()
client = google.cloud.logging.Client()
client.setup_logging()

def create_app():
    app = FastAPI()
    app.include_router(products.router)
    return app
