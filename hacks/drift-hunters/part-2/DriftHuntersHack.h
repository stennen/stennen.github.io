#pragma once

/*
*   This code was created by:
*
*   STENNEN (C), Copyright 2016.
*
*   This file might not be distributed in someone elses name!
*/

#include <Windows.h>
#include <winreg.h>
#include <strsafe.h>

#pragma comment(lib, "Advapi32.lib") // winreg's imports file

#define DRIFT_HUNTERS_PLAYERPREFS_KEY TEXT("SOFTWARE\\studionum43\\Drift Hunters") // Registry key of Drift Hunters PlayerPrefs
#define CMD_INPUT  0x1
#define CMD_BUTTON 0x2