:: ==========================================================
:: Setup Script for LipiMerge
::
:: Sets up a Python virtual environment and install dependencies
:: ==========================================================

@ECHO OFF & SETLOCAL

:: Sanity check: Ensure the script is run from the correct directory
IF NOT EXIST pyproject.toml (
    ECHO The pyproject.toml root configuration file not found. Please run this script from the project root directory.
    EXIT /B 1
)

:: Check if Python is installed
WHERE py > NUL 2>&1

IF %ERRORLEVEL% NEQ 0 (
    ECHO Python is not installed. Please install Python and try again.
    EXIT /B 1
)

:: Check if pip is installed
WHERE pip > NUL 2>&1

IF %ERRORLEVEL% NEQ 0 (
    ECHO pip is not installed. Please install pip and try again.
    EXIT /B 1
)

:: Create virtual environment
IF NOT EXIST .venv (

    ECHO Creating virtual environment...

) ELSE (

    CHOICE /M "Virtual environment already exists. Do you want to recreate it?"
    IF %ERRORLEVEL% NEQ 0 (
        ECHO Exiting without changes.
        EXIT /B 0
    )

    ECHO Recreating virtual environment...
    RMDIR /S /Q .venv

    IF %ERRORLEVEL% NEQ 0 (
        ECHO Failed to remove existing virtual environment.
        EXIT /B 1
    )
    ECHO Existing virtual environment removed.

)

ECHO Creating a new virtual environment...
py -m venv .venv

IF %ERRORLEVEL% NEQ 0 (
    ECHO Failed to create virtual environment.
    EXIT /B 1
)

:: Activate it
CALL .venv\Scripts\activate.bat

IF %ERRORLEVEL% NEQ 0 (
    ECHO Failed to activate virtual environment.
    EXIT /B 1
)

:: Install dependencies
py -m pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    ECHO Failed to install dependencies.
    EXIT /B 1
)

:: Done
ECHO Environment setup complete.
PAUSE
