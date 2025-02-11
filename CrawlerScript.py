import boto3

# Configuración AWS
aws_region = "eu-south-2"  # Cambia según tu región
database_name = "trade_data_imat3a08"  # Nombre de la base de datos en Glue
role_arn = "arn:aws:iam::043309335245:role/service-role/AWSGlueServiceRole-workshop"  # ARN de IAM Role
bucket_name = "crypto-data-4e822955"  # Nombre del bucket de S3

# Lista de criptomonedas a procesar
cryptos = ["AAVE", "ADA", "BTC", "DOGE", "DOT", "ETH", "SHIB", "SOL", "XLM", "XRP"]  # Agrega más si es necesario

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
    """Crea un único Crawler por cada criptomoneda apuntando a la carpeta correcta en S3."""
    existing_crawlers = glue_client.get_crawlers()["Crawlers"]  # Obtener lista de crawlers existentes
    existing_crawler_names = {crawler["Name"] for crawler in existing_crawlers}  # Guardar nombres de crawlers existentes

    for crypto in cryptos:
        crawler_name = f"crawler_{crypto}"
        s3_target_path = f"s3://{bucket_name}/{crypto}/"  # Carpeta donde están los CSV preprocesados
        
        if crawler_name in existing_crawler_names:
            print(f"El Crawler '{crawler_name}' ya existe, saltando creación.")
            continue

        try:
            glue_client.create_crawler(
                Name=crawler_name,
                Role=role_arn,
                DatabaseName=database_name,
                Targets={"S3Targets": [{"Path": s3_target_path}]},
                TablePrefix=f"trade_data_",  # Prefijo actualizado para incluir "trade_data_"
                Description=f"Crawler para datos preprocesados de {crypto}",
                Schedule="cron(0 12 * * ? *)",  # Corre diariamente a las 12 PM
                SchemaChangePolicy={"UpdateBehavior": "UPDATE_IN_DATABASE", "DeleteBehavior": "LOG"},
                Configuration='{"Version":1.0,"Grouping":{"TableLevelConfiguration":3}}'
            )
            print(f"Crawler '{crawler_name}' creado exitosamente para {crypto}.")
        except Exception as e:
            print(f"Error al crear el crawler '{crawler_name}': {e}")

def start_crawlers():
    """Ejecuta cada uno de los crawlers creados."""
    for crypto in cryptos:
        crawler_name = f"crawler_{crypto}"
        try:
            glue_client.start_crawler(Name=crawler_name)
            print(f"Crawler '{crawler_name}' iniciado para {crypto}.")
        except Exception as e:
            print(f"Error al iniciar el crawler '{crawler_name}': {e}")

# Ejecutar funciones
if __name__ == "__main__":
    create_database()
    create_crawlers()
    start_crawlers()

