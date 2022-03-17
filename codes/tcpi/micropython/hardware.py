import os


ON_BOARD_LED_PIN_NO = 2
ON_BOARD_LED_HIGH_IS_ON = (os.uname().sysname == 'esp32')

gpio_pins = (0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16)
