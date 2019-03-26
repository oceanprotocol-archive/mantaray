import schedule
import time
import datetime
from pathlib import Path
import subprocess

PATH_CONTROL_LOG = Path.home() / 'Started performance test at {}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

PATH_TEST_FLOW = Path.cwd() / 'ipython_scripts' / '1_notebooks_blocks' / 's04_consume_asset.py'
assert PATH_TEST_FLOW.exists(), "Can't find {}".format(PATH_TEST_FLOW)

START_TIME = "12:04"
END_TIME = "10:38"
INTERVAL = 30

def job():
    schedule.every(INTERVAL).seconds.do(maintest)

def maintest():

    log_str = "Running script {} at {}".format(PATH_TEST_FLOW, datetime.datetime.utcnow().isoformat())
    print(log_str)
    with PATH_CONTROL_LOG.open('a') as f:
        f.write(log_str)

    # Run the process
    ret_code = subprocess.call(['python', PATH_TEST_FLOW])

    log_str = "Finished run at {}, process returns {}".format(datetime.datetime.utcnow().isoformat(), ret_code)
    print(log_str)
    with PATH_CONTROL_LOG.open('a') as f:
        f.write(log_str)

schedule.every().day.at(START_TIME).do(job)

while 1:
    schedule.run_pending()





