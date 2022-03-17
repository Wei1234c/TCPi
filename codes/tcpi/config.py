import sys


# 'esp8266' or 'win32'
# SYS_PLATFORM = sys.platform

# 'micropython' or 'cpython'
# SYS_IMPLEMENTATION = sys.implementation.name
IS_MICROPYTHON = sys.implementation.name == 'micropython'

# DEBUG_MODE = True


# Shared ************************
BUFFER_SIZE = 1024 * 10  # ADAU1701 needs 9332 bytes to accommodate full update from SigmaStudio.

# Socket Server ***************************
BIND_IP = '0.0.0.0'  # the ip which broker listens to.
BIND_PORT = 8086
MAX_CONCURRENT_CONNECTIONS = 20

# Socket Client ************************
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8086
CLIENT_RETRY_TO_CONNECT_AFTER_SECONDS = 3
CLIENT_RECEIVE_TIME_OUT_SECONDS = 1
MICROPYTHON_SOCKET_CONNECTION_RESET_ERROR_MESSAGE = '[Errno 104] ECONNRESET'
