@echo off
title Script-Scrapper
set PYTHON=python

if not "%PYTHON%" == "python" (
    set PYTHON=py
)

if exist installer.py (
    %PYTHON% installer.py
    del installer.py
    %PYTHON% main.py
) else (
    %PYTHON% main.py
)