@ECHO off

REM set .bat file curdir to script path, and one above it to venv path (disabled .venv here)
set "SCRIPT_PATH=%~dp0.py\"
set "VENV_PATH=%~dp0"

REM ECHO "%SCRIPT_PATH%"
REM ECHO "%VENV_PATH%"

REM activate venv
call "%VENV_PATH%.venv\Scripts\activate.bat"

REM ECHO Virtual Environment active.

REM call python script
python "%SCRIPT_PATH%new_ascii_generator.py"

:PROMPT
SET /P PROMPT=Would you like to generate a comment now? (y/n): 
IF /I "%PROMPT%"=="y" (
  python "%SCRIPT_PATH%comment_generator.py"
  GOTO END
)
IF /I "%PROMPT%"=="n" GOTO END

ECHO Invalid input, please try again.
GOTO PROMPT

:END
pause