import os
import shutil
import sys

SOURCE_FOLDER = "./mc_data"  # 復元先フォルダ
BACKUP_PREFIX = "backup_"  # バックアップフォルダのプレフィックス

def restore_backup(backup_folder):
    if not os.path.exists(backup_folder):
        print(f"Backup folder '{backup_folder}' does not exist.")
        return
    
    if not os.path.exists(SOURCE_FOLDER):
        os.makedirs(SOURCE_FOLDER)
        print(f"Created destination folder '{SOURCE_FOLDER}'.")
    
    try:
        # Copy files and directories from backup folder to mc_data
        for item in os.listdir(backup_folder):
            source_path = os.path.join(backup_folder, item)
            destination_path = os.path.join(SOURCE_FOLDER, item)
            
            if os.path.isdir(source_path):
                if os.path.exists(destination_path):
                    shutil.rmtree(destination_path)
                shutil.copytree(source_path, destination_path)
            else:
                shutil.copy2(source_path, destination_path)
            
            print(f"Restored '{source_path}' to '{destination_path}'.")
        
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

def main():
    if len(sys.argv) != 2:
        print("Usage: python restore_backup.py <date>")
        print("Example: python restore_backup.py 2023101012")
        return
    
    date_str = sys.argv[1]
    backup_folder = f"./{BACKUP_PREFIX}{date_str}"
    
    if confirm_restore(backup_folder):
        restore_backup(backup_folder)

if __name__ == "__main__":
    main()
