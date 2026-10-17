@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 goto usepython
py -3 install-models.py
set "result=%errorlevel%"
goto finish
:usepython
where python >nul 2>nul
if errorlevel 1 goto nopython
python install-models.py
set "result=%errorlevel%"
goto finish
:nopython
echo Python 3 is required. You can also use python3 install-models.py in WSL.
set "result=1"
:finish
echo.
if not "%result%"=="0" echo Downloads did not all finish. Read the errors above, then rerun.
pause
exit /b %result%
