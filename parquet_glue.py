import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year

# Configurar el contexto de Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init("CSV_to_Parquet_Conversion") 

# Definir los buckets de origen y destino
bucket_bronce = "s3://crypto-data-4e822955/"
bucket_plata = "s3://crypto-data-plata/"

# Lista de criptomonedas (las carpetas dentro del bucket)
criptos = ["AAVE", "ADA", "BTC", "DOGE", "DOT", "ETH", "SHIB", "SOL", "XLM", "XRP"]

# Procesar cada criptomoneda
for cripto in criptos:
    ruta_origen = f"{bucket_bronce}{cripto}/"
    ruta_destino = f"{bucket_plata}{cripto}/"

    print(f"Procesando: {cripto}")

    # Leer los CSV en un DataFrame
    df = spark.read.option("header", "true").csv(ruta_origen)

    # Convertir tipos de datos
    df = (
        df.withColumn("datetime", col("datetime").cast("timestamp"))
          .withColumn("open", col("open").cast("double"))
          .withColumn("high", col("high").cast("double"))
          .withColumn("low", col("low").cast("double"))
          .withColumn("close", col("close").cast("double"))
    )

    # Particionar por símbolo y año para mejorar rendimiento
    df = df.withColumn("year", year(col("datetime")))

    # Guardar en formato Parquet en la capa Plata
    df.write.mode("overwrite").partitionBy("symbol", "year").parquet(ruta_destino)

print("Conversión completada.")

# Finalizar el job
job.commit()