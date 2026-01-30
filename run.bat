@ECHO OFF & SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION & SET "ERRORLEVEL=" & GOTO :MAIN

:: ===========================================================
:HELP

ECHO :: ==========================================================
ECHO :: Runs the LipiMerge application.
ECHO ::
ECHO :: This script initializes the Python environment and starts the application.
ECHO ::
ECHO :: Usage:
ECHO ::   run [options and parameters]
ECHO ::
ECHO :: Options and parameters:
ECHO ::   Options and parameters are passed directly to the LipiMerge Python application.
ECHO ::   Use "run.bat -h" to see the help for the LipiMerge application.
ECHO :: 
ECHO :: ==========================================================

GOTO :RETURN

:: ===========================================================
:MAIN

SET "run.ERRORLEVEL=0"

:: Activate virtual environment

CALL :CALL_WRAP init.bat /N /NP 
IF %run.ERRORLEVEL% NEQ 0 ECHO Failed to initialize the Python environment 1>&2 & GOTO :RETURN

CALL :CALL_WRAP .venv\Scripts\activate.bat
IF %run.ERRORLEVEL% NEQ 0 ECHO Failed to activate virtual environment. 1>&2 & GOTO :RETURN

:: Run
SET "PYTHONPATH=%PYTHONPATH%;src"
SET "PYTHONUTF8=1"
CALL :CALL_WRAP py -m lipimerge %*
IF %run.ERRORLEVEL% NEQ 0 ECHO LipiMerge application failed. 1>&2 & GOTO :RETURN

:: ===============================================================
:RETURN

:: Deactivate virtual environment; if there was an error before, keep it
rem see init.bat for details 
SET "run._errorlevel=%run.ERRORLEVEL%"
CALL :CALL_WRAP .venv\Scripts\deactivate.bat
IF %run.ERRORLEVEL% NEQ 0 ECHO Failed to deactivate virtual environment. 1>&2
IF %run._errorlevel% NEQ 0 SET "run.ERRORLEVEL=%run._errorlevel%"

PAUSE

EXIT /B %run.ERRORLEVEL%

:: ===========================================================
:: Handles ERRORLEVEL handling boilerplate
:: %* - calee + arguments
:CALL_WRAP

    rem Reset ERRORLEVEL
    CALL cmd /c EXIT 0
    
    CALL %*
    SET "run.ERRORLEVEL=%ERRORLEVEL%" 

EXIT /B %run.ERRORLEVEL%
