:: Powershell Windows10 CLI command to apply all env variables
:: call env.bat

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
set PYTHONPATH=%{PYTHONPATH}%;C:\Users\sbord_iu0ld13\PycharmProjects\ApiPytestRequests\tests_suite
