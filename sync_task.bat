@echo off
REM Run by Windows Task Scheduler (task "Belt Tension Sync", daily 08:00). Appends to logs\sync.log
set "PATH=C:\Program Files\GitHub CLI;C:\Program Files\Git\cmd;%PATH%"
echo ===== %DATE% %TIME% >> "%~dp0logs\sync.log"
"C:\Users\ithcc\AppData\Local\Python\pythoncore-3.14-64\python.exe" "%~dp0scripts\sync.py" >> "%~dp0logs\sync.log" 2>&1
