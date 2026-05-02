@echo off
python "%~dp0..\..\src\serve.py"
if errorlevel 1 pause
