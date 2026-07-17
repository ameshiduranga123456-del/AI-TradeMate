import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

# config.yaml එක Load කිරීම
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # --- Dashboard කොටස ---
    st.title("📊 Live Market Signal Monitor")
    authenticator.logout('Logout', 'sidebar')
    
    if 'history' not in st.session_state:
        st.session_state.history = []

    assets = {"USDJPY=X": 15, "AUDUSD=X": 15, "NZDUSD=X": 15}
    placeholder = st.empty()

    while True:
        with placeholder.container():
            st.subheader("Market Status")
            current_time = datetime.now().strftime("%H:%M:%S")
            
            for symbol, window in assets.items():
                df = yf.download(symbol, period="1d", interval="1m", progress=False)
                if df.empty: continue
                
                current_price = df['Close'].iloc[-1].item()
                ma = df['Close'].rolling(window=window).mean().iloc[-1].item()
                diff = abs(current_price - ma)
                threshold = current_price * 0.0002
                
                if diff < threshold:
                    msg = f"🚨 ALERT: {symbol} | [SIGNAL] | {current_time} | Price: {current_price:.4f}"
                    st.error(msg)
                    st.session_state.history.append(msg)
                else:
                    trend = "BUY" if current_price > ma else "SELL"
                    st.success(f"✅ {symbol} | Trend: {trend} | Price: {current_price:.4f}")
            
            st.write("---")
            st.subheader("Signal History")
            for log in reversed(st.session_state.history[-5:]):
                st.text(log)
            st.caption(f"Last updated: {current_time}")
        time.sleep(5)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
