from typing_extensions import Final
import logging
from datetime import datetime
import json
import requests
from .config import MODEL_ID

class ProductService:
    def __init__(self, feature_store):
        self.feature_store = feature_store

    def predict(self, product_id):
        product_features = self.feature_store.get_features(product_id)
        prediction = self.get_model_prediction(product_features)
        return {"productid": product_id, "prediction": prediction, "version": MODEL_ID}

    def get_model_prediction(self, product_features):
        data_json = {"columns": list(product_features.columns), "data": product_features.values.tolist()}
        response = requests.post(url = "http://127.0.0.1:5001/invocations", json = data_json)
        return response.json()[0]

    

