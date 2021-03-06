# ml-engineer-test
Repositorio base para desarrollo de la prueba practica que forma parte del proceso de contratación para ML Engineer

# Contexto
Este repositorio usa como estructura base Cookiecutter Data Science el cual te ayudara a estructurar la logica de limpieza de datos y de feature engineering para tu prueba de forma ordenada.

Si tienes dudas o curiosidad sobre este template puedes visitar su [documentación oficial](https://drivendata.github.io/cookiecutter-data-science/).

## Estructura de carpetas

**EDA**. Para hacer exploración de datos esta permitido el uso de jupyter notebooks dentro de la carpeta notebooks.

**ML workflow**. El resultado final de tu proceso de ML debera estan dentro de la carpeta `ml-engineer-test/tamales_inc` el cual ya contiene una estructura base para que puedas modularizar tu proceso. Recuerda que todo tu código debe estar en archivos python.

**API**. Todo el código resultante de la implementación del API debe vivir dentro de la carpeta `tamales_sales_service` que se encuentra al primer nivel de este repositorio. La estructura de carpetas internas queda a tu consideración, pero recuerda que debe existir un mecanismo claro para echar andar tu API.

## Datos
Los datos raw necesarios para realizar tu prueba se encuentran dentro de una cuenta de almancenamiento en azure (Blob storage).

Para descargar los archivos deben acceder por medio del [Explorador de Datos de Azure](https://azure.microsoft.com/es-es/features/storage-explorer/) usando la siguiente cadena de conexión:

```https://opimltest.blob.core.windows.net/tamales-inc?sv=2020-04-08&st=2021-03-22T18%3A47%3A59Z&se=2022-03-23T18%3A47%3A00Z&sr=c&sp=rl&sig=4iGCoaMc5ZphqSrGrUNIK85t%2B6ovM%2FEvuIIv6WYyLAI%3D```

Este acceso es de solo lectura y les permitira navegar de forma remota en los datos y descargarlos en tu ambiente local para que trabajaes en tu propuesta.

Los datos raw que debes descargar viviran dentro de la carpeta `ml-engineer-test/data/raw` de este repositorio durante el ciclo de desarrollo.

Los datos procesados resultantes de tus pipelines de datos deberan vivir dentro de `ml-engineer-test/data/processed/`  y seguir la siguiente estructura

**Nota** No es necesario que incluyas los datos crudos en tu commit o tu Pull Request.

```
{nombre-fuente}/{version-datos-yyyymmdd}/archivo
```
Los formatos de datos sugeridos para escribir los datos son `csv` y `parquet`.

## ¿Como realizar esta prueba?
1. Es necesario que hagas un fork de este repositorio
2. Completes tu prueba practica dentro de tu fork. No olvides documentar los detalles de tu implementación en el readme del proyecto. 
3. Los diagramas de proceso y de infraestructura propuesta de diseño debeb estar embebidos en este readme en la sección de propuesta de diseño. Agregar descripciones necesarias para entender la solución.
4. Cuando tengas todo listo, mandar un Pull request a este repositorio con el siguiente formato `Ml Engineer: {tu-nombre}` y agregar en la descripción las limitantes o faltantes de tu examen de existir :)

Si existen dudas o problemas

# Propuesta de diseño

# Contacto
Cualquier duda enviar un email a f.vaquero@opianalytics.com copiando al contacto de RH que esta llevando tu proceso de contratación. 