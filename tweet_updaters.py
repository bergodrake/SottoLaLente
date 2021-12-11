from scrape_data import * 
from message_generators import *
from config import consumer_key, consumer_secret, access_key, access_secret
import schedule
import tweepy


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

def update(message=None):
    if datetime.now().weekday() < 5:
        api.update_status(message)
        print("Tweet posted successfully!")

def schedule_macro_event():
    time_events = read_event_time()
    for i, val in enumerate(time_events):
        print(time_events[i])
        schedule.every().day.at(f"{time_events[i]}").do(tweet_macro_event, event_number=i).tag('macro-event')


def tweet_macro_event(event_number):
    event_df = scrape_macro()
    message = sll_macro(event_df.iloc[event_number])
    update(message)


def tweet_ftse_mib(moment):
    message=sll_ftse_mib(moment)
    if 'FTSEMIB' not in read_markets_in_holiday():
        update(message)
        
def tweet_night_eu():
    message = sll_night_eu()
    if 'CAC40' not in read_markets_in_holiday() and 'DAX' not in read_markets_in_holiday():
        update(message)
        
def tweet_usa_asia_morning():
    index_data = scrape_indexes()
    message = sll_morning(index_data)
    if 'HSI' not in read_markets_in_holiday() and 'N225' not in read_markets_in_holiday():
        update(message)


def clear_event_jobs():
    return schedule.clear('macro-event')     