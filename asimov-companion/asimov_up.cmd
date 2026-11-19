@echo off
REM Restore the Asimov companion stack after a Hermes reload.
REM Every service here is local, no credentials, no cloud.
REM Run:  C:\ae\agents\asimov_up.cmd

set HERMES_HOME=C:\Users\yaelm\AppData\Local\hermes
set PY=C:\gpu\Scripts\python.exe
set SC=%HERMES_HOME%\cache\scratch
set NODE=%HERMES_HOME%\tools\node-26.7.0-win32-x64\node.exe
set CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe

echo [1/4] perception server :8162
start "asimov-env" /min "%PY%" "C:\ae\agents\asimov_env.py"

echo [2/4] companion scene   :8161
cd /d "%SC%\webgl-asimov"
start "asimov-scene" /min "%PY%" -m http.server 8161 --bind 127.0.0.1

echo [3/4] Chrome on the RTX :9333
REM --force_high_performance_gpu is the whole unlock: without it ANGLE/D3D11
REM selects the Intel iGPU and the discrete card stays idle.
start "asimov-chrome" "%CHROME%" --headless=new --remote-debugging-port=9333 ^
  --force_high_performance_gpu --use-angle=d3d11 --no-first-run ^
  --no-default-browser-check --user-data-dir="%SC%\chrome-rtx" ^
  http://127.0.0.1:8161/index.html

echo [4/4] VLC truth pane    :8081
start "asimov-vlc" "C:\Program Files\VideoLAN\VLC\vlc.exe" ^
  --extraintf=http --http-host=127.0.0.1 --http-port=8081 ^
  --http-password=asimov --no-video-title-show

echo.
echo Wait ~8s, then verify:
echo   curl http://127.0.0.1:8162/env
echo   curl http://127.0.0.1:8161/index.html
echo   node %SC%\webgl-asimov\companion.mjs status
echo.
echo The robot is a browser companion. It shows anything and grants nothing.
