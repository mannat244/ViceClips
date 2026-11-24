@echo off
title Stream Reel Studio - Viral Clips & Social Auto-Publisher
color 0B
cd /d "D:\Reels"

:MENU
cls
echo ==============================================================================
echo       🔥 STREAM REEL STUDIO: CUT, AUTO-SUBTITLE, APPROVE & POST
echo       Transform Gaming Streams, Podcasts & Videos into Viral Shorts & Reels
echo ==============================================================================
echo   [1] Cut Single Video / Stream (Enter URL - Gaming, Podcast, or IRL)
echo   [2] Batch Process Multiple Links (Process a list of videos at once)
echo   [3] Review & Approve Pending Clips (Review titles, captions & status)
echo   [4] 1-Click Publish Approved Clips (Push to Instagram Reels & Shorts)
echo   [5] Quick Direct Publisher Menu
echo   [6] List All Registered Clips & Analytics
echo   [S] Interactive API Key Setup Wizard (Instagram, YouTube, Cloudinary)
echo   [Q] Quit
echo ==============================================================================
echo.
set /p opt="Select Option [1-6 / S / Q]: "

if /i "%opt%"=="1" goto CUT_STREAM
if /i "%opt%"=="2" goto BATCH_STREAM
if /i "%opt%"=="3" goto REVIEW_CLIPS
if /i "%opt%"=="4" goto POST_CLIPS
if /i "%opt%"=="5" goto QUICK_PUB
if /i "%opt%"=="6" goto LIST_CLIPS
if /i "%opt%"=="S" goto SETUP_WIZARD
if /i "%opt%"=="Q" exit /b
goto MENU

:SETUP_WIZARD
echo.
python clip_master.py setup
echo.
pause
goto MENU

:CUT_STREAM
echo.
echo ------------------------------------------------------------------------------
echo  Enter the YouTube video, stream, or podcast URL:
echo ------------------------------------------------------------------------------
set /p target_url="Paste YouTube URL: "
if "%target_url%"=="" goto MENU

echo.
echo Select Content Mode:
echo   [1] Auto-Detect (Default)
echo   [2] Gaming (Facecam Top 38%% + Gameplay Bottom 62%%)
echo   [3] Podcast / Talk Show (Focused Center Framing + Pop Subtitles)
set /p mode_opt="Select Mode [1-3, default 1]: "

set selected_mode=auto
if "%mode_opt%"=="2" set selected_mode=gaming
if "%mode_opt%"=="3" set selected_mode=podcast

echo.
echo Slicing high-retention standalone moments with animated word-pop subtitles...
python clip_master.py run --url "%target_url%" --mode %selected_mode%
echo.
pause
goto MENU

:BATCH_STREAM
echo.
echo ------------------------------------------------------------------------------
echo  BATCH PROCESSING: Multiple Videos / Streams at once
echo ------------------------------------------------------------------------------
echo   [1] Process batch_links.txt file
echo   [2] Enter comma-separated URLs
set /p batch_choice="Select Batch Input [1 or 2]: "

if "%batch_choice%"=="1" (
    if not exist "batch_links.txt" (
        copy batch_links.example.txt batch_links.txt >nul
        echo Created batch_links.txt. Please add your URLs to it and run again!
        notepad batch_links.txt
        pause
        goto MENU
    )
    python clip_master.py batch --file batch_links.txt
) else (
    set /p batch_urls="Enter URLs separated by comma: "
    if not "%batch_urls%"=="" (
        python clip_master.py batch --urls "%batch_urls%"
    )
)
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
echo Publishing to Instagram Reels and YouTube Shorts...
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
