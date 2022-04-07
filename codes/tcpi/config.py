import sys


# 'esp8266' or 'win32'
# SYS_PLATFORM = sys.platform

# 'micropython' or 'cpython'
# SYS_IMPLEMENTATION = sys.implementation.name
IS_MICROPYTHON = sys.implementation.name == 'micropython'

# DEBUG_MODE = True

# Hardware **********************
ON_BOARD_LED_PIN_NO = 5
ON_BOARD_LED_HIGH_IS_ON = False
LED_ON_ms = 3
LED_OFF_ms = 0

# Avoid some pins of ESP32,
# see: https://randomnerdtutorials.com/esp32-pinout-reference-gpios/
I2C_SCL_PIN_ID = 17
I2C_SDA_PIN_ID = 5
RESET_PIN_ID = 13

# WiFi **********************
SSID = 'SSID'
PASSWORD = 'PASSWORD'

# Shared ************************
BUFFER_SIZE = 1024 * 10  # ADAU1701 needs 9332 bytes to accommodate full update from SigmaStudio.

# Socket Server ***************************
CMD_RESET = b'Reset'
CMD_SET_PROTERTIES = b'SetProterties'
CMD_GET_PROTERTIES = b'GetProterties'
BIND_IP = '0.0.0.0'  # the ip which broker listens to.
BIND_PORT = 8086
MAX_CONCURRENT_CONNECTIONS = 20
SERVER_POLLING_REQUEST_TIMEOUT_SECONDS = 60

# Socket Client ************************
SERVER_IP = '127.0.0.1'
SERVER_PORT = BIND_PORT
CLIENT_RETRY_TO_CONNECT_AFTER_SECONDS = 3
CLIENT_RECEIVE_TIME_OUT_SECONDS = 2
MICROPYTHON_SOCKET_CONNECTION_RESET_ERROR_MESSAGE = '[Errno 104] ECONNRESET'
