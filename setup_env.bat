@echo off

REM Create Virtual Environment
python -m venv .venv

REM Activate Virtual Environment
call .\.venv\Scripts\activate.bat

REM Check Virtual Environment
if not defined VIRTUAL_ENV (
    echo Failed to activate virtual environment.
    exit /b 1
)

REM Install Packages
if exist requirements.txt (
    echo requirements.txt 파일을 찾았습니다. 패키지를 설치합니다...
    pip install -r requirements.txt
) else (
    echo requirements.txt 파일을 찾을 수 없습니다. 기본 패키지를 설치합니다...
    pip install pygame
    pip install black isort
    pip freeze > requirements.txt
)

echo Done
