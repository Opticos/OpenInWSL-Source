---
layout: default
title: GWSL Roadmap & Changelog
permalink: /roadmap.html
---

## This is a rough draft

## 1.3.3
First Stable Release

## 1.3.4
*  First Broken Build
*  Added process management stability (No more disappearing windows)
*  Fixed DPI fpr dashboard and tray menu
*  Decreased service cpu usage from 20% to 0.2%
*  Added catch for older versions of windows

## 1.3.5
*  Attempted Build Fix (FAILED)
*  First version with Traditional Installer Support

## 1.3.6
*  Fixed Broken Build
*  Added option to change Dashboard position
*  Changed method of finding Host IP
*  ADD NOTE ON SITE TO SAY FIXED

## 1.3.7 (Future: InDev)
*  PulseAudio Bundle (NEED POC)
*  Add Try/Catch for Colorization (See Log)
*  Add test X button (xclock) (NEED POC & DOCS)
*  Add button to open logs and one to open settings.
*  Add catch to make sure WSL is v2 on 1909. Somehow get rid of support for previous builds. (RESEARCH BUILD NUMBERS)
*  Oh, and also make sure all the registry values exist back then too... Light mode is only so old...
*  Dont let user add export script twice. Debug the script... alot
*  Maybe revert to older script
*  check to see if bash is existing with which to fix problems with other shells. Or just see which shell is default and port or override
*  Add localization with gettext and poedit. Get Volunteers.
*  Update DOCS accordingly.
*  If gwsl closed before service can start, keep service a little longer and try to finish starting service in background
*  Remove "." to specify profile and use -l to start a login shell (it is an L)
*  Add logging for output of linux commands
*  Add settings.json option to pass flags to vcxsrv
*  Make GWSL move with new taskbar positions too...
*  Make shell button also use windows terminal. Put in settings
*  Upload blur to github
*  Get people to port GWSL_helper.sh into more shells
*  Fix localhost typo in title (facepalm)

