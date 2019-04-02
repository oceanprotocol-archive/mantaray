import schedule
import time
import datetime
from pathlib import Path
import subprocess
import os

# Save the logs to this path
PATH_CONTROL_LOG = Path('/test_logs') / 'Started performance test at {}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Controller script started. Log file at", PATH_CONTROL_LOG)

# This is the test script to run
PATH_TEST_FLOW = Path.cwd() / 'integration' / 'test04_consume_asset.py'
assert PATH_TEST_FLOW.exists(), "Can't find {}".format(PATH_TEST_FLOW)

DOCKER_STRICT = True # Strictly enforce the environment variables
DOCKER_STRICT = False # Strictly enforce the environment variables
if DOCKER_STRICT:
    assert 'DOCKER_START_TIME' in os.environ
    assert 'DOCKER_END_TIME' in os.environ
    assert 'DOCKER_INTERVAL' in os.environ

# Get the schedule variables
# Testing start time
if 'DOCKER_START_TIME' in os.environ:
    if os.environ['DOCKER_START_TIME'] == 'now':
        START_TIME = datetime.datetime.now().strftime("%H:%M")

    else:
        START_TIME = os.environ['DOCKER_START_TIME']
elif 0: # Enable for a manual start time
    START_TIME = "12:17"
else: # Otherwise, just start now
    START_TIME = datetime.datetime.now().strftime("%H:%M")

# Testing end time
if 'DOCKER_END_TIME' in os.environ:
    END_TIME = os.environ['DOCKER_END_TIME']
    END_HOUR = int(END_TIME.split(':')[0])
    END_MINUTE = int(END_TIME.split(':')[1])
else: # Enable for a manual start time
    END_TIME = "20:00"
    END_HOUR = int(END_TIME.split(':')[0])
    END_MINUTE = int(END_TIME.split(':')[1])

# Testing interval
if 'DOCKER_INTERVAL' in os.environ:
    INTERVAL = int(os.environ['DOCKER_INTERVAL'])
else:
    INTERVAL = 30


def schedule_at_interval():
    """Add scheduled jobs at INTERVAL time
    """
    schedule.every(INTERVAL).seconds.do(run_python_test_script)


def run_python_test_script():
    """Simple wrapper on subprocess.call()
    """
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


# Schedule the jobs
try:
    schedule.every().day.at(START_TIME).do(schedule_at_interval)
except:
    print(START_TIME)
    raise
schedule.every(INTERVAL).seconds.do(run_python_test_script)

log_str = "Scheduler set to start at {} every {} seconds until {}\n".format(START_TIME, INTERVAL,  END_TIME)
print("Current datetime:", datetime.datetime.now())
print(log_str, end="")
with PATH_CONTROL_LOG.open('a') as f:
    f.write(log_str)

while 1:
    schedule.run_pending()

    # Check if END_TIME, and break
    if datetime.datetime.now().hour >= END_HOUR and datetime.datetime.now().minute >= END_MINUTE:
        log_str = "Scheduler finished at {}".format(END_TIME)
        print(log_str, end="")
        with PATH_CONTROL_LOG.open('a') as f:
            f.write(log_str)
        break

    time.sleep(1)


