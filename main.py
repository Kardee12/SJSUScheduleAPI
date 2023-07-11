from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import scraper

app = FastAPI()

@app.get("/")
async def root():
    data_scraper = scraper.scrapeData()
    json_data = data_scraper.to_json()
    return json_data

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}