import schedule
import time
import datetime
from pathlib import Path
import subprocess


PATH_TEST_FLOW = Path.cwd() / 'ipython_scripts' / '1_notebooks_blocks' / 's04_consume_asset.py'
assert PATH_TEST_FLOW.exists(), "Can't find {}".format(PATH_TEST_FLOW)

def maintest():
    print("Hi",datetime.datetime.utcnow().isoformat())
    subprocess.call(['python', PATH_TEST_FLOW])

START_TIME = "10:57"
END_TIME = "10:38"
INTERVAL = 30

def job():
    schedule.every(INTERVAL).seconds.do(maintest)

schedule.every().day.at(START_TIME).do(job)

while 1:
    schedule.run_pending()





