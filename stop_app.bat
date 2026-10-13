@echo off
rem Stop the AI writing tool that is running in the background (the one listening on port 8501)
powershell -NoProfile -Command "$p = Get-NetTCPConnection -LocalPort 8501 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; if ($p) { $p | ForEach-Object { Stop-Process -Id $_ -Force }; Write-Host 'AI writing tool stopped.' } else { Write-Host 'AI writing tool is not running.' }"
pause
