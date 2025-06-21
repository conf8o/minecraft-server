# minecraft-server

マイクラサーバーのDockerコンテナを動かすやつ

# Features

- 基本的にはDockerイメージの `itzg/minecraft-server` を動かすだけ
- セーブデータは、 `mc_data` というフォルダに保存される
- バックアップ機能つき
  - 日時(yyyymmddhh)を識別子としてバックアップ
  - 復元機能あり

# How to run

1. Docker, Pythonをインストールする
2. `compose.yml` ファイルを確認、設定する
3. `docker compose up -d`(バックグラウンドで走らせたい場合) or `docker compose up`(ログをリアルタイムで確認したい場合)

# Dependencies

- Docker
- Python
