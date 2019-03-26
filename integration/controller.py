import schedule
INTERVAL = 30
schedule.every(INTERVAL).minutes
import time
import datetime
from pathlib import Path
PATH_TEST_FLOW = Path.cwd() / 'ipython_scripts' / '1_notebooks_blocks' / 's04_consume_asset.py'
assert PATH_TEST_FLOW.exists(), PATH_TEST_FLOW
import subprocess

def maintest():
    print("Hi",datetime.datetime.utcnow().isoformat())
    subprocess.call(['python', PATH_TEST_FLOW])

INTERVAL = 30
schedule.every(INTERVAL).seconds.do(maintest)

while 1:
    schedule.run_pending()

