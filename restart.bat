@echo off

cls

echo Restarting...

timeout 5

cls

if "%1"=="py" python Main.py
if "%1"=="exe" Main.exe