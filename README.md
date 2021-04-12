# ml-engineer-test
Repositorio base para desarrollo de la prueba practica que forma parte del proceso de contratación para ML Engineer

## Estructura de carpetas

**EDA**. Se realizó la exploración de los datasets dentro del notebook data_exploration.ipynb

**ML workflow**. Contiene una serie de carpetas:
- dags: Se guardan los dags de Airflow programados para la orquestación de tareas.
- mlruns: Aquí se almacena la metadata correspondiente a los experimentos con MLFlow junto con los modelos resultantes. Contiene métricas calculadas e hiperparametros utilizados.
- secrets: Se guardan las credenciales para conectarse al proyecto de gcp que se levantó para este examen.

**API**. Contiene las siguientes carpetas para una mayor modularización:
- data: Código correspondiente para conectarse a base de datos.
- bp: Maneja la lógica de negocio del proceso de predicción. En este caso a partir del id del producto obtengo los features correspondientes desde la feature store.
A partir de esta información se construye y se llama al microservicio que MLFlow utliza para servir predicciones.
- endpoints: Se programan los endpoints destinados a llamar al servicio de predicción.
- di: Se crean los módulos necesarios para todas las capas a traves de inyección de dependencias.

## Datos
- Se utiliza bigquery para construir un feature store.
- Se crean 2 buckets:
   - opi_raw_data donde se almacenan los datos en crudo
   - opi_processed_data guarda los datos procesados en dos carpetas train_set y test_set en formato parquet.


## ¿Como correr el proyecto?
1. Descargar el código desde el repositorio de github.

2. Instalar poetry de manera global en el sistema.

3. Para correr el pipeline de entrenamiento.
   - Ir a la raíz del proyecto y luego entrar a la carpeta ml-engineer-test.
   - Instalar los paquetes requeridos: poetry install
   - Setear la variable de entorno AIRFLOW_HOME a esta carpeta
   - Levantar airflow: airflow scheduler en una terminal y airflow webserver en otra.
   - Activar manualmente el dag "train_dag"

   - Levantar la interfaz donde se visualizan los modelos entrenados: mlflow ui
   - Tomar la ruta del modelo que se quiere desplegar en producción.
   - Levantar el microservicio de predicción con mlflow models serve <uri del modelo>

4. Para levantar el servicio web

    - Ir a la raíz del proyecto
    - Instalar los paquetes requeridos: poetry install
    - En bp/config.py setear la versión del modelo que esta en producción.
    - Levantar el servicio web con python tamales-sales-service/main.py

5. Para solicitar predicciones.
    En postman u otro cliente hacer un POST request a la dirección http://localhost:8080/apis/products/predict/1.0.0
    junto con un json con el siguiente formato: {"productid": "206050084"}


# Diagrama de proceso de integración (MLOps)
![Screen 4](/images/proceso_de_integracion.png)

# Diagrama de infraestructura para escalar en la nube
![Screen 4](/images/diagrama_de_infraestructura.png)

