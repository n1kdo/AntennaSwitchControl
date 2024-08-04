# Installation and Setup

This page describes how to install and set up this project.

There are three main steps:

1. Installing Micropython
2. Installing the Python code.
3. Connecting to your Wi-Fi network.

## Installing MicroPython on your Pico-W

1. Download the latest stable build of [Pico W MicroPython](https://micropython.org/download/RPI_PICO_W/). 
   [This is the direct link](https://micropython.org/resources/firmware/RPI_PICO_W-20240105-v1.22.1.uf2).
2. Connect a micro-USB cable to your PC.  Hold down the white "BOOTSEL" button on the Pico-W, and insert the
   micro-USB cable into your Pico-W.
3. The Pico-W should appear as a USB storage device on your computer.  On mine, it shows up as "RPI-RP2 (F:)".
4. Copy/Paste the MicroPython .uf2 file to this drive.
5. Disconnect the Pico-W and prepare for the next step.

## Installing this software onto the Pico-W

The easiest way to get this software installed onto your Pico-W is to use the `loader.py` tool, also
provided in this repository.  

Note that these commands are written from a Windows perspective, but the Python commands should work the same way 
on macOS or Linux.  I have no Macs, so I cannot test this.

1. Download Python 3 from https://www.python.org/downloads/ and install it.  Make sure to select "Add 
   Python 3 to Path."
2. Download the contents of this GitHub repository as a zip.  Use
   [this URL](https://github.com/n1kdo/switch-control/archive/refs/heads/master.zip)
3. Unpack that zip file somewhere. 
4. Open a command prompt.  (your choice.  Could be PowerShell, could be good old CMD.)
5. From the command line, execute the following command: `pip install pyserial` -- this will install the Python 
   serial port support.
6. Change directory to where you unpacked the GitHub zip file, and then change directory to the `src/loader` directory.
7. From the command line, execute the following command: `python loader.py` -- this will install all the python  
   software onto the Pico-W.

If you want to experiment, you can use the open-source "Thonny" IDE to load the python source code and HTML files
onto the Pico W.  Unfortunately, Thonny cannot load binary files, but you can work around this "upload" feature in
the "Files" page.

## Setup and Connecting to your Wi-Fi Network

The software has a setup web page that allows you to set the SSID and secret to connect to you Wi-Fi network, 
but how can you access this page if the controller is not already connected to your network? This is the function
of the "mode" button. When the mode button is pressed, the device will restart as a Wi-Fi access point named
"kpa500" using password "elecraft".  Connect to this access point with your phone or other Wi-Fi device. Some 
devices will complain that this network does not offer Internet access--that is ok, because it does not! 
You may need to check a box to keep your device connected to this network.

Once connected to the "kpa500" network, open the device's web page by accessing http://192.168.4.1 – from here you
can click the "Setup" link and configure the network. After you enter your network’s SSID and secret, click the "Apply"
button to save the configuration, and then press the "Restart" button to return the device to normal mode.

Access point mode can also be used in locations where there is no Wi-Fi service, the device is completely 
usable in access point mode.

## Electrical Connections

(To be added.  Meanwhile, consult the schematic.)

## Controls and Indicators

| Control/Indicator | Purpose          |
|-------------------|------------------|
| LED D20           | Status indicator |
| Switch SW1        | Mode Selector    |

The Status Indicator normally blinks out the device's IP address in slow Morse code.  
When the device is configured in Access Point mode, it will blink out "AP" followed by the device's IP address. 
If the device cannot connect to the Wi-Fi network, it will blink "ERR" in Morse code.

Hold down the Mode Selector button two seconds to switch the device in or out of Access Point Mode (for configuring
the Wi-Fi network.) The device will restart, and you should see a different message blinking out in Morse code.

## What is all this software stuff, anyway?

Here's a brief guide to what all code is...

### Application files:

This table describes what the source modules do.

| Filename                                 | Description                                                                      |
|------------------------------------------|----------------------------------------------------------------------------------|
| src/switch-control/http_server.py        | this is a lightweight HTTP ("web") server.                                       |
| src/switch-control/main.py               | mainline program.                                                                |
| src/switch-control/micro_logging.py      | lightweight logging, similar to Python's 'logging'                               |
| src/switch-control/morse_code.py         | code to send morse code on the LED.  Not all letters are included to save space. |
| src/switch-control/not_machine.py        | mock 'machine' interface, for debugging on platforms other than MicroPython.     |
| src/switch-control/picow_network.py      | networking common code for Pico-W                                                |
| src/switch-control/relays.py             | relay control code                                                               |
| src/switch-control/utils.py              | common utility functions                                                         |
| src/switch-control/content/antennas.html | Antennas Configuration page                                                      |
| src/switch-control/content/favicon.ico   | Icon for web site                                                                |
| src/switch-control/content/files.html    | Files page                                                                       |
| src/switch-control/content/network.html  | Network Configuration Page                                                       |
| src/switch-control/content/radios.html   | Radios Configuration Page                                                        |
| src/switch-control/content/switch.html   | Switch Control Panel Page                                                        |
| src/switch-control/data/config.json      | configuration file for device.                                                   |

Note that it is possible to modify any of the User Interface pages.  The software wants to protect these files, you
will need to upload them using a different name, and then rename them.

If you feel adventurous, you can modify the `config.json` file to set your Wi-Fi SSID and secret prior to loading the
software.

### Additional Stuff

Here's the code that makes up the "Easy Loader".

| Filename              | Description                                                                       |
|-----------------------|-----------------------------------------------------------------------------------|
| src/loader/loader.py  | tool to more easily install Python code on Pico W                                 |
| src/loader/pyboard.py | code to allow communication and control of MicroPython boards, used by loader.py. |


