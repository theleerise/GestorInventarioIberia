@echo off

REM Solicitar al usuario el nombre del entorno virtual
set /p VENV_NAME=Introduce el nombre de la carpeta del entorno virtual (por ejemplo, venv, .venv, env): 

REM Comprobar si el entorno virtual existe
set VENV_DIR=%cd%\%VENV_NAME%
if not exist "%VENV_DIR%" (
    echo La carpeta del entorno virtual "%VENV_NAME%" no existe en el directorio actual.
    pause
    exit /b
)

REM Solicitar al usuario el archivo .py a ejecutar
set /p PYTHON_FILE=Introduce el nombre del archivo .py a ejecutar (por ejemplo, main.py): 

REM Comprobar si el archivo .py existe
if not exist "%cd%\%PYTHON_FILE%" (
    echo El archivo "%PYTHON_FILE%" no existe en el directorio actual.
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

REM Ejecutar el archivo .py
python "%cd%\%PYTHON_FILE%"

REM Desactivar el entorno virtual
call "%VENV_DIR%\Scripts\deactivate.bat"

pause
