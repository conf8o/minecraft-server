import os
import sys
from .backup_config import BackupConfig
from .lib import copy_item

def restore_backup(backup_folder):
    if not os.path.exists(BackupConfig.source):
        os.makedirs(BackupConfig.source)
        print(f"Created destination folder '{BackupConfig.source}'.")
    
    try:
        for item in os.listdir(backup_folder):
            copy_item(item, backup_folder, BackupConfig.source)
        
        print(f"Backup restoration completed successfully to '{BackupConfig.source}'.")
    except Exception as e:
        print(f"An error occurred during restoration: {e}")

def confirm_restore(backup_folder):
    if not os.path.exists(backup_folder):
        print(f"Backup folder '{backup_folder}' does not exist.")
        return False
    
    print(f"Backup folder to restore: '{backup_folder}'")
    proceed = input("Do you want to proceed with the restoration? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Restoration aborted.")
        return False
    return True

def read_arg():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        # 引数が無い場合は、yyyymmddhh形式の引数を要求する
        raise ValueError("Backup ID is required as an argument in the format 'yyyymmddhh'.")
    
def main():
    try:
        backup_id = BackupConfig.read_backup_id(read_arg())
        backup_folder = BackupConfig.backup_folder_name(backup_id)
        if confirm_restore(backup_folder):
            restore_backup(backup_folder)
    except ValueError as e:
        print(e)
        print("Restoration aborted.")

if __name__ == "__main__":
    main()
