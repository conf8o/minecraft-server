@echo off
echo Resetting Minecraft server data...

docker compose down -v

echo Removing host folder: ./mc_data
rmdir /s /q mc_data

echo Reset completed.
pause
