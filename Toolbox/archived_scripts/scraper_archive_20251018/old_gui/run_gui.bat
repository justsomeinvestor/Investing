@echo off
echo Starting YouTube Transcript Downloader GUI...

echo Installing/updating dependencies...
pip install -r "%~dp0requirements.txt" > nul 2>&1

echo Starting GUI...
python "%~dp0transcript_gui.py"

pause