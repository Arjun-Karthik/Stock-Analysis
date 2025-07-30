# 📈 Stock-Analysis

## ⚙️ Workflow
1. Data Ingestion

   - Initially, stock data was collected in YAML format. 
   - Converted YAML to CSV using Python for easier tabular analysis.

2. Data Cleaning & Feature Engineering
   
      - Parsed and converted date column to datetime.
      - Ensured numeric types for open, close, high, low, volume.
      Calculated:
        - Daily Return = (Close - Open) / Open
        - Cumulative Return
        - Volatility (std dev of daily returns)
        - Resampled data monthly for trend analysis.
        - Removed duplicates, handled nulls, normalized volume.

3. Streamlit Dashboard
   
      - Upload nifty_data.csv in the app.
      Filter by:
        - Stock ticker
        - Date range
      Explore:
        - Cumulative Return Over Time
        - Daily Return Trends
        - Top 5 Gainers/Losers (Monthly & Yearly)
        - Volatility & Correlation Heatmap
      - Download filtered dataset as CSV.
  
4. Power BI Dashboard
   
      - Integrated visuals:
          - Sector-wise monthly return breakdown
          - Monthly Gainers and Losers (Top 5/Bottom 5)
          - Heatmap: Monthly performance comparison
          - Average volume and price charts
      - Interactive slicers by month, symbol, and sector.
  
## ▶️ Running the App

Ensure Python 3.8+ is installed.

1. Clone the repo:
   
       https://github.com/Arjun-Karthik/Stock-Analysis
       cd Stock-Analysis

2.Install dependencies

       pip install -r requirements.txt

3. Run Streamlit app

       streamlit run app.py

4. Upload the CSV file (Stock Market Data.csv) when prompted in the app.

## 🧩 Features

  - YAML to CSV conversion pipeline
  - Interactive stock performance visualizations
  - Correlation matrix and volatility insights
  - Monthly stock gainers/losers (Power BI + Plotly)
  - Download cleaned/filtered stock data
  - Price and volume comparison for all Nifty 50 stocks
  - Helps analysts and investors make better decisions

## ✅ Requirements

   - streamlit
   - pandas
   - plotly
   - matplotlib
   - seaborn

Install all with:

       pip install -r requirements.txt

## 📸 Screenshots

### 📊 Top 10 Most Volatile Stocks and 📈 Cumulative Return Over Time

<img src="Screenshots/Bar and Line Chart.png" width="800"/>

### 📊 Sector-wise Performance

<img src="Screenshots/Bar Chart.png" width="800"/>

## 🎥 Demo Video

   <a href="[https://www.linkedin.com/posts/arjun-t-a51383200_imdb-movie-dashboard-app-activity-7348370456242003969-Nd0G?utm_source=share&utm_medium=member_desktop&rcm=ACoAADNQBh0BQsEphYCjQb01l17Z8-pUyINZuxs](https://www.linkedin.com/posts/arjun-t-a51383200_stock-performance-dashboard-visualization-activity-7356235958826012672-QRSc?utm_source=share&utm_medium=member_desktop&rcm=ACoAADNQBh0BQsEphYCjQb01l17Z8-pUyINZuxs)">Stock Performance Dashboard Demo Video</a>

## 📃 License

   This project is licensed under the MIT License – see the LICENSE file for details.
