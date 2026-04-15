@echo off
REM Get the directory where the script is located
SET "SCRIPT_DIR=%~dp0"

REM Navigate to the script directory
cd /d "%SCRIPT_DIR%"

REM Run the attendance fetching script
REM Using "python" assuming it is in the PATH. 
REM Redirecting output to sync_log.txt for troubleshooting.
python fetch_attendance_all.py >> sync_log.txt 2>&1
