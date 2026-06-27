@echo off
title Redrob AI - Local Launcher
echo ============================================================
echo           Launching Redrob AI Platform
echo ============================================================
echo.

set "PATH=%PATH%;C:\Program Files\nodejs;D:\Python311"
cd /d "D:\Desktop\Challenge\talentmind-ai"

if exist "D:\Python311\python.exe" (
    "D:\Python311\python.exe" run_local.py
) else (
    python run_local.py
)

pause
