import boto3

# Configuración AWS
aws_region = "eu-south-2"  # Cambia según tu región
database_name = "trade_data_imat3a08"  # Nombre de la base de datos en Glue
crawler_name = "crypto_trade_data_crawler"  # Nombre del Crawler
role_arn = "arn:aws:iam::043309335245:role/service-role/AWSGlueServiceRole-workshop"  # ARN de IAM Role

# Lista de criptomonedas y años a procesar
cryptos = ["AAVE", "ADA", "BTC", "DOGE", "DOT", "ETH", "SHIB", "SOL", "XLM", "XRP"]  # Agrega más si es necesario
years = ["2021-2022", "2022-2023", "2023-2024", "2024-2025"]  # Asegúrate de incluir todos los años que necesites

# Inicializar el cliente de AWS Glue
glue_client = boto3.client("glue", region_name=aws_region)

def create_database():
    """Crea la base de datos en AWS Glue si no existe."""
    try:
        glue_client.create_database(
            DatabaseInput={"Name": database_name, "Description": "Base de datos para trade data"}
        )
        print(f"Base de datos '{database_name}' creada exitosamente.")
    except glue_client.exceptions.AlreadyExistsException:
        print(f"La base de datos '{database_name}' ya existe.")

def create_crawlers():
    """Crea un Crawler diferente para cada criptomoneda y año."""
    for crypto in cryptos:
        for year in years:
            crawler_name = f"crawler_{crypto}_{year}"
            s3_target_path = f"s3://crypto-data-fd7f0498/{crypto}/{year}/"

            try:
                glue_client.create_crawler(
                    Name=crawler_name,
                    Role=role_arn,
                    DatabaseName=database_name,
                    Targets={"S3Targets": [{"Path": s3_target_path}]},
                    TablePrefix=f"{crypto}_{year}_",  # Prefijo para diferenciar cada tabla
                    Description=f"Crawler para {crypto} en el año {year}",
                    Schedule="cron(0 12 * * ? *)",  # Corre diariamente a las 12 PM
                    SchemaChangePolicy={"UpdateBehavior": "UPDATE_IN_DATABASE", "DeleteBehavior": "LOG"},
                    Configuration='{"Version":1.0,"Grouping":{"TableLevelConfiguration":3}}'
                )
                print(f"Crawler '{crawler_name}' creado exitosamente para {crypto} en {year}.")
            except glue_client.exceptions.AlreadyExistsException:
                print(f"El Crawler '{crawler_name}' ya existe.")

def start_crawlers():
    """Ejecuta cada uno de los crawlers creados."""
    for crypto in cryptos:
        for year in years:
            crawler_name = f"crawler_{crypto}_{year}"
            try:
                glue_client.start_crawler(Name=crawler_name)
                print(f"Crawler '{crawler_name}' iniciado para {crypto} en {year}.")
            except Exception as e:
                print(f"Error al iniciar el crawler '{crawler_name}': {e}")

# Ejecutar funciones
if __name__ == "__main__":
    create_database()
    create_crawlers()
    start_crawlers()
