"""
Use this script to convert all *.py files to jupyter notebook format
"""


#%%
import pathlib
import jupytext
import logging

# Get the IPython script root dir
root_dir = pathlib.Path.cwd().joinpath("")
path_ipy_root=root_dir.joinpath("ipython_scripts")
path_jupyter_root=root_dir.joinpath("jupyter_notebooks")

# The main header template, inserted into all notebooks
header_path=path_ipy_root / 'header_template.py'
assert header_path.exists()

notebook_folders = ['0_verify','1_blocks','2_uses','3_stories']

#%%
# Load the header
header_lines=header_path.read_text()

# Walk the directory tree
for item in path_ipy_root.iterdir():
    if not item.is_dir():
        continue
    if not item.parts[-1] in notebook_folders:
        continue

    for script_path in item.glob('*.py'):
        logging.info("Processing: {} / {}".format(script_path.parts[-2], script_path.parts[-1]))

        # Select (make) the output folder
        jupyter_dir_name = script_path.parts[-2]
        jupyter_path = path_jupyter_root / jupyter_dir_name
        jupyter_path.mkdir(parents=True, exist_ok=True)

        # The output path
        jupyter_file_name = script_path.stem + '.ipynb'
        out_path = jupyter_path / jupyter_file_name

        script_lines = script_path.read_text()

        # Concatenate the header
        total_script_lines = header_lines + script_lines
        logging.info("{}+{}={} total lines".format( len(header_lines.split('\n')), len(script_lines.split('\n')), len(total_script_lines.split('\n')), ))

        # Parse the script to Jupyter format
        parsed = jupytext.reads(total_script_lines, ext='.py', format_name='percent')

        # Delete the file if it exists
        if out_path.exists():
            out_path.unlink()

        jupytext.writef(parsed, out_path)

