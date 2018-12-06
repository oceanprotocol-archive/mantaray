import os
import logging
from pathlib import Path

CONFIG_MAP = {
'JUPYTER_DEPLOYMENT' : {
    'config_ini_name':'config_jupyter.ini',

}
}

def get_deployment_type():
    if 'JUPYTER_DEPLOYMENT' in os.environ:
        logging.info("Environment configuration detected: JupyterHub cluster.".format())
        return 'JUPYTER_DEPLOYMENT'
    if 'USE_K8S_CLUSTER' in os.environ:
        logging.info("Environment configuration detected: Use deployed k8s endpoints.".format())
        return 'USE_K8S_CLUSTER'
    else:
        logging.info("Environment configuration detected: Local machine with start-ocean local components.".format())
        return 'DEFAULT'

def get_config_file_path():
        config_file = 'config_k8s_deployed.ini'
        config_file = 'conf'

def get_project_path():
    print(Path.cwd())
# if not 'PATH_PROJECT' in locals():
#     PATH_PROJECT = Path.cwd()
# print("Project root path:", PATH_PROJECT)


if 0:
    from pathlib import Path
    # Ensure paths are correct in Jupyter Hub
    # The PATH_PROJECT path variable must be the root of the project folder
    # By default the root is the current working directory
    PATH_PROJECT = Path.cwd()

    # But if run as a Jupyter Notebook, the cwd will be one of:
    script_folders = ['0_verify', '1_blocks', '2_use_cases', '3_demos']

    if any(folder == Path.cwd().parts[-1] for folder in script_folders):
        # Go up to the parent
        PATH_PROJECT = Path.cwd().parents[0]

    assert PATH_PROJECT.parts[-1] == 'mantaray_jupyter'