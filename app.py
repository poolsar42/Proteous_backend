from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1",
    "https://proteous-9352268979b2.herokuapp.com",
    "https://proteous.work"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv('data.csv')  # Assuming data.csv is your CSV file


@app.get("/")
async def main():
    return {"message": "Hello World"}


@app.get('/all-entries')
async def all_entries():
    return df.head().to_json(orient='records')


@app.get('/substring-search')
async def substring_search():
    substring = request.args.get('substring')
    if substring:
        result = df[df['name'].str.startswith(substring)]
        return result.to_json(orient='records')
    return jsonify([])
