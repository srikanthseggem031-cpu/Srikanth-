import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Quotex Advanced Signal Bot", page_icon="📈", layout="centered")

st.title("📈 Quotex 1-Min & 5-Min Advanced Signal Bot")
st.write("Real-time market analysis and prediction engine for binary options.")

# Comprehensive asset dictionary mapping real tickers and major pairs
assets = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "AUD/USD": "AUDUSD=X",
    "EUR/JPY": "EURJPY=X",
    "AUD/CAD": "AUDCAD=X",
    "EUR/CAD": "EURCAD=X",
    "EUR/GBP": "EURGBP=X",
    "CAD/JPY": "CADJPY=X",
    "USD/CAD": "USDCAD=X",
    "GBP/AUD": "GBPAUD=X",
    "GBP/JPY": "GBPJPY=X",
    "USD/CHF": "USDCHF=X",
    "CHF/JPY": "CHFJPY=X",
    "EUR/CHF": "EURCHF=X",
    "GBP/CHF": "GBPCHF=X",
    "Gold (OTC/Real)": "GC=F",
    "Ethereum": "ETH-USD",
    "Bitcoin": "BTC-USD",
    "Solana": "SOL-USD",
    "Litecoin": "LTC-USD"
}

selected_name = st.selectbox("Select Asset / Market", list(assets.keys()))
ticker_symbol = assets[selected_name]

expiry = st.radio("Select Expiry Timeframe", ["1-Min Expiry", "5-Min Expiry"])

if st.button("Generate Binary Prediction"):
    with st.spinner(f"Analyzing high-profit candles for {selected_name}..."):
        try:
            interval_val = "1m" if "1m" in expiry else "5m"
            data = yf.download(ticker_symbol, period="1d", interval=interval_val, progress=False)

            if data.empty or len(data) < 5:
                data = yf.download(ticker_symbol, period="5d", interval="1h", progress=False)

            if data.empty:
                st.error("Could not fetch candles for this market right now. Try another asset.")
            else:
                close_prices = data['Close'].squeeze()
                recent_close = float(close_prices.iloc[-1])
                prev_close = float(close_prices.iloc[-2])
                
                sma_5 = float(close_prices.rolling(window=5).mean().iloc[-1])

                st.subheader(f"Analysis Report: {selected_name}")
                st.metric(label="Current Market Price", value=f"{recent_close:.4f}", delta=f"{recent_close - prev_close:.4f}")

                if recent_close >= prev_close and recent_close >= sma_5:
                    signal = "CALL (UP) 🚀"
                    confidence = "High (Bullish momentum confirmed)"
                    st.success(f"### Prediction Signal: **{signal}**")
                    st.info(f"***Confidence & Strategy:** {confidence} for {expiry} trade.*")
                elif recent_close < prev_close and recent_close < sma_5:
                    signal = "PUT (DOWN) 🔻"
                    confidence = "High (Bearish momentum confirmed)"
                    st.error(f"### Prediction Signal: **{signal}**")
                    st.info(f"***Confidence & Strategy:** {confidence} for {expiry} trade.*")
                else:
                    signal = "SIDEWAYS / WAIT ⚠️"
                    confidence = "Moderate - Market is consolidating"
                    st.warning(f"### Prediction Signal: **{signal}**")
                    st.write(f"***Note:** {confidence}. Better to wait for a clear breakout on expiry.*")

                st.write("Live Price Trend Chart:")
                st.line_chart(close_prices)

        except Exception as e:
            st.error(f"An error occurred during market scanning: {e}")
            
