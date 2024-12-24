from TCP import TCPClient
import gc

if __name__ == "__main__":
    print("Frei verfügbarer Speicher:", gc.mem_free())  

    client = TCPClient(host = "192.168.2.81", port = 53563, ssid='BabaninWlani', pw='BabaCocuk-1')
    client.connect_to_wifi()
    client.connect()
    client.message_timer(10, 0)

    print("unterbrochen!")