@echo off
title GTA 6 & Gaming Stream Reel Studio
color 0B
cd /d "D:\Reels"

:MENU
cls
echo ================================================================
echo       🎮 GTA VI & GAMING STREAM REELS STUDIO (1-CLICK)
echo ================================================================
echo   [1] Cut New Stream/Video from YouTube Link (Cut + Store)
echo   [2] Review & Approve Pending Clips
echo   [3] Publish Approved Clips (YouTube Shorts & Instagram Reels)
echo   [4] Quick Interactive Publisher Menu
echo   [5] List All Registered Streams & Clips
echo   [Q] Quit
echo ================================================================
echo.
set /p opt="Select Option [1-5 / Q]: "

if /i "%opt%"=="1" goto CUT_STREAM
if /i "%opt%"=="2" goto REVIEW_CLIPS
if /i "%opt%"=="3" goto POST_CLIPS
if /i "%opt%"=="4" goto QUICK_PUB
if /i "%opt%"=="5" goto LIST_CLIPS
if /i "%opt%"=="Q" exit /b
goto MENU

:CUT_STREAM
echo.
echo ----------------------------------------------------------------
echo  Enter the YouTube livestream or video URL below:
echo ----------------------------------------------------------------
set /p target_url="Paste YouTube URL: "
if "%target_url%"=="" goto MENU
echo.
echo Processing stream and cutting top standalone moments...
python clip_master.py run --url "%target_url%"
echo.
pause
goto MENU

:REVIEW_CLIPS
echo.
python clip_master.py list
echo.
set /p stream_slug="Enter stream folder name to review (e.g. xyaa or techno_gamerz): "
if "%stream_slug%"=="" goto MENU
python clip_master.py review --stream "%stream_slug%"
echo.
set /p approve_choice="Approve all clips in this stream now? (y/n): "
if /i "%approve_choice%"=="y" (
    python clip_master.py approve --stream "%stream_slug%" --clip all
)
echo.
pause
goto MENU

:POST_CLIPS
echo.
python clip_master.py list
echo.
set /p stream_slug="Enter stream folder name to post (e.g. xyaa or techno_gamerz): "
if "%stream_slug%"=="" goto MENU
set /p clip_num="Enter clip ID (1, 2, 3 or 'all'): "
if "%clip_num%"=="" set clip_num=all
echo.
python clip_master.py post --stream "%stream_slug%" --clip %clip_num% --platform all
echo.
pause
goto MENU

:QUICK_PUB
echo.
python auto_publisher.py
echo.
pause
goto MENU

:LIST_CLIPS
echo.
python clip_master.py list
echo.
pause
goto MENU
