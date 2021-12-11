import schedule
import time

from message_generators import *
from scrape_data import *
from tweet_updaters import *


#daily data ingestion
schedule.every().day.at("06:00").do(retrieve_event_time_formatted)    
schedule.every().day.at("06:05").do(retrieve_markets_in_holiday)


#schedules events tweets
schedule.every().day.at("06:10").do(schedule_macro_event)


#single tweets
schedule.every().day.at("08:00").do(tweet_usa_asia_morning)
schedule.every().day.at("08:20").do(tweet_ftse_mib,"morning")
schedule.every().day.at("11:45").do(tweet_ftse_mib,"noon")
schedule.every().day.at("17:20").do(tweet_ftse_mib,"night")
schedule.every().day.at("17:05").do(tweet_night_eu)


#clear schedule
schedule.every().day.at("23:55").do(clear_event_jobs)

while True:
    schedule.run_pending()
    time.sleep(15)
    #print("Bot Running..")
    print(schedule.get_jobs('macro-event'))




