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

for script_dir in path_ipy_root.glob('*'):
    dir_name = script_dir.parts[-1]
    out_dir = path_jupyter_root.joinpath(dir_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    for script_path in script_dir.glob('*.py'):
        script_fname = script_path.stem + '.ipynb'
        out_path = out_dir.joinpath(script_fname)

        # Read the script, and parse it into memory
        with script_path.open() as fin:
            data = fin.read()
            parsed = jupytext.reads(data, ext='.py', format_name='percent')

        jupytext.writef(parsed, out_path)

        print("Converted {} to .ipynb format".format(out_path.stem))


