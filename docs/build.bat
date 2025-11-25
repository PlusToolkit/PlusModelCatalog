@echo off
REM Build PlusModelCatalog documentation

echo Building PlusModelCatalog Documentation...
echo.

cd /d %~dp0

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -q --upgrade pip
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements
    exit /b 1
)

REM Generate catalog pages
echo.
echo Generating catalog pages from STL files...
python generate_catalog.py --repo-root .. --docs-dir .
if errorlevel 1 (
    echo Failed to generate catalog
    exit /b 1
)

REM Build documentation
echo.
echo Building Sphinx documentation...
sphinx-build -b html . _build/html
if errorlevel 1 (
    echo Failed to build documentation
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo Documentation is in: _build\html
echo ========================================
echo.

REM Open in browser
echo Opening documentation in browser...
start _build\html\index.html

deactivate
