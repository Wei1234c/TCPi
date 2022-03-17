# SigmaStudio TCPIP Channel Tools Box

## What is this?
- This is a Python package, with which you can:
    - Use USBi as a general-purpose USB-I2C converter.
    - Control I2C devices from PC.
- Functionality of USB-SPI converter is also implemented, but not tested yet (2022/3/14).

## Why?
- I was playing with ADI SigmaDSP (ADAU1701/ADAU1401), see [github repo](https://github.com/Wei1234c/SigmaDSP), and need a USB-I2C converter.
- [FTDI FT232H](https://www.google.com/search?q=ftdi+ft232h&sxsrf=APq-WBvh8jByLE89c5v9AHCrUAZXqxOAmA:1646325613903&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjCrZrrsKr2AhVL05QKHeoaD4gQ_AUoAXoECAEQAw&biw=1396&bih=585&dpr=1.38) is a good piece of USB-I2C converter. However, some may already have an USBi device, why not use it for that?

## How to use it
- Please see [here](https://github.com/Wei1234c/USBi/blob/master/codes/test/i2c_test.py), [here](https://github.com/Wei1234c/USBi/blob/master/notebooks/USBi%20as%20USB-to-I2C%20convertor%20test.ipynb) and [here](https://github.com/Wei1234c/SigmaDSP/blob/master/notebooks/Functional%20test/Functional%20Demostration%20-%20with%20USBi%20as%20USB-I2C%20converter.ipynb).

## Limitations
- I found that communication hangs when handling a large chunk (1K bytes or so) of data, not sure why. 

## Dependencies
- [Zadig](https://zadig.akeo.ie/)
    - Need to switch the USB driver to WinUSB for USBi (on Windows).
    - To restore USBi, go to "Windows device manager" and switch back to the ADI USBi driver, therefore SigmaStudio can recognize the device again.
- [libusb1](https://pypi.org/project/libusb1/)
- [pyusb](https://pypi.org/project/pyusb/)
- [FX2LP](https://github.com/Wei1234c/FX2LP)