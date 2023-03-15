from fastapi import FastAPI
from routes.llaveros import llavero
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = FastAPI()
app.include_router(llavero)