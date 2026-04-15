# Stock Analysis Pro 📈

A comprehensive data-driven stock analysis application built with Python and Streamlit. Organize, clean, and visualize market trends for NIFTY 50 stocks with an intuitive dashboard and multiple analytical tools.

## 🎯 Features

- **Data Processing & Cleaning**: Convert and preprocess raw stock market data
- **Interactive Dashboard**: Real-time visualizations of stock performance
- **Volatility Analysis**: Analyze price volatility patterns and trends
- **Cumulative Returns**: Track cumulative returns over time
- **Sector Performance**: Compare performance across different market sectors
- **Stock Price Correlation**: Understand relationships between different stocks
- **Top Gainers & Losers**: Identify best and worst performing stocks
- **MySQL Database Integration**: Persistent data storage and retrieval

## 📁 Project Structure

```
stockprice/
├── Home.py                          # Main landing page (Streamlit)
├── pages/
│   ├── 1_Processing.py             # Data processing and cleaning
│   ├── 2_Dashboard.py              # Interactive stock dashboard
│   ├── 3_VolatilityAnalysis.py     # Volatility metrics and analysis
│   ├── 4_Cumulativereturn.py       # Cumulative returns visualization
│   ├── 5_SectorPerformance.py      # Sector-wise performance
│   ├── 6_StockPriceCorrelation.py  # Correlation analysis
│   └── 7_Top5Gainers&Losers.py     # Top performers identification
├── ticker_data/                    # Individual stock CSV files
│   ├── ADANIENT.csv, ADANIPORTS.csv, ...
│   └── (40+ NIFTY 50 stocks)
├── config.py                       # Database configuration
├── database.py                     # Database operations manager
├── conversion.ipynb                # Data conversion notebook
├── FullData.csv                    # Consolidated full dataset
├── SectorData.csv                  # Sector-wise data
└── stockprice.avif                 # Application logo/image
```

## 🛠️ Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stockprice
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database connection**
   - Open `config.py`
   - Update MySQL connection details:
     ```python
     class ConnectionInfo:
         HOST = "your_host"
         USER = "your_user"
         PASSWORD = "your_password"
         DATABASE = "stockprice"
         PORT = "3306"
     ```

5. **Set up MySQL database**
   - Create a database named `stockprice`
   - Run data processing page to load data into MySQL

## 🚀 Usage

### Run the Streamlit Application
```bash
streamlit run Home.py
```

The application will open in your default browser at `http://localhost:8501`

### Navigation

- **Home**: Overview and introduction to the analysis platform
- **Processing**: Import, clean, and prepare stock data
- **Dashboard**: View overall market trends and individual stock performance
- **Volatility Analysis**: Examine price volatility metrics
- **Cumulative Return**: Track investment performance over time
- **Sector Performance**: Analyze sector-wise market movements
- **Stock Price Correlation**: Identify correlated stocks for portfolio building
- **Top 5 Gainers & Losers**: Monitor best and worst performers

## 📊 Data Sources

The project includes historical price data for 40+ NIFTY 50 stocks including:
- ADANIENT, ADANIPORTS, APOLLOHOSP, ASIANPAINT, AXISBANK
- BAJAJ-AUTO, BAJAJFINSV, BAJFINANCE, BHARTIARTL, CIPLA
- HDFCBANK, ICICIBANK, INFY, ITC, KOTAKBANK
- RELIANCE, TCS, WIPRO, and 20+ more...

## 🔧 Key Technologies

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **MySQL**: Database backend
- **SQLAlchemy**: ORM for database operations
- **NumPy**: Numerical computations
- **Plotly/Matplotlib**: Data visualization

## 📝 Configuration

Edit `config.py` to customize:
- Database host and credentials
- Database name and port
- Connection parameters

## 🤝 Contributing

Contributions are welcome! Please feel free to fork the project and submit pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Created by Tharaniya VM

## 📞 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Last Updated**: April 2026
