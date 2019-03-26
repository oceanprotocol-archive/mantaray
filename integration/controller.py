import schedule
import time
import datetime
from pathlib import Path
assert PATH_TEST_FLOW.exists(), PATH_TEST_FLOW
import subprocess


PATH_TEST_FLOW = Path.cwd() / 'ipython_scripts' / '1_notebooks_blocks' / 's04_consume_asset.py'
assert PATH_TEST_FLOW.exists(), "Can't find {}".format(PATH_TEST_FLOW)

def maintest():
    print("Hi",datetime.datetime.utcnow().isoformat())

START_TIME = "10:37"
END_TIME = "10:38"
INTERVAL = 2

def job():
    schedule.every(INTERVAL).seconds.do(maintest)

schedule.every().day.at(START_TIME).do(job)

while 1:
    schedule.run_pending()





