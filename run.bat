@echo off
title SafeRoute AI - Local Navigation Server
echo ========================================================
echo        SafeRoute AI - Intelligent Navigation
echo ========================================================
echo.
echo Starting server at http://127.0.0.1:8000 ...
start http://127.0.0.1:8000
python -m uvicorn main:app --host 127.0.0.1 --port 8000
if errorlevel 1 (
    echo.
    echo [Notice] Trying with py -3 launcher...
    py -3 -m uvicorn main:app --host 127.0.0.1 --port 8000
)
pause
