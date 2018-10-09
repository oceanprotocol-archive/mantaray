"""
Use this script to convert all *.py files to jupyter notebook format
"""


#%%
# from py2jnb.tools import python_to_notebook
import pathlib
import jupytext

path_ipy_scripts=pathlib.Path.cwd().joinpath("../ipython_scripts")

path_jupyter_nbs=pathlib.Path.cwd().joinpath("../jupyter_notebooks")

for py_path in list(path_ipy_scripts.glob('**/*.py')):
    print(py_path)

    with py_path.open() as fin:
        data = fin.read()
        parsed = jupytext.reads(data, ext='.py', format_name='percent')

    OUTPUT_IPYNB = path_jupyter_nbs / Path(str(py_path.stem) + '.ipynb')

    # assert OUTPUT_IPYNB.exists()

    jupytext.writef(parsed, OUTPUT_IPYNB)


