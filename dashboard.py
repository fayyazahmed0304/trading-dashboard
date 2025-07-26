import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import plotly.graph_objects as go

# ——— Sidebar Input
st.sidebar.title("Asset Selector")
ticker = st.sidebar.text_input("Enter Stock Symbol (e.g. AAPL, TSLA)", value="AAPL")

# ——— Fetch Data
data = yf.download(ticker, period="6mo", interval="1d")
st.title(f"{ticker} Dashboard")
st.write(data.tail())

# ——— Technical Indicators
data['EMA20'] = ta.trend.ema_indicator(data['Close'], window=20)
data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
macd = ta.trend.macd(data['Close'])
data['MACD'] = macd.macd_diff()

# ——— Chart
fig = go.Figure()
fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'],
                name='Price'))
fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], line=dict(color='orange'), name='EMA20'))
st.plotly_chart(fig)

# ——— Technical Summary
st.subheader("Technical Indicators")
st.metric("Latest RSI", round(data['RSI'].iloc[-1], 2))
st.metric("Latest MACD", round(data['MACD'].iloc[-1], 2))

# ——— Fundamentals
st.subheader("Basic Fundamentals")
stock = yf.Ticker(ticker)
info = stock.info

st.write({
    "P/E Ratio": info.get("trailingPE"),
    "EPS": info.get("trailingEps"),
    "Market Cap": info.get("marketCap"),
    "Dividend Yield": info.get("dividendYield"),
    "52 Week High": info.get("fiftyTwoWeekHigh"),
    "52 Week Low": info.get("fiftyTwoWeekLow"),
})
