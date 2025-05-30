import os

# Path to the current script
this_script = os.path.abspath(__file__)

# Current working directory
root_folder = os.getcwd()

# Walk through all subdirectories
for dirpath, _, filenames in os.walk(root_folder):
    for filename in filenames:
        if 'thumb' in filename.lower():
            filepath = os.path.join(dirpath, filename)
            # Skip the file if it is this script itself
            if os.path.abspath(filepath) == this_script:
                continue
            try:
                os.remove(filepath)
                print(f'🗑 Deleted: {filepath}')
            except Exception as e:
                print(f'⚠ Error deleting {filepath}: {e}')

print('\n✅ Done: all files containing "thumb" in their names have been deleted.')
