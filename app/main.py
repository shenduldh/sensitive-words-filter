import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter

from .types import FilterInput, FilterOutput
from src.logger import logger
from src.filter import SensitiveFilter


sensitive_words_path = os.getenv("SENSITIVE_WORDS_PATH", None)
tokenized_words_path = os.getenv("TOKENIZED_WORDS_PATH", None)
filter_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global filter_model
    filter_model = SensitiveFilter(sensitive_words_path, tokenized_words_path)
    logger.info("Filter is ready.")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/alive")
async def alive() -> dict:
    return {"status": "alive"}


@app.post("/filter")
async def filter(req: FilterInput) -> FilterOutput:
    logger.info("Request: %s" % req)
    is_sensitive, filtered, dirty_words = filter_model.filter(
        req.text, replace_char=req.replace_char
    )
    res = FilterOutput(
        filtered=filtered, dirty_words=dirty_words, is_sensitive=is_sensitive
    )
    logger.info("Response: %s" % res)
    return res
