@echo off
echo checking Python...
python --version
if errorlevel 1 (
    echo Python is not installed! Install Python and try again.
    pause
    exit /b
)

echo Checking pip...
pip --version
if errorlevel 1 (
    echo Pip is not installed! Install pip and try again.
    pause
    exit /b
)

echo Libraries installing...
pip install -r requirements.txt
echo Libraries installed successfully!
python app.py
pause