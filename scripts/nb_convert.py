#%%
from py2jnb.tools import python_to_notebook
import os
import pathlib

path_ipy_scripts=pathlib.Path.cwd().joinpath("../ipython_scripts")

path_jupyter_nbs=pathlib.Path.cwd().joinpath("../jupyter_notebooks")
# print(path_ipy_scripts)


# path_ipy_scripts=os.path.join(os.getcwd(),"../ipython_scripts")
# for ipy_file in [x for x in path_ipy_scripts.iterdir() if x.is_file()]:
#     print(ipy_file)

for py_file in path_ipy_scripts.glob('*.py'):
    print(py_file)
    # print(py_file.stem)
    out_path = path_jupyter_nbs.joinpath(py_file.stem + '.ipynb')
    print(out_path)
    # print(py_file.parents[0].joinpath(""))

    print(out_path.absolute())

    python_to_notebook(py_file,out_path)


