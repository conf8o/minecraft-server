import os
import sys
from datetime import datetime
import shutil

DEFAULT_FILE_LIST_PATH = "./save_default_files_list.txt"  # バックアップするファイルのリスト
DYNAMIC_FILE_LIST_PATH = "./save_dynamic_files_list.txt"  # バックアップするファイルのリストのうち動的に生成されるやつ
SOURCE_FOLDER = "./mc_data"  # バックアップ元フォルダ
MC_DATA_BACKUP_FOLDER = "./mc_data_backup"  # バックアップ先の親フォルダ
BACKUP_PREFIX = "backup_"  # バックアップフォルダのプレフィックス

def prepare_backup_folder_name(date_str):
    backup_folder = os.path.join(MC_DATA_BACKUP_FOLDER, f"{BACKUP_PREFIX}{date_str}")
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

def validate_source_files(default_files_to_backup, dynamic_files_to_backup):
    # デフォルトのバックアップファイルの存在を確認。存在しなければ例外を投げる
    missing_default_items = [
        item for item in default_files_to_backup
        if not os.path.exists(os.path.join(SOURCE_FOLDER, item))
    ]
    if missing_default_items:
        raise FileNotFoundError(
            "The following required items are missing and the backup cannot proceed:\n" +
            "\n".join(f"- {item}" for item in missing_default_items)
        )
    
    # 動的なファイルのリストは存在しない場合は警告を出す
    for item in dynamic_files_to_backup:
        if not os.path.exists(os.path.join(SOURCE_FOLDER, item)):
            print(f"Warning: Dynamic file or folder '{item}' does not exist and will be skipped.")

def copy_item(item, source_folder, destination_folder):
    source_path = os.path.join(source_folder, item)
    destination_path = os.path.join(destination_folder, item)

    print(f"Copying '{source_path}' to '{destination_path}'.")
    if os.path.isdir(source_path):
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    else:
        shutil.copy2(source_path, destination_path)
    print(f"Copied '{source_path}' to '{destination_path}'.")

def perform_backup(backup_folder):
    try:
        # バックアップファイルのリスト
        default_files_to_backup = get_backup_list(DEFAULT_FILE_LIST_PATH)
        dynamic_files_to_backup = get_backup_list(DYNAMIC_FILE_LIST_PATH)
        
        # バックアップ元のファイルの検証。
        # デフォルトのリストは、存在しなければ例外を投げる
        # 動的なリストは、存在しなければ警告を出す
        validate_source_files(default_files_to_backup, dynamic_files_to_backup)
        
        os.makedirs(backup_folder, exist_ok=True)

        for item in default_files_to_backup:
            copy_item(item, SOURCE_FOLDER, backup_folder)

        for item in dynamic_files_to_backup:
            if os.path.exists(os.path.join(SOURCE_FOLDER, item)):
                copy_item(item, SOURCE_FOLDER, backup_folder)
        
        print(f"Backup completed successfully to '{backup_folder}'.")
    except FileNotFoundError as e:
        print(e)
        print("Backup aborted.")
    except Exception as e:
        print(f"An error occurred during backup: {e}")

def read_backup_id():
    if len(sys.argv) > 1:
        backup_id = sys.argv[1]
        # 形式の検証 (yyyymmddhh)
        if not backup_id.isdigit() or len(backup_id) != 10:
            raise ValueError("Invalid backup ID format. Expected yyyymmddhh.")
        return backup_id
    else:
        raise ValueError("Backup ID is required as a program argument.")

def main():
    try:
        backup_id = read_backup_id()
        print(f"Using backup ID: {backup_id}")
        backup_folder_name = prepare_backup_folder_name(backup_id)
        if backup_folder_name:
            perform_backup(backup_folder_name)
    except ValueError as e:
        print(e)
        print("Backup aborted.")

if __name__ == "__main__":
    main()
