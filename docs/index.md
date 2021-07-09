---
layout: homepage
title: OpenInWSL
---


<img src="./tutorials/oiwcentered.png">

## GWSL

### What on Earth does this do? What is it for? How can it help me?

GWSL automates the process of running X on top of WSL and over SSH:
*  It lets you easily run graphical Linux apps on Windows 10.
*  It lets you run graphical apps located on remote Linux machines.
*  It provides a simple UI for launching Linux apps, managing them graphically, and creating customized Windows shortcuts for them.
*  All this at the click of a button! No memorization of commands necessary. *Easy!*

Basically, it does a lot of stuff so *you* don't have to! Maybe you'd better watch the video ↓

<iframe width="560" height="315" src="https://www.youtube.com/embed/VEbnVK70A0M" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Here is another video showing it in action:
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/S6GXBEQ5KzA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### Wait... Why is it called GWSL? From your title it looks like it should be called TFPHIWXS. Why didn't you call it that?

Meh... That doesn't sound too great. GWSL stands for Graphical WSL. WSL in turn stands for Windows Subsystem for Linux. :-)

### Great. But there are other XServers for Windows. Why should I use GWSL?

There are several alternative XServers for Windows 10. Some are proprietary (and costly). Some have not been updated for years. 

GWSL is Free.

GWSL is easy to install.

GWSL Builds on the VCXSRV XServer, one of the best open source Windows Xservers. It uses VCXSRV as a backend but adds many useful features. 

### Minimum System Requirements

Windows 10 Version 2004 [(See FAQ)](#frequently-asked-questions)



### Using GWSL

[GWSL Manual](./tutorials/manual.html)

Quick Links:

[Familiarizing Yourself With WSL](https://docs.microsoft.com/en-us/windows/wsl/about).

[Enabling WSL and Installing Distros](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

[Creating Start Menu Shortcuts for Linux Apps](./tutorials/manual.html#using-the-gwsl-shortcut-creator).

<!--
TODO: [Prepare a Distro for X (Graphics Compatibility)](https://guides.github.com/features/mastering-markdown/).
TODO: [Enable Dbus (To Run Gnome Apps)](https://guides.github.com/features/mastering-markdown/).


#### More

Digging Deeper

TODO: [Frequently Asked Questions](./tutorials/shortcut.html).

[Creating a Linux App Shortcut on Windows](./tutorials/shortcut.html).

[Changing DPI Options](./tutorials/dpi.html).

TODO: [Changing the GTK Theme](https://guides.github.com/features/mastering-markdown/).

TODO: [Using the Integrated Linux App Launcher](https://guides.github.com/features/mastering-markdown/).

TODO: [Using Remote Linux Apps With X](https://guides.github.com/features/mastering-markdown/).

TODO: [Creating Windows Shortcuts for Remote Linux *Apps* With X](https://guides.github.com/features/mastering-markdown/).

TODO: [Creating Windows Shortcuts *ENTIRE* Remote Linux *Machines* With X](https://guides.github.com/features/mastering-markdown/).

Miscellaneous

[Installing a Graphical Linux Package Manager](./tutorials/package-managers.html).
What will happen when WSL2 gets official Wayland support? *I am just as excited about this as you are. Till it is available, GWSL will only function as an XServer. When Wayland is available, there will be an option to swicth between Wayland and X as a GWSL backend. The shortcut creator and app launcher will continue to work in the new Wayland mode.*
-->

### Frequently Asked Questions ###
*  Why doesn't GWSL seem to work with Linux shells other than Bash? *Here is some info: [Using GWSL with other Shells](./tutorials/manual.html#using-gwsl-with-other-shells).*
*  Does WSL work on Windows 10 versions older than 2004? *Yes, now that Microsoft has made WSL2 compatible with older versions of Windows 10, GWSL can run on them too. To run GWSL on older versions of Windows 10, you will need to install WSL2.*
*  Does GWSL work with every single app? *No. But most work well*
*  Why aren't there more questions? *We are woking on this... Not many questions have been asked frequently enough to put here. Start asking!*


### Help and Support

Need help? Visit our [help page](https://opticos.github.io/gwsl/help.html).

### Donate ###

If you enjoy GWSL, please consider buying me a cup of coffee. I worked hard to make it free and plan to spend alot of time supporting it. Donations are greaty appreciated. If you can't donate, please consider leaving a 5-star review on the Microsoft Store.

##### Any Amount Helps!

<form action="https://www.paypal.com/donate" method="post" target="_top">
<input type="hidden" name="cmd" value="_donations" />
<input type="hidden" name="business" value="VV8W4XA2PZ5R8" />
<input type="hidden" name="item_name" value="GWSL Donation" />
<input type="hidden" name="currency_code" value="USD" />
<input type="image" src="https://www.paypalobjects.com/webstatic/en_US/i/buttons/cc-badges-ppmcvdam.png" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
<img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
</form>

##### Or use Ko-Fi ☕
<script type='text/javascript' src='https://ko-fi.com/widgets/widget_2.js'></script><script type='text/javascript'>kofiwidget2.init('Support Me on Ko-fi', '#e08a28', 'G2G24743G');kofiwidget2.draw();</script> 

(Ko-Fi is the floating button on the left side.)

##### Or BuyMeACoffee.com ⭐
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="optico5" data-color="#e08a28" data-emoji=""  data-font="Poppins" data-text="Donate: Buy me a coffee.com" data-outline-color="#000000" data-font-color="#ffffff" data-coffee-color="#FF7673" ></script>

(BuyMeACoffee is the floating button on the right side.)

<script src='https://storage.ko-fi.com/cdn/scripts/overlay-widget.js'></script>
<script>
  kofiWidgetOverlay.draw('optico5', {
    'type': 'floating-chat',
    'floating-chat.donateButton.text': 'Donate: Ko-Fi',
    'floating-chat.donateButton.background-color': '#f45d22',
    'floating-chat.donateButton.text-color': '#fff'
  });
</script>


<script data-name="BMC-Widget" data-cfasync="false" src="https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js" data-id="optico5" data-description="Support me on Buy me a coffee!" data-message="Donate on BuyMeACoffee.com" data-color="#FF813F" data-position="Right" data-x_margin="18" data-y_margin="18"></script>

### My Other Sites:
<!--*  [LinkedIn Profile](https://www.linkedin.com/in/paul-elliot-foy)-->
*  [Opticos Main Website](https://sites.google.com/bartimee.com/opticos-studios/home)
*  [Optico5 on Bandcamp](https://opticos.bandcamp.com/)
*  [Optico5 on Soundcloud](https://soundcloud.com/opticos)
*  [Opticos on GitHub](https://github.com/Opticos)
*  [Personal Github Page (Pololot64)](https://github.com/Pololot64)
