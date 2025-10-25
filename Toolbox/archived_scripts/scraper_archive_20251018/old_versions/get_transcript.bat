@echo off
setlocal enabledelayedexpansion
echo YouTube Transcript Downloader
echo ============================

if "%1"=="" (
    echo.
    set /p channel_url="Enter YouTube channel URL: "
    if "!channel_url!"=="" (
        echo No URL provided. Exiting.
        pause
        exit /b 1
    )
) else (
    set channel_url=%1
)

echo Installing/updating dependencies...
pip install -r "%~dp0requirements.txt" > nul 2>&1

echo.
echo Running transcript downloader...
python "%~dp0get_transcript.py" "%channel_url%"

echo.
pause