import boto3
import os
import uuid

# Configuración de AWS
AWS_REGION = "eu-south-2"
LOCAL_FOLDER = "preprocessed_data"  # Carpeta con los datos procesados

def create_s3_bucket():
    """Crea un bucket de S3 con un nombre único."""
    s3_client = boto3.client("s3", region_name=AWS_REGION)
    bucket_name = f"crypto-data-{uuid.uuid4().hex[:8]}"  # Nombre único
    
    s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': AWS_REGION})
    print(f"Bucket creado: {bucket_name}")
    return bucket_name

def upload_files_to_s3(bucket_name, local_folder):
    """Sube los archivos manteniendo la estructura de carpetas en S3."""
    s3_client = boto3.client("s3")

    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            s3_key = os.path.relpath(local_path, local_folder).replace("\\", "/")  # Convertir rutas para S3
            s3_client.upload_file(local_path, bucket_name, s3_key)
            print(f"Subido: {local_path} → s3://{bucket_name}/{s3_key}")

if __name__ == "__main__":
    bucket_name = create_s3_bucket()
    upload_files_to_s3(bucket_name, LOCAL_FOLDER)
    print(f"Todos los archivos han sido subidos a s3://{bucket_name}/")
