from pickle import NONE
import time
from httplib2 import Credentials
import requests
import json
import math
from datetime import datetime
from pytz import timezone
import pytz
import numpy as np
import pandas as pd

# def strRed(skk): return "\033[91m {}\033[00m".format(skk)
# def strGreen(skk): return "\033[92m {}\033[00m".format(skk)
# def strYellow(skk): return "\033[93m {}\033[00m".format(skk)
# def strLightPurple(skk): return "\033[94m {}\033[00m".format(skk)
# def strPurple(skk): return "\033[95m {}\033[00m".format(skk)
# def strCyan(skk): return "\033[96m {}\033[00m".format(skk)
# def strLightGray(skk): return "\033[97m {}\033[00m".format(skk)
# def strBlack(skk): return "\033[98m {}\033[00m".format(skk)
# def strBold(skk): return "\033[1m {}\033[0m".format(skk)


now = datetime.now()
format = "%d-%m-%Y %H:%M:%S %Z%z"
now_utc = datetime.now(timezone('UTC'))
now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
ocTime = now_asia.strftime(format)
fName = now_asia.strftime(format)
tdate = fName.split(" IST")
nowTime = tdate[0]
print(nowTime)
curWeekday = datetime.today().weekday()
dtTime = fName.split(" IST")
dt = dtTime[0].split(" ")
isHolidayNxtDay = ""
reqTime = ocTime[11:16]
reqSec = ocTime[14:16]
intTime = int(reqTime[0:2])
intSec = int(reqSec)
counter = 0

#Fetch Updated Index values from csv file
nse_ce_df = pd.read_csv('./levels.csv',usecols=['ce_level'],nrows=1)
nse_pe_df = pd.read_csv('./levels.csv',usecols=['pe_level'],nrows=1)
bnf_ce_df = pd.read_csv('./levels.csv',usecols=['ce_level'],nrows=2)
bnf_pe_df = pd.read_csv('./levels.csv',usecols=['pe_level'],nrows=2)
nseCeLevels = nse_ce_df['ce_level'].loc[nse_ce_df.index[0]]
nsePeLevels = nse_pe_df['pe_level'].loc[nse_pe_df.index[0]]
bnfCeLevels = bnf_ce_df['ce_level'].loc[bnf_ce_df.index[1]]
bnfPeLevels = bnf_pe_df['pe_level'].loc[bnf_pe_df.index[1]]

#Notify Index values To Telegram Channel before 9AM
if(intTime>9 and intSec<30):
    t_url = "https://api.telegram.org/bot6377307246:AAEuJAlBiQgDQEa03yNmKQJmZbXyQ0WINOk/sendMessage?chat_id=-996001230&text="+"======================\n"+nowTime+"\n======================"+"\nWELCOME TO MAGIC AI BOT TRADING"+"\n======================"+"\nMAGIC LEVEL BOT STARTED SUCCESSFULLY..!"+"\n======================\n"+"TODAY's MAGIC LEVELS\n"+"======================\n"+"NIFTY MAGIC LEVEL: "+str(nseCeLevels)+"\n"+"=========================\n"+str(nsePeLevels)+"\n"+"=========================\n"+"BNF BO LEVEL: "+str(bnfCeLevels)+"\n=========================\n"+str(bnfPeLevels)+"\n"+"=========================\n"+"NOTE : ONLY FOR EDUCATIONAL PURPOSE."+"\n----------------------------------------------"+"\nI AM NOT SEBI REG..!"+"\n----------------------------------------------"+"\nTRADE AT YOUR OWN RISK..!"+"\n----------------------------------------------\n"+"WISH YOU PROFITABLE DAY..!"
    requests.post(t_url) 

c = datetime.now()
runTm = c.strftime('%H:%M:%S')

#Keep Running below code from 9AM to 3PM
if intTime >= 9 and intTime <= 15:
    while(intTime<=15 ):
        if intTime>14:
            break
        c = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
        runTime = c.strftime('%H:%M:%S')
        print("Nifty CE Levels : ",nseCeLevels)
        print("Nifty PE Levels : ",nsePeLevels)
        print("Bnf CE Levels : ",bnfCeLevels)
        print("Bnf PE Levels : ",bnfPeLevels)
        # nifty_minus_range = nseLevels - 15 
        # print("Nifty minus range : ",nifty_minus_range)
        # nifty_plus_range = nseLevels + 15
        # print("Nifty plus range : ", nifty_plus_range)

        # bnf_minus_range = bnfLevels - 20 
        # print("Bnf minus range : ",bnf_minus_range)
        # bnf_plus_range = bnfLevels + 20
        # print("Bnf plus range : ", bnf_plus_range)

        # Method to get nearest strikes
        def round_nearest(x, num=50): return int(math.ceil(float(x)/num)*num)
        def nearest_strike_bnf(x): return round_nearest(x, 100)
        def nearest_strike_nf(x): return round_nearest(x, 50)


        # Urls for fetching Data
        url_oc = "https://www.nseindia.com/option-chain"
        url_bnf = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
        url_nf = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
        #url_finNif = 'https://www.nseindia.com/api/option-chain-indices?symbol=FINNIFTY'
        url_indices = "https://www.nseindia.com/api/allIndices"

        # Headers
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                   'authority': 'www.nseindia.com',
                    'scheme':'https'}

        sess = requests.Session()
        cookies = dict()

        # Local methods

        def set_cookie():
            request = sess.get(url_oc, headers=headers, timeout=60)
            cookies = dict(request.cookies)


        def get_data(url):
            set_cookie()
            response = sess.get(url, headers=headers, timeout=60, cookies=cookies)
            if (response.status_code == 401):
                set_cookie()
                response = sess.get(url_nf, headers=headers,
                                    timeout=60, cookies=cookies)
            if (response.status_code == 200):
                return response.text
            return ""


        def set_header():
            global bnf_ul
            global nf_ul
            global bnf_nearest
            global nf_nearest
            response_text = get_data(url_indices)
            data = json.loads(response_text)
            for index in data["data"]:
                if index["index"] == "NIFTY 50":
                    nf_ul = index["last"]
                    print("nifty")
                if index["index"] == "NIFTY BANK":
                    bnf_ul = index["last"]
                    print("banknifty")
            bnf_nearest = nearest_strike_bnf(bnf_ul)
            nf_nearest = nearest_strike_nf(nf_ul)


        # Showing Header in structured format with Last Price and Nearest Strike
        # def print_header(index="", ul=0, nearest=0):
        #     print(strPurple(index.ljust(12, " ") + " => ") + strLightPurple(" Last Price: ") +
        #         strBold(str(ul)) + strLightPurple(" Nearest Strike: ") + strBold(str(nearest)))


        # def print_hr():
        #     print(strYellow("|".rjust(70, "-")))

        def send_lastprice():
            global nf_ul
            global nf_nearest
            response_text = get_data(url_indices)
            data = json.loads(response_text)
            nf_nearest = 0
            nf_ul = 0
            for index in data["data"]:
                if index["index"] == "NIFTY 50":
                    nf_ul = index["last"]
                    #print(nf_ul)
                    nf_nearest = nearest_strike_nf(nf_ul)
            return nf_ul

        def send_Bnflastprice():
            global bnf_ul
            global bnf_nearest
            response_text = get_data(url_indices)
            data = json.loads(response_text)
            bnf_nearest = 0
            bnf_ul = 0
            for index in data["data"]:
                if index["index"] == "NIFTY BANK":
                    bnf_ul = index["last"]
                    #print(bnf_ul)
                    bnf_nearest = nearest_strike_bnf(bnf_ul)
            return bnf_ul

        #print_header("Nifty", nf_ul, nf_nearest)
        print("NIFTY CMP : ",send_lastprice())
        print("BNF CMP : ",send_Bnflastprice())
        counter= counter+1
        niftyLastPrice = int(send_lastprice())
        bnfLastPrice = int(send_Bnflastprice())
        print("Run Time : ", runTime)
        print("Counter : ", counter)
        

        if(niftyLastPrice > nseCeLevels ):
            t_url = "https://api.telegram.org/bot6377307246:AAEuJAlBiQgDQEa03yNmKQJmZbXyQ0WINOk/sendMessage?chat_id=-996001230&text="+"======================\n"+dt[0]+"-"+runTime+"\n======================\n"+"PYTHON-BOT FOR TODAY's LEVELS\n"+"======================\n"+"NIFYT CMP : "+str(niftyLastPrice)+"\n======================\n"+"NIFTY TRADING NEAR BO LEVEL: "+str(nseCeLevels)+"\n"+"\n=========================\n"+"CHOOSE STRIKE : "+str(nearest_strike_nf(nf_ul))+"\n=========================\n"+"NOTE : ONLY FOR EDUCATIONAL PURPOSE.\n"+"----------------------------------------------\n"+"I AM NOT SEBI REG..!"+"\n----------------------------------------------"+"\nTRADE AT YOUR OWN RISK..!"
            requests.post(t_url)
        
        if(niftyLastPrice < nsePeLevels ):
            t_url = "https://api.telegram.org/bot6377307246:AAEuJAlBiQgDQEa03yNmKQJmZbXyQ0WINOk/sendMessage?chat_id=-996001230&text="+"======================\n"+dt[0]+"-"+runTime+"\n======================\n"+"PYTHON-BOT FOR TODAY's LEVELS\n"+"======================\n"+"NIFYT CMP : "+str(niftyLastPrice)+"\n======================\n"+"NIFTY TRADING NEAR BO LEVEL: "+str(nsePeLevels)+"\n"+"\n=========================\n"+"CHOOSE STRIKE : "+str(nearest_strike_nf(nf_ul))+"\n=========================\n"+"NOTE : ONLY FOR EDUCATIONAL PURPOSE.\n"+"----------------------------------------------\n"+"I AM NOT SEBI REG..!"+"\n----------------------------------------------"+"\nTRADE AT YOUR OWN RISK..!"
            requests.post(t_url)

        if(bnfLastPrice > bnfCeLevels):
            t_url = "https://api.telegram.org/bot6377307246:AAEuJAlBiQgDQEa03yNmKQJmZbXyQ0WINOk/sendMessage?chat_id=-996001230&text="+"======================\n"+dt[0]+"-"+runTime+"\n======================\n"+"PYTHON-BOT FOR TODAY's LEVELS\n"+"======================\n"+"BNF CMP : "+str(bnfLastPrice)+"\n======================\n"+"BANK-NIFTY TRADING NEAR BO LEVEL: "+str(bnfCeLevels)+"\n"+"\n=========================\n"+"CHOOSE STRIKE : "+str(nearest_strike_bnf(bnf_ul))+"\n=========================\n"+"NOTE : ONLY FOR EDUCATIONAL PURPOSE.\n"+"----------------------------------------------\n"+"I AM NOT SEBI REG..!"+"\n----------------------------------------------"+"\nTRADE AT YOUR OWN RISK..!"
            requests.post(t_url)

        if(bnfLastPrice < bnfPeLevels):
            t_url = "https://api.telegram.org/bot6377307246:AAEuJAlBiQgDQEa03yNmKQJmZbXyQ0WINOk/sendMessage?chat_id=-996001230&text="+"======================\n"+dt[0]+"-"+runTime+"\n======================\n"+"PYTHON-BOT FOR TODAY's LEVELS\n"+"======================\n"+"BNF CMP : "+str(bnfLastPrice)+"\n======================\n"+"BANK-NIFTY TRADING NEAR BO LEVEL: "+str(bnfCeLevels)+"\n"+"\n=========================\n"+"CHOOSE STRIKE : "+str(nearest_strike_bnf(bnf_ul))+"\n=========================\n"+"NOTE : ONLY FOR EDUCATIONAL PURPOSE.\n"+"----------------------------------------------\n"+"I AM NOT SEBI REG..!"+"\n----------------------------------------------"+"\nTRADE AT YOUR OWN RISK..!"
            requests.post(t_url)
        
        time.sleep(120)

if(intTime>14):
    print("PROGRAM EXIT AT : ", runTm)
    exit()