@echo off
title Server Turneu Sah
color 0B
echo.
echo  ============================================
echo    Server Turneu Swiss de Sah
echo  ============================================
echo.
echo  Instalez dependentele (prima rulare e mai lenta)...
call npm install --silent 2>nul
echo  Pornesc serverul...
echo.
node server.js
echo.
echo  Serverul s-a oprit.
pause
