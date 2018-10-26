"""
Use this script to convert all *.py files to jupyter notebook format
"""


#%%
# from py2jnb.tools import python_to_notebook
import pathlib
import jupytext

root_dir = pathlib.Path.cwd().joinpath("")
path_ipy_root=root_dir.joinpath("../ipython_scripts")
path_ipy_root=root_dir.joinpath("ipython_scripts")
path_jupyter_root=root_dir.joinpath("jupyter_notebooks")

for script_dir in path_ipy_scripts.glob('*'):
    dir_name = script_dir.parts[-1]

    out_dir =
    for script in script_dir.glob('*.py'):
        print(script)
for py_path in list(path_ipy_scripts.glob('*.py')):
    # print(py_path)

    with py_path.open() as fin:
        data = fin.read()
        parsed = jupytext.reads(data, ext='.py', format_name='percent')

    OUTPUT_IPYNB = path_jupyter_nbs / Path(str(py_path.stem) + '.ipynb')

    # assert OUTPUT_IPYNB.exists()
    # print(OUTPUT_IPYNB)
    jupytext.writef(parsed, OUTPUT_IPYNB)

    print("Converted {} to .ipynb format".format(py_path.stem))


