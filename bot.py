import requests, time
import pandas as pd
from datetime import datetime
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

TOKEN = "8415329017:AAHiQZhJ8UA9SYGKTS4ajgQdGb9yfGM9N6Q"
CHAT_ID = "5225146258"

def send(msg):
    url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def get_crypto(pair):
    url=f"https://api.binance.com/api/v3/klines?symbol={pair}&interval=5m&limit=150"
    data=requests.get(url).json()
    df=pd.DataFrame(data)
    df['close']=df[4].astype(float)
    return df[['close']]

def signal_logic(df):
    ema9 = EMAIndicator(df['close'],9).ema_indicator()
    ema21 = EMAIndicator(df['close'],21).ema_indicator()
    rsi = RSIIndicator(df['close'],14).rsi()

    i=len(df)-1

    if ema9[i]>ema21[i] and ema9[i-1]<=ema21[i-1] and 50<rsi[i]<70:
        return "BUY 📈", round(rsi[i],2)

    if ema9[i]<ema21[i] and ema9[i-1]>=ema21[i-1] and 30<rsi[i]<50:
        return "SELL 📉", round(rsi[i],2)

    return None,None

pairs=["BTCUSDT","ETHUSDT","BNBUSDT"]

for pair in pairs:
    df=get_crypto(pair)
    sig,rsi=signal_logic(df)
    if sig:
        msg=f"{pair} {sig}\nRSI:{rsi}\nTime:{datetime.utcnow().strftime('%H:%M')}"
        send(msg)
