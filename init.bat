@ECHO OFF & SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION & SET "ERRORLEVEL=" & GOTO :MAIN

:: ===========================================================
:HELP

ECHO :: ==========================================================
ECHO :: Python environment initialization Script for LipiMerge
ECHO ::
ECHO :: Sets up a Python virtual environment and installs dependencies.
ECHO ::
ECHO :: Usage:
ECHO ::   init [/Y ^| /N] [/NP] [/?]
ECHO ::
ECHO :: Options (order does not matter):
ECHO ::   /Y  if the virtual environment already exists, recreate it without prompting.
ECHO ::   /N  if the virtual environment already exists, exit without changes.
ECHO ::   /NP do not pause.
ECHO ::   /?  display this help message.
ECHO ::       If present, no action happens and all options beyond this are ignored.
ECHO :: 
ECHO :: ==========================================================

GOTO :RETURN

:: ===========================================================
:MAIN

:: Parse command line arguments

SET "init.ERRORLEVEL=0"
SET "init.args.recreate_env=?"
SET "init.args.no_pause=0"

:ARGS

    SHIFT
    IF /I "%~0"=="" GOTO :ARGS_END
    IF /I "%~0"=="/?" GOTO :HELP
    IF /I "%~0"=="/Y" IF NOT "%init.args.recreate_env%"=="n" SET "init.args.recreate_env=y" & GOTO :ARGS
    IF /I "%~0"=="/N" IF NOT "%init.args.recreate_env%"=="y" SET "init.args.recreate_env=n" & GOTO :ARGS
    IF /I "%~0"=="/NP" SET "init.args.no_pause=1" & GOTO :ARGS

    ECHO Invalid argument: '%0'. Run `init /?` for help. 1>&2
    SET "init.ERRORLEVEL=1" 
    GOTO :RETURN

:ARGS_END

:: Sanity checks

IF NOT EXIST pyproject.toml (
    ECHO The pyproject.toml root configuration file not found. Please run this script from the project root directory. 1>&2
    SET "init.ERRORLEVEL=1"
    GOTO :RETURN
)

CALL :CALL_WRAP WHERE py > NUL 2>&1
IF %init.ERRORLEVEL% NEQ 0 ECHO Python is not installed. Please install Python and try again. 1>&2 & GOTO :RETURN

CALL :CALL_WRAP py -m pip --version > NUL 2>&1
IF %init.ERRORLEVEL% NEQ 0 ECHO pip is not installed. Please install pip and try again. 1>&2 & GOTO :RETURN

:: Create & activate virtual environment + dependencies

IF NOT EXIST .venv (

    ECHO.
    ECHO Creating virtual environment...

) ELSE (

    IF "%init.args.recreate_env%"=="?" (

        CHOICE /M "Virtual environment already exists. Do you want to recreate it?"
        IF !ERRORLEVEL! EQU 1 SET "init.args.recreate_env=y"
        IF !ERRORLEVEL! EQU 2 SET "init.args.recreate_env=n"

    )

    IF "!init.args.recreate_env!"=="n" GOTO :RETURN

    ECHO.
    ECHO Recreating virtual environment...
    RMDIR /S /Q .venv
    rem No way to find that RMDIR failed, so we check if the directory still exists
    rem https://stackoverflow.com/questions/11137702/rd-exits-with-errorlevel-set-to-0-on-error-when-deletion-fails-etc
    IF EXIST .venv (
        ECHO Failed to remove existing '.venv' directory. Please remove it manually and try again. 1>&2
        SET "init.ERRORLEVEL=1"
        GOTO :RETURN
    )
    ECHO Existing virtual environment removed.

)

ECHO.
ECHO Creating a new virtual environment...
CALL :CALL_WRAP py -m venv .venv
IF %init.ERRORLEVEL% NEQ 0 ECHO Failed to create virtual environment. 1>&2 & GOTO :RETURN

CALL :CALL_WRAP .venv\Scripts\activate.bat
IF %init.ERRORLEVEL% NEQ 0 ECHO Failed to activate virtual environment. Please check if the .venv directory exists. 1>&2 & GOTO :RETURN

CALL :CALL_WRAP py -m pip install --upgrade pip
IF %init.ERRORLEVEL% NEQ 0 ECHO Failed to upgrade pip. 1>&2 & GOTO :RETURN

CALL :CALL_WRAP py -m pip install -r requirements.txt
IF %init.ERRORLEVEL% NEQ 0 ECHO Failed to install dependencies from requirements.txt. 1>&2 & GOTO :RETURN

:: Deactivate the virtual environment again
:: To be activated on demand through run.bat or devel.bat or manually.
rem This action does not matter really since activate does nothing but
rem setting up environment variables that are be discarded anyway by SETLOCAL
rem but it is a good practice to deactivate explicitly
rem which prevents future surprises if activate starts doing something more than that.
CALL .venv\Scripts\deactivate.bat

ECHO.
ECHO Virtual environment is installed but deliberately not activated.

:: ===============================================================
:RETURN

IF %init.args.no_pause% NEQ 1 ECHO. & PAUSE

EXIT /B %init.ERRORLEVEL%

:: ===========================================================
:: Handles ERRORLEVEL handling boilerplate
:: %* - calee + arguments
:CALL_WRAP

    rem Reset ERRORLEVEL
    CALL cmd /c EXIT 0
    
    CALL %*
    SET "init.ERRORLEVEL=%ERRORLEVEL%" 

EXIT /B %init.ERRORLEVEL%
