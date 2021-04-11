import os
import warnings
import sys

import pandas as pd
import numpy as np
from urllib.parse import urlparse
from tamales_inc.models.custom_model import TemplateClassifier
from sklearn.model_selection import train_test_split
import mlflow

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # Read the wine-quality csv file from the URL
    csv_url = (
        "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    )
    try:
        data = pd.read_csv(csv_url, sep=";")
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s", e
        )

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    model = TemplateClassifier()
    model.fit(train_x, train_y)

        #Here we predict qualities

    

    with mlflow.start_run():
        #Here we train a model
        model = TemplateClassifier()
        model.fit(train_x, train_y)

        #Here we predict qualities

        df = pd.DataFrame({"ventas": [1, 2, 3, 4], "peso_mes_por_categoria_calorica":[5, 6, 7, 8]})

        predictions = model.predict(df)
        print("The predictions are", predictions)

        #(rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        alpha = 0.5
        l1_ratio = 5.3

        rmse = 5.6
        mae = 6.9
        r2 = 9.8
        
        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":

            # Register the model
            # There are other ways to use the Model Registry, which depends on the use case,
            # please refer to the doc for more information:
            # https://mlflow.org/docs/latest/model-registry.html#api-workflow
            mlflow.sklearn.log_model(model, "model", registered_model_name="ElasticnetWineModel")
        else:
            mlflow.sklearn.log_model(model, "model")
