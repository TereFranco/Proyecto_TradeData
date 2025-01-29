import os
import pandas as pd

def analyze_data(csv_folder):
    files = [f for f in os.listdir(csv_folder) if f.endswith(".csv")]
    
    # Crear un archivo de reporte
    with open("data_analysis_report.txt", "w") as report:
        for file in files:
            crypto_name = file.split("_")[0]  # Obtener el nombre del activo
            file_path = os.path.join(csv_folder, file)
            df = pd.read_csv(file_path, parse_dates=["datetime"], index_col="datetime")
            
            # Información general del DataFrame
            report.write(f"Analisis de datos para {crypto_name}:\n")
            report.write(f"-------------------------------------------------\n")
            
            # Resumen de estadísticas descriptivas
            report.write(f"Estadisticas descriptivas:\n{df.describe()}\n\n")
            
            # Resumen de los tipos de datos
            report.write(f"Tipos de datos:\n{df.dtypes}\n\n")
            
            # Conteo de valores nulos por columna
            report.write(f"Conteo de valores nulos:\n{df.isnull().sum()}\n\n")
            
            # Verificar la existencia de duplicados
            duplicated_rows = df[df.duplicated()]
            report.write(f"Numero de filas duplicadas: {len(duplicated_rows)}\n\n")
            
            # Correlación entre variables numéricas (excluir columnas no numéricas)
            numeric_df = df.select_dtypes(include=['number'])  # Seleccionar solo columnas numéricas
            if not numeric_df.empty:
                corr_matrix = numeric_df.corr()
                report.write(f"Correlaciones entre variables numericas:\n{corr_matrix}\n\n")
            else:
                report.write("No hay columnas numéricas para calcular correlaciones.\n\n")
            
            # Espacio vacío entre criptomonedas
            report.write(f"\n\n{'='*50}\n\n")

if __name__ == "__main__":
    analyze_data("crypto_data")
