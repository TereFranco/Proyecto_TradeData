import os
import pandas as pd

def preprocess_and_split_by_sets_of_years(csv_folder):
    # Crear una carpeta "preprocessed_data" si no existe
    output_folder = "preprocessed_data"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Listar todos los archivos CSV en la carpeta dada
    files = [f for f in os.listdir(csv_folder) if f.endswith(".csv")]
    
    for file in files:
        # Obtener el nombre de la criptomoneda (ej. BTCUSD) y eliminar "USD"
        crypto_name = file.split(".")[0].replace("USD_daily_data", "")  # Eliminar "USD" del nombre
        file_path = os.path.join(csv_folder, file)

        # Cargar los datos
        print(f"Procesando datos de {crypto_name}...")
        df = pd.read_csv(file_path, parse_dates=["datetime"], index_col="datetime")
        
        # Preprocesar los datos: eliminar valores nulos y duplicados
        df = df.dropna()  # Eliminar filas con valores nulos
        df = df.drop_duplicates()  # Eliminar filas duplicadas

        # Crear una subcarpeta para cada criptomoneda si no existe
        crypto_folder = os.path.join(output_folder, crypto_name)
        if not os.path.exists(crypto_folder):
            os.makedirs(crypto_folder)

        # Crear intervalos de 1 año (enero - diciembre)
        start_year = df.index.year.min()  # Año inicial (primer año en los datos)
        end_year = df.index.year.max()   # Año final (último año en los datos)

        # Iterar a través de los intervalos año a año
        for year in range(start_year, end_year + 1):
            # Definir el inicio y el final del intervalo (enero a diciembre)
            start_date = pd.Timestamp(f"{year}-02-13")
            end_date = pd.Timestamp(f"{year+1}-02-12")

            # Filtrar los datos para el intervalo actual (enero - diciembre)
            year_data = df[(df.index >= start_date) & (df.index <= end_date)]

            # Verificar si hay datos en el intervalo
            if not year_data.empty:
                # Definir el nombre del archivo CSV para este año
                csv_filename = f"{crypto_name}_{year}.csv"
                csv_filepath = os.path.join(crypto_folder, csv_filename)

                # Guardar los datos filtrados para este año
                year_data.to_csv(csv_filepath)
                print(f"Datos de {crypto_name} para el año {year} guardados en {csv_filepath}")

if __name__ == "__main__":
    # Carpeta donde se encuentran los archivos CSV originales
    csv_folder = "crypto_data"  # Cambia este valor según tu carpeta de entrada
    preprocess_and_split_by_sets_of_years(csv_folder)