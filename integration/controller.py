import schedule
import time
import datetime
from pathlib import Path
import subprocess

PATH_CONTROL_LOG = Path.home() / 'Started performance test at {}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

PATH_TEST_FLOW = Path.cwd() / 'ipython_scripts' / '1_notebooks_blocks' / 's04_consume_asset.py'
assert PATH_TEST_FLOW.exists(), "Can't find {}".format(PATH_TEST_FLOW)

START_TIME = "12:17"
END_TIME = "12:22"
END_HOUR = int(END_TIME.split(':')[0])
END_MINUTE = int(END_TIME.split(':')[1])
INTERVAL = 30

def job():
    schedule.every(INTERVAL).seconds.do(maintest)

def maintest():
    log_str = "Running script {} at {}\n".format(PATH_TEST_FLOW, datetime.datetime.utcnow().isoformat())
    print(log_str, end="")
    with PATH_CONTROL_LOG.open('a') as f:
        f.write(log_str)

    # Run the process
    ret_code = subprocess.call(['python', PATH_TEST_FLOW])

    log_str = "Finished run at {}, process returns {}\n\n".format(datetime.datetime.utcnow().isoformat(), ret_code)
    print(log_str, end="")
    with PATH_CONTROL_LOG.open('a') as f:
        f.write(log_str)
if 0:
    # For starting at a specific time
    schedule.every().day.at(START_TIME).do(job)
if 1:
    # Start immediately on process start
    schedule.every(INTERVAL).seconds.do(maintest)
    START_TIME = datetime.datetime.now().isoformat()

log_str = "Scheduler set to start at {} every {} seconds until {}\n".format(START_TIME, INTERVAL,  END_TIME)
print("Current datetime:", datetime.datetime.now())
print(log_str, end="")
with PATH_CONTROL_LOG.open('a') as f:
    f.write(log_str)

while 1:
    schedule.run_pending()
    if datetime.datetime.now().hour >= END_HOUR and datetime.datetime.now().minute >= END_MINUTE:
        log_str = "Scheduler finished at {}".format(END_TIME)
        print(log_str, end="")
        with PATH_CONTROL_LOG.open('a') as f:
            f.write(log_str)
        break
    time.sleep(1)


