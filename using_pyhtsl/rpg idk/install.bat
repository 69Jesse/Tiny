@echo off

cd "C:\Users\jesse\Desktop\Hackerman\GitHub\smaller\PyHTSL"
pip install .

cd "C:\Users\jesse\Desktop\Hackerman\GitHub\smaller\Tiny\using_pyhtsl\rpg idk"
set run=%*
if "%run%" == "" (
    exit /b 0
)
python %run%
