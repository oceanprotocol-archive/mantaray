#%%
import pathlib
import jupytext

root_dir = pathlib.Path.cwd().joinpath("")
path_script1 = root_dir / 'tests' / 'resources' / 'test_jupy.py'

assert path_script1.exists()
print("Processing", path_script1)
script_fname = path_script1.stem + '.ipynb'
outpath = path_script1.parent / script_fname

# Read the script, and parse it into memory
with path_script1.open() as fin:
    data = fin.read()
    parsed = jupytext.reads(data, ext='.py', format_name='percent')

# Delete the file if it exists
if out_path.exists():
    out_path.unlink()

jupytext.writef(parsed, out_path)

print("Converted {} to .ipynb format".format(out_path.stem))
print("Saved to {}".format(out_path))
