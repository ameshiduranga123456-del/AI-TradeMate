import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="Signal Dashboard", layout="wide")

st.title("📊 Live Market Signal Monitor")

# සිග්නල් හිස්ට්‍රි එක තියාගන්න
if 'history' not in st.session_state:
    st.session_state.history = []

assets = {"USDJPY=X": 15, "AUDUSD=X": 15, "NZDUSD=X": 15}

placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader("Market Status & Signals")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        for symbol, window in assets.items():
            df = yf.download(symbol, period="1d", interval="1m", progress=False)
            
            if df.empty:
                continue
            
            current_price = df['Close'].iloc[-1].item()
            ma = df['Close'].rolling(window=window).mean().iloc[-1].item()
            diff = abs(current_price - ma)
            threshold = current_price * 0.0002
            
            if diff < threshold:
                msg = f"🚨 ALERT: {symbol} | [SIGNAL READY] | Time: {current_time} | Price: {current_price:.4f}"
                st.error(msg)
                st.session_state.history.append(msg) # සිග්නල් එක History එකට දාන්න
            else:
                trend = "BUY" if current_price > ma else "SELL"
                st.success(f"✅ {symbol} | Trend: {trend} | Price: {current_price:.4f}")
        
        # පරණ සිග්නල් ටික පහළින් පෙන්වීම
        st.write("---")
        st.subheader("Signal History (Last few alerts)")
        for log in reversed(st.session_state.history[-5:]): # අන්තිම සිග්නල් 5
            st.text(log)
            
        st.caption(f"Last updated: {current_time}")

    time.sleep(5)
