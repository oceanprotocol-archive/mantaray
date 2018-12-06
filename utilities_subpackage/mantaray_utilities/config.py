import os
import logging
from pathlib import Path

CONFIG_MAP = {
    'JUPYER_DEPLOYMENT' : {
        'config_ini_name':'config_jupyter.ini',
    },
    'USE_K8S_CLUSTER' : {
        'config_ini_name':'config_k8s_deployed.ini',
    },
    'DEFAULT' : {
        'config_ini_name':'config.ini',
    },
}
SCRIPT_FOLDERS = ['0_verify', '1_blocks', '2_use_cases', '3_demos']

def get_deployment_type():
    if 'JUPYTER_DEPLOYMENT' in os.environ:
        # logging.info("Environment configuration detected: JupyterHub cluster.".format())
        return 'JUPYTER_DEPLOYMENT'
    if 'USE_K8S_CLUSTER' in os.environ:
        # logging.info("Environment configuration detected: Use deployed k8s endpoints.".format())
        return 'USE_K8S_CLUSTER'
    else:
        # logging.info("Environment configuration detected: Local machine with start-ocean local components.".format())
        return 'DEFAULT'

def name_deployment_type():
    if 'JUPYTER_DEPLOYMENT' in os.environ:
        logging.info("Environment configuration detected: JupyterHub cluster.".format())
    if 'USE_K8S_CLUSTER' in os.environ:
        logging.info("Environment configuration detected: Use deployed k8s endpoints.".format())
    else:
        logging.info("Environment configuration detected: Local machine with start-ocean local components.".format())

def get_config_file_path():
    # The configuration ini file is in the root of the project
    proj_path = get_project_path() / CONFIG_MAP[get_deployment_type()]['config_ini_name']
    assert proj_path.exists()
    return proj_path

def get_project_path():
    if get_deployment_type() == 'JUPYTER_DEPLOYMENT':
        # Detect a jupyter notebook running within one of the allowed folders
        if any(folder == Path.cwd().parts[-1] for folder in SCRIPT_FOLDERS):
            # Go up to the parent, this is the project root
            return Path.cwd().parents[0]
        else:
            print("JUPYTER_DEPLOYMENT is set, but can't find the correct paths!")
            raise EnvironmentError
    elif get_deployment_type() == 'USE_K8S_CLUSTER':
        return Path.cwd()
    elif get_deployment_type() == 'DEFAULT':
        return Path.cwd()
    else:
        raise NameError

    # print(Path.cwd())
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
    SCRIPT_FOLDERS = ['0_verify', '1_blocks', '2_use_cases', '3_demos']

    if any(folder == Path.cwd().parts[-1] for folder in SCRIPT_FOLDERS):
        # Go up to the parent
        PATH_PROJECT = Path.cwd().parents[0]

    assert PATH_PROJECT.parts[-1] == 'mantaray_jupyter'