:: Powershell Windows 10 CLI commands list to apply all environment variables
:: All variables are applied with 'call env.bat' command in CLI

:: Environment
set MACHINE=machine1
set WP_HOST=localhost

:: Verification credentials
set WC_KEY=your_key
set WC_SECRET=your_secret

:: Database credentials
set DB_USER=your_user
set DB_PASSWORD=your_password

:: Required to resolve 'module not found' issues during tests execution
set PYTHONPATH=%{PYTHONPATH}%;C:\Users\<path_to_project_folder>
