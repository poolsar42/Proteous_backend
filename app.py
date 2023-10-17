from fastapi import FastAPI
from flask import jsonify
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from models.request import XGBoostRequest, BestVarianceRequest
from models.response import XGBoostResponse, BestVarianceResponse
from models.service import XGBoostService
import xgboost

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


@app.get('/all-entries')
async def all_entries():
    n = len(df)
    idx = np.arange(n)
    np.random.shuffle(idx)
    return df.iloc[idx[:5]].to_json(orient='records')


@app.post('/get_best_variants', response_model=BestVarianceResponse)
async def get_best_variants(request: BestVarianceRequest):
    aa = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
          'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    results = [''] * 5
    # for demo its 5, but it needs to be the length of sequence
    tms = np.zeros(5)
    for i in range(5):  # range(len(request.sequence)):
        for j in range(len(aa)):
            seq_t = list(request.sequence)
            seq_t[i] = aa[j]
            request_tm = XGBoostRequest(sequence=''.join(seq_t))
            tm = XGBoostService.predict(request_tm).tm
            for p in range(5):
                if tms[p] < tm:
                    results[p] = seq_t
                    tms[p] = tm
                    break

    return BestVarianceResponse(sequences=[''.join(x) for x in results])


@app.get('/substring-search')
async def substring_search():
    substring = request.args.get('substring')
    if substring:
        result = df[df['name'].str.startswith(substring)]
        return result.to_json(orient='records')
    return jsonify([])


@app.post('/predict', response_model=XGBoostResponse)
async def predict(request: XGBoostRequest):
    return XGBoostService.predict(request)
