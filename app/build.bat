echo off
pyinstaller --onefile -p src\ --distpath builds\monitoring\1.1\dist\ --workpath builds\monitoring\1.1\temp\ --specpath builds\monitoring\1.1\spec\ src\tasks\monitor_task.py