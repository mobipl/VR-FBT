@echo off

cls

echo Restarting...

timeout 5

cls

if "%1"=="py" start Main.py

if "%1"=="exe" start Main.exe