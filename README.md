# 📈 Crypto Data Extractor  

Este proyecto permite obtener datos históricos de 10 criptomonedas utilizando la API de **TradingView**. Se recopilan datos con una frecuencia de **1 día** durante los últimos **4 años** y se almacenan en formato CSV.

## Historia de Usuario  

**Como:** Manager del proyecto  
**Quiero:**  
- Que las consultoras conozcan el proyecto.  
- Que comprendan el uso de **TradingView** para extraer datos históricos.  
- Que sepan cómo obtener datos de 10 criptomonedas.  

**Para:**  
- Garantizar un buen inicio del proyecto con acceso a datos históricos de calidad.

## Criptomonedas Incluidas  

| Nombre       | Símbolo  |
|-------------|---------|
| Bitcoin     | BTC     |
| Ethereum    | ETH     |
| Ripple      | XRP     |
| Solana      | SOL     |
| Dogecoin    | DOGE    |
| Cardano     | ADA     |
| Shiba Inu   | SHIB    |
| Polkadot    | DOT     |
| Aave        | AAVE    |
| Stellar     | XLM     | 

## Instalación y Uso  

### Requisitos  

Asegúrate de tener **Python 3.8+** y las siguientes librerías instaladas:  
```sh
pip install pandas websocket-client TradingviewData

### Estructura del Repositorio
/Crypto-Data-Extractor
│── crypto_data/              # Archivos CSV con los datos históricos  
│── TradingviewData/          # Librería para acceder a TradingView  
│── DataExtractor.py          # Script principal  
│── README.md                 # Este archivo  
