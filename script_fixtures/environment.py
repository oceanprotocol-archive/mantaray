import os
import logging

def jupyter_env():
    if 'JUPYTER_DEPLOYMENT' in os.environ:
        logging.info("Jupyter Hub deployement detected.".format())
        return True
    else:
        logging.info("Default deployment detected.".format())
        return False


