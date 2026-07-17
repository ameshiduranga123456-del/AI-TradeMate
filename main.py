import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="AI-TradeMate Dashboard", layout="wide")

st.title("📊 AI-TradeMate Live Signal Monitor")

assets = {"USDJPY=X": 15, "AUDUSD=X": 15, "NZDUSD=X": 15}

placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader("Market Status & Signals")
        
        current_time = datetime.now().strftime("%H:%M:%S")
        
        for symbol, window in assets.items():
            df = yf.download(symbol, period="1d", interval="1m", progress=False)
            
            if df.empty:
                st.warning(f"⚠️ {symbol}: දත්ත නොමැත / Inactive")
                continue
            
            current_price = df['Close'].iloc[-1].item()
            ma = df['Close'].rolling(window=window).mean().iloc[-1].item()
            
            # සිග්නල් වල ගුණාත්මකභාවය මැනීමට පරතරය ගණනය කිරීම
            diff = abs(current_price - ma)
            threshold = current_price * 0.0002
            
            # සිග්නල් පෙන්වීම
            if diff < threshold:
                st.error(f"🚨 ALERT: {symbol} | [SIGNAL READY] | Price: {current_price:.4f} | Diff: {diff:.5f}")
            else:
                trend = "BUY" if current_price > ma else "SELL"
                st.success(f"✅ {symbol} | Trend: {trend} | Price: {current_price:.4f} | Gap: {diff:.5f}")
        
        st.caption(f"Last updated: {current_time}")

    time.sleep(5)
