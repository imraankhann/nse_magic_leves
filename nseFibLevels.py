import time
import requests
import json
from datetime import datetime
import pytz
import pandas as pd
import math
import yfinance as yf

# Timezone and Timestamp
IST = pytz.timezone('Asia/Kolkata')
now = datetime.now(IST)
format = "%d-%m-%Y %H:%M:%S"
nowTime = now.strftime(format)
intTime = int(now.strftime("%H"))
intSec = int(now.strftime("%S"))
runTm = now.strftime('%H:%M:%S')

# Fetch levels from CSV
nse_ce_df = pd.read_csv('./levels.csv', usecols=['ce_level'], nrows=1)
nse_pe_df = pd.read_csv('./levels.csv', usecols=['pe_level'], nrows=1)
nseCeLevels = nse_ce_df['ce_level'].iloc[0]
nsePeLevels = nse_pe_df['pe_level'].iloc[0]

# Round CMP to nearest strike
def round_nearest(x, num=50): return int(math.ceil(float(x)/num)*num)

# Get CMP using yfinance
def fetch_nifty_cmp():
    data = yf.download("^NSEI", period="1d", interval="1m")
    if data.empty:
        return None
    cmp = float(data['Close'].iloc[-1]) 
    return round(cmp, 2)

# Send Telegram message
def notify_telegram(message):
    bot_token = "5771720913:AAH0A70f0BPtPjrOCTrhAb9LR7IGFBVt-oM"
    chat_id = "-703180529"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.post(url)

# Notify startup before 9:30 AM
if intTime == 9 and intSec < 30:
    notify_telegram(
        f"========================\n"
        f"🟢 BOT STARTED\n\n📅 {nowTime}\n"
        f"NIFTY CE Level: {nseCeLevels}\n"
        f"NIFTY PE Level: {nsePeLevels}\n"
        f"⚠️ For Educational Use Only\n"
        f"========================\n"

    )

# Run check loop from 9:15 to 15:30
if 9 <= intTime <= 15:
    while intTime <= 15:
        c = datetime.now(IST)
        runTime = c.strftime('%H:%M:%S')
        intTime = int(c.strftime('%H'))

        cmp = fetch_nifty_cmp()
        if cmp is None:
            print("⚠️ Couldn't fetch CMP.")
            time.sleep(60)
            continue

        print(f"[{runTime}] NIFTY CMP: {cmp} | CE Level: {nseCeLevels} | PE Level: {nsePeLevels}")

        strike = round_nearest(cmp)

        if cmp > nseCeLevels:
            notify_telegram(
                f"==============\n\n📈 NIFTY CE BREAKOUT\n\n🕒 {runTime}\nCMP: {cmp}\nBreakout above: {nseCeLevels}\nStrike: {strike} CE\n\n ===============\n\n"
            )

        if cmp < nsePeLevels:
            notify_telegram(
                f"===============\n\n📉 NIFTY PE BREAKDOWN\n\n🕒 {runTime}\nCMP: {cmp}\nBreakdown below: {nsePeLevels}\nStrike: {strike} PE\n\n ================\n\n"
            )

        time.sleep(300)

else:
    print(f"⏳ Market closed or outside hours at {runTm}")
