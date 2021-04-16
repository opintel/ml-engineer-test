from airflow import DAG
import pandas
from airflow.utils.dates import days_ago
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator
from airflow.contrib.operators.dataproc_operator import DataProcPySparkOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterDeleteOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from tamales_inc.models.train_model import train_model

default_arguments = {'owner': 'Cesar Juarez', 'start_date': days_ago(1)}


with DAG(
    'update_feature_store_and_retrain',
    schedule_interval='0 20 * * *',
    catchup=False,
    default_args=default_arguments) as dag:

    dag.doc_md = __doc__

    create_cluster_task = DataprocClusterCreateOperator(
        task_id='create_cluster',
        project_id='youtubelist-256522',
        cluster_name='spark-cluster1-{{ ds_nodash }}',
        num_workers=2,
        storage_bucket="opi_staging_bucket",
        metadata={'PIP_PACKAGES':'pandas praw google-cloud-storage'},
        region="us-central1"
    )


    feature_engineering_task = DataProcPySparkOperator(
        task_id='feature_engineering',
        main='gs://opi_processed_data/pyspark/create_feature_store.py',
        cluster_name='spark-cluster1-{{ ds_nodash }}',
        dataproc_pyspark_jars="gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar",
        arguments=['--timestamp', '{{ ts_nodash }}', '--train_perc', "70"],
        region="us-central1"
    )

    delete_cluster_task = DataprocClusterDeleteOperator(
        task_id="delete_cluster",
        project_id="youtubelist-256522",
        cluster_name="spark-cluster1-{{ ds_nodash }}",
        region="us-central1"
    )

    train_task = PythonOperator(
        task_id="train_model", python_callable=train_model, op_args=['{{ ts_nodash }}', 0.9, 0.5],
    )

create_cluster_task >> feature_engineering_task >> delete_cluster_task >> train_task
