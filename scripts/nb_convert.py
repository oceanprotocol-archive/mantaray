"""
Use this script to convert all *.py files to jupyter notebook format
"""


#%%
from py2jnb.tools import python_to_notebook
import pathlib

root_dir = pathlib.Path.cwd().joinpath("")
path_ipy_root=root_dir.joinpath("../ipython_scripts")
path_ipy_root=root_dir.joinpath("ipython_scripts")
path_jupyter_root=root_dir.joinpath("jupyter_notebooks")
list(path_ipy_scripts.glob('*'))

for script_dir in path_ipy_scripts.glob('*'):
    dir_name = script_dir.parts[-1]

    out_dir =
    for script in script_dir.glob('*.py'):
        print(script)

for py_file in path_ipy_scripts.glob('*.py'):
    print(py_file)
    # print(py_file.stem)
    out_path = path_jupyter_nbs.joinpath(py_file.stem + '.ipynb')
    print(out_path)
    # print(py_file.parents[0].joinpath(""))

    print(out_path.absolute())

    python_to_notebook(py_file,out_path)


