from metaflow import FlowSpec, step
from fastapi import FastAPI
import numpy as np
import pickle


app = FastAPI()

@app.get('/')
def index():
    return{'v01 api'}
@app.get('/lineal/{sales_value}/{Wcomp_value}')
def lineal(sales_value: float, Wcomp_value: float):
    x = [sales_value, Wcomp_value]
    vals = np.asarray(X)
    vals = vals.reshape(1,2)
    y = vals[:, 0] * vals[:, 1] + np.log(vals[:, 0])
    return y