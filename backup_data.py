import os
import sys
from datetime import datetime
from .backup_config import BackupConfig
from .lib import copy_item


def prepare_backup_folder_name(id):
    backup_folder = BackupConfig.backup_folder_name(id)
    print(f"Proposed backup folder name: '{backup_folder}'")
    proceed = input("Do you want to proceed with this folder name? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Backup aborted.")
        return None
    return backup_folder

def create_backup_folder(backup_folder):
    if os.path.exists(backup_folder):
        print(f"Folder '{backup_folder}' already exists.")
        overwrite = input("Do you want to overwrite it? (y/n): ")

        if overwrite != 'y':
            print("Backup aborted.")
            return None
    else:
        os.makedirs(backup_folder)
        print(f"Folder '{backup_folder}' created successfully.")
    print(f"Backup folder is ready: {backup_folder}")
    return backup_folder

def perform_backup(backup_folder):
    try:
        os.makedirs(backup_folder, exist_ok=True)

        for item in BackupConfig.default_files_to_backup:
            copy_item(item, BackupConfig.source, backup_folder)

        for item in BackupConfig.dynamic_files_to_backup:
            if os.path.exists(BackupConfig.source_item(item)):
                copy_item(item, BackupConfig.source, backup_folder)
        
        print(f"Backup completed successfully to '{backup_folder}'.")
    except FileNotFoundError as e:
        print(e)
        print("Backup aborted.")
    except Exception as e:
        print(f"An error occurred during backup: {e}")

def read_arg():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return None

def main():
    try:
        BackupConfig.validate_file_list()
        backup_id = BackupConfig.read_backup_id(read_arg())
        print(f"Using backup ID: {backup_id}")
        backup_folder_name = prepare_backup_folder_name(backup_id)
        if backup_folder_name:
            perform_backup(backup_folder_name)
    except ValueError as e:
        print(e)
        print("Backup aborted.")

if __name__ == "__main__":
    main()
