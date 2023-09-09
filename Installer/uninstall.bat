@echo off
setlocal

NET SESSION >nul 2>&1
if %errorLevel% == 0 (
    goto :continue
) else (
    echo This script requires administrative privileges. Please run as administrator.
    pause
    exit
)

:continue
set "InstallDir=C:\Program Files (x86)\ShowMyHash"
set "ExeName=ShowMyHash.exe"
set "RegKey=HKEY_CLASSES_ROOT\*\shell\ShowMyHash"
set "StartMenuDir=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "ShortcutPath=%StartMenuDir%\ShowMyHash.lnk"

echo This will uninstall ShowMyHash. Are you sure? (Y/N)
set /p "choice="
if /i "%choice%" neq "Y" goto :eof

echo Removing registry key...
reg delete "%RegKey%" /f > nul 2>&1

echo Removing shortcut...
if exist "%ShortcutPath%" (
    del "%ShortcutPath%"
)

echo Removing installation directory...
if exist "%InstallDir%" (
    rmdir /s /q "%InstallDir%"
)

echo Uninstallation completed.
pause
