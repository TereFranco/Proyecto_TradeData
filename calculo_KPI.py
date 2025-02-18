import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, lit, lag, when, sum
from pyspark.sql.window import Window

# Configurar el contexto de Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init("TechnicalIndicatorsCalculation")

# Definir los buckets de origen y destino
bucket_plata = "s3://crypto-data-plata/"
bucket_oro = "s3://crypto-data-oro/"

# Lista de criptomonedas (las carpetas dentro del bucket)
criptos = ["AAVE", "ADA", "BTC", "DOGE", "DOT", "ETH", "SHIB", "SOL", "XLM", "XRP"]

# Definir las ventanas para los indicadores
WINDOW_SMA = 14
WINDOW_EMA = 14
WINDOW_RSI = 14
WINDOW_MACD_FAST = 12
WINDOW_MACD_SLOW = 26
WINDOW_MACD_SIGNAL = 9

# Función para calcular el EMA
def calculate_ema(df, column, window):
    alpha = 2 / (window + 1)
    return df.withColumn(f"EMA_{window}", col(column) * alpha + lag(f"EMA_{window}", 1).over(Window.orderBy("datetime")) * (1 - alpha))

# Procesar cada criptomoneda
for cripto in criptos:
    ruta_origen = f"{bucket_plata}{cripto}/"
    ruta_destino = f"{bucket_oro}{cripto}/"

    print(f"Procesando: {cripto}")

    # Leer los datos desde la capa Plata
    df = spark.read.parquet(ruta_origen)

    # Calcular SMA (Media Móvil Simple)
    df = df.withColumn(f"SMA_{WINDOW_SMA}", avg("close").over(Window.orderBy("datetime").rowsBetween(-WINDOW_SMA, 0)))

    # Calcular EMA
    df = calculate_ema(df, "close", WINDOW_EMA)

    # Calcular RSI (Relative Strength Index)
    df = df.withColumn("diff", col("close") - lag("close", 1).over(Window.orderBy("datetime")))
    df = df.withColumn("gain", when(col("diff") > 0, col("diff")).otherwise(0))
    df = df.withColumn("loss", when(col("diff") < 0, -col("diff")).otherwise(0))

    df = df.withColumn("avg_gain", sum("gain").over(Window.orderBy("datetime").rowsBetween(-WINDOW_RSI, 0)) / WINDOW_RSI)
    df = df.withColumn("avg_loss", sum("loss").over(Window.orderBy("datetime").rowsBetween(-WINDOW_RSI, 0)) / WINDOW_RSI)

    df = df.withColumn("RS", col("avg_gain") / col("avg_loss"))
    df = df.withColumn("RSI", 100 - (100 / (1 + col("RS"))))

    # Calcular MACD
    df = calculate_ema(df, "close", WINDOW_MACD_FAST)
    df = calculate_ema(df, "close", WINDOW_MACD_SLOW)
    df = df.withColumn("MACD", col(f"EMA_{WINDOW_MACD_FAST}") - col(f"EMA_{WINDOW_MACD_SLOW}"))

    df = calculate_ema(df, "MACD", WINDOW_MACD_SIGNAL)
    df = df.withColumn("MACD_Signal", col(f"EMA_{WINDOW_MACD_SIGNAL}"))

    # Guardar en formato Parquet en la capa Oro
    df.write.mode("overwrite").parquet(ruta_destino)

print("Cálculo de indicadores completado.")

# Finalizar el Job
job.commit()