---
layout: default
title: GWSL Manual
permalink: /tutorials/manual.html
---
## Table of Contents
1.  [Prerequisites](#prerequisites)
2.  [Installing GWSL](#installing-gwsl)
3.  [The GWSL User Interface](#the-gwsl-user-interface)
4.  [Configuring a WSL Distro for use with GWSL](#configuring-a-wsl-distro-for-use-with-gwsl)
5.  [Using the GWSL Shortcut Creator](#using-the-gwsl-shortcut-creator)
6.  [Using the Integrated Linux App Launcher](#using-the-integrated-linux-app-launcher)
7.  [Installing a Graphical Package Manager](#installing-a-graphical-package-manager)
8.  [Using GWSL with a Full Linux Desktop](#using-gwsl-with-a-full-linux-desktop)
9.  [Using GWSL with SSH](#using-gwsl-with-ssh)
10.  [Using GWSL with other Shells](#using-gwsl-with-other-shells)
11.  [Using GWSL Configuration Files](#using-gwsl-configuration-files)
12.  [Finding Logs](#finding-logs)
13.  [Starting GWSL Silently (without dashboard)](#silent-startup)
14.  [Troubleshooting](#troubleshooting)


***

## GWSL Manual

### Prerequisites ###

GWSL requires [Windows 10 version 2004](https://support.microsoft.com/en-us/help/4028685/windows-10-get-the-update). If you do not have it, please update Windows to continue.

Once Windows is up to date, be sure you have the WSL feature installed and configured properly. Here are some helpful links:
*  [Familiarizing Yourself With WSL](https://docs.microsoft.com/en-us/windows/wsl/about)
*  [Enabling WSL and Installing Distros](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

To make sure WSL is installed correctly, type ```wsl.exe``` in the command line and verify that there are no errors.

### Installing GWSL ###

GWSL can be easily installed from the Microsoft Store. If it is not already installed, get it [here](ms-windows-store://pdp/?productid=9NL6KD1H33V3) or [here](https://www.microsoft.com/en-us/p/gwsl/9nl6kd1h33v3).

On the first run of GWSL, Windows will ask you if you want to allow GWSL through the firewall. GWSL requires public network access to function. You may be asked to allow access twice when using certain options in the [Shortcut Creator](#using-the-gwsl-shortcut-creator) or changing the dpi mode(See Options with an Asterisk).

If you are not sure you allowed GWSL through the firewall, you can test the xserver by going to the GWSL Dashboard --> About --> XClock. A simple clock window should open.

If you did not allow it through the firewall the first time, you can simply go to the GWSL Dashboard --> About --> Allow GWSL Through the Firewall.
This will open a window to show you how to allow it. (This feature was added in GWSL 1.3.8)

Note: Some Antiviruses might detect GWSL and block its installation. This is a known bug in Pyinstaller, the program I use to package GWSL. If this occurs, you might want to disable the Antivirus during installation.

### The GWSL User Interface ###
#### The Dashboard 

You can open the GWSL Dashboard by clicking the GWSL icon in the Start Menu. Once GWSL is running, you can quickly pull up the Dashboard with ```CTRL+ALT+G``` or by clicking the "G" icon in the notification area.

Overview: The GWSL Dashboard is where you can configure WSL machines, create shortcuts, and quickly launch apps.

<img src="https://opticos.github.io/gwsl/tutorials/dash annotated.png" width="350">

#### Key
1.  **GWSL Distro Tools:** Access various management and configuration options for WSL Distros.
2.  **Shortcut Creator:** Create Windows Shortcuts that launch graphical Linux apps running in WSL. Usage is explained [here](#using-the-gwsl-shortcut-creator).
3.  **Linux Apps:** You can access and launch most graphical Linux apps installed on WSL here. You can also instantly create shortcuts for these apps. *Note: The App Launcher does not always find all graphical programs. Also, some links might not be functional. To access these programs, please use the [Shortcut Creator](#using-the-gwsl-shortcut-creator) or WSL Shell.*
4.  **Linux Shell:** Access the shells of installed WSL Distros.
5.  **Graphical SSH Connection:** This feature allows you to log in to remote Linux machines and access their graphical apps on Windows. More is explained [here](#using-gwsl-with-ssh).
6.  **Donate:** I spent a long time developing this app and am now offering it for free. *Donations are appreciated.* [Donate here (-:](https://sites.google.com/bartimee.com/opticos-studios/donate)
7.  **Help:** Umm... This opens the [GWSL help page](https://opticos.github.io/gwsl/help.html).
8.  **About:** Shows GWSL credits, version, and license information.

*Note: If any of these features are missing you might want to make sure you have all the [prerequisites installed](#prerequisites).*

### Configuring a WSL Distro for use with GWSL ###

##### Note: These setup steps will only work if bash is the default Linux shell. If you don't know what this means, you're probably good to go. If you are using Fish as the default shell, [read this](#using-gwsl-with-other-shells).

#### Getting Started

After a new WSL Distro is installed, several steps are required to get it up and running with GWSL: 
1.  On the first run of GWSL, Windows will ask you to allow GWSL through the Windows firewall. It is **important** to give it access to public networks. You might be asked to allow it through twice.
2.  The next step is to enable "Auto-Export Display" in the Distro configuration.
3.  After this, the user may tweak other settings explained in this section.

If you are not sure you allowed GWSL through the firewall, you can test the xserver by going to the GWSL Dashboard --> About --> XClock. A simple clock window should open.

If you did not allow it through the firewall the first time, you can simply go to the GWSL Dashboard --> About --> Allow GWSL Through the Firewall.
This will open a window to show you how to allow it. (This feature was added in GWSL 1.3.8)


Tip: You can open the GWSL Dashboard by clicking the GWSL icon in the Start Menu. Once GWSL is running, you can quickly pull up the Dashboard with ```CTRL+ALT+G``` or by clicking the GWSL icon in the notification area.

#### Accessing Other Distro Settings ####

To access per-distro-settings, open the GWSL Dashboard and click "GWSL Machine Tools".


<img src="https://opticos.github.io/gwsl/tutorials/dashboardlink.png" width="500">


**NOTE: To toggle the default X Window Mode and/or Shared Clipboard settings, Right-Click the "G" Icon in the notification area. These are the default settings for the XServer on port 0 but specific shortcuts can override them.** 


##### Choose the WSL Distro you want to configure:

<img src="https://opticos.github.io/gwsl/tutorials/chooser.png" width="300">

#### GWSL Distro Manager Overview ###

<img src="https://opticos.github.io/gwsl/tutorials/configure.png" width="300">

#### Key:

1.  **Display Auto Export:** With other XServers for Windows 10, the user must type in several commands each time they launch a gui app. With GWSL, clicking this button makes these commands run automatically when the current WSL Distro starts. This must be enabled for every new WSL distro. NOTE: After converting a WSL machine between WSL 1 and 2, this button must be pressed again. 

2.  **Configure DBus:** Some Gnome apps have trouble running on WSL. Clicking this button attempts to enable DBus to fix these issues. The root password of the current WSL Distro is required to do this. NOTE: This option is only available on Debian-based distributions. This option also requires WSL2. It is not guaranteed to work.

3.  **GTK DPI Toggle:** This button toggles the default DPI environment variable for GTK.

4.  **QT DPI Toggle:** This button toggles the default DPI environment variable for QT. 

5.  **Theme Chooser:** Unstable: This option allows users to set the default GTK theme of the Distro being configured. This attempts to scan ```/usr/share/themes/``` for GTK themes.

6.  **Reboot Distro:** Reboot the current WSL Distro.


### Using the GWSL Shortcut Creator ###

To access the Shortcut Creator, open the GWSL Dashboard and click "Shortcut Creator".

#### The Shortcut Creator UI:

<img src="https://opticos.github.io/gwsl/tutorials/shortcut annotated.png" width="450">

#### Key:

1.  **Shortcut Label:** This is the label that will apper on your Windows shortcut. The label is used to find an icon for the shortcut.

2.  **Shortcut Command:** This is the Bash command that will launch your app.

3.  **Run In:** The WSL machine that will run the app. Be sure that the app you want to pin is installed on the machine you select. 

4.  **Reset Icon:** Click this if the icon automatically selected by the Shortcut Creator does not match that of the desired app. 

5.  **Help:** Opens this help page.

6.  **More/Less Options:** Show and hide advanced shortcut options.

7.  **Display Mode:** Choose if you want to run the app in GWSL Single Window, Multi Window, or Fullscreen mode. If Default is selected, the current app mode is used. *

8.  **GTK Scale Mode:** Override the HI-DPI scale factor for GTK. If Default is selected, the current GTK scale factor for the current machine is used. 

9.  **QT Scale Mode:** Override the HI-DPI scale factor for QT. If Default is selected, the current QT scale factor for the current machine is used.

10. **Shared Clipboard:** Enable or Disable the shared clipboard for this app. If set to Disabled, the Windows clipboard will not synchronize with the Linux app. If set to Default, the current default clipboard mode is used. *

11.  **Color Mode:** If set to Follow Windows, GTK will try to synchronize light and dark theme modes with Windows.

12.  **Run As Root:** If set to true, the shortcut will ask for a password at launch and run the command with sudo.

13.  **Use DBus:** This only works on Debian-based distros. Use it for Gnome apps if they do not start. Ex. Gnome Software.

14.  **Experimental Flags:** These might not work. If GTK and QT scaling does not work, try using these flags.
15.  **Keep XServer Instance:** This is useful when a shortcut is running with its own XServer Instance. Enable this if Linux GUI apps randomly close.

16.  **Add to Start Menu:** Add a shortcut for the app to the Windows Start Menu with these current settings. It is recommended to test your configuration with "Test Configuration" before creating the shortcut.

17.   **Test Configuration:** Test the current settings to make sure everything works before adding your shortcut.

##### * These settings make an app run in its own XServer. It is usually better to let an app use the default GWSL XServer on port 0 but this can be helpful if an app needs to be separated from others (whether is be by settings or clipboard preferences). If these options are changed from their defaults, a new XServer on a random port will run when the shortcut is launched. If you are unsure about these settings, test them before by using the "Test Shortcut" button.

#### More

You can also use the [Linux App Launcher](#using-the-integrated-linux-app-launcher) to create shortcuts.

### Using the Integrated Linux App Launcher ###

##### Note: The Integrated app launcher can be useful for quickly finding and launching Linux GUI apps running on WSL distros. However, due to the many different standards for Linux apps, not all apps shortcuts will work and some might be missing. If an app is missing, you can launch it using the [Shortcut Creator](#using-the-gwsl-shortcut-creator) or the shell of a WSL Distro.

Access the Linux App Launcher by opening the Dashboard and clicking "Linux Apps". If you are prompted to select a Distro, select the Distro where the app is installed. 

Click the icon of an app to launch it. Click the link: ```🔗``` icon beside a shortcut to open the Shortcut Creator and create a shortcut. [Shortcut settings](#using-the-gwsl-shortcut-creator) may need to be adjusted for everything to work properly.

### Installing a Graphical Package Manager ###

#### Choosing a Package Manager

There are several to choose from depending on your Linux distribution. Here are some common ones.

##### Package Managers for Debian-Based Distributions Using APT

*  Synaptic - Easy to Install and Very Powerful.

   In the WSL terminal:
   
   ```bash
   sudo apt install synaptic
   ```
   To run Synaptic, use ```sudo synaptic```

*  Gnome Software - Streamlined But Quirky and Buggy at Times. We do not recommend using this one.

   In the WSL terminal:
   
   ```bash
   sudo apt install gnome-software
   sudo apt install network-manager-pptp-gnome #This is required due to a WSL quirk
   ```
   To run Gnome Software, use ```sudo gnome-software``` after starting [DBus](https://opticos.github.io/gwsl/tutorials/dbus.html).
   NOTE: To create a shortcut with the shortut creator, be sure to set "Enable DBus" under "More Options" to True:
   
##### Package Managers for OpenSuse

*  YaST - The Recommended Default.
   In the WSL terminal:
   
   ```bash
   sudo zypper install xterm
   ```
   To run YaST, use ```sudo xterm yast2```

##### Package Managers for Other Distributions

There are hundreds of other Linux Distributions. Try checking [this page](https://www.tecmint.com/linux-package-managers/) out.

#### Creating a Windows Shorcut for the Package Manager

Use the [Shortcut Creator](#using-the-gwsl-shortcut-creator) with the command and name of the package manager. Be sure to set "Run as Root" to ```True```.

### Using GWSL with a Full Linux Desktop ###

GWSL can be used to launch full Linux Desktop Environments (DE's) full screen or in their own windows. GWSL has been tested with [XFCE](https://www.xfce.org/) and [MATE](https://mate-desktop.org/). [LXDE](https://wiki.lxde.org/en/Main_Page) and others may also work. To use one of these desktops, install it using your Distro's repository, start GWSL, and run the DE.

To create a shortcut that links to the Desktop Environment, open the [Shortcut Creator](#using-the-gwsl-shortcut-creator), type in the name of your distro, and enter the command needed to launch the distro. For XFCE, use the command ```startxfce4```. For Mate, use ```mate-session```. Be sure to use ```Single Window Mode``` or ```Fullscreen Mode```. Otherwise wierd things will happen.

### Using GWSL with SSH ###

##### Note: This is an experimental feature. 

<img src="https://opticos.github.io/gwsl/tutorials/ssh.png" width="450">

This feature lets you login to remote Linux machines and run graphical apps installed remotely on your Windows desktop.'

To use it, open the Dashboard and click the "Graphical SSH Connection" button. Type in the IP address of the remote machine, hit enter, and enter your credentials. You will then see a Putty SSH window preset to forward X to the GWSL XServer. Enter a command to run a graphical app and it should run.

### Using GWSL with other Shells ###

#### GWSL 1.3.8 now supports Fish and Zsh.
To export the display for these shells, go do the dashboard --> GWSL Distro Tools --> Distro --> More Shells and Options.

#### Using X with Fish (OLD METHOD FOR GWSL 1.3.7 and under. DOES NOT ALWAYS WORK)
Auto-exporting does not work if Fish is the default shell but you can use this script. Note this can break on some systems...
```fish
set --export WSL2 1
set ipconfig_exec (wslpath "C:\\Windows\\System32\\ipconfig.exe")
if which ipconfig.exe >/dev/null
    set ipconfig_exec (which ipconfig.exe)
end

set wsl2_d_tmp (eval $ipconfig_exec | grep -n -m 1 "Default Gateway.*: [0-9a-z]" | cut -d : -f 1)
if test -n "$wsl2_d_tmp"
    set first_line (expr $wsl2_d_tmp - 4)
    set wsl2_d_tmp (eval $ipconfig_exec | sed $first_line,$wsl2_d_tmp!d | grep IPv4 | cut -d : -f 2 | sed -e "s|\s||g" -e "s|\r||g")
    set --export DISPLAY "$wsl2_d_tmp:0"
    set -e first_line
else
    set --export DISPLAY (cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
end

set -e wsl2_d_tmp
set -e ipconfig_exec
```
Add this to the end of `config.fish` and you should be good to go! (Credit to [Jtiai](https://github.com/jtiai)).

### Using GWSL Configuration Files ###

#### The GWSL blacklist configuration option allows users to block certain applications and distros from showing up in the app launcher and machine chooser.
1.  Open Windows Explorer.

2.  In the path entry box, paste ```%AppData%/GWSL/```and hit enter.

3.  The configuration file is called ```settings.json```.

4.  Stop the GWSL Service and open this file in your favorite text editor to make changes.

#### Blocking Distros

In the settings file, add the phrases you want blocked to the ```distro_blacklist``` list.

#### Blocking Apps

In the settings file, add the phrases you want blocked to the ```app_blacklist``` list.

##### Note: The format for the blacklists is ```["name1", "name2", "name3"]```. Commas are required between entries.

#### Changing the position of the GWSL Dashboard

The Dashboard in GWSL 1.3.6 can now be configured to pop up on the left side of the desktop. To access this option, open the configuration file and edit the ```"start_menu_mode"``` variable to be ```true``` (for left) or ```false``` (for default right).

#### Changing the Default Terminal App

You can use CMD or the new Windows Terminal. In the settings file, change the value of ```"shell_gui"``` to ```"wt"``` to use Windows Terminal or use ```"cmd"``` to use CMD.

#### Disabling Acrylic for Compatibility with HDR Displays

The GWSL Dashboard does not always display properly when HDR is on (on certain displays). To fix this, open the settings file and set the value of ```"acrylic_enabled"``` to ```false```.


### Finding Logs ###

#### Reporting a bug? Here is how to find bug reports and logs
1.  Open Windows Explorer.

2.  In the path entry box, paste ```%AppData%/GWSL/```and hit enter.

3.  The logs are stored in ```dashboard.log``` and ```service.log```.

4.  Include these logs in support emails or share them in the [Discord help server](https://discord.gg/VkvNgkH). Make sure no personal information is contained in them before sharing.


### Silent Startup ###
#### Want to start GWSL silently at startup? Or just want to bypass the dashboard? Here is how to do it. ####
#### To Run Silently At Startup ####
The easiest way is to add it to the Start Menu's startup folder. 
*  First navigate to ```%AppData%/Microsoft/Windows/Start Menu/Programs/Startup``` in File Explorer (Paste the path in Explorer's path entry box). 
*  Then RightClick --> New --> Shortcut. 
*  If you installed GWSL from the Store, type ```GWSL.exe --r --startup```, click next, and finish. 
*  If you have installed it with the traditional GitHub installer, type ```%AppData%/GWSL/GWSL.exe --r --startup``` in the text box, click next, then finish.

Note the ```--startup``` flag requires GWSL version 1.3.7 and up.

#### To run silently from the Start-Menu, Desktop, or Taskbar make the same shortcut described above outside of the startup folder and pin it where it needs to be. ####

### Troubleshooting ###

Not here yet. But there is alot of material in the GWSL Source Github issues list.

