import schedule
INTERVAL = 30
schedule.every(INTERVAL).minutes
import time
import datetime



time.time()

def maintest():
    print("Hi",datetime.datetime.utcnow().isoformat())


INTERVAL = 2
schedule.every(INTERVAL).seconds.do(maintest)

while 1:
    schedule.run_pending()

