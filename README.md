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
```

### Estructura del Repositorio
/Crypto-Data-Extractor

│── crypto_data/              # Archivos CSV con los datos históricos  

│── crypto_visual/            # Imágenes para la visualización de cada moneda
│   ├── AAVEUSD.csv           # Datos históricos de AAVE/USD  
│   ├── ADAUSD.csv            # Datos históricos de ADA/USD  
│   ├── BTCUSD.csv            # Datos históricos de BTC/USD  
│   ├── DOGEUSD.csv           # Datos históricos de DOGE/USD  
│   ├── DOTUSD.csv            # Datos históricos de DOT/USD  
│   ├── ETHUSD.csv            # Datos históricos de ETH/USD  
│   ├── SHIBUSD.csv           # Datos históricos de SHIB/USD  
│   ├── SOLUSD.csv            # Datos históricos de SOL/USD  
│   ├── XLMUSD.csv            # Datos históricos de XLM/USD  
│   └── XRPUSD.csv            # Datos históricos de XRP/USD  

│── docs/                     # Docuentación de la práctica

│   ├── Documentation Proyecto.docx  # Documentación del proyecto  
│   ├── Historias Usuario.pdf     # Historias de usuario  
│   ├── Proyecto Tecnologías Processament...  # Documentación técnica  

│── preprocessed_data/        # Datos preprocesados sin nulos, duplicados... y separados anualmente

│── TradingviewData/          # Librería para acceder a TradingView  

│── DataExtractor.py          # Script principal para extraer datos  
│── DataPreprocess.py         # Script para preprocesar datos  
│── GraphicData.py            # Script para generar gráficos  
│── ObtainDataReport.py       # Script para generar reportes  
│── README.md                 # Este archivo  
│── data_analysis_report.txt  # Reporte de análisis de datos  
