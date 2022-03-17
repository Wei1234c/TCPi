# WiFi network _________________________
def wait_for_wifi():
    import network

    network.WLAN(network.AP_IF).active(False)
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        # sta_if.connect('SSID', 'PASSWORD')

        while not sta_if.isconnected():
            pass

    print('Network configuration:', sta_if.ifconfig())



wait_for_wifi()

# Signal boot successfully ___________
import led


led.blink_on_board_led(times = 2)
