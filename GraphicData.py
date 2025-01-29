import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_crypto_data(csv_folder, output_folder):
    files = [f for f in os.listdir(csv_folder) if f.endswith(".csv")]
    
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file in files:
        crypto_name = file.split("_")[0]  # Obtener el nombre del activo
        file_path = os.path.join(csv_folder, file)
        df = pd.read_csv(file_path, parse_dates=["datetime"], index_col="datetime")
        
        # Crear subcarpeta para cada criptomoneda
        crypto_folder = os.path.join(output_folder, crypto_name)
        if not os.path.exists(crypto_folder):
            os.makedirs(crypto_folder)
        
        # Configurar estilo
        sns.set_style("darkgrid")
        
        # Gráfico de precio de cierre
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df["close"], label=f"{crypto_name} Close Price", color="blue")
        plt.title(f"Precio de Cierre de {crypto_name}")
        plt.xlabel("Fecha")
        plt.ylabel("Precio de Cierre (USD)")
        plt.legend()
        plt.xticks(rotation=45)
        
        # Guardar la imagen
        close_price_path = os.path.join(crypto_folder, f"{crypto_name}_close_price.png")
        plt.savefig(close_price_path)
        plt.close()  # Cerrar la figura para liberar memoria
        
        # Gráfico de velas (OHLC)
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df["high"], label="High", color="green", linestyle="dashed")
        plt.plot(df.index, df["low"], label="Low", color="red", linestyle="dashed")
        plt.fill_between(df.index, df["low"], df["high"], color='gray', alpha=0.3)
        plt.title(f"Rango de Precios de {crypto_name}")
        plt.xlabel("Fecha")
        plt.ylabel("Precio (USD)")
        plt.legend()
        plt.xticks(rotation=45)
        
        # Guardar la imagen
        ohlc_path = os.path.join(crypto_folder, f"{crypto_name}_ohlc.png")
        plt.savefig(ohlc_path)
        plt.close()  # Cerrar la figura para liberar memoria
        
        # Histograma de retornos diarios
        df["returns"] = df["close"].pct_change()
        plt.figure(figsize=(10, 5))
        sns.histplot(df["returns"].dropna(), bins=50, kde=True, color='purple')
        plt.title(f"Distribución de Retornos Diarios de {crypto_name}")
        plt.xlabel("Retorno Diario")
        plt.ylabel("Frecuencia")
        
        # Guardar la imagen
        returns_hist_path = os.path.join(crypto_folder, f"{crypto_name}_returns_hist.png")
        plt.savefig(returns_hist_path)
        plt.close()  # Cerrar la figura para liberar memoria
        
if __name__ == "__main__":
    plot_crypto_data("crypto_data", "crypto_visual")
