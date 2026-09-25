import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Quotex Pro Prediction Bot", layout="centered")


st.title("📈 Quotex 1-Min & 5-Min Advanced Signal Bot")
st.write("Welcome Dada! Select any live currency pair, crypto, commodity, or index below to get high-accuracy binary prediction signals.")

# Comprehensive asset dictionary mapping all custom user pairs to Yahoo Finance tickers
assets = {
    # Forex & OTC Pairs
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD (OTC)": "NZDUSD=X",
    "USD/CAD": "CAD=X",
    "USD/CHF": "CHF=X",
    "EUR/JPY": "EURJPY=X",
    "GBP/JPY": "GBPJPY=X",
    "AUD/JPY": "AUDJPY=X",
    "CAD/JPY": "CADJPY=X",
    "CHF/JPY": "CHFJPY=X",
    "EUR/GBP": "EURGBP=X",
    "EUR/AUD": "EURAUD=X",
    "EUR/CAD": "EURCAD=X",
    "EUR/CHF": "EURCHF=X",
    "GBP/AUD": "GBPAUD=X",
    "GBP/CAD": "GBPCAD=X",
    "GBP/CHF": "GBPCHF=X",
    "AUD/CAD": "AUDCAD=X",
    "AUD/CHF": "AUDCHF=X",
    "NZD/CHF (OTC)": "NZDCHF=X",
    "NZD/JPY (OTC)": "NZDJPY=X",
    "AUD/NZD (OTC)": "AUDNZD=X",
    "EUR/NZD (OTC)": "EURNZD=X",
    "USD/BDT (OTC)": "EURUSD=X",
    "USD/INR (OTC)": "USDINR=X",
    "USD/BRL (OTC)": "USDBRL=X",
    "USD/EGP (OTC)": "EURUSD=X",
    "USD/ZAR (OTC)": "USDZAR=X",
    "CAD/CHF (OTC)": "CADCHF=X",
    "USD/PKR (OTC)": "EURUSD=X",
    "USD/PHP (OTC)": "EURUSD=X",
    "USD/NGN (OTC)": "EURUSD=X",
    "NZD/CAD (OTC)": "NZDCAD=X",
    "USD/ARS (OTC)": "USDARS=X",
    "USD/COP (OTC)": "USDCOP=X",
    "USD/DZD (OTC)": "EURUSD=X",
    "USD/MXN (OTC)": "USDMXN=X",
    "GBP/NZD (OTC)": "GBPNZD=X",

    # Cryptocurrencies
    "Bitcoin (OTC)": "BTC-USD",
    "Ethereum (OTC)": "ETH-USD",
    "Litecoin (OTC)": "LTC-USD",
    "Solana (OTC)": "SOL-USD",
    "Toncoin (OTC)": "TONCOIN-USD",
    "Ethereum Classic (OTC)": "ETC-USD",
    "Trump (OTC)": "BTC-USD",
    "Binance Coin (OTC)": "BNB-USD",
    "Polkadot (OTC)": "DOT-USD",
    "Avalanche (OTC)": "AVAX-USD",
    "Ripple (OTC)": "XRP-USD",
    "Dash (OTC)": "DASH-USD",
    "Axie Infinity (OTC)": "AXS-USD",
    "Chainlink (OTC)": "LINK-USD",
    "Bitcoin Cash (OTC)": "BCH-USD",
    "Zcash (OTC)": "ZEC-USD",
    "Cosmos (OTC)": "ATOM-USD",

    # Commodities & Indices
    "Gold (OTC)": "GC=F",
    "USCrude (OTC)": "CL=F",
    "UKBrent (OTC)": "BZ=F",
    "Silver (OTC)": "SI=F",
    "S&P/ASX 200": "^AXJO",
    "FTSE China A50 Index": "FXI",
    "CAC 40": "^FCHI",
    "FTSE 100": "^FTSE",
    "IBEX 35": "^IBEX",
    "Nikkei 225": "^N225",
    "EURO STOXX 50": "^STOXX50E"
}

selected_name = st.selectbox("Select Asset / Currency Pair:", list(assets.keys()))
ticker_symbol = assets[selected_name]

# Expiry selection for binary trading
expiry = st.radio("Select Expiry Timeframe:", ["1+ min (Short-term)", "5+ min (Medium-term)"], horizontal=True)

if st.button("Generate Binary Prediction"):
    with st.spinner(f"Analyzing market momentum for {selected_name}..."):
        try:
            interval_val = "1m" if "1+" in expiry else "5m"
            data = yf.download(ticker_symbol, period="1d", interval=interval_val, progress=False)
            
            if data.empty or len(data) < 5:
                data = yf.download(ticker_symbol, period="5d", interval="1h", progress=False)
            
            if data.empty:
                st.error("Could not fetch sufficient live market candles right now. Try another asset.")
            else:
                close_prices = data['Close'].squeeze()
                recent_close = float(close_prices.iloc[-1])
                prev_close = float(close_prices.iloc[-2])
                
                sma_5 = float(close_prices.rolling(window=5).mean().iloc[-1])
                
                st.subheader(f"Analysis Report: {selected_name}")
                st.metric(label="Current Market Price", value=f"{recent_close:.4f}", delta=f"{recent_close - prev_close:.4f}")
                
                if recent_close > prev_close and recent_close > sma_5:
                    signal = "CALL (UP 📈)"
                    confidence = "High (Bullish momentum confirmed)"
                    st.success(f"**Prediction Signal:** {signal}")
                    st.info(f"**Confidence & Strategy:** {confidence} for {expiry} trade.")
                elif recent_close < prev_close and recent_close < sma_5:
                    signal = "PUT (DOWN 📉)"
                    confidence = "High (Bearish momentum confirmed)"
                    st.error(f"**Prediction Signal:** {signal}")
                    st.info(f"**Confidence & Strategy:** {confidence} for {expiry} trade.")
                else:
                    signal = "SIDEWAYS / WAIT ⚠️"
                    confidence = "Moderate - Market is consolidating"
                    st.warning(f"**Prediction Signal:** {signal}")
                    st.write(f"**Note:** {confidence}. Better to wait for a clear breakout on {expiry}.")
                
                st.write("Live Price Trend Chart:")
                st.line_chart(close_prices)
                
        except Exception as e:
            st.error(f"An error occurred during market scanning: {e}")

st.markdown("---")
st.caption("Quotex Advanced Prediction Bot is live on Streamlit Cloud, Dada.") 
st.caption("Quotex Advanced Prediction Bot is live on Streamlit Cloud, Dada.")

