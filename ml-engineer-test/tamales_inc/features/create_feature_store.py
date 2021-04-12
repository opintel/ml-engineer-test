#!/usr/bin/python
from pyspark.sql import SparkSession
import pyspark
from pyspark.sql.types import StructType, StructField, DateType, StringType, IntegerType, DoubleType, LongType
from pyspark.sql.functions import expr
import pyspark.sql.functions as sf
import time
import argparse, sys

def update_feature_store(timestamp, train_perc):

    spark = SparkSession \
    .builder \
    .master('yarn') \
    .appName('bigquery-analytics-feature_engineering') \
    .getOrCreate()

    bucket = 'opi_staging_bucket'
    spark.conf.set('temporaryGcsBucket', bucket)

    mapping_month= {
            'Jan': "1",
            'Feb': "2",
            'Mar': "3",
            'Apr': "4",
            'May': "5",
            'Jun': "6",
            'Jul': "7",
            'Aug': "8",
            'Sep': "9",
            'Oct': "10",
            'Nov': "11",
            'Dec': "12",
        }

    url_to_load = "gs://opi_raw_data/09042021/teinvento_inc/ventas_reportadas_mercado_tamales/mx/20200801/fact_table"

    fact_table_schema = StructType([
            StructField("year", IntegerType()),
            StructField("month", StringType()),
            StructField("sales", DoubleType()),
            StructField("id_region", LongType()),
            StructField("id_product", StringType()),
        ])

    fact_table = spark.read.schema(fact_table_schema).csv(url_to_load)

    url_to_load = "gs://opi_raw_data/09042021/teinvento_inc/ventas_reportadas_mercado_tamales/mx/20200801/product_dim"

    product_dim_schema = StructType([
            StructField("id_product", StringType()),
            StructField("calorie_category", StringType()),
            StructField("product", StringType()),
            StructField("product_brand", StringType()),
            StructField("producer", StringType()),
        ])

    product_dim = spark.read.schema(product_dim_schema).csv(url_to_load)

    url_to_load = "gs://opi_raw_data/09042021/teinvento_inc/ventas_reportadas_mercado_tamales/mx/20200801/region_dim"

    region_dim_schema = StructType([
            StructField("id_region", LongType()),
            StructField("country", StringType()),
            StructField("region", StringType()),
        ])

    region_dim = spark.read.schema(region_dim_schema).csv(url_to_load)

    #Join tables and sort columns
    join_expr = fact_table.id_product == product_dim.id_product
    join_expr2 = fact_table.id_region == region_dim.id_region

    inventadasa_table = fact_table.join(product_dim, join_expr, "inner").drop(product_dim.id_product)
    inventadasa_table = inventadasa_table.join(region_dim, join_expr2, "inner").drop(region_dim.id_region)
    inventadasa_table = inventadasa_table.withColumn("source", sf.lit("inventadasa"))
    inventadasa_table = inventadasa_table.select("source", "year", "month", "country", "calorie_category", "id_region", "region", "id_product", "product", "product_brand", "producer", "sales")
    inventadasa_table

    #Process tamalesinc information

    url_to_load = "gs://opi_raw_data/09042021/tamales_inc/ventas_mensuales_tamales_inc/mx/20200801/csv/Centro"

    tamales_schema = StructType([
            StructField("year", IntegerType()),
            StructField("month", StringType()),
            StructField("country", StringType()),
            StructField("calorie_category", StringType()),
            StructField("flavor", StringType()),
            StructField("zone", StringType()),
            StructField("product_code", StringType()),
            StructField("product_name", StringType()),
            StructField("sales", DoubleType()),
        ])

    ventas_centro = spark.read.schema(tamales_schema).csv(url_to_load)

    url_to_load = "gs://opi_raw_data/09042021/tamales_inc/ventas_mensuales_tamales_inc/mx/20200801/csv/E._Privados"

    tamales_schema = StructType([
            StructField("year", IntegerType()),
            StructField("month", StringType()),
            StructField("country", StringType()),
            StructField("calorie_category", StringType()),
            StructField("flavor", StringType()),
            StructField("zone", StringType()),
            StructField("product_code", StringType()),
            StructField("product_name", StringType()),
            StructField("sales", DoubleType()),
        ])

    ventas_privados = spark.read.schema(tamales_schema).csv(url_to_load)

    url_to_load = "gs://opi_raw_data/09042021/tamales_inc/ventas_mensuales_tamales_inc/mx/20200801/csv/Norte"

    tamales_schema = StructType([
            StructField("year", IntegerType()),
            StructField("month", StringType()),
            StructField("country", StringType()),
            StructField("calorie_category", StringType()),
            StructField("flavor", StringType()),
            StructField("zone", StringType()),
            StructField("product_code", StringType()),
            StructField("product_name", StringType()),
            StructField("sales", DoubleType()),
        ])

    ventas_norte = spark.read.schema(tamales_schema).csv(url_to_load)

    url_to_load = "gs://opi_raw_data/09042021/tamales_inc/ventas_mensuales_tamales_inc/mx/20200801/csv/Sur"

    tamales_schema = StructType([
            StructField("year", IntegerType()),
            StructField("month", StringType()),
            StructField("country", StringType()),
            StructField("calorie_category", StringType()),
            StructField("flavor", StringType()),
            StructField("zone", StringType()),
            StructField("product_code", StringType()),
            StructField("product_name", StringType()),
            StructField("sales", DoubleType()),
        ])

    ventas_sur = spark.read.schema(tamales_schema).csv(url_to_load)

    #Join tables and sort columns

    tamalesinc_table = ventas_norte.union(ventas_sur).union(ventas_privados).union(ventas_centro)
    join_expr = tamalesinc_table.zone == region_dim.region
    tamalesinc_table = tamalesinc_table.join(region_dim, join_expr, "inner")
    tamalesinc_table = tamalesinc_table.drop(region_dim.country).drop(region_dim.region).withColumnRenamed("zone", "region")
    tamalesinc_table = tamalesinc_table.withColumnRenamed("product_code", "id_product")
    tamalesinc_table = tamalesinc_table.withColumn("product", expr("concat(product_name, ' ', flavor)")).withColumn("product_brand", expr("concat(product_name, ' ', flavor)"))
    tamalesinc_table = tamalesinc_table.withColumn("producer", sf.lit("Tamales Inc"))
    tamalesinc_table = tamalesinc_table.withColumn("source", sf.lit("tamalesinc"))
    tamalesinc_table = tamalesinc_table.select("source", "year", "month", "country", "calorie_category", "id_region", "region", "id_product", "product", "product_brand", "producer", "sales")
    tamalesinc_table



    full_table = inventadasa_table.union(tamalesinc_table)
    full_table

    #Sum across sources and regions
    sum_sales = sf.sum("sales").alias("total_sales")
    sum_table = full_table.groupBy("year", "month", "country", "calorie_category", "id_product", "product", "product_brand", "producer").agg(sum_sales)

    #Sum grouped by year, month, product and category
    avg_product_category = sf.avg("total_sales").alias("avg_sales_month_by_calorie_category")
    max_product_category = sf.max("total_sales").alias("max_sales_month_by_calorie_category")
    calorie_category_agg = sum_table.groupBy("year", "month", "id_product", "calorie_category").agg(*[avg_product_category, max_product_category])
    calorie_category_agg = calorie_category_agg.withColumn("weight_sales_month_by_calorie_category", sf.col("avg_sales_month_by_calorie_category")/sf.col("max_sales_month_by_calorie_category"))

    join_expr = (sum_table.year == calorie_category_agg.year) & (sum_table.month == calorie_category_agg.month) & (sum_table.id_product == calorie_category_agg.id_product) & (sum_table.calorie_category == calorie_category_agg.calorie_category)
    engineered_table = sum_table.join(calorie_category_agg, join_expr, "inner").drop(calorie_category_agg.year).drop(calorie_category_agg.month).drop(calorie_category_agg.id_product).drop(calorie_category_agg.calorie_category)
    engineered_table = engineered_table.replace(to_replace=mapping_month, subset=['month'])
    engineered_table = engineered_table.withColumn("year_month", expr("to_date(concat('1', '/', month,'/',year), 'd/M/y')"))
    engineered_table = engineered_table.select("year", "month", "year_month", "country", "calorie_category", "id_product", "product", "product_brand", "producer", "total_sales", "weight_sales_month_by_calorie_category")

    engineered_table.write.format('bigquery') \
        .option('table', 'products_feature_store.features') \
        .mode('overwrite') \
        .save()

    #Take a snapshot for the training set
    engineered_table.createOrReplaceTempView("engineered_table")
    train_set = spark.sql(f"""
            SELECT *
            FROM engineered_table
            WHERE MOD(ABS(HASH(id_product)), 10) < {train_perc//10}""")

    url_to_dump_train = "gs://opi_processed_data/" + timestamp + "/train_set"
    train_set.write.parquet(url_to_dump_train)

    #Take a snapshot for the test set
    test_set = spark.sql(f"""
            SELECT *
            FROM engineered_table
            WHERE MOD(ABS(HASH(id_product)), 10) >= {train_perc//10}""")

    url_to_dump_test = "gs://opi_processed_data/" + timestamp + "/test_set"
    test_set.write.parquet(url_to_dump_test)

if __name__ == "__main__":
    parser=argparse.ArgumentParser()

    parser.add_argument('--timestamp', help='Timestamp in string format')
    parser.add_argument('--train_perc', help='Number from 0 to 100')

    args=parser.parse_args()

    timestamp = args.timestamp
    train_perc = int(args.train_perc)

    update_feature_store(timestamp, train_perc)