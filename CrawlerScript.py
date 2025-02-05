import boto3

# Configuración AWS
aws_region = "eu-south-2"  # Cambia según tu región
database_name = "trade_data_imat3a08"  # Nombre de la base de datos en Glue
crawler_name = "crypto_trade_data_crawler"  # Nombre del Crawler
s3_target_path = "s3://crypto-data-18b6b3f4/"  # Ruta S3 donde están los CSV
role_arn = "arn:aws:iam::043309335245:role/service-role/AWSGlueServiceRole-workshop"  # Cambia esto por tu ARN de IAM Role

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

def create_crawler():
    """Crea el AWS Glue Crawler para leer los archivos CSV organizados en S3."""
    try:
        glue_client.create_crawler(
            Name=crawler_name,
            Role=role_arn,
            DatabaseName=database_name,
            Targets={"S3Targets": [{"Path": s3_target_path}]},
            TablePrefix="trade_data_",  # Prefijo para las tablas
            Description="Crawler para datos de criptomonedas organizados por año",
            Schedule="cron(0 12 * * ? *)",  # Corre diariamente a las 12 PM (opcional)
            SchemaChangePolicy={"UpdateBehavior": "UPDATE_IN_DATABASE", "DeleteBehavior": "LOG"},
            Configuration='{"Version":1.0,"Grouping":{"TableLevelConfiguration":3}}'
        )
        print(f"Crawler '{crawler_name}' creado exitosamente.")
    except glue_client.exceptions.AlreadyExistsException:
        print(f"El Crawler '{crawler_name}' ya existe.")

def start_crawler():
    """Ejecuta el crawler para actualizar los metadatos en el catálogo."""
    try:
        glue_client.start_crawler(Name=crawler_name)
        print(f"Crawler '{crawler_name}' iniciado.")
    except Exception as e:
        print(f"Error al iniciar el crawler: {e}")

# Ejecutar funciones
if __name__ == "__main__":
    create_database()
    create_crawler()
    start_crawler()

