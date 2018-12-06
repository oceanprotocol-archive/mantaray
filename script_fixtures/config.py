import os
import logging

if 'JUPYTER_DEPLOYMENT' in os.environ:
    logging.info("Jupyter Hub deployment detected.".format())
if 'USE_K8S_CLUSTER' in os.environ:
    logging.info("Local ".format())
else:
    logging.info("Default deployment detected.".format())
