
import datetime as dt
import random
from scrape_data import * 



def describe_perf(ticker=None, market=False):
    index_data = scrape_indexes()
    returns = index_data.pct_change().iloc[-1]*100
    perf_pos = ['in rialzo a ','in positivo a ', 'sopra la pari a ','guadagna il ', 'avanza del ', 'cresce del ']
    perf_neg = ['in ribasso a ','in rosso a ','sotto la pari a ','cede il ', 'arretra del ', 'scende del ']
    close_pos = ['chiuso in rialzo: ', 'chiuso in positivo: ', 'chiuso sopra la pari: ']
    close_neg = ['chiuso sotto la pari: ', 'chiuso in ribasso: ', 'chiuso in rosso: ']
    if ticker:
        if returns[ticker] > 0:
            perf_description =  random.choice(perf_pos)
        else:
            perf_description =  random.choice(perf_neg)
    if market:
        if returns['^DJI'] > 0 and returns['^IXIC'] > 0 and returns['^GSPC'] > 0:
            perf_description = random.choice(close_pos)
        elif returns['^DJI'] < 0 and returns['^IXIC'] < 0 and returns['^GSPC'] < 0:
            perf_description = random.choice(close_neg)
        else:
            perf_description = 'hanno registrato le seguenti performance: '
    return perf_description

    
def ticker_return(ticker):
    index_data = scrape_indexes()
    returns = index_data.pct_change().iloc[-1]*100
    if returns[ticker] > 0:
        result = f'+{round(returns[ticker], 2)}'
    else: 
        result = f'{round(returns[ticker], 2)}'
    return result

def sll_morning(index_data):
    returns = index_data.pct_change().iloc[-1]*100
    today=dt.date.today()
    yesterday = today - dt.timedelta(days=1)
    last_closing_day = index_data.index[-1].date()
    day_of_the_week = {0 :'lunedì',
                   1: 'martedì',
                   2: 'mercoledì',
                   3: 'giovedì',
                   4: 'venerdì',
                   5: 'sabato',
                   6 : 'domenica'}
    if last_closing_day == yesterday:
        day = 'ieri'
    else:
        day = f'{day_of_the_week[last_closing_day.weekday()]} {last_closing_day.day}'
    
    incipit = [f'Gli indici americani nella giornata di {day} hanno' , 
               f'Il mercato americano nella giornata di {day} ha']
    close_pos = ['chiuso in rialzo: ', 'chiuso in positivo: ', 'chiuso sopra la pari: ']
    close_neg = ['chiuso sotto la pari: ', 'chiuso in ribasso: ', 'chiuso in rosso: ']
    asian_markets = ['Sul fronte asiatico invece ', 'Sul mercato asiatico invece ']
    perf_pos_strings = ['in rialzo a ','in positivo a ', 'sopra la pari a ','guadagna il ']
    perf_neg_strings = ['in ribasso a ','in rosso a ','sotto la pari a ','cede il ']
    message = f"{random.choice(incipit)} {describe_perf(ticker=None, market=True)}"\
    f"#DowJones e #SP500 rispettivamente a {ticker_return('^DJI')}% e {ticker_return('^GSPC')}% "\
    f"mentre il #Nasdaq ha concluso a {ticker_return('^IXIC')}%. {random.choice(asian_markets)}il #Nikkei"\
    f" {describe_perf(ticker='^N225')}{ticker_return('^N225')}%, #HangSeng segna {ticker_return('^HSI')}%."
            
    return message


def describe_perf_mib(ftse_mib_data):
    pos_perf = ['è in rialzo: ', 'è in positivo: ', 'è sopra la pari: '
               ,'è in rialzo a ','è in positivo a ', 'è sopra la pari a ','guadagna il ']
    neg_perf = ['è sotto la pari: ', 'è in ribasso: ', 'è in rosso: '
               ,'è in ribasso a ','è in rosso a ','è sotto la pari a ','cede il ']
    if float(ftse_mib_data.replace("%", "")) > 0:
        perf_description = random.choice(pos_perf)
    else: 
        perf_description = random.choice(neg_perf)
    return perf_description

def maybe_plus(i):
    if i > 0:
        return "+"
    else:
        return ""

def sll_ftse_mib(moment):
    mib_stocks_data = scrape_ftse_mib()

    bests = mib_stocks_data[2]
    worsts = mib_stocks_data[3]
    incipit = ['A metà seduta il #FTSEMib ', 'A fine giornata il #FTSEMib ', 'In apertura il #FTSEMib ']
    if moment == "noon":
        incipit = incipit[0]
    if moment == "night":
        incipit = incipit[1]
    if moment == "morning":
        incipit = incipit[2]
    best_sent = ['Tra i titoli in territorio positivo spiccano ','In testa troviamo ', 'Tra i rialzi troviamo ', 'Conducono la classifica ','In cima alla classifica troviamo ','Tra i titoli del paniere principale spiccano i rialzi di ']
    worst_sent = ['In coda invece ' , 'Tra i peggiori invece troviamo ' ,'Chiudono la classifica ', 'In rosso invece ', 'Giù invece ', 'Tra i ribassi troviamo ']
    message = f"{incipit}{describe_perf_mib(mib_stocks_data[1])}{mib_stocks_data[1]}. {random.choice(best_sent)}"\
    f"#{bests['Stocks'].iloc[2]} a {maybe_plus(bests['Return'].iloc[0])}{bests['Return'].iloc[0]}%"\
    f", #{bests['Stocks'].iloc[1]} a {maybe_plus(bests['Return'].iloc[1])}{bests['Return'].iloc[1]}%"\
    f" e #{bests['Stocks'].iloc[0]} a {maybe_plus(bests['Return'].iloc[1])}{bests['Return'].iloc[1]}%"\
    f". {random.choice(worst_sent)}#{worsts['Stocks'].iloc[0]} a {maybe_plus(worsts['Return'].iloc[0])}{worsts['Return'].iloc[0]}%"\
    f", #{worsts['Stocks'].iloc[1]} a {maybe_plus(worsts['Return'].iloc[1])}{worsts['Return'].iloc[1]}%"\
    f" e #{worsts['Stocks'].iloc[2]} a {maybe_plus(worsts['Return'].iloc[1])}{worsts['Return'].iloc[1]}%."
    return message

def macro_incipit(macro_event):
    country_dict = {'CHN' : '#CINA:',
                   'USA' : '#USA:',
                   'EUR' : '#EUROZONA:',
                   'ITA': '#ITALIA:',
                   'DEU': '#GERMANIA:',
                   'JPN': '#GIAPPONE:',
                   'GBR': '#REGNO UNITO:',
                   'ESP' : '#SPAGNA:',
                   'FRA': '#FRANCIA:'}
    
    incipit = country_dict[macro_event['Country']]
    return incipit


def describe_macro_numbers(macro_event):
    if macro_event['Actual'] != "--":
        actual = float(macro_event['Actual'].replace(",", "."))
    else:
        actual = None
    if macro_event['Previous'] != "--":
        previous = float(macro_event['Previous'].replace(",", "."))
    else:
        previous = None
    if macro_event['Forecast'] != "--":
        forecast = float(macro_event['Forecast'].replace(",", "."))
    else:
        forecast = None
    unit = macro_event['Unit']
    if len(unit) > 1: #if unit != %, $, £, €...
        isPlural = True
        if isPlural:
            prop = ["di", "ai", "precedenti", "attesi"]
            unit = f" {unit}"    
    else:
        prop = ["del", "al", "precedente", "atteso"]   
    if actual and actual > 0:
        desc_actual = f"si è attestato a {actual}{unit}"
    if actual and actual < 0:
        desc_actual = f"si è attestato a {actual}{unit}"
    if actual and actual < 0:
        desc_actual ="a crescita nulla"
    if not actual:
        desc_actual = ""
    if previous:
        prev_comparison = f", rispetto {prop[1]} {maybe_plus(previous)}{previous}{unit} {prop[2]}"
    if forecast and not previous:
        fore_comparison = f" rispetto {prop[1]} {maybe_plus(forecast)}{forecast}{unit} {prop[3]}."
    if previous and forecast:
        fore_comparison = f" e {prop[1]} {maybe_plus(forecast)}{forecast}{unit} {prop[3]}."
    if not forecast:
        fore_comparison = "."
    message = f"{desc_actual}{prev_comparison}{fore_comparison}"
    return message


def sll_macro(macro_event):
    event_name = macro_event['EventName'].replace("[", "(").replace("]", ")")
    message = f"{macro_incipit(macro_event)} {event_name} {describe_macro_numbers(macro_event)}"
    return message


def sll_night_eu():
    incipit = "Le borse europee hanno chiuso con le seguenti performance:"
    message = f"{incipit} il #DAX di Francoforte {describe_perf('^GDAXI')}{ticker_return('^GDAXI')}%, "\
    f"mentre a Parigi il #CAC40 {describe_perf('^FCHI')}{ticker_return('^FCHI')}%"
    return message