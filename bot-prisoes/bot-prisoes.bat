@echo off
setlocal enabledelayedexpansion
title Criar repositorio e publicar bot-prisoes

echo =======================================
echo   CRIAR REPO NOVO + PUBLICAR

echo =======================================

echo.
set /p GH_USER=Seu usuario GitHub: 
if "%GH_USER%"=="" (
  echo Usuario nao informado.
  pause
  exit /b 1
)

set /p GH_REPO=Nome do novo repositorio [bot-prisoes]: 
if "%GH_REPO%"=="" set GH_REPO=bot-prisoes

set /p GH_TOKEN=GitHub Token (PAT com permissao repo): 
if "%GH_TOKEN%"=="" (
  echo Token nao informado.
  pause
  exit /b 1
)

echo.
set /p GH_PRIVATE=Repositorio privado? (s/n) [s]: 
if "%GH_PRIVATE%"=="" set GH_PRIVATE=s

set IS_PRIVATE=true
if /I "%GH_PRIVATE%"=="n" set IS_PRIVATE=false

echo.
echo Criando repositorio no GitHub...
powershell -NoProfile -Command ^
  "$headers = @{ Authorization = 'Bearer %GH_TOKEN%'; Accept = 'application/vnd.github+json'; 'X-GitHub-Api-Version'='2022-11-28' };" ^
  "$body = @{ name = '%GH_REPO%'; private = [System.Convert]::ToBoolean('%IS_PRIVATE%') } | ConvertTo-Json;" ^
  "try { Invoke-RestMethod -Method Post -Uri 'https://api.github.com/user/repos' -Headers $headers -Body $body | Out-Null; exit 0 } catch { Write-Host $_.Exception.Message; exit 1 }"
if errorlevel 1 (
  echo Falha ao criar repositorio. Verifique token/permissoes.
  pause
  exit /b 1
)

echo.
echo Configurando remoto e enviando arquivos...
set REPO_URL=https://github.com/%GH_USER%/%GH_REPO%.git

git remote remove origin >nul 2>nul
git remote add origin %REPO_URL%
git branch -M main
git add .
git commit -m "chore: publicar bot-prisoes" >nul 2>nul
git push -u origin main
if errorlevel 1 (
  echo Falha no push. Verifique login/permissao.
  pause
  exit /b 1
)

echo.
echo SUCESSO: https://github.com/%GH_USER%/%GH_REPO%
pause
