import os
from datetime import datetime

class BackupConfig:
  required_file_list = [
      "world/",
      "server.properties",
      "ops.json",
      "whitelist.json",
      "banned-players.json",
      "banned-ips.json",
      "logs/"
    ]
  optional_file_list = [
      "world_nether/",
      "world_the_end/"
    ]
  source = "./mc_data"
  dest = "./mc_data_backup"
  prefix = "backup_"


  @staticmethod
  def backup_folder_name(name: str) -> str:
    return os.path.join(BackupConfig.dest, f"{BackupConfig.prefix}{name}")
  
  @staticmethod
  def source_item(item: str) -> str:
    return os.path.join(BackupConfig.source, item)
  
  @staticmethod
  def validate_file_list() -> None:
    """
    バックアップ元のファイルの検証。\n
    デフォルトのリストは、存在しなければ例外を投げる。\n
    動的なリストは、存在しなければ警告を出す。
    """
    missing_default_items = [
        item for item in BackupConfig.default_files_to_backup
        if not os.path.exists(BackupConfig.source_item(item))
    ]
    if missing_default_items:
        raise FileNotFoundError(
            "The following required items are missing and the backup cannot proceed:\n" +
            "\n".join(f"- {item}" for item in missing_default_items)
        )
    for item in BackupConfig.dynamic_files_to_backup:
        if not os.path.exists(BackupConfig.source_item(item)):
            print(f"Warning: Dynamic file or folder '{item}' does not exist and will be skipped.")

  @staticmethod
  def read_backup_id(s: str | None) -> str:
    """
    バックアップIDを生成する。\n
    現在の日時を基にした文字列を返す。\n
    フォーマットは yyyymmddhh。
    """
    if s:
        if not s.isdigit() or len(s) != 10:
            raise ValueError("Invalid backup ID format. Expected yyyymmddhh.")
        return s
    else:
        # 引数が指定されていない場合は、現在時刻のyyyymmddhh形式を使用
      return datetime.now().strftime("%Y%m%d%H")