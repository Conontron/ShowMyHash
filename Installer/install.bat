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
set "ZipUrl=https://github.com/Conontron/ShowMyHash/raw/main/Installer/ShowMyHash.zip"
set "TempDir=%TEMP%\ShowMyHashTemp"
set "StartMenuDir=%APPDATA%\Microsoft\Windows\Start Menu\Programs"

if not exist "%InstallDir%" mkdir "%InstallDir%"

echo Downloading and extracting files...

if not exist "%TempDir%" mkdir "%TempDir%"

powershell -command "$webClient = New-Object System.Net.WebClient; $webClient.DownloadFile('%ZipUrl%', '%TempDir%\ShowMyHash.zip')"
if not exist "%TempDir%\ShowMyHash.zip" (
    echo Failed to download archive.
    pause
    exit /b
)
powershell -command "Expand-Archive -Path '%TempDir%\ShowMyHash.zip' -DestinationPath '%InstallDir%'"

move "%InstallDir%\ShowMyHash%ExeName%" "%InstallDir%"

echo Adding registry key...
reg add "HKEY_CLASSES_ROOT\*\shell\ShowMyHash\command" /ve /t REG_SZ /d "\"%InstallDir%\%ExeName%\" \"%%1\"" /f

echo Creating shortcut...
set "ShortcutPath=%StartMenuDir%\ShowMyHash.lnk"
powershell -command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%ShortcutPath%'); $Shortcut.TargetPath = '%InstallDir%\%ExeName%'; $Shortcut.WorkingDirectory = '%InstallDir%'; $Shortcut.Save()"

echo Installation completed.
pause
