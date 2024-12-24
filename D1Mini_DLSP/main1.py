#Verbindung prüfen
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('BabaninWlani', 'BabaCocuk-1')

while not wlan.isconnected():
    pass
print("Connected to WiFi:", wlan.ifconfig())