import os
import warnings
import sys

import pandas as pd
import numpy as np
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tamales_inc.models.custom_model import BaseModel
from sklearn.model_selection import train_test_split
import mlflow
import argparse, sys
import google.auth
import gcsfs

import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

load_dotenv()

def get_data(mode, data_version):
    credentials, _ = google.auth.default()
    fs = gcsfs.GCSFileSystem(project='youtubelist-256522')

    files = [path for path in fs.ls(f'opi_processed_data/{data_version}/{mode}_set') if path.endswith(".parquet")]

    df = pd.DataFrame()
    for file_ in files:
        csv = pd.read_parquet("gs://" + file_)
        df = df.append(csv)
    return df


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train_model(data_version, alpha, l1_ratio):
    print("Training model with information", data_version, alpha, l1_ratio)
    warnings.filterwarnings("ignore")

    train_data = get_data("train", data_version)
    test_data = get_data("test", data_version)

    train_data = train_data[["year", "month", "total_sales", "weight_sales_month_by_calorie_category"]].fillna(0)
    test_data = test_data[["year", "month", "total_sales", "weight_sales_month_by_calorie_category"]].fillna(0)


    # Separate features from target 
    train_x = train_data.drop(["total_sales"], axis=1)
    test_x = test_data.drop(["total_sales"], axis=1)
    train_y = train_data[["total_sales"]]
    test_y = test_data[["total_sales"]]
    

    with mlflow.start_run():
        #Here we train a model
        model = BaseModel(alpha, l1_ratio)
        model.fit(train_x, train_y)

        #Here we predict qualities
        predictions = model.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predictions)

        mlflow.log_param("dataversion", data_version)
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(model, "model", registered_model_name="BaseOpiAnalyticsModel")
        else:
            mlflow.sklearn.log_model(model, "model")

        artifact_uri = mlflow.get_artifact_uri()
        print("Artifact uri: {}".format(artifact_uri))
        return artifact_uri

if __name__ == "__main__":

    parser=argparse.ArgumentParser()

    parser.add_argument('--dataversion', help='Get data version')
    parser.add_argument('--alpha', help='Alpha parameter')
    parser.add_argument('--l1ratio', help='l1ratio parameter')

    args=parser.parse_args()

    train_model(args.dataversion, float(args.alpha), float(args.l1ratio))
