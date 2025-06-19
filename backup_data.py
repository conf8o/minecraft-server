import os
import sys
from datetime import datetime
import shutil

DEFAULT_FILE_LIST_PATH = "./save_default_files_list.txt"  # グローバル変数として定義
SOURCE_FOLDER = "./mc_data"  # バックアップ元フォルダをグローバル変数として定義
DYNAMIC_FILE_LIST_PATH = "./save_dynamic_files_list.txt"  # 動的ファイルリストの保存先
BACKUP_PREFIX = "mc_backup_"  # バックアップフォルダのプレフィックス

def prepare_backup_folder_name(date_str):
    backup_folder = f"{BACKUP_PREFIX}{date_str}"
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

def get_backup_list(file_list_path):
    if not os.path.exists(file_list_path):
        print(f"File list '{file_list_path}' does not exist.")
        return []
    
    with open(file_list_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def validate_source_and_files(source_folder, default_files_to_backup, dynamic_files_to_backup):
    # Default files: Throw exception if missing
    missing_default_items = [
        item for item in default_files_to_backup
        if not os.path.exists(os.path.join(source_folder, item))
    ]
    if missing_default_items:
        raise FileNotFoundError(
            "The following required items are missing and the backup cannot proceed:\n" +
            "\n".join(f"- {item}" for item in missing_default_items)
        )
    
    # Dynamic files: Warn if missing
    for item in dynamic_files_to_backup:
        if not os.path.exists(os.path.join(source_folder, item)):
            print(f"Warning: Dynamic file or folder '{item}' does not exist and was skipped.")

def perform_backup(backup_folder):
    try:
        # Get files to backup
        default_files_to_backup = get_backup_list(DEFAULT_FILE_LIST_PATH)
        dynamic_files_to_backup = get_backup_list(DYNAMIC_FILE_LIST_PATH)  # 動的扱いのファイル/フォルダ
        
        # Validate source folder and required files. If invalid, raise an exception
        validate_source_and_files(SOURCE_FOLDER, default_files_to_backup, dynamic_files_to_backup)
        
        all_files_to_backup = default_files_to_backup + dynamic_files_to_backup
        
        destination_folder = backup_folder  # 直接バックアップフォルダを使用
        
        os.makedirs(destination_folder, exist_ok=True)
        
        # Copy listed files and directories
        for item in all_files_to_backup:
            source_path = os.path.join(SOURCE_FOLDER, item)
            destination_path = os.path.join(destination_folder, item)
            
            if os.path.exists(source_path):
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, destination_path)
                else:
                    shutil.copy2(source_path, destination_path)
                print(f"Copied '{source_path}' to '{destination_path}'.")
            else:
                if item in dynamic_files_to_backup:
                    print(f"Warning: Dynamic file or folder '{item}' does not exist and was skipped.")
                else:
                    print(f"Error: Required file or folder '{item}' does not exist.")
        
        print(f"Backup completed successfully to '{destination_folder}'.")
    except FileNotFoundError as e:
        print(e)
        print("Backup aborted.")
    except Exception as e:
        print(f"An error occurred during backup: {e}")

def main():
    # Get date argument or use current date/time
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now().strftime("%Y%m%d%H")
    
    print(f"Using date: {date_str}")
    backup_folder_name = prepare_backup_folder_name(date_str)
    if backup_folder_name:
        backup_folder = create_backup_folder(backup_folder_name)
        if backup_folder:
            perform_backup(backup_folder)

if __name__ == "__main__":
    main()
