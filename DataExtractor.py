from TradingviewData import TradingViewData, Interval
import pandas as pd
import time
import os

# Definir las criptomonedas y los intervalos
cryptos = [
    {"symbol": "BTCUSD", "name": "Bitcoin"},
    {"symbol": "ETHUSD", "name": "Ethereum"},
    {"symbol": "XRPUSD", "name": "Ripple"},
    {"symbol": "SOLUSD", "name": "Solana"},
    {"symbol": "DOGEUSD", "name": "Dogecoin"},
    {"symbol": "ADAUSD", "name": "Cardano"},
    {"symbol": "SHIBUSD", "name": "Shiba Inu"},
    {"symbol": "DOTUSD", "name": "Polkadot"},
    {"symbol": "AAVEUSD", "name": "Aave"},
    {"symbol": "XLMUSD", "name": "Stellar"}
]

# Obtener y guardar los datos históricos
def fetch_and_save_data():
    # Hago la conexion con Trading para hacer requests
    request = TradingViewData()
    request.search('METAL')
    # Intervalo de 1 día
    interval = Interval.daily
    # 4 años
    time_requested = 365*4
    for crypto in cryptos:
        print(f"Obteniendo datos para {crypto['name']} ({crypto['symbol']})...")
        try:
            # Obtengo los datos históricos para la criptomoneda
            data = request.get_hist(
                symbol=crypto["symbol"],
                exchange="CRYPTO",  # Intercambio
                interval=interval,
                n_bars=time_requested
            )
            print(f"Datos obtenidos para {crypto['name']}: {data}")  # Imprimir datos para inspeccionar

            # Convierto los datos a un DataFrame
            df = pd.DataFrame(data)
            df.index = pd.to_datetime(df.index)  # Establecer el índice como datetime (ya viene en ese formato)

            # Guardar el DataFrame como un CSV en la carpeta 'crypto_data'
            folder_path = 'crypto_data'
            csv_path = os.path.join(folder_path, f"{crypto['symbol']}_daily_data.csv")

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            df.to_csv(csv_path, index=True) 
            print(f"Datos guardados en {csv_path} para {crypto['name']}")
 

        except Exception as e:
            print(f"Error obteniendo datos para {crypto['name']}: {e}")
        time.sleep(2) 

if __name__ == "__main__":
    fetch_and_save_data()