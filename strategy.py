import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Symbol mapping for better compatibility
SYMBOL_MAP = {
    'NAS100': '^NDX',  # NASDAQ-100 Index
    'XAUUSD': 'GC=F',  # Gold Futures
    'GBPUSD': 'GBPUSD=X'  # GBP/USD Forex pair
}

def fetch_data(ticker):
    try:
        # Map the ticker to its Yahoo Finance equivalent if needed
        yahoo_ticker = SYMBOL_MAP.get(ticker, ticker)
        
        # Download data with progress bar disabled
        df = yf.download(yahoo_ticker, period="7d", interval="15m", progress=False)
        
        # Check for required columns
        required_columns = {'Open', 'High', 'Low', 'Close'}
        if df.empty:
            print(f"⚠️ No data returned for {ticker}")
            return pd.DataFrame()
            
        if not required_columns.issubset(df.columns):
            missing_cols = required_columns - set(df.columns)
            print(f"⚠️ Missing required price data columns for {ticker}: {missing_cols}")
            return pd.DataFrame()
            
        # Check for minimum data points
        if len(df) < 5:
            print(f"⚠️ Insufficient data points for {ticker}: {len(df)} points")
            return pd.DataFrame()
            
        return df
    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def find_zones(data):
    if data.empty:
        return pd.Series(), pd.Series()
    demand = data['Low'][data['Low'] == data['Low'].rolling(10).min()]
    supply = data['High'][data['High'] == data['High'].rolling(10).max()]
    return supply.dropna(), demand.dropna()

def detect_sr(data):
    levels = []
    if len(data) < 5:
        print("⚠️ Not enough data points to detect support/resistance levels")
        return levels

    for i in range(2, len(data)-2):
        try:
            if data['Low'][i] < data['Low'][i-1] and data['Low'][i] < data['Low'][i+1]:
                levels.append(data['Low'][i])
            elif data['High'][i] > data['High'][i-1] and data['High'][i] > data['High'][i+1]:
                levels.append(data['High'][i])
        except KeyError:
            print("⚠️ Missing required price data columns")
            continue
        except Exception as e:
            print(f"⚠️ Error processing data point: {e}")
            continue

    return levels

def generate_chart(data, supply, demand, levels, name):
    if data.empty:
        print(f"⚠️ Cannot generate chart for {name}: No data available")
        return None
        
    plt.figure(figsize=(14, 6))
    plt.plot(data['Close'], label="Close Price", color="black")
    for s in supply:
        plt.axhline(s, color='red', linestyle='--', alpha=0.5)
    for d in demand:
        plt.axhline(d, color='green', linestyle='--', alpha=0.5)
    for lvl in levels:
        plt.axhline(lvl, color='blue', linestyle=':', alpha=0.3)
    plt.title(f"{name} - Supply & Demand + S/R")
    plt.legend()
    filename = f"{name.lower()}_chart.png"
    plt.savefig(filename)
    plt.close()
    return filename

def analyze_symbol(name, ticker):
    data = fetch_data(ticker)
    if data.empty:
        return None, None
        
    # Additional validation for required columns
    if not {'High', 'Low', 'Close'}.issubset(data.columns):
        print(f"⚠️ Missing required price data columns for {ticker}")
        return None, None
        
    supply, demand = find_zones(data)
    levels = detect_sr(data)
    
    if supply.empty and demand.empty and not levels:
        print(f"⚠️ No trading signals found for {name}")
        return None, None
        
    chart = generate_chart(data, supply.values, demand.values, levels, name)
    if chart is None:
        return None, None
        
    latest = data['Close'].iloc[-1]
    sl = latest - 100
    tp = latest + 150
    signal = f"📊 *{name} Signal*\n\nEntry: {latest:.2f}\nSL: {sl:.2f}\nTP: {tp:.2f}"
    return signal, chart
