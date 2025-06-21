import os
import shutil
import sys

SOURCE_FOLDER = "./mc_data"  # 復元先フォルダ
MC_DATA_BACKUP_FOLDER = "./mc_data_backup"  # バックアップ先の親フォルダ
BACKUP_PREFIX = "backup_"  # バックアップフォルダのプレフィックス

def copy_item(item, source_folder, destination_folder):
    source_path = os.path.join(source_folder, item)
    destination_path = os.path.join(destination_folder, item)

    print(f"Copying '{source_path}' to '{destination_path}'.")
    if os.path.isdir(source_path):
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    else:
        shutil.copy2(source_path, destination_path)
    print(f"Copied '{source_path}' to '{destination_path}'.")

def restore_backup(backup_folder):
    if not os.path.exists(SOURCE_FOLDER):
        os.makedirs(SOURCE_FOLDER)
        print(f"Created destination folder '{SOURCE_FOLDER}'.")
    
    try:
        for item in os.listdir(backup_folder):
            copy_item(item, backup_folder, SOURCE_FOLDER)
        
        print(f"Backup restoration completed successfully to '{SOURCE_FOLDER}'.")
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

def read_backup_id():
    if len(sys.argv) > 1:
        backup_id = sys.argv[1]
        # フォーマットの検証 (yyyymmddhh)
        if not backup_id.isdigit() or len(backup_id) != 10:
            raise ValueError("Invalid backup ID format. Expected yyyymmddhh.")
        return backup_id
    else:
        raise ValueError("Backup ID is required as a program argument.")

def main():
    try:
        backup_id = read_backup_id()
        backup_folder = os.path.join(MC_DATA_BACKUP_FOLDER, f"{BACKUP_PREFIX}{backup_id}")
        if confirm_restore(backup_folder):
            restore_backup(backup_folder)
    except ValueError as e:
        print(e)
        print("Restoration aborted.")

if __name__ == "__main__":
    main()
