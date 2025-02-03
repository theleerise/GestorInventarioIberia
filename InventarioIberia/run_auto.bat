@echo off

REM Ruta donde se encuentra el entorno virtual
set VENV_DIR=%cd%\.venv

REM Comprobamos si la carpeta del entorno virtual existe
if not exist "%VENV_DIR%" (
    echo El entorno virtual no existe en la carpeta "%VENV_DIR%".
    echo Crea el entorno virtual ejecutando: python -m venv .venv
    pause
    exit /b
)

REM Activar el entorno virtual
call "%VENV_DIR%\Scripts\activate.bat"

if errorlevel 1 (
    echo No se pudo activar el entorno virtual.
    pause
    exit /b
)

REM Ejecutar el script main.py
REM Editar el nombre del archivo .py a ejecutar si es necesario
python run_flask.py

REM Desactivar el entorno virtual
call "%VENV_DIR%\Scripts\deactivate.bat"

pause
