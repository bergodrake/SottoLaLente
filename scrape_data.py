import pandas as pd
import datetime as dt
from datetime import timedelta
from datetime import datetime
from pandas_datareader import data as wb 
import requests
import requests_cache
from bs4 import BeautifulSoup
import re
from settings import *
import random

def scrape_indexes():
    session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=3600)
    session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',     
                       'Accept': 'application/json;charset=utf-8'}
    tickers = ['^DJI','^HSI', '^GSPC', '^IXIC', '^N225', '^GDAXI' , '^FCHI']
    index_data = pd.DataFrame()
    today = dt.date.today()
    week_ago = today - dt.timedelta(days=7)
    for t in tickers:
        index_data[t]= wb.DataReader(t, data_source='yahoo', start=week_ago, session=session)['Adj Close']
    return index_data

def scrape_ftse_mib():
    url_fsteMib = "https://markets.businessinsider.com/index/ftse_mib?op=1"
    page_ftseMib = requests.get(url_fsteMib)
    soup = BeautifulSoup(page_ftseMib.content, "html.parser")
    mib_index_perf = soup.find_all('span', class_="price-section__relative-value")[0].get_text()
    perfs = []
    session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=3600)
    session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',     
                    'Accept': 'application/json;charset=utf-8'}
    ftse_tickers_df = pd.read_csv(f"{ROOT_DIR}/ftse_mib_stocks.csv", sep=";", header=0)
    tickers = ftse_tickers_df['Ticker'].to_list()
    ftse_mib_data = pd.DataFrame()
    today = dt.date.today()
    week_ago = today - dt.timedelta(days=7)
    for t in tickers:
        ftse_mib_data[t]= wb.DataReader(t, data_source='yahoo', start=week_ago, session=session)['Adj Close']
    ftse_tickers_df['Return'] = round((ftse_mib_data.pct_change().iloc[-1]*100),2).to_list()
    top3 = ftse_tickers_df.sort_values('Return')[-3:]
    bottom3 = ftse_tickers_df.sort_values('Return')[:3]
    return ftse_tickers_df, mib_index_perf, top3, bottom3


def scrape_macro():
    months_dict = {'gennaio' : 1,
                  'febbraio' : 2,
                  'marzo': 3,
                  'aprile': 4,
                  'maggio': 5,
                  'giugno': 6,
                  'luglio': 7,
                  'agosto' : 8,
                  'settembre': 9,
                  'ottobre': 10,
                  'novembre': 11,
                  'dicembre': 12}
    url_macro = "https://www.teleborsa.it/Agenda/?mode=calendar"
    page_macro = requests.get(url_macro)
    soup = BeautifulSoup(page_macro.content, "html.parser")
    table = soup.find_all("table", class_="grid")
    text_data_soups = []
    for j in range(len(table[0].findAll('tr'))):
        for i in table[0].findAll('tr')[j].find_all("td", class_="l"):
            text_data_soups.append(i)
    text_data_soups = BeautifulSoup(str(text_data_soups), "html.parser")
    number_data_soups = []
    for j in range(len(table[0].findAll('tr'))):
        for i in table[0].findAll('tr')[j].find_all("td", class_="c"):
            number_data_soups.append(i)
    number_data_soups = BeautifulSoup(str(number_data_soups), "html.parser")
    ##################################### retrieving days
    full_text_soup = []
    for i in table[0].findAll('tr'):
        full_text_soup.append(i)
    full_text_soup = BeautifulSoup(str(full_text_soup), "html.parser")
    hours_and_days =[i.get_text() for i in full_text_soup.find_all("span", id=re.compile("lblDate"))]
    #####################################
    for i, val in enumerate(hours_and_days):
        if i < (len(hours_and_days)-1):
            if len(val)> 10 and len(hours_and_days[i+1])<10:
                hours_and_days[i+1] = val
                del hours_and_days[i]
            else:
                continue
    ################################## first cycle removes the "header" row with the date of each day
    for i, val in enumerate(hours_and_days):
        if i < (len(hours_and_days)-1):
            if len(val)> 10 and len(hours_and_days[i+1])<10:
                hours_and_days[i+1] = val

            else:
                continue
    ################################## second cycle transforms each time in the date of the event
    macro_df = pd.DataFrame()
    macro_df['Time'] = [i.get_text() for i in text_data_soups.find_all("span", id=re.compile("lblDateFrom"))]
    hours_and_days = hours_and_days[:len(macro_df['Time'])] #get date for every event in string then convert to datetime
    years = [i[-5:].strip() for i in hours_and_days] 
    daymonth = [i[:-5].split(" ") for i in hours_and_days]
    datetimes = [dt.date(int(years[i]), months_dict[daymonth[i][2]], int(daymonth[i][1])) for i in range(len(daymonth))]
    macro_df['DateTime'] = datetimes
    macro_df['Country'] = [i.get_text() for i in text_data_soups.find_all("span", id=re.compile("lblSource"))]
    macro_df['EventName'] = [i.get_text() for i in text_data_soups.find_all("span", id=re.compile("lblDescription"))]
    macro_df['Period'] = [i.get_text() for i in number_data_soups.find_all("span", id=re.compile("lblReference"))]        
    macro_df['Actual'] = [i.get_text() for i in number_data_soups.find_all("span", id=re.compile("lblActual"))]
    macro_df['Previous'] = [i.get_text() for i in number_data_soups.find_all("span", id=re.compile("lblPrevious"))]
    macro_df['Forecast'] = [i.get_text() for i in number_data_soups.find_all("span", id=re.compile("lblForecast"))]
    macro_df['Unit'] = [i.get_text() for i in text_data_soups.find_all("span", id=re.compile("lblUnits"))]
    macro_df = macro_df[macro_df['DateTime'] == dt.date.today()]
    return macro_df

def retrieve_event_time_formatted(): 
    macro_data = scrape_macro()
    time_format_str = '%H.%M'
    event_time = [datetime.strptime(macro_data['Time'].iloc[i], time_format_str) for i in range(len(macro_data))]
    n = random.randrange(-30, -45)
    final_time = [i + timedelta(minutes=n) for i in event_time] # Add n+60 minutes to the event time
    final_time_formatted = [i.strftime('%H:%M') for i in final_time]
    final_time_series = pd.Series(final_time_formatted, name = 'time')
    return final_time_series.to_csv(f"{ROOT_DIR}/event_time_today.csv", index = False, header = True)

def read_event_time():
    event_time_df = pd.read_csv(f"{ROOT_DIR}/event_time_today.csv", header=0, sep=",") #header on first row
    event_time = event_time_df['time'].to_list()
    return event_time

def retrieve_markets_in_holiday():
    holiday_df = pd.read_csv(f"{ROOT_DIR}/bank_holidays.csv")
    tickers = ['DAX', 'CAC40', 'HSI', 'FTSEMIB', 'N225']
    today=dt.date.today()
    holiday_df['datetime'] = holiday_df['Holiday'].apply(lambda x: dt.date(int(str(x)[0:4]), int(str(x)[4:6]), int(str(x)[6:8])))
    markets_in_holiday = holiday_df[holiday_df['datetime']==today]['Ticker']
    markets_in_holiday.to_csv(f"{ROOT_DIR}/markets_in_holiday_today.csv", index = False, header = True)
    return

def read_markets_in_holiday():
    markets_in_holiday_df = pd.read_csv(f"{ROOT_DIR}/markets_in_holiday_today.csv", header=0) #header on first row
    markets_in_holiday = markets_in_holiday_df['Ticker'].to_list()
    return markets_in_holiday