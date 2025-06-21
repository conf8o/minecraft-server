import shutil
import os


def copy_item(item, source_folder, destination_folder):
    source_path = os.path.join(source_folder, item)
    destination_path = os.path.join(destination_folder, item)

    print(f"Copying '{source_path}' to '{destination_path}'.")
    if os.path.isdir(source_path):
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    else:
        shutil.copy2(source_path, destination_path)
    print(f"Copied '{source_path}' to '{destination_path}'.")