@ECHO OFF
TITLE PACKAGE TEMPLATE.exe
CD "%~dp0..\"

:: Read settings into memory
for /f "delims== tokens=1,2" %%I in (settings.config) do set %%I=%%J

:: Call scripts with specific flags passed
:: ALL flags are optional, if none are provided or one is missing
    :: called script will default value to factory value
IF %1==MODE IF %2==console (
        ECHO Script is starting. Just one moment for boot-up
        pythonw -m PKG_DIR "--USRDIR=%USER_DIRECTORY%" "--LOG-OUTPUT=%LOG_OUTPUT%" "--LOG-LEVEL=%LOG_LEVEL%"
) ELSE (
    IF %1==MODE IF %2==hybrid (
        ECHO Script is starting. Just one moment for boot-up
        python -m PKG_DIR "--USRDIR=%USER_DIRECTORY%" "--LOG-OUTPUT=%LOG_OUTPUT%" "--LOG-LEVEL=%LOG_LEVEL%"
        echo Press ENTER to exit && set /p input=
    ) ELSE (
        python -m PKG_DIR --MODE="%2%" "--USRDIR=%USER_DIRECTORY%" "--LOG-OUTPUT=%LOG_OUTPUT%" "--LOG-LEVEL=%LOG_LEVEL%"
        echo Press ENTER to exit && set /p input=
    )
)
