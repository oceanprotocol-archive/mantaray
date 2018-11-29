"""
Use this script to convert all *.py files to jupyter notebook format
"""


#%%
import pathlib
import jupytext

# Get the IPython script root dir
root_dir = pathlib.Path.cwd().joinpath("")
path_ipy_root=root_dir.joinpath("ipython_scripts")
path_jupyter_root=root_dir.joinpath("jupyter_notebooks")

notebook_folders = ['0_verify','1_blocks','2_uses','3_stories']

for item in path_ipy_root.iterdir():
    if not item.is_dir():
        continue
    if not item.parts[-1] in notebook_folders:
        continue
    for script_path in item.glob('*.py'):
        print(script_path)
    print(item)
    item.iterdir()
    item.is_dir()
    # if item.is_dir() and item.parts[-1]
    #     print(item)



for script_dir in path_ipy_root.glob('*'):
    dir_name = script_dir.parts[-1]
    out_dir = path_jupyter_root.joinpath(dir_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    for script_path in script_dir.glob('*.py'):
        print("Processing", script_path)
        script_fname = script_path.stem + '.ipynb'
        out_path = out_dir.joinpath(script_fname)

        # Read the script, and parse it into memory
        with script_path.open() as fin:
            data = fin.read()
            parsed = jupytext.reads(data, ext='.py', format_name='percent')

        # Delete the file if it exists
        if out_path.exists():
            out_path.unlink()

        jupytext.writef(parsed, out_path)

        print("Converted {} to .ipynb format".format(out_path.stem))
        print("Saved to {}".format(out_path))

