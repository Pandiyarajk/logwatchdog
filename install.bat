@echo off
echo Installing LogWatchdog...
echo.

REM Create application directory
if not exist "%PROGRAMFILES%\LogWatchdog" mkdir "%PROGRAMFILES%\LogWatchdog"

REM Copy executable
copy "dist\LogWatchdog.exe" "%PROGRAMFILES%\LogWatchdog\"

REM Copy configuration files
copy "log_config.ini" "%PROGRAMFILES%\LogWatchdog\"
copy "env_example.txt" "%PROGRAMFILES%\LogWatchdog\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\LogWatchdog.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\LogWatchdog\LogWatchdog.exe'; $Shortcut.Save()"

echo.
echo LogWatchdog has been installed successfully!
echo You can find the application in: %PROGRAMFILES%\LogWatchdog\
echo Desktop shortcut has been created.
echo.
pause
