@echo off
REM Script para instalar Python via Microsoft Store
REM Este script abrirá o Microsoft Store para que você possa instalar Python

echo ================================================
echo    Instalador de Python - Microsoft Store
echo ================================================
echo.
echo Este script irá abrir o Microsoft Store para instalar Python.
echo Procure por "Python" e instale a versão mais recente.
echo.
timeout /t 3
echo Abrindo Microsoft Store...
start ms-windows-store://pdp/?productid=9NBLGGH4NNS1
echo.
echo Se a loja não abrir, acesse:
echo https://www.microsoft.com/store/productId/9NBLGGH4NNS1
echo.
pause
