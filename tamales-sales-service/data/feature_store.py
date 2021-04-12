import pandas as pd
import random
from google.cloud import bigquery


class FeatureStore():
    def __init__(self, path):
        self.path = path
        self.client = bigquery.Client()

    def get_features(self, product_id):
        
        # Perform a query.
        QUERY = (
            "SELECT * FROM `youtubelist-256522.products_feature_store.features` WHERE id_product = '{}' ORDER BY year_month DESC LIMIT 1".format(product_id)
        )
        query_job = self.client.query(QUERY)  
        rows = query_job.result()  

        for row in rows:
            sales = row.total_sales
            weight = row.weight_sales_month_by_calorie_category

        return pd.DataFrame({"ventas": [sales], "peso_mes_por_categoria_calorica":[weight]})