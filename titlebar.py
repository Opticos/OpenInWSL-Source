import win32con
from ctypes import *
import sys

# Structure passed to CreateSolidBrush function
# Represents RGB
class COLORREF(Structure):
    _fields_ = [
    ("byRed", c_byte),
    ("byGreen", c_byte),
    ("byBlue", c_byte)
    ]

# Menu structure used in calls to SetMenuInfo
class MENUINFO(Structure):
    _fields_ = [
    ("cbSize", c_long),
    ("fMask", c_long),
    ("dwStyle", c_long),
    ('cyMax', c_long),
    ("hbrBack", c_long),
    ("dwContextHelpID", c_long),
    ("dwMenuData", c_long)
    ]


def ChangeMenuBarColor(hwnd):
    """
    Changes the background color of the menubar and optionally gives
    different colors to menu items
    """
    user32 = windll.user32
    DrawMenuBar = user32.DrawMenuBar
    GetMenu = user32.GetMenu
    GetSubMenu = user32.GetSubMenu
    GetSystemMenu = user32.GetSystemMenu
    SetMenuInfo = user32.SetMenuInfo
    GetMenuInfo = user32.GetMenuInfo
    gdi32 = windll.gdi32
    CreateSolidBrush = gdi32.CreateSolidBrush
    # Instantiate MENUINFO
    menuinfo = MENUINFO()
    # Important to set the size
    menuinfo.cbSize = sizeof(MENUINFO)
    menuinfo.fMask = win32con.MIM_BACKGROUND
    #if not self.bShadeSubMenus:
    #menuinfo.fMask |= win32con.MIM_APPLYTOSUBMENUS

    menuinfo.hbrBack = CreateSolidBrush(COLORREF(255, 0, 0))
    # Important! Pass *pointer* of the menuinfo instance to the win32 call
    SetMenuInfo(GetMenu(hwnd), pointer(menuinfo))

    menuinfo.fMask = win32con.MIM_BACKGROUND | win32con.MIM_APPLYTOSUBMENUS
    menuinfo.hbrBack = CreateSolidBrush(COLORREF(255, 255, 0))
    SetMenuInfo(GetSubMenu(GetMenu(hwnd), 0), pointer(menuinfo))
    menuinfo.fMask = win32con.MIM_BACKGROUND | win32con.MIM_APPLYTOSUBMENUS
    menuinfo.hbrBack = CreateSolidBrush(COLORREF(128, 255, 128))
    SetMenuInfo(GetSubMenu(GetMenu(hwnd), 1), pointer(menuinfo))


    DrawMenuBar(hwnd)

