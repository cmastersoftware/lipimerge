@ECHO OFF & SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION & SET "ERRORLEVEL=" & GOTO :MAIN

:: ===========================================================
:HELP

ECHO :: ==========================================================
ECHO :: Set up the environment for development.
ECHO ::
ECHO :: This script initializes the Python environment, installs development and testing dependencies,
ECHO :: and registeres the application module in the Python environment in the editable mode.
ECHO ::
ECHO :: Usage:
ECHO ::   devel /?
ECHO ::   devel {/A ^| /D ^| /I ^| /U} 
ECHO ::
ECHO :: Options:
ECHO ::   /? Show this help message.
ECHO ::
ECHO ::   /A Activate .venv environment.
ECHO ::      Assumes that the .venv directory exists and is already initialized (see /I).
ECHO ::
ECHO ::   /D Deactivate .venv environment.
ECHO ::      Assumes that the .venv directory exists and is already initialized (see /I).
ECHO ::      Deactivates the virtual environment, but does not change it in any way.
ECHO ::
ECHO ::   /I Initialize the development and test environment.
ECHO ::      Also installs the lipimerge package in editable mode into the .venv.
ECHO ::
ECHO ::   /U Unregister the development and test packages.
ECHO ::      Only unretistering the packages from the virtual environment,
ECHO ::      not removing the .venv directory.
ECHO ::      Seems that the .venv remains polluted by some extra packages
ECHO ::      compared to the pure initialization with the requirements.txt.
ECHO :: 
ECHO :: ==========================================================

GOTO :RETURN

:: ===========================================================
:MAIN

SET "devel.ERRORLEVEL=0"

IF "%~2" NEQ "" (
    ECHO Invalid number of arguments. Run 'devel /?' for help. 1>&2
    SET "devel.ERRORLEVEL=1"
    GOTO :RETURN
)

IF /I "%~1"=="/A" (

    SET "devel.action=activate"
    GOTO :RETURN

) ELSE IF /I "%~1"=="/D" (

    SET "devel.action=deactivate"
    GOTO :RETURN

) ELSE IF /I "%~1"=="/I" (

    rem Install devel virtual environment
    rem Do not reinstall the .venv if already installed
    
    CALL :CALL_WRAP init.bat /N /NP
    IF !devel.ERRORLEVEL! NEQ 0 ECHO Failed to initialize the Python environment 1>&2 & GOTO :RETURN

    CALL :CALL_WRAP .venv\Scripts\activate.bat
    IF !devel.ERRORLEVEL! NEQ 0 ECHO Failed to activate virtual environment. 1>&2 & GOTO :RETURN

    CALL :CALL_WRAP py -m pip install -r requirements-dev.txt
    IF !devel.ERRORLEVEL! NEQ 0 ECHO Failed to install development dependencies 1>&2 & GOTO :RETURN

    CALL :CALL_WRAP py -m pip install -e .
    IF !devel.ERRORLEVEL! NEQ 0 ECHO Failed to install lipimerge package 1>&2 & GOTO :RETURN

    ECHO.
    ECHO Development environment initialized successfully.
    SET "devel.action=activate"
    GOTO :RETURN

) ELSE IF /I "%~1"=="/U" (

    rem Unregister from the virtual environment
    rem Keep the .venv directory, just cleaning it (but see :HELP)

    CALL :CALL_WRAP .venv\Scripts\activate.bat
    IF !devel.ERRORLEVEL! NEQ 0 ECHO Failed to activate virtual environment. 1>&2 & GOTO :RETURN

    CALL :CALL_WRAP py -m pip uninstall -y -r requirements-dev.txt
    IF !devel.ERRORLEVEL! NEQ 0 ECHO Failed to uninstall development dependencies 1>&2 & GOTO :RETURN

    CALL :CALL_WRAP py -m pip uninstall -y lipimerge
    IF !devel.ERRORLEVEL! NEQ 0 ECHO Failed to clean the development environment 1>&2 & GOTO :RETURN

    SET "devel.action=deactivate"
    ECHO.
    ECHO Development environment cleaned successfully.
    GOTO :RETURN
    
) ELSE IF /I "%~1"=="/?" (

    GOTO :HELP

) ELSE (

    ECHO Invalid option. Run 'devel /?' for help. 1>&2
    SET "devel.ERRORLEVEL=1"
    GOTO :RETURN

)

:: ===============================================================
:RETURN

rem SETLOCAL masks the environment variables set by the
rem .\.venv\Scripts\(de)activate.bat 
rem but we want to stay (de)activated after executing this script...
ENDLOCAL & SET "devel.ERRORLEVEL=%devel.ERRORLEVEL%" & SET "devel.action=%devel.action%" 

rem Calling the action cannot be placed inside `IF (...)` or the `devel.ERRORLEVEL` cannot be checked
rem Delayed expansion requires SETLOCAL, which we just said we cannot use here...
IF "%devel.action%"=="" GOTO :SKIP_ACTION

CALL :CALL_WRAP .venv\Scripts\%devel.action%.bat 
IF %devel.ERRORLEVEL% NEQ 0 ECHO An error occurred during the execution of `.venv\Scripts\%devel.action%.bat`. 1>&2

:SKIP_ACTION

PAUSE

SET "devel.ERRORLEVEL=" & SET "devel.action=" & EXIT /B %devel.ERRORLEVEL%

:: ===========================================================
:: Handles ERRORLEVEL handling boilerplate
:: %* - callee + arguments
:CALL_WRAP

    rem Reset ERRORLEVEL
    CALL cmd /c EXIT 0
    
    CALL %*
    SET "devel.ERRORLEVEL=%ERRORLEVEL%" 

EXIT /B %devel.ERRORLEVEL%
