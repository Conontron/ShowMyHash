@echo off
setlocal

taskkill /IM ShowMyHash.exe /F

set "InstallDir=C:\Program Files (x86)\ShowMyHash"
set "ExeName=ShowMyHash.exe"
set "ZipUrl=https://github.com/Conontron/ShowMyHash/raw/main/Installer/ShowMyHash.zip"
set "TempDir=%TEMP%\ShowMyHashTemp"

NET SESSION >nul 2>&1
if %errorLevel% == 0 (
    goto :continue
) else (
    echo This script requires administrative privileges. Please run as administrator.
    pause
    exit
)

:continue
if exist "%InstallDir%" (
    echo Removing existing program files...
    rmdir /s /q "%InstallDir%"
)

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


echo Update completed.
pause
