@echo off
chcp 65001 >nul

set "VENV_DIR=.venv"

echo Running single test...

python -m pip install --upgrade pip

if not exist %VENV_DIR% (
    python -m venv %VENV_DIR%
    if %ERRORLEVEL% NEQ 0 goto failed_venv
)

call %VENV_DIR%\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 goto failed_activate

pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 goto failed_dependencies

pytest -v -n auto --alluredir=allure-results -m yandex_disk
if %ERRORLEVEL% NEQ 0 goto failed_tests

:: --- Успешное завершение ---
echo.
echo =================================
echo Тесты успешно завершены!
echo =================================
goto end

:: --- Обработка ошибок (Фолбэки) ---
:failed_activate
echo.
echo 🚨 Ошибка: Не удалось активировать виртуальное окружение.
goto error_exit

:failed_dependencies
echo.
echo 🚨 Ошибка: Не удалось установить зависимости.
goto error_exit

:failed_venv
echo.
echo 🚨 Ошибка: Не удалось создать виртуальное окружение.
goto error_exit

:failed_tests
echo.
echo 🚨 Ошибка: Тесты завершились неудачно.
goto error_exit

:error_exit
echo.
pause
exit /b %ERRORLEVEL%

:end
echo.
pause