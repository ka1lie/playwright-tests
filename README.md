Currently created for tests

Main task is do some synthetic test in web site, do some things like clicking on buttons, filling the forms, secure auth, send the result via API and show it by web page with json-likes data (success or not)

How to:
  1. Create ./creds folder
  2. Run generate-key.py ONLY ONE TIME!
  3. Run password-encryption.py and encrypt your password for auth into web site
  4. Run web.py for receive check 
  4. Use the main-secure-auth.py with fill into script your URL and credential filename
  5. Enjoy the result of your check


TODO:
  1. Playwright test runs every X minutes (docker or crontab?)
  2. Playwright test should close after execute to avoid memory leaking (still should be checked)
  3. Playwright test should stdout result in file or curl POST? (READY!)
  4. Web server shoud run forever (READY! just run with nohup command)
  5. Create simple auth to web server (not necessary)
  6. Playwright should use secure auth with encrypted password (READY!)
  7. Python and cred file should be the same
  8. Different web pages on different checkers (one web server with one opened port NOT many of web servers)
