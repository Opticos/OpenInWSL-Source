# My New Project... It *is* WSL related. Lets see what happens :)

# Dedicated to the unborn. 

# Copyright Paul-E / Opticos Studios 2021-♾
#print("GO PYTHON!!!")
version = "1.7 MSIX"
lc_name = "Licenses1.txt"
import time
import re


# Here we go

import sys
#import pygame
import os
import subprocess
import random
import logging
import iset
import winreg
#import titlebar
import threading
import webbrowser
import ipaddress
# So this is like a strange descendant of GWSL. Lots of common code.

default_icon = "oiwcenteredsmall.png"#"icon3.png"
default_ico = "icon_centered.ico"
program_name = "OpenInWSL"

#args = sys.argv + ["--r"] + [r"C:\Users\PEF\AppData\Roaming\OpenInWSL\settings.json"]#[r"C:\Users\PEF\Desktop\GWSL-Source\assets\x11-icon.png"]

BUILD_MODE = "WIN32"  # MSIX or WIN32
BUILD_MODE = "MSIX"  # MSIX or WIN32

debug = False



frozen = 'not'
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    frozen = 'ever so'
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))


# region Logging
if debug == True:
    print("debug mode")
    print('we are', frozen, 'frozen')
    print('bundle dir is', bundle_dir)
    print('sys.argv[0] is', sys.argv[0])
    print('sys.executable is', sys.executable)
    print('os.getcwd is', os.getcwd())

asset_dir = bundle_dir + "\\assets\\"

app_path = os.getenv('APPDATA') + f"\\{program_name}\\"

if os.path.isdir(app_path) == False:
    # os.mkdir(app_path)
    print(subprocess.getoutput('mkdir "' + app_path + '"'))
    print("creating appdata directory")



class DuplicateFilter(logging.Filter):

    def filter(self, record):
        # add other fields if you need more granular comparison, depends on your app
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            return True
        return False


logger = logging.Logger(f"{program_name} " + version, level=0)
# logger = logging.getLogger("GWSL " + version)
# Create handlers
f_handler = logging.FileHandler(app_path + 'main.log')

# f_handler.setLevel(10)

f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(f_handler)
logger.addFilter(DuplicateFilter())
# endregion

try:
    iset.path = app_path + "settings.json"

    if os.path.exists(app_path + "\\settings.json") == False:
        iset.create(app_path + "\\settings.json")
        print("creating settings")
    else:
        sett = iset.read()
        if sett["conf_ver"] >= 2:
            if debug == True:
                print("Settings up to date")
        else:
            print("Updating settings")
            old_iset = iset.read()
            iset.create(app_path + "\\settings.json")

            new_iset = iset.read()

            # migrate user settings
            new_iset["backend"] = old_iset["backend"]
            new_iset["acrylic_enabled"] = old_iset["acrylic_enabled"]
            new_iset["theme"] = old_iset["theme"]
            new_iset["assocs"] = old_iset["assocs"]
            try:
                new_iset["hide_donation_reminder"] = old_iset["hide_donation_reminder"]
            except:
                pass
            iset.set(new_iset)


    # Get the script ready
    import wsl_tools as tools

    if os.path.exists(app_path + "GWSL_helper.sh") == False:
        # print("Moving helper script")
        print(subprocess.getoutput('copy "' + bundle_dir + "\\assets\GWSL_helper.sh" + '" "' + app_path + '"'))
    else:
        # make sure the script is up to date
        scr = open(app_path + "GWSL_helper.sh", "r")
        lines = scr.read()
        if "v4" in lines:
            if debug == True:
                print("Script is up to date")
        else:
            print("Updating Script")
            print(subprocess.getoutput('copy "' + bundle_dir + "\\assets\GWSL_helper.sh" + '" "' + app_path + '"'))

    if os.path.exists(app_path + lc_name) == False:
        print("Moving Licenses")
        print(subprocess.getoutput('copy "' + bundle_dir + "\\assets\\" + lc_name + '" "' + app_path + '"'))
except Exception as e:
    logger.exception("Exception occurred - Config generation")
    sys.exit()

tools.script = app_path + "\\GWSL_helper.sh"

enable = """Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\SOFTWARE\Classes\*\shell\Open in WSL]
"Icon"="ic_path"

[HKEY_CURRENT_USER\SOFTWARE\Classes\*\shell\Open in WSL\command]
@="app_path"
"""

disable = """Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\SOFTWARE\Classes\*\shell\Open in WSL]
"Icon"="ic_path"

[-HKEY_CURRENT_USER\SOFTWARE\Classes\*\shell\Open in WSL\command]
@="app_path"


"""

#if app_mode != "MSIX":
try:
    if os.path.exists(app_path + "context.ico") == False:
        print("Moving Context Icon")
        print(subprocess.getoutput('copy "' + bundle_dir + "\\assets\\" + "context.ico" + '" "' + app_path + '"'))
    if BUILD_MODE == "MSIX":
        if os.path.exists(app_path + "\\context_enable.reg") == False:
            with open(app_path + "\\context_enable.reg", "w") as enabler:
                ic_path = app_path.replace("""\\""", """\\\\""") + "context.ico"
                apps_path = os.getenv('LOCALAPPDATA').replace("""\\""", """\\\\""") + """\\\\Microsoft\\\\WindowsApps\\\\oiw.exe %1"""
                enable = enable.replace("ic_path", ic_path)
                enable = enable.replace("app_path", apps_path)
                enabler.write(enable)
                enabler.close()

        if os.path.exists(app_path + "\\context_disable.reg") == False:
            with open(app_path + "\\context_disable.reg", "w") as disabler:
                ic_path = app_path.replace("""\\""", """\\\\""") + "context.ico"
                apps_path = os.getenv('LOCALAPPDATA').replace("""\\""", """\\\\""") + """\\\\Microsoft\\\\WindowsApps\\\\oiw.exe %1"""
                disable = disable.replace("ic_path", ic_path)
                disable = disable.replace("app_path", apps_path)
                disabler.write(disable)
                disabler.close()
    else:
        # WIN32
        if os.path.exists(app_path + "\\context_enable_w32.reg") == False:
            with open(app_path + "\\context_enable_w32.reg", "w") as enabler:
                ic_path = app_path.replace("""\\""", """\\\\""") + "context.ico"
                apps_path = app_path.replace("""\\""", """\\\\""") + "oiw.exe %1"
                enable = enable.replace("ic_path", ic_path)
                enable = enable.replace("app_path", apps_path)
                enabler.write(enable)
                enabler.close()

        if os.path.exists(app_path + "\\context_disable_w32.reg") == False:
            with open(app_path + "\\context_disable_w32.reg", "w") as disabler:
                ic_path = app_path.replace("""\\""", """\\\\""") + "context.ico"
                apps_path = app_path.replace("""\\""", """\\\\""") + "oiw.exe %1"
                disable = disable.replace("ic_path", ic_path)
                disable = disable.replace("app_path", apps_path)
                disabler.write(disable)
                disabler.close()

except:
    logger.exception("Cannot Create .reg for context menu")


try:
    import ctypes
    import platform

    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception as e:
    logger.exception("Exception occurred - Cannot set dpi aware")

# Tkinter Stuff
import tkinter as tk
from tkinter import *
from tkinter import ttk
root = None  # tk.Tk() #this is intensive... import as needed?
# root.withdraw()
from PIL import Image, ImageTk
import PIL
import PIL.ImageTk

import win32gui
import win32con
import win32api

def get_light():
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
        key_value = winreg.QueryValueEx(key, 'AppsUseLightTheme')
        k = int(key_value[0])
        return k
    except:
        return 0

def get_system_light():
    """
    Sets color of white based on Windows registry theme setting
    :return:
    """
    global light, white, accent
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
        key_value = winreg.QueryValueEx(key, 'SystemUsesLightTheme')
        k = int(key_value[0])
        light = False
        white = [255, 255, 255]
        if k == 1:
            light = True
            white = [0, 0, 0]
            #for i in range(3):
            #    if accent[i] > 50:
            #        accent[i] -= 50
        return white, light
    except:
        logger.exception("get l")
        white = [255, 255, 255]
        light = False
        return white, light



default_font = asset_dir + "segoeui.ttf"

import OpticUI as ui

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "4.0.2"

import pygame
# print("whoops")

ui.asset_dir = asset_dir


import animator as anima

#from pygame.locals import *

t = time.perf_counter()
import pygame.gfxdraw

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

ui.init("dpi")  # , tk, root)
from ctypes import wintypes, windll

if int(platform.release()) >= 8:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)

from win32api import GetMonitorInfo, MonitorFromPoint
from pathlib import Path

sett = iset.read()
show_donate = not sett["hide_donation_reminder"]

def runs(distro, command, nolog=False):
    #cmd = '"' + str(command) + '&"'
    cmd = shlex.quote(str(command))
    cmd = "wsl.exe ~ -d " + str(distro) + " . ~/.profile;nohup /bin/sh -c " + cmd + "&"
    #print("runs yay")
    if nolog == False:
        logger.info(f"(runos) WSL SHELL $ {cmd}")
    subprocess.Popen(cmd,
                     shell=True)  # .readlines()
    #print("runs. it would be", cmd)
    return None

    # return wsl_run(distro, command, "runs")



def get_ip(machine):
    """
    Get IP of select WSL instance
    :return:
    """
    # print("get_ip")
    cmd = "wsl.exe -d " + str(
        machine) + ' ' + "/bin/sh -c " + '"' + """(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}')""" + '"'

    # print(cmd)
    result = os.popen(cmd).readlines()[0]

    try:
        result = result.rstrip()
    except:
        pass
    if "nameserver" in result:
        result = result[len("nameserver") + 1:]

    try:
        ipa = ipaddress.ip_address(result)
    except:
        cmd = "wsl.exe -d " + str(
            machine) + ' ' + "/bin/sh -c " + '"' + """echo $(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}')""" + '"'
        result = os.popen(cmd).readlines()[0]
        # result = "localhost"

    # print("ipa", ipa, "ipd")

    # result = runo3(machine, """echo $(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}')""")
    # print("ip", result, "done")
    return result  # [0][:-1]


def get_version(machine):
    try:
        machines = os.popen("wsl.exe -l -v").read()  # lines()
        machines = re.sub(r'[^a-z A-Z0-9_./\n-]', r'', machines).splitlines()
        # machines = machines.splitlines()
        machines2 = []
        wsl_1 = True

        for i in machines:
            b = ''.join(i).split()
            if 'VERSION' in b:
                wsl_1 = False
            if 'NAME' not in b and b != [] and b != None:
                machines2.append(b)
        if wsl_1 == True:
            #print("assuming wsl 1")
            return 1

        for i in machines2:
            if i[0] == machine:
                return int(i[2])
        return 1

    except:
        return 1

import psutil
def spawn_n_run(machine, command):
    #start_t = time.perf_counter()
    #fast = time.perf_counter() - start_time
    #print("lets go")
    ver = get_version(machine)
    sett = iset.read()
    backend = sett["backend"]
    command = command.strip()
    l_mode = ""

    def start_gwsl():
        cancel = False
        try:
            #print("checking for store version")
            proc = subprocess.getoutput("gwsl.exe --r --startup")
            if "not recognized" in proc:
                raise FileNotFoundError

        except:
            #print("No Store Version")
            if os.path.exists(os.getenv('APPDATA') + "\\GWSL\\gwsl.exe"):
                #print("Traditional Version Installed")
                try:
                    subprocess.Popen(os.getenv('APPDATA') + "\\GWSL\\gwsl.exe --r --startup", shell=True)
                except:
                    logger.exception("Cannot start traditional GWSL")
            else:
                #print("No gwsl found")
                logger.info("No GWSL installed. Install or get another xserver")
                cancel = True
                
    try:
        gtk = ""
        qt = ""
        append = ""
        if backend == "x" or backend == "gwsl":
            #print("USING XSERVER")
            if backend == "gwsl":
                #print("gwsl integration enabled")
                #print("For GWSL Integration. Make sure GWSL is running by doing a silent start?")
                
                gwsl_running = False#chk_process.get_running("GWSL_service.exe")
                """
                for p in psutil.process_iter(attrs=["name"]):
                    #print(p)
                    # if p.status() == "running":
                    try:
                        name = p.info['name'].lower()
                        if "gwsl_vcxsrv" in name:
                            gwsl_running = True
                            #print("GWSL is running")
                            break
                    except:
                        continue
                """
                def windowEnumerationHandler(hwnd, top_windows):
                    nonlocal gwsl_running
                    if "SysTrayIconPy" in win32gui.GetWindowText(hwnd):
                        gwsl_running = True

                top_windows = []
                win32gui.EnumWindows(windowEnumerationHandler, top_windows)
               

                if gwsl_running == False:
                    print("Starting GWSL in silent")
                    gw = threading.Thread(target=start_gwsl)
                    gw.daemon=False
                    gw.start()

                    #if cancel == False:
                    test = 0
                    started = False
                    #print("finding")
                    while started == False:
                        for p in psutil.process_iter(["name"]):
                            try:
                                name = p.info['name'].lower()
                                if "gwsl_vcxsrv" in name:
                                    started = True
                                    print("found")
                                    break
                            except:
                                continue
                        if started == False:
                            time.sleep(0.4)
                            test += 1
                            if test > 10:
                                break
            #print("run")
            #fast = time.perf_counter() - start_time
            #print(2, fast)
            else:
                #print("basic x")
                logger.info("Hey, I see you are not using GWSL but are using some other xserver. You should get GWSL :-)")
            if ver == 1:
                # print("check1")
                runs(machine, "DISPLAY=:0 PULSE_SERVER=tcp:localhost " + command,
                     nolog=True)
            else:
                ip = get_ip(machine).strip()
                #print("ready")
                # print("check2")
                runs(machine,
                     "DISPLAY=" + str(ip) + f":0 PULSE_SERVER=tcp:{ip} " + command,
                     nolog=True)
        else:
            #print("USING WSLG")
            runs(machine, command,
                 nolog=True)

    except Exception as e:
        logger.exception("Exception occurred - cannot spawn process")


def w2l(file_path):
    pass

def path_converter(path):
    if "/" in path:
        pt = path.split("/")
    else:
        pt = path.split("\\")
    lin = "/mnt/" + pt[0][0].lower()
    for f in pt[1:]:
        lin += "/" + str(f.lower())
    return lin


#home()





    

def open_help(context):
    #print("helper", context)
    webbrowser.open("https://opticos.github.io/openinwsl/help")

import win32mica
from win32mica import MICAMODE, ApplyMica

#mode = MICAMODE.DARK  # Dark mode mica effect

#from ttkthemes import ThemedStyle

import sv_ttk

def dark_title_bar(window, dark):
    #window.update()

    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ctypes.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2 if dark else 0
    value = ctypes.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ctypes.byref(value), ctypes.sizeof(value))

    root = window
    root.geometry(str(root.winfo_width()+1) + "x" + str(root.winfo_height()+1))
    #Returns to original size
    root.geometry(str(root.winfo_width()-1) + "x" + str(root.winfo_height()-1))


def home():
    #ui.set_icons(asset_dir + "Paper/")
    #k = get_light()

    global root
    if root:
        root.withdraw()
        boxRoot = tk.Toplevel(master=root)  # , fg="red", bg="black")
        boxRoot.withdraw()
    else:
        root = tk.Tk()
        root.withdraw()
        sett = iset.read()
        if sett["theme"] == "dark":
            en = "superhero"
        elif sett["theme"] == "light":
            en = "lumen"
        #style = ThemedStyle(root)
        #style.set_theme("equilux")
        #root.style = style
        #root.style = Style(theme=en)#darkly')
        boxRoot = tk.Toplevel(master=root)

        boxRoot.withdraw()

    #get tkinter hwnd
    hwnd = boxRoot.winfo_id()

    if sett["theme"] == "dark":
        sv_ttk.set_theme("dark")
        mode = win32mica.MICAMODE.DARK
    elif sett["theme"] == "light":
        sv_ttk.set_theme("light")
        mode = win32mica.MICAMODE.LIGHT



    #label = tk.Label(boxRoot, bg='#000000')
    #boxRoot.lift()
    #boxRoot.configure(bg="red")
    #boxRoot.configure(bg="#000000")
    #boxRoot.wm_attributes("-transparent", "#fafafa")
    boxRoot.update()

    HWND = windll.user32.GetParent(boxRoot.winfo_id())

    if sett["theme"] == "dark":
        ApplyMica(HWND, ColorMode=mode)



    #style = Style(theme='superhero')#darkly')
    #boxRoot.style = Style(theme='superhero')#darkly')



    def quitter():
        boxRoot.quit()
        boxRoot.destroy()
        boxRoot.running = False
        # pygame.quit()
        # sys.exit()
        return None

    boxRoot.title("Open In WSL")
    boxRoot.iconname("Dialog")
    WIDTH, HEIGHT = ui.inch2pix(5), ui.inch2pix(5.5)
    boxRoot.minsize(WIDTH, HEIGHT)
    boxRoot.running = True
    boxRoot.protocol("WM_DELETE_WINDOW", quitter)
    boxRoot.geometry('+%d+%d' % (screensize[0] / 2 - WIDTH / 2, screensize[1] / 2 - HEIGHT / 2 - ui.inch2pix(0.5)))
    #boxRoot.configure(background='white')
    #boxRoot.iconphoto(False, tk.PhotoImage(file=asset_dir + default_icon))
    boxRoot.iconbitmap(asset_dir + default_ico)
    # First the label
    frame_0 = ttk.Frame(boxRoot)
    frame_01 = ttk.Frame(frame_0)
    logo = tk.Label(frame_01, text=f"Open In WSL",# font="SunValleyTitleLargeFont",
                       justify=LEFT)
    logo.configure(font=("Segoe UI Semibold",13))
    logo.grid(row=0, pady=0, sticky="WN")

    explain = tk.Label(frame_01, text=f"Make Linux Apps Windows File Handlers ({version})", justify=LEFT)#, font="SunValleySubtitleFont")
    explain.configure(font=("Segoe UI Semibold",10))
    explain.grid(row=1, pady=0, sticky="wS")
    frame_01.grid(row=0, column=1, padx=5, pady=(25, 20), sticky="NW", rowspan=1)  # , columnspan=3)

    imager = Image.open(asset_dir + "oiw6.png")
    # imager = imager.resize([48, 48])

    img = PIL.ImageTk.PhotoImage(imager.resize([60, 60]))#[75, 75]))
    labelm = tk.Label(frame_0, image=img)
    labelm.image = img
    labelm.grid(row=0, column=0, padx=20, pady=(15, 0))
    frame_0.columnconfigure(1, weight=1)

    frame_0.grid(row=0, column=0, padx=10, pady=0, sticky="NEW", rowspan=1)  # , columnspan=3)

    opt_label = ttk.Label(boxRoot, text=" Open In WSL Configuration ", font=("SunValleyBodyLargeFont", 9))

    frame_1 = ttk.LabelFrame(boxRoot, style="Card.TFrame", padding="0.14i", labelwidget=opt_label)#text=" Open In WSL Configuration ", , font="SunValleyBodyStrongFont")

    #opt_label = ttk.Label(frame_1, text="Open In WSL Configuration:")
    #opt_label.grid(row=0, padx=0, pady=10, sticky="w")


    gui_frame = ttk.Frame(frame_1)
    backend = tk.StringVar()
    sett = iset.read()

    backend.set(sett["backend"])
    def set_back():
        sett = iset.read()
        sett["backend"] = backend.get()
        iset.set(sett)
    x_lab = ttk.Label(gui_frame, text="Graphical Backend: ")
    x_lab.grid(column=0, row=0, pady=10, sticky="w")

    gwsl_radio = ttk.Radiobutton(gui_frame, text="GWSL", value='gwsl', variable=backend, command=set_back)#, style=style)
    gwsl_radio.grid(row=0, column=1, sticky="w", ipadx=5)

    wslg_radio = ttk.Radiobutton(gui_frame, text="wslg", value='wslg', variable=backend, command=set_back)
    wslg_radio.grid(row=0, column=2, sticky="w", ipadx=5)

    xserver_radio = ttk.Radiobutton(gui_frame, text="Other XServer", value='x', variable=backend, command=set_back)
    xserver_radio.grid(row=0, column=3, sticky="w", ipadx=5)

    gui_frame.grid(row=1, sticky="w", padx=0)

    acrylic_frame = ttk.Frame(frame_1)
    acrylic = tk.StringVar()
    sett = iset.read()
    if sett["acrylic_enabled"] == True:
        en = 1
    else:
        en = 0
    acrylic.set(en)

    def set_acrylic():
        sett = iset.read()

        sett["acrylic_enabled"] = int(acrylic.get()) == 1
        iset.set(sett)

    x_lab = ttk.Label(acrylic_frame, text="Popup Transparency: ")
    x_lab.grid(column=0, row=0, pady=10, sticky="w")

    gwsl_radio = ttk.Radiobutton(acrylic_frame, text="On", value=1, variable=acrylic, command=set_acrylic)
    gwsl_radio.grid(row=0, column=1, sticky="w", ipadx=5)

    wslg_radio = ttk.Radiobutton(acrylic_frame, text="Off", value=0, variable=acrylic, command=set_acrylic)
    wslg_radio.grid(row=0, column=2, sticky="w", ipadx=5)


    acrylic_frame.grid(row=2, sticky="w", padx=0)


    dark_frame = ttk.Frame(frame_1)
    darkmode = tk.StringVar()
    sett = iset.read()
    if sett["theme"] == "dark":
        en = "dark"
    elif sett["theme"] == "light":
        en = "light"
    else:
        en = "dark"
    darkmode.set(en)

    def set_theme():
        sett = iset.read()
        sett["theme"] = darkmode.get()
        iset.set(sett)
        color = darkmode.get()
        HWND = windll.user32.GetParent(boxRoot.winfo_id())

        #tk.messagebox.showinfo(master=boxRoot, title="Theme Changed", message="Restart Open In WSL to apply changes")
        if darkmode.get() == "dark":
            sv_ttk.use_dark_theme()
            dark_title_bar(boxRoot, True)
            mode = win32mica.MICAMODE.DARK
            ApplyMica(HWND, ColorMode=mode)
        elif darkmode.get() == "light":
            sv_ttk.use_light_theme()
            dark_title_bar(boxRoot, False)
            mode = win32mica.MICAMODE.LIGHT
            #ApplyMica(HWND, ColorMode=mode)
            win32mica.Disable(HWND)





    x_lab = ttk.Label(dark_frame, text="App Theme: ")
    x_lab.grid(column=0, row=0, pady=10, sticky="w")

    dark_radio = ttk.Radiobutton(dark_frame, text="Dark", value='dark', variable=darkmode, command=set_theme)
    dark_radio.grid(row=0, column=1, sticky="w", ipadx=5)

    light_radio = ttk.Radiobutton(dark_frame, text="Light", value='light', variable=darkmode, command=set_theme)
    light_radio.grid(row=0, column=2, sticky="w", ipadx=5)

    #auto_radio = ttk.Radiobutton(dark_frame, text="Auto", value='auto', variable=darkmode, command=set_theme)
    #auto_radio.grid(row=0, column=3, sticky="w", ipadx=5)

    dark_frame.grid(row=3, sticky="w", padx=0)

    def manage():
        #print("opening association manager")
        manage_assoc(parent=boxRoot)

    frame_buttons = ttk.Frame(boxRoot, padding="0.14i") #style="Card.TFrame"

    manage_button = ttk.Button(frame_buttons, text="Manage File Associations", style="secondary.TButton", command=manage)
    manage_button.grid(row=0, column=0, padx=0, pady=10, ipadx=5, sticky="w")

    ########
    frame_22 = ttk.Frame(frame_buttons)
    def config():
        old_pat = os.getcwd()
        os.chdir(app_path)
        #os.popen("notepad service.log")
        os.popen("settings.json")
        os.chdir(old_pat)

    def get_gwsl():
        webbrowser.open("ms-windows-store://pdp/?productid=9nl6kd1h33v3")
    manage_button = ttk.Button(frame_buttons, text="Get GWSL XServer", style="primary.Link.TButton", command=get_gwsl)
    #manage_button.grid(row=0, padx=0, pady=5, ipadx=5, sticky="W", column=0)

    def optic_web():
        webbrowser.open("https://sites.google.com/bartimee.com/opticos-studios/home")

    #manage_button = ttk.Button(frame_22, text="Opticos Website", style="primary.Link.TButton", command=optic_web)
    manage_button.grid(row=0, padx=0, pady=5, ipadx=20, sticky="E", column=2)

    def logs():
        old_pat = os.getcwd()
        os.chdir(app_path)
        os.popen("notepad main.log")
        os.chdir(old_pat)
    #manage_button = ttk.Button(frame_22, text="Logs", style="primary.Outline.TButton", command=logs)
    #manage_button.grid(row=2, padx=5, pady=5, ipadx=0, sticky="e", column=0)

    def license():
        old_pat = os.getcwd()
        os.chdir(app_path)
        #os.popen("notepad service.log")
        os.popen("notepad Licenses1.txt")
        os.chdir(old_pat)
    #manage_button = ttk.Button(frame_22, text="Licenses", style="primary.Outline.TButton", command=license)
    #manage_button.grid(row=1, padx=5, pady=5, ipadx=0, sticky="e", column=0)

    frame_22.columnconfigure(0, weight=1)
    frame_22.columnconfigure(1, weight=1)
    frame_22.columnconfigure(2, weight=1)

    frame_22.grid(row=1, sticky="SEW", columnspan=1, pady=(10, 6))#, padx="0.14i")
    frame_1.columnconfigure(0, weight=1)

    def context():
        try:
            w32 = ""
            if BUILD_MODE == "WIN32":
                w32 = "_w32"
            if contexter.get() == 1:
                print("Enabling")
                #print(subprocess.getoutput(f"regedit /s {app_path}/context_enable{w32}.reg"))
                print(subprocess.getoutput(f"reg import {app_path}/context_enable{w32}.reg"))
            else:
                print("Disabling")
                #print(subprocess.getoutput(f"regedit /s {app_path}/context_disable{w32}.reg"))
                print(subprocess.getoutput(f"reg import {app_path}/context_disable{w32}.reg"))
                
        except:
            logger.exception("cannot toggle context option")

    contexter = tk.IntVar()
    contexter.set(1)
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    try:
        key = winreg.OpenKey(registry, r'SOFTWARE\Classes\*\shell\Open in WSL\command')
        key_value = winreg.QueryValueEx(key, None)

        k = key_value[0]

    except:
        contexter.set(0)



    #contexter.set(1)

    cont_button = ttk.Checkbutton(frame_1, text='Show "Open In WSL" in Explorer Context Menu',  command=context, variable=contexter)
    cont_button.grid(row=4, padx=0, pady=10, ipadx=5, sticky="w")


    # Donation disabling system (11/30/22)
    def hide_donate():
        if donater.get() == 1:
            show_donate = False
            sett = iset.read()
            sett["hide_donation_reminder"] = True
            iset.set(sett)

            donate.grid_forget()

        else:
            show_donate = True
            sett = iset.read()
            sett["hide_donation_reminder"] = False
            iset.set(sett)
            donate.grid(row=3, padx=30, pady=0, ipadx=5, ipady=5, sticky="wE")


    donater = tk.IntVar()
    donater.set(1)
    try:
        sett = iset.read()
        print(sett["hide_donation_reminder"])
        donater.set(1 if sett["hide_donation_reminder"] else 0)

    except:
        donater.set(0)


    ad_button = ttk.Checkbutton(frame_1, text='Disable Donation Reminders', command=hide_donate,
                                  variable=donater)
    ad_button.grid(row=5, padx=0, pady=10, ipadx=5, sticky="w")

    """
    autolaunch = tk.IntVar()
    sett = iset.read()
    if sett["start_gwsl"] == True:
        ent = 1
    else:
        ent = 0

    def launch_gwsl():
        sett = iset.read()
        sett["start_gwsl"] = autolaunch.get() == 1
        iset.set(sett)

    autolaunch.set(ent)


    cont_button = ttk.Checkbutton(frame_1, text='Auto-Launch GWSL (Sometimes Slower)',  command=launch_gwsl, variable=autolaunch)
    cont_button.grid(row=5, padx=0, pady=10, ipadx=5, sticky="w")
    """
    #frame_1.columnconfigure(1, weight=1)
    frame_1.grid(row=1, column=0, padx="0.25i", pady=10, sticky="NEW")  # , columnspan=3)

    frame_buttons.columnconfigure(0, weight=2)

    frame_buttons.grid(row=2, column=0, padx="0.11i", pady=0, sticky="NEWS")

    def donate():
        webbrowser.open_new("https://opticos.github.io/openinwsl/#donate")
    donate = ttk.Button(boxRoot, text="Please Consider Donating 💖", style="Accent.TButton", command=donate) # old for bootstrapstyle="success.TButton"

    if show_donate:
        donate.grid(row=3, padx=30, pady=0, ipadx=5, ipady=5, sticky="wE")

    #frame_2.columnconfigure(1, weight=1)
    #frame_2.grid(row=2, column=0, padx=20, pady=20, sticky="NWE")#, columnspan=4)
    #frame_2.grid_columnconfigure(1, weight=1)

    frame_3 = ttk.Frame(boxRoot)#, borderwidth=3, relief="ridge")
    cancel = ttk.Button(frame_3, text="Opticos Website", style="secondary.TButton", command=optic_web)
    cancel.grid(row=0, column=0, sticky="We", padx=5, ipadx=5)

    manage_button = ttk.Button(frame_3, text="Configuration File", style="primary.Outline.TButton", command=config)
    manage_button.grid(row=0, padx=5, pady=5, ipadx=5, sticky="we", column=1)


    manage_button = ttk.Button(frame_3, text="Licenses", style="primary.Outline.TButton", command=license)
    manage_button.grid(row=0, padx=5, pady=5, ipadx=0, sticky="we", column=2)

    manage_button = ttk.Button(frame_3, text="Logs", style="primary.Outline.TButton", command=logs)
    manage_button.grid(row=0, padx=5, pady=5, ipadx=0, sticky="We", column=3)



    def helper():
        open_help("home")
    help = ttk.Button(frame_3, text="Help", command=helper)
    help.grid(row=0, column=4, sticky="wE", padx=5, ipadx=5)



    #apply = ttk.Button(frame_3, text="Save Configuration", style="success.TButton")
    #apply.grid(row=0, column=2, sticky="WE", padx=5, ipadx=5)

    frame_3.columnconfigure(0, weight=1)
    frame_3.columnconfigure(4, weight=1)


    frame_3.columnconfigure(1, weight=1)
    frame_3.columnconfigure(2, weight=1)
    frame_3.columnconfigure(3, weight=1)

    frame_3.grid(row=4, column=0, padx=25, pady=(20, 23), sticky="SWE")
    #HWN = root.winfo_id()
    #titlebar.ChangeMenuBarColor(HWN)
    #boxRoot.overrideredirect(True)
    #lbl = tk.Label(boxRoot, text="Create a Start Menu Shortcut:", justify=CENTER)  # , font=("Helvetica", 16))
    #lbl.grid(row=0, padx=10, pady=10, sticky="EW")
    #boxRoot.grid_rowconfigure(0, weight=0)

    #boxRoot.bind("<Return>", login)
    boxRoot.columnconfigure(0, weight=1)
    boxRoot.rowconfigure(2, weight=1)


    if sett["theme"] == "dark":
        dark_title_bar(boxRoot, True)
    elif sett["theme"] == "light":
        dark_title_bar(boxRoot, False)

    boxRoot.deiconify()
    #boxRoot.wm_attributes("-topmost", 1)
    #boxRoot.mainloop()


    boxRoot.update()
    boxRoot.minsize(boxRoot.winfo_width(), boxRoot.winfo_height())
    #boxRoot.geometry('+%d+%d' % (screensize[0] / 2 - boxRoot.winfo_width() / 2,
    #                             screensize[1] / 2 - boxRoot.winfo_height() / 2 - ui.inch2pix(0.5)))

    #HWND = windll.user32.GetParent(boxRoot.winfo_id())
    #if sett["theme"] == "dark":
    #    win32mica.ApplyMica(HWND, mode)

    while True:
        # draw(canvas, mouse=False)
        boxRoot.update()
        if boxRoot.running == False:
            break
        time.sleep(0.05)


def create(extension, test_file=False, comd=None, machine=None):
    #ui.set_icons(asset_dir + "Paper/")
    #k = get_light()
    pre_machine = machine
    global root
    if root:
        root.withdraw()
        boxRoot = tk.Toplevel(master=root)  # , fg="red", bg="black")
        boxRoot.withdraw()
    else:
        root = tk.Tk()
        root.withdraw()
        sett = iset.read()
        if sett["theme"] == "dark":
            en = "superhero"

        elif sett["theme"] == "light":
            en = "lumen"

        #root.style = Style(theme=en)  # darkly')
        boxRoot = tk.Toplevel(master=root)


        boxRoot.withdraw()

    sett = iset.read()
    if sett["theme"] == "dark":
        sv_ttk.set_theme("dark")
    elif sett["theme"] == "light":
        sv_ttk.set_theme("light")

    boxRoot.update()

    HWND = windll.user32.GetParent(boxRoot.winfo_id())

    if sv_ttk.get_theme() == "dark":
        ApplyMica(HWND, ColorMode=win32mica.MICAMODE.DARK)
    else:
        win32mica.Disable(HWND)
        boxRoot.update()


    #style = Style(theme='superhero')#darkly')
    #boxRoot.style = Style(theme='superhero')#darkly')


    def quitter():
        boxRoot.quit()
        boxRoot.destroy()
        boxRoot.running = False
        # pygame.quit()
        # sys.exit()
        return None

    boxRoot.title("Association Editor")
    boxRoot.iconname("Dialog")
    WIDTH, HEIGHT = ui.inch2pix(5), ui.inch2pix(4)
    boxRoot.minsize(WIDTH, HEIGHT)
    boxRoot.running = True
    boxRoot.protocol("WM_DELETE_WINDOW", quitter)
    boxRoot.geometry('+%d+%d' % (screensize[0] / 2 - WIDTH / 2, screensize[1] / 2 - HEIGHT / 2 - ui.inch2pix(0.5)))
    #boxRoot.configure(background='white')
    #boxRoot.iconphoto(False, tk.PhotoImage(file=asset_dir + default_icon))
    boxRoot.iconbitmap(asset_dir + default_ico)
    # First the label
    """
    explain = tk.Label(boxRoot, text=f"You have chosen OpenInWSL to open a {extension} file. \n\nHow do you want to handle this file type?")
    explain.grid(row=0, column=0, padx=10, pady=20, sticky="NEW", rowspan=1)#, columnspan=3)


    """
    frame_0 = ttk.Frame(boxRoot)
    explain = tk.Label(frame_0, text=f"You have chosen OpenInWSL to open a {extension} file.\nHow do you want to handle this file type?", justify=LEFT)
    explain.grid(row=0, column=1, padx=10, pady=20, sticky="NW", rowspan=1)  # , columnspan=3)
    imager = Image.open(asset_dir + "linkedit.png")
    # imager = imager.resize([48, 48])

    img = PIL.ImageTk.PhotoImage(imager.resize([50, 50]))
    labelm = tk.Label(frame_0, image=img)
    labelm.image = img
    labelm.grid(row=0, column=0, padx=10, pady=10)
    frame_0.columnconfigure(1, weight=1)

    frame_0.grid(row=0, column=0, padx=10, pady=0, sticky="NEW", rowspan=1)  # , columnspan=3)

    frame_1 = ttk.Frame(boxRoot)  # , padding="0.15i")

    selector_label = ttk.Label(frame_1, text="WSL Distro:")
    selector_label.grid(row=0, column=0, padx=10, pady=0, sticky="W", rowspan=1)

    machines = os.popen("wsl.exe -l -q").read()
    machines = re.sub(r'[^a-zA-Z0-9_./\n-]', r'', machines).splitlines()
    machines[:] = (value for value in machines if value != "")


    if len(machines) > 1:
        # animator.animate("start", [0, 0])
        machine_chooser = ttk.Combobox(frame_1, values=machines, state="readonly")
        machine_chooser.current(0)

    elif len(machines) == 1:
        # animator.animate("start", [0, 0])
        machine_chooser = ttk.Label(frame_1, text=machines[0])
        machine = machines[0]

    else:
        pymsgbox.alert(text='No WSL Distros Found', title='Please Install a WSL Distro', button='OK')
        quitter()
        return None

    machine_chooser.grid(row=0, column=1, padx=0, pady=20, sticky="WE", rowspan=1, columnspan=2)

    if pre_machine != None:
        try:
            machine_chooser.set(pre_machine)
        except:
            machine_chooser["text"] = pre_machine



    cmd_label = ttk.Label(frame_1, text="Command:  ")
    cmd_label.grid(row=1, column=0, padx=10, pady=0, sticky="WE", rowspan=1)

    cmd = ttk.Entry(frame_1, width=20)
    cmd.focus_force()
    if comd != None:
        cmd.insert(0, comd)

    cmd.grid(row=1, column=1, padx=0, pady=0, sticky="WE", rowspan=1)

    def app_choose():
        nonlocal machine
        try:
            mach = machine_chooser.get()
        except:
            mach = machine
        app = applist(mach)
        if app != None:
            cmd.delete(0, 'end')
            cmd.insert(0, app[1]["cmd"])

    def saver():
        nonlocal machine
        try:
            sett = iset.read()
            #print("b", cmd.get(), cmd.get().strip())
            cmd_s = cmd.get()
            if cmd_s.startswith(" ") or cmd_s.endswith(" "):
                cmd_s = cmd_s.strip()
                cmd.delete(0, 'end')
                cmd.insert(0, cmd_s)
            if cmd_s.strip() != "":
                if "#fpth#" not in cmd_s:
                    cmd_s += " #fpth#"
                sett["assocs"][extension] = {"distro": None, "command": None}
                try:
                    mach = machine_chooser.get()
                except:
                    mach = machine
                sett["assocs"][extension]["distro"] = mach
                sett["assocs"][extension]["command"] = cmd_s
                iset.set(sett)
                quitter()
            #elif "#fpth#" not in cmd.get() and cmd.get() != "":
            #    tk.messagebox.showinfo(master=boxRoot, title="Command Helper",
            #                           message=f"Your command must contain #fpth#. ")
        except:
            logger.exception("cannot save edited assoc")
    chooser = ttk.Button(frame_1, text="App List", style="secondary.TButton", command=app_choose)
    chooser.grid(row=1, column=2, padx=(15, 0), pady=0, sticky="ENS", rowspan=1, columnspan=1)
    frame_1.rowconfigure(1, weight=2)

    cmd_label = ttk.Label(frame_1, text="* If using custom arguments, use the #fpth# variable in \nplace of the file path.") #" * Variable #fpth# replaced with filename being opened."
    cmd_label.grid(row=2, column=1, padx=10, pady=10, sticky="W", columnspan=2)

    cmd_label = ttk.Label(frame_1,
                          text="Example: gedit --new-window #fpth#")  # " * Variable #fpth# replaced with filename being opened."
    cmd_label.configure(font=("Segoe UI Light", 10))
    cmd_label.grid(row=3, column=1, padx=10, pady=0, sticky="WN", columnspan=2)
    def manpage():
        nonlocal cmd
        try:
            app = cmd.get().strip().split(" ")[0]
            if app != "":
                webbrowser.open(f"https://man.cx/{app}")
        except:
            logger.exception("cannot launch manpage func")
    man = ttk.Button(frame_1, text="See Command Manpage", command=manpage, style="info.TButton")
    man.grid(row=4, column=1, padx=0, pady=35, ipadx=5, sticky="E", rowspan=1, columnspan=2)

    frame_1.columnconfigure(1, weight=1)
    frame_1.grid(row=1, column=0, padx=20, pady=10, sticky="NEW")  # , columnspan=3)

    #frame_2.columnconfigure(1, weight=1)
    #frame_2.grid(row=2, column=0, padx=20, pady=20, sticky="NWE")#, columnspan=4)
    #frame_2.grid_columnconfigure(1, weight=1)

    frame_3 = ttk.Frame(boxRoot)#, borderwidth=3, relief="ridge")
    cancel = ttk.Button(frame_3, text="Cancel", style="warning.TButton", command=quitter)
    cancel.grid(row=0, column=0, sticky="WE", padx=5, ipadx=5)

    def helper():
        open_help("create")
    help = ttk.Button(frame_3, text="Help", command=helper)
    help.grid(row=0, column=1, sticky="WE", padx=5, ipadx=5)

    column = 2
    def tester():
        nonlocal machine
        try:
            cmd_s = cmd.get()
            if cmd_s.startswith(" ") or cmd_s.endswith(" "):
                cmd_s = cmd_s.strip()
                cmd.delete(0, 'end')
                cmd.insert(0, cmd_s)
            if cmd_s.strip() != "":
                if "#fpth#" not in cmd_s:
                    cmd_s += " #fpth#"

            pather = path_converter(file)
            pather = shlex.quote(pather)
            command = str(cmd_s.replace("#fpth#", pather))
            try:
                mach = machine_chooser.get()
            except:
                mach = machine
            machine = mach

            #command = str(cmd_s.replace("#fpth#", "'" + path_converter(test_file) + "'"))
            logger.info("RUN TEST: " + str(command))
            #spawn_n_run(machine, command)
            try:
                st = threading.Thread(target=spawn_n_run, args=[machine, command])
                # st.daemon=True
                st.start()
            except:
                logger.exception("cannot spawn n run")

            try:
                #print("ext", extension)
                splash(extension, cmd_s.split(" ")[0], machine)
            except:
                logger.exception("Cannot run splash for test config... not a problem.")
        except:
            logger.exception("Cannot test association")

    test = ttk.Button(frame_3, text="Test Configuration", style="secondary.TButton", command=tester)
    if test_file != False:
        test.grid(row=0, column=2, sticky="WE", padx=5, ipadx=5)
        column += 1
        frame_3.columnconfigure(3, weight=1)
    apply = ttk.Button(frame_3, text="Save Configuration", style="success.TButton", command=saver)
    apply.grid(row=0, column=column, sticky="WE", padx=5, ipadx=5)

    frame_3.columnconfigure(0, weight=1)
    frame_3.columnconfigure(1, weight=1)
    frame_3.columnconfigure(2, weight=1)

    frame_3.grid(row=3, column=0, padx=20, pady=20, sticky="SWE")
    #HWN = root.winfo_id()
    #titlebar.ChangeMenuBarColor(HWN)
    #boxRoot.overrideredirect(True)
    #lbl = tk.Label(boxRoot, text="Create a Start Menu Shortcut:", justify=CENTER)  # , font=("Helvetica", 16))
    #lbl.grid(row=0, padx=10, pady=10, sticky="EW")
    #boxRoot.grid_rowconfigure(0, weight=0)

    if sv_ttk.get_theme() == "dark":
        dark_title_bar(boxRoot, True)
    elif sv_ttk.get_theme() == "light":
        dark_title_bar(boxRoot, False)

    #boxRoot.bind("<Return>", login)
    boxRoot.columnconfigure(0, weight=1)
    boxRoot.rowconfigure(2, weight=1)
    boxRoot.deiconify()
    #boxRoot.wm_attributes("-topmost", 1)

    old = sv_ttk.get_theme()
    while True:
        if sv_ttk.get_theme() == "light" and old == "dark":
            win32mica.Disable(HWND)
            #print("DisableMica")
            dark_title_bar(boxRoot, False)
        elif sv_ttk.get_theme() == "dark" and old == "light":
            #print("enableMica")
            ApplyMica(HWND, win32mica.MICAMODE.DARK)
            dark_title_bar(boxRoot, True)

        old = sv_ttk.get_theme()
        # draw(canvas, mouse=False)
        time.sleep(0.05)
        boxRoot.update()
        if boxRoot.running == False:
            break

def applist(machine):
    ui.set_icons(asset_dir + "Paper/")
    #k = get_light()
    selected = None
    app_list = []
    app_dict = {}
    loading = True
    def get_apps():
        nonlocal app_list, app_dict, loading
        try:
            read = tools.get_apps(machine, logger=logger)
            apper = {}
            for i in read:
                name = i[0].lower() + i[1:]
                cmd = read[i]["cmd"]
                # if " " in cmd:
                #    cmd = cmd.split(" ")[0] #Hope this was here for a reason...

                if ' ' in cmd and '"' in cmd:
                    # print("replace", cmd)
                    cmd = cmd.replace('"', "'")  # this fixes paths in commands
                    ## nope cmd = cmd.replace(" ", "\\ ")

                if "%" in cmd:
                    cmd = cmd[:cmd.index("%")]
                if "gnome-control-center" in cmd or "gnome-session-properties" in cmd:
                    continue
                ico_name = read[i]["ico"]
                if ico_name == None or "." in ico_name:
                    ico_name = name
                icon = ui.icon_path(ico_name)
                """
                imag = Image.open(asset_dir + "applist2.png")
                img = PIL.ImageTk.PhotoImage(imag.resize([50, 50]))
                icon_Label = tk.Label(frame_0, image=img)
                icon_label.image = img
                """

                apper.update({name: {"icon": icon, "cmd": cmd}})

            app_dict = apper
            apps = apper
            app_list = list(apps)
            app_list.sort()
            #print(app_dict)
            loading = False
        except:
            logger.exception(f"Cannot load apps... for machine {machine}")
    global root

    if root:
        root.withdraw()
        boxRoot = tk.Toplevel(master=root)  # , fg="red", bg="black")
        boxRoot.withdraw()
    else:
        root = tk.Tk()
        root.withdraw()
        root.style = Style(theme='superhero')  # darkly')
        boxRoot = tk.Toplevel(master=root)
        boxRoot.withdraw()

    #style = Style(theme='superhero')#superhero or lumen')
    #boxRoot = style.master

    if sv_ttk.get_theme() == "dark":
        dark_title_bar(boxRoot, True)
    elif sv_ttk.get_theme() == "light":
        dark_title_bar(boxRoot, False)

    boxRoot.update()
    HWND = windll.user32.GetParent(boxRoot.winfo_id())

    if sv_ttk.get_theme() == "dark":
        ApplyMica(HWND, ColorMode=win32mica.MICAMODE.DARK)
    else:
        win32mica.Disable(HWND)
        boxRoot.update()

    def quitter():
        boxRoot.quit()
        boxRoot.destroy()
        boxRoot.running = False
        # pygame.quit()
        # sys.exit()
        return None

    def select_app(name):
        nonlocal selected
        selected = [name, app_dict[name]]
        quitter()

    boxRoot.title(f"Apps on {machine}")
    boxRoot.iconname("Dialog")
    WIDTH, HEIGHT = ui.inch2pix(5), ui.inch2pix(6)
    boxRoot.minsize(WIDTH, HEIGHT)
    #boxRoot.resizable(False, False)
    boxRoot.running = True
    boxRoot.protocol("WM_DELETE_WINDOW", quitter)
    boxRoot.geometry('+%d+%d' % (screensize[0] / 2 - WIDTH / 2, screensize[1] / 2 - HEIGHT / 2 - ui.inch2pix(0.5)))
    #boxRoot.configure(background='white')
    #boxRoot.iconphoto(False, tk.PhotoImage(file=asset_dir + default_icon))
    boxRoot.iconbitmap(asset_dir + default_ico)
    
    app_loader = threading.Thread(target=get_apps)
    app_loader.daemon = True
    app_loader.start()

    # First the label
    frame_0 = ttk.Frame(boxRoot)
    explain = tk.Label(frame_0, text=f"Apps installed on {machine}.\nSelect an app to continue.", justify=LEFT)
    explain.grid(row=0, column=1, padx=10, pady=20, sticky="NW", rowspan=1)#, columnspan=3)
    imager = Image.open(asset_dir + "applist2.png")
    # imager = imager.resize([48, 48])

    img = PIL.ImageTk.PhotoImage(imager.resize([50, 50]))
    labelm = tk.Label(frame_0, image=img)
    labelm.image = img
    labelm.grid(row=0, column=0, padx=10, pady=10)
    frame_0.columnconfigure(1, weight=1)

    frame_0.grid(row=0, column=0, padx=10, pady=0, sticky="NEW", rowspan=1)#, columnspan=3)

    frame_1 = ttk.Frame(boxRoot)#, borderwidth=2, relief="solid")#, pflatadding="0.15i")

    #list_frame = ttk.Frame(frame_1)#, borderwidth=3, relief="ridge")
    list_canvas = tk.Canvas(frame_1, bd=0, relief="groove", highlightthickness=0, highlightbackground="black")#, borderwidth=0, background="#ffffff")
    list_canvas.focus_force()
    list_canvas.grid(column=0, row=0, sticky="NWSE")

    list_frame = ttk.Frame(list_canvas)#, borderwidth=2, relief="solid")

    load_msg = ttk.Label(list_frame, text="Loading...")
    load_msg.grid(sticky="ews")

    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        #list_frame.configure(width=canvas.winfo_width())
    list_frame.bind("<Configure>", lambda event, canvas=list_canvas: onFrameConfigure(list_canvas))
    list_frame.configure()
    list_frame.columnconfigure(0, weight=1)

    def FrameWidth(event):
        #list_canvas.configure(scrollregion=list_canvas.bbox("all"))

        canvas_width = event.width
        list_canvas.itemconfig(1, width=canvas_width - 20)

        #boxRoot.update()
    list_canvas.bind('<Configure>', FrameWidth)



    scroller = ttk.Scrollbar(frame_1, command=list_canvas.yview)
    list_canvas.configure(yscrollcommand=scroller.set)
    list_canvas.create_window((4, 4), window=list_frame, anchor="center")


    scroller.grid(column=1, row=0, sticky="NES", padx=5, pady=5)

    frame_1.columnconfigure(0, weight=1)
    frame_1.rowconfigure(0, weight=1)

    def bound_to_mousewheel(event):
        frame_1.bind_all("<MouseWheel>", on_mousewheel)

    def unbound_to_mousewheel(event):
        frame_1.unbind_all("<MouseWheel>")

    def on_mousewheel(event):
        list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    frame_1.bind('<Enter>', bound_to_mousewheel)
    frame_1.bind('<Leave>', unbound_to_mousewheel)



    frame_1.grid(row=1, column=0, padx=20, sticky="NEWS")#, columnspan=3)
    #frame_1.grid_columnconfigure(2, weight=1)




    frame_3 = ttk.Frame(boxRoot)#, borderwidth=3, relief="ridge")
    cancel = ttk.Button(frame_3, text="Cancel", style="warning.TButton", command=quitter)
    cancel.grid(row=0, column=0, sticky="W", padx=5)

    def helper():
        open_help("applist")
    help = ttk.Button(frame_3, text="Help", command=helper)
    help.grid(row=0, column=1, sticky="E", padx=5)

    #test = ttk.Button(frame_3, text="Test Configuration", style="secondary.TButton")
    #test.grid(row=0, column=2, sticky="EW", padx=5)

    #apply = ttk.Button(frame_3, text="Save Configuration", style="success.TButton")
    #apply.grid(row=0, column=3, sticky="E", padx=5)

    frame_3.columnconfigure(2, weight=1)
    frame_3.grid(row=2, column=0, padx=20, pady=20, sticky="SWE")
    #HWN = root.winfo_id()
    #titlebar.ChangeMenuBarColor(HWN)
    #boxRoot.overrideredirect(True)
    #lbl = tk.Label(boxRoot, text="Create a Start Menu Shortcut:", justify=CENTER)  # , font=("Helvetica", 16))
    #lbl.grid(row=0, padx=10, pady=10, sticky="EW")
    #boxRoot.grid_rowconfigure(0, weight=0)

    #boxRoot.bind("<Return>", login)
    boxRoot.columnconfigure(0, weight=1)
    boxRoot.rowconfigure(1, weight=1)
    boxRoot.deiconify()
    #boxRoot.wm_attributes("-topmost", 1)
    done = False

    old = sv_ttk.get_theme()
    while True:
        if sv_ttk.get_theme() == "light" and old == "dark":
            win32mica.Disable(HWND)
            #print("DisableMica")
            dark_title_bar(boxRoot, False)
        elif sv_ttk.get_theme() == "dark" and old == "light":
            #print("enableMica")
            ApplyMica(HWND, win32mica.MICAMODE.DARK)
            dark_title_bar(boxRoot, True)

        old = sv_ttk.get_theme()

        # draw(canvas, mouse=False)
        #time.sleep(0.05)
        boxRoot.update()
        if loading == False and done == False:
            load_msg.destroy()
            for app_num in range(len(app_list)):
                app = app_list[app_num]
                app_frame = ttk.Frame(list_frame)
                imag = Image.open(app_dict[app]["icon"])
                img = PIL.ImageTk.PhotoImage(imag.resize([48, 48]))
                icon_label = tk.Label(app_frame, image=img)
                icon_label.image = img
                icon_label.grid(row=0, column=0, sticky="WNE", padx=10, pady=10)


                app_name = ttk.Label(app_frame, text=app[0].upper() + app[1:])
                app_name.grid(row=0, column=1, padx=5, pady=10, sticky="we")

                app_button = ttk.Button(app_frame, text="Select", style="success.TButton", command=lambda j=app: select_app(j))
                app_button.grid(row=0, column=2, padx=10, pady=10, sticky="E")
                app_frame.columnconfigure(1, weight=1)

                app_frame.grid(row=app_num, sticky="NWE")

            done = True
            boxRoot.update()
            list_canvas.yview_moveto(0.0)
            boxRoot.update()

        if boxRoot.running == False:
            break
    return selected



def manage_assoc(parent=None):
    ui.set_icons(asset_dir + "Paper/")
    #k = get_light()
    associations = {}
    def assoc_read():
        nonlocal associations
        associations = iset.read()["assocs"]

    assoc_read()
    global root
    #root = parent
    if root:
        root.withdraw()
        boxRoot = tk.Toplevel(master=root)  # , fg="red", bg="black")
        boxRoot.withdraw()
        #print("Exists")
    else:
        root = tk.Tk()
        root.withdraw()
        root.style = Style(theme='superhero')  # darkly')
        boxRoot = tk.Toplevel(master=root)
        boxRoot.withdraw()
        #print("ss")

    if sv_ttk.get_theme() == "dark":
        dark_title_bar(boxRoot, True)
    elif sv_ttk.get_theme() == "light":
        dark_title_bar(boxRoot, False)

    #style = Style(theme='superhero')#superhero or lumen')
    #boxRoot = style.master
    boxRoot.update()

    HWND = windll.user32.GetParent(boxRoot.winfo_id())

    if sv_ttk.get_theme() == "dark":
        ApplyMica(HWND, ColorMode=win32mica.MICAMODE.DARK)
    else:
        win32mica.Disable(HWND)
        boxRoot.update()


    def quitter():
        boxRoot.quit()
        boxRoot.destroy()
        boxRoot.running = False
        #root.deiconify()
        # pygame.quit()
        # sys.exit()
        return None

    def select_app(name):
        nonlocal done
        try:
            attrib = associations[name]
            #boxRoot.wm_attributes("-topmost", 0)
            create(extension=name, comd=attrib["command"], machine=attrib["distro"])
            assoc_read()
            done = False
            #boxRoot.wm_attributes("-topmost", 1)

            #quitter()
        except:
            logger.exception("cannot edit assoc")

    def delete_app(name):
        nonlocal done
        choice = pymsgbox.confirm(text=f"Delete Association: {name}?",
                                  title="Delete Association?",
                                  buttons=["Yes", "No"])

        try:
            if choice == "Yes":
                sett = iset.read()
                sett["assocs"].pop(name)
                iset.set(sett)
                #time.sleep(1)
                assoc_read()
                done = False
                boxRoot.update()
        except:
            logger.exception("cannot delete assoc")

        #quitter()

    def add_app():
        global root
        nonlocal done
        extension = None
        sett = iset.read()
        assocs = sett["assocs"]
        try:
            while extension == None:
                answer = tk.simpledialog.askstring("Extension Input", "What File Extension? (eg .txt)",
                                            parent=boxRoot)
                answer = str(answer).lower()

                if answer == "" or answer == "none":
                    return None
                if answer.startswith("."):
                    if answer not in assocs:
                        extension = answer
                    else:
                        tk.messagebox.showinfo(master=boxRoot, title="Association Already Exists",
                                               message=f"You already have an association for {answer} files.")
                        return None
                else:
                    tk.messagebox.showinfo(master=boxRoot, title="Invalid Extension",
                                           message=f"Invalid File Extension: {answer}. Extensions must begin with a dot!")

                    #choice = pymsgbox.confirm(text=f"Invalid File Extension: {answer}. Must begin with a dot!",
                    #                          title="Invalid Extension",
                    #                          buttons=["Ok"])
            create(extension.strip())
            assoc_read()
            done = False
            boxRoot.update()
        except:
            logger.exception("cannot add assoc")

    boxRoot.title(f"Association Manager")
    boxRoot.iconname("Dialog")
    WIDTH, HEIGHT = ui.inch2pix(5), ui.inch2pix(6)
    boxRoot.minsize(WIDTH, HEIGHT)
    #boxRoot.resizable(False, False)
    boxRoot.running = True
    boxRoot.protocol("WM_DELETE_WINDOW", quitter)
    boxRoot.geometry('+%d+%d' % (screensize[0] / 2 - WIDTH / 2, screensize[1] / 2 - HEIGHT / 2 - ui.inch2pix(0.5)))
    #boxRoot.configure(background='white')
    #boxRoot.iconphoto(False, tk.PhotoImage(file=asset_dir + default_icon))
    boxRoot.iconbitmap(asset_dir + default_ico)

    # First the label
    frame_0 = ttk.Frame(boxRoot)
    explain = tk.Label(frame_0, text=f"Open In WSL Associations.\nCreate, Edit, and Delete Associations.", justify=LEFT)
    explain.grid(row=0, column=1, padx=10, pady=20, sticky="NW", rowspan=1)#, columnspan=3)
    imager = Image.open(asset_dir + "manageassoc.png")
    # imager = imager.resize([48, 48])

    img = PIL.ImageTk.PhotoImage(imager.resize([50, 50]))
    labelm = tk.Label(frame_0, image=img)
    labelm.image = img
    labelm.grid(row=0, column=0, padx=10, pady=10)
    frame_0.columnconfigure(1, weight=1)

    frame_0.grid(row=0, column=0, padx=10, pady=0, sticky="NEW", rowspan=1)#, columnspan=3)

    frame_1 = ttk.Frame(boxRoot)#, borderwidth=2, relief="solid")#, pflatadding="0.15i")

    #list_frame = ttk.Frame(frame_1)#, borderwidth=3, relief="ridge")
    list_canvas = tk.Canvas(frame_1, bd=0, relief="groove", highlightthickness=0, highlightbackground="black")#, borderwidth=0, background="#ffffff")
    list_canvas.focus_force()
    list_canvas.grid(column=0, row=0, sticky="NWSE")

    list_frame = ttk.Frame(list_canvas)#, borderwidth=2, relief="solid")

    load_msg = ttk.Label(list_frame, text="Loading...")
    load_msg.grid(sticky="ews")

    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        #list_frame.configure(width=canvas.winfo_width())
    list_frame.bind("<Configure>", lambda event, canvas=list_canvas: onFrameConfigure(list_canvas))
    list_frame.configure()
    list_frame.columnconfigure(0, weight=1)

    def FrameWidth(event):
        #list_canvas.configure(scrollregion=list_canvas.bbox("all"))

        canvas_width = event.width
        list_canvas.itemconfig(1, width=canvas_width - 20)

        #boxRoot.update()
    list_canvas.bind('<Configure>', FrameWidth)



    scroller = ttk.Scrollbar(frame_1, command=list_canvas.yview)
    list_canvas.configure(yscrollcommand=scroller.set)
    list_canvas.create_window((4, 4), window=list_frame, anchor="center")


    scroller.grid(column=1, row=0, sticky="NES", padx=5, pady=5)

    frame_1.columnconfigure(0, weight=1)
    frame_1.rowconfigure(0, weight=1)

    def bound_to_mousewheel(event):
        frame_1.bind_all("<MouseWheel>", on_mousewheel)

    def unbound_to_mousewheel(event):
        frame_1.unbind_all("<MouseWheel>")

    def on_mousewheel(event):
        list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    frame_1.bind('<Enter>', bound_to_mousewheel)
    frame_1.bind('<Leave>', unbound_to_mousewheel)



    frame_1.grid(row=1, column=0, padx=20, sticky="NEWS")#, columnspan=3)
    #frame_1.grid_columnconfigure(2, weight=1)




    frame_3 = ttk.Frame(boxRoot)#, borderwidth=3, relief="ridge")
    cancel = ttk.Button(frame_3, text="Close", style="secondary.TButton", command=quitter)
    cancel.grid(row=0, column=0, sticky="W", padx=5)

    def helper():
        open_help("manage")
    help = ttk.Button(frame_3, text="Help", command=helper)
    help.grid(row=0, column=1, sticky="E", padx=5)

    test = ttk.Button(frame_3, text="Add Association", style="success.TButton", command=add_app)
    test.grid(row=0, column=3, sticky="E", padx=5, ipadx=5)

    #apply = ttk.Button(frame_3, text="Save Configuration", style="success.TButton")
    #apply.grid(row=0, column=3, sticky="E", padx=5)

    frame_3.columnconfigure(2, weight=1)
    frame_3.grid(row=2, column=0, padx=20, pady=20, sticky="SWE")
    #HWN = root.winfo_id()
    #titlebar.ChangeMenuBarColor(HWN)
    #boxRoot.overrideredirect(True)
    #lbl = tk.Label(boxRoot, text="Create a Start Menu Shortcut:", justify=CENTER)  # , font=("Helvetica", 16))
    #lbl.grid(row=0, padx=10, pady=10, sticky="EW")
    #boxRoot.grid_rowconfigure(0, weight=0)

    #boxRoot.bind("<Return>", login)
    boxRoot.columnconfigure(0, weight=1)
    boxRoot.rowconfigure(1, weight=1)
    boxRoot.deiconify()
    #boxRoot.wm_attributes("-topmost", 1)
    done = False
    old = sv_ttk.get_theme()

    while True:
        if sv_ttk.get_theme() == "light" and old == "dark":
            win32mica.Disable(HWND)
            #print("DisableMica")
            dark_title_bar(boxRoot, False)
        elif sv_ttk.get_theme() == "dark" and old == "light":
            #print("enableMica")
            ApplyMica(HWND, win32mica.MICAMODE.DARK)
            dark_title_bar(boxRoot, True)

        old = sv_ttk.get_theme()

        # draw(canvas, mouse=False)
        time.sleep(0.05)
        boxRoot.update()
        #print(done)
        if done == False:
            for i in list_frame.winfo_children():
                i.destroy()
            #load_msg.destroy()
            assoc_list = list(associations)
            assoc_list.sort()
            font = tk.font.Font(family="Segoe UI Semibold", size=15)
            separator = ttk.Separator(list_frame, orient=tk.HORIZONTAL)
            #separator.grid(row=0, columnspan=4, sticky="we")

            for assoc_num in range(len(assoc_list)):
                app = assoc_list[assoc_num]
                app_frame = ttk.Frame(list_frame)#, borderwidth=1, relief="solid")

                icon_label = tk.Label(app_frame, text=app, width=5)
                icon_label.configure(font=font)
                icon_label.grid(row=0, column=0, sticky="WNE", padx=10, pady=10, ipadx=0, ipady=10)

                attrib = associations[app]
                com = attrib['command'].replace('#fpth#', '"file"')
                app_name = ttk.Label(app_frame, text=f"Distro: {attrib['distro']}\n\nApp: {com[0].upper() + com[1:]}")
                app_name.grid(row=0, column=1, padx=5, pady=10, sticky="weNS")

                app_button = ttk.Button(app_frame, text="Edit", style="success.TButton", command=lambda j=app: select_app(j))
                app_button.grid(row=0, column=2, padx=5, pady=10, sticky="E")


                del_button = ttk.Button(app_frame, text="Delete", style="danger.TButton",
                                        command=lambda j=app: delete_app(j))
                del_button.grid(row=0, column=3, padx=5, pady=10, sticky="E")

                app_frame.columnconfigure(1, weight=1)
                separator = ttk.Separator(app_frame, orient=tk.HORIZONTAL)

                if assoc_num != len(assoc_list) - 1:
                    separator.grid(row=1, columnspan=4, sticky="we")

                app_frame.grid(row=assoc_num + 1, sticky="NWE", pady=5, ipadx=5)

            done = True
            boxRoot.update()
            list_canvas.yview_moveto(0.0)
            boxRoot.update()

        if boxRoot.running == False:
            break

#pg_init = False

def splash(extension, app, distro, icon=False):
    global show_donate
    ui.set_scale(1)
    # pygame init takes a long time...
    # pygame.display.init()

    donate = random.choice([True, False, False, False])

    if not show_donate:
        donate = False

    WIDTH, HEIGHT = ui.inch2pix(2.5), ui.inch2pix(0.8)  ##ui.inch2pix(7.9), ui.inch2pix(5)

    if donate == True:
        HEIGHT = ui.inch2pix(1.6)
    monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
    monitor_area = monitor_info.get("Monitor")
    work_area = monitor_info.get("Work")
    taskbar = int(monitor_area[3] - work_area[3])

    pos_config = "bottom"  # loc of taskbar

    if work_area[1] != 0:
        taskbar = work_area[1]
        pos_config = "top"

    elif work_area[0] != 0:
        taskbar = work_area[0]
        pos_config = "left"

    elif work_area[2] != monitor_area[2]:
        taskbar = monitor_area[2] - work_area[2]
        pos_config = "right"

    else:
        taskbar = int(monitor_area[3] - work_area[3])
        pos_config = "bottom"
    # print(pos_config)
    winpos = int(screensize[0] / 2 - WIDTH / 2)
    # winh = int(screensize[1] / 2 - HEIGHT)
    winh = 0
    if pos_config == "top":
        winh = taskbar

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (winpos, -HEIGHT)  # screensize[1] - taskbar)

    py_root = pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME)

    HWND = pygame.display.get_wm_info()["window"]
    try:
        SetWindowPos = windll.user32.SetWindowPos
        SetWindowPos(HWND, -1, 0, -400, 0, 0, 0x0001)
    except:
        pass
    # win32gui.MoveWindow(HWND, screensize[0] - WIDTH, screensize[1] - taskbar - HEIGHT, WIDTH, HEIGHT, True)

    # , pygame.SRCALPHA)
    try:
        win32gui.ShowWindow(HWND, 5)
        win32gui.SetForegroundWindow(HWND)
    except:
        pass

    white, light = get_system_light()

    pygame.display.init()
    canvas = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)

    ui.set_size([WIDTH, HEIGHT])
    pygame.display.set_caption("OpenInWSL")
    ui.start_graphics(pygame, asset_dir)
    ico = pygame.image.load(asset_dir + default_icon).convert_alpha()
    pygame.display.set_icon(ico)
    fpsClock = pygame.time.Clock()
    FPS = 60

    icons = {"refresh": "", "clock": "", "link": "",
             "laptop": "", "error": "", "settings": "", "app_list": "",
             "shell": "", "network": "", "heart": "", "question": "",  # oldshell 
             "plus": "", "minus": "", "x": "", "check": "", "dbus_config": "",
             "theme": "", "discord": "", "export": "", "folder": ""}

    ico_font = asset_dir + "segoefluent.ttf"  # "SEGMDL2.TTF"

    def get_pos():
        rect = win32gui.GetWindowRect(HWND)
        return [int(rect[0]), int(rect[1])]

    poser = get_pos()

    accent = ui.get_color()

    fuchsia = [12, 222, 123]

    # Set window transparency color
    hwnd = HWND

    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

    sett = iset.read()
    try:
        acrylic = sett["acrylic_enabled"]
    except Exception as e:
        logger.exception("Exception occurred - Please reset settings")
        acrylic = True

    show_donate = not sett["hide_donation_reminder"]

    import rounder

    s = rounder.round(HWND)

    if s == True:
        pad = ui.inch2pix(0.14)
        
        fade = True#False
    else:
        pad = 0
        fade = True
    if acrylic == True:
        import blur

        blur.blur(HWND)
    else:
        try:
            mini1 = pygame.image.load(
                os.getenv('APPDATA') + r"\Microsoft\Windows\Themes\TranscodedWallpaper").convert()
        except:
            bak = asset_dir + random.choice(["1", "2", "3"]) + ".jpg"
            mini1 = pygame.image.load(bak).convert()
        back = mini1.copy()  #
        back = pygame.transform.scale(back, screensize)

    # except Exception as e:
    #    logger.exception("Exception occurred - Cannot Init Display")

    animator = anima.animator(fpsClock)
    animator.register("start", [1, 0])
    animator.register("icon1", [0, 0])
    animator.register("arrows", [0, 0])
    animator.register("icon2", [0, 0])


    animator.animate("start", [100, 0])

    ui.set_icons(asset_dir + "Paper/")
    lin_icon = ui.pygame_icon(app, spec=app)
    ico_size = ui.inch2pix(0.4)
    lin_icon = pygame.transform.smoothscale(lin_icon, [ico_size, ico_size])

    # distro = "ubuntu-20.04"

    start_time = time.time()
    while True:
        # if win32gui.GetFocus() != HWND:
        #    animator.animate("start", [0, 0])
        canvas.fill([0, 0, 0, 0])
        start = animator.get("start")[0] / 100
        icon1 = start  # animator.get("icon1")[0] / 100
        arrows = animator.get("arrows")[0] / 100
        icon2 = animator.get("icon2")[0] / 100
        if start == 0:
            #pygame.quit()
            pygame.display.quit()
            break
            #sys.exit()
        if start < 1:
            try:
                win32gui.MoveWindow(HWND, winpos, winh - HEIGHT + int(start * (HEIGHT + pad)), WIDTH, HEIGHT, 1)
                if fade == True:
                    win32gui.SetLayeredWindowAttributes(HWND, win32api.RGB(*fuchsia), int(start * 255), win32con.LWA_ALPHA)
                else:
                    win32gui.SetLayeredWindowAttributes(HWND, win32api.RGB(*fuchsia), int(255), win32con.LWA_ALPHA)
            except:
                pass
        else:
            win32gui.MoveWindow(HWND, winpos, winh + pad, WIDTH, HEIGHT, 1)
            if fade == True:
                win32gui.SetLayeredWindowAttributes(HWND, win32api.RGB(*fuchsia), int(255), win32con.LWA_ALPHA)
            else:
                win32gui.SetLayeredWindowAttributes(HWND, win32api.RGB(*fuchsia), int(255), win32con.LWA_ALPHA)
            # animator.animate("icon1", [100, 0])
            # if icon1 == 1:
            animator.animate("arrows", [100, 0])
            if arrows == 1:
                animator.animate("icon2", [100, 0])

        if light == False:
            pass#pygame.gfxdraw.rectangle(canvas, [0, 0, WIDTH, HEIGHT + 1], [100, 100, 100, 100])
            #pygame.gfxdraw.box(canvas, [0, 0, WIDTH, HEIGHT], [100, 100, 100, 255])
            pygame.gfxdraw.rectangle(canvas, [0, 0, WIDTH, HEIGHT], [255, 255, 255, 100])
            #pygame.gfxdraw.line(canvas, padd, l_h, WIDTH - padd, l_h, [180, 180, 180, int(80 * launch)])

        else:
            pass
            #pygame.gfxdraw.box(canvas, [0, 0, WIDTH, HEIGHT], [255, 255, 255, 200]) pre 11

            pygame.gfxdraw.box(canvas, [0, 0, WIDTH, HEIGHT], [255, 255, 255, 180])

            pygame.gfxdraw.rectangle(canvas, [0, 0, WIDTH, HEIGHT], [255, 255, 255, 80])
           
        if acrylic == False:
            pygame.gfxdraw.box(canvas, [0, 0, WIDTH, HEIGHT], accent)

        if donate == True:
            title_font = ui.font(default_font, int(ui.inch2pix(0.21)))
            txt = title_font.render(f"Consider Donating @", True, white)
            txt.set_alpha(int(start * 255))
            canvas.blit(txt, [WIDTH / 2 - txt.get_width() / 2, ui.inch2pix(0.2)])

            txt = title_font.render(f"paypal.me/pololot64", True, white)
            txt.set_alpha(int(start * 255))
            canvas.blit(txt, [WIDTH / 2 - txt.get_width() / 2, ui.inch2pix(0.5)])


        if icon == False:
            ext_font = ui.font(default_font, int(ui.inch2pix(0.21)))
            offset = 0
        else:
            ext_font = ui.font(ico_font, int(ui.inch2pix(0.3)))
            offset = ui.inch2pix(0.03)
        #extension = ".gitigno"#ore"
        ext = extension
        if len(extension) > 7:
            ext = extension[:7] + "..."
        txt = ext_font.render(ext, True, white)
        txt.set_alpha(int(icon1 * 255))
        canvas.blit(txt, [WIDTH / 4 - txt.get_width() / 2,
                          offset + HEIGHT - txt.get_height() - ui.inch2pix(0.29) - int(ui.inch2pix(0.2) * (1 - icon1))]) #used to be 24

        icon_font = ui.font(ico_font, int(ui.inch2pix(0.2)))
        arrow = icon_font.render("", True, white)

        offset = ui.inch2pix(0.0)
        arrow.set_alpha(int(arrows * 255))
        h = 0.29 #utb25
        canvas.blit(arrow, [
            WIDTH / 2 - arrow.get_width() / 2 - arrow.get_width() + offset - int(ui.inch2pix(0.6) * (1 - arrows)),
            HEIGHT - ui.inch2pix(h) - arrow.get_height()])  # - int(ui.inch2pix(0.2) * (1 - arrows))])

        canvas.blit(arrow, [WIDTH / 2 - arrow.get_width() / 2 + offset - int(ui.inch2pix(0.4) * (1 - arrows)),
                            HEIGHT - ui.inch2pix(
                                h) - arrow.get_height()])  # - int(ui.inch2pix(0.15) * (1 - arrows))])

        canvas.blit(arrow, [
            WIDTH / 2 - arrow.get_width() / 2 + arrow.get_width() + offset - int(ui.inch2pix(0.2) * (1 - arrows)),
            HEIGHT - ui.inch2pix(h) - arrow.get_height()])  # - int(ui.inch2pix(0.1) * (1 - arrows))])

        title_font = ui.font(default_font, int(ui.inch2pix(0.1)))
        pretty = str(distro[0].upper() + distro[1:].replace('-', ' '))
        if len(pretty) > 15:
            pretty = pretty[:15]
        txt = title_font.render(pretty, True, white)
        txt.set_alpha(int(icon2 * 255))
        canvas.blit(txt, [WIDTH / 4 * 3 - txt.get_width() / 2 + ui.inch2pix(0.05), HEIGHT - ui.inch2pix(0.23)])

        lin_icon.set_alpha(int(icon2 * 200))
        offset = ui.inch2pix(0.1)
        canvas.blit(lin_icon, [WIDTH / 4 * 3 - lin_icon.get_width() / 2 + ui.inch2pix(0.05),
                               HEIGHT - lin_icon.get_height() - ui.inch2pix(0.14) - offset - int(
                                   ui.inch2pix(0.2) * (1 - icon2))])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                animator.animate("start", [0, 0])
        py_root.fill([0, 0, 0, 255])
        # canvas.set_alpha(50)
        if light == True:
            py_root.blit(canvas, [0, 0], special_flags=(pygame.BLEND_RGBA_ADD))
        else:
            py_root.blit(canvas, [0, 0])

        pygame.display.update()
        animator.update()
        fpsClock.tick(FPS)

        wait = 2.5
        #if donate == True:
        #    wait += 1.5
        if time.time() - start_time > wait and icon2 == 1:
            animator.animate("start", [0, 0])



args = sys.argv# + [r'''C:\blur.py''']#[r"C:\Users\PEF\Desktop\GWSL-Source\assets\x11-icon.png"]

if __name__ == "__main__":
    #logger.info(str(args))
    handler_mode = False
    if len(args) >= 2:
        handler_mode = True
    if handler_mode:
        file = " ".join(args[1:])
        print("F", file, os.path.basename(file))
        extension = os.path.splitext(file)[1].lower().strip()
        if extension == "":
            base = os.path.basename(file)
            if len(base) != 0 and base.startswith("."):
                extension = base

        handlers = iset.read()["assocs"]
        import shlex
        if extension in handlers:
            try:
                #print(f"Looking for handler for {extension}")
                handler = handlers[extension]
            except:
                logger.exception("I think this extension has not been registered. Not sure")
                from ttkbootstrap import Style
                import wsl_tools as tools
                import tkinter.font
                import pymsgbox
                from tkinter import simpledialog
                create(extension, test_file=file)
                sys.exit()
            try:
                handler = handlers[extension]
                distro = handler["distro"]
                pather = path_converter(file)
                pather = shlex.quote(pather)
                command = str(handler["command"].replace("#fpth#", pather))
                logger.info("RUN TEST: " + str(command))
                #fast = time.perf_counter() - start_time
                #print("started in", fast)
                #logger.info("started " + str(fast))

                #subprocess.getoutput(command)
                app = handler["command"].split(" ")[0]
                try:
                    """
                    from ttkbootstrap import Style
                    import wsl_tools as tools
                    import tkinter.font
                    import pymsgbox
                    from tkinter import simpledialog
                    """
                    try:
                        st = threading.Thread(target=spawn_n_run, args=[distro, command])
                        #st.daemon=True
                        st.start()
                    except:
                        logger.exception("cannot spawn n run")

                    try:
                        #print("splash")
                        splash(extension, app, distro)
                    except:
                        logger.info("Cannot splash... probably not a big deal. we'll see what happens next.")



                except:
                    logger.exception("cannot launch splash")
            except:
                logger.exception("Cannot Open extension error")
        else:
            try:
                from ttkbootstrap import Style
                import wsl_tools as tools
                import tkinter.font
                import pymsgbox
                from tkinter import simpledialog
                create(extension, test_file=file)
            except:
                logger.exception("Cannot create assoc 2")

    else:
        from ttkbootstrap import Style
        import wsl_tools as tools
        import tkinter.font
        import pymsgbox
        from tkinter import simpledialog
        #splash("", "preferences", "Dashboard", icon=True)
        try:
            #print("Starting home")
            home()
        except:
            logger.exception("cannot launch home")
