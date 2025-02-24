from TCP import TCPClient
import gc

if __name__ == "__main__":
    print("Frei verfügbarer Speicher:", gc.mem_free())  

    client = TCPClient(host = "192.168.2.107", port = 53565, ssid='BabaninWlani24Ghz', pw='BabaCocuk-1')
    client.connect_to_wifi()
    client.connect()
    client.get_time()
    client.set_rtc_time()
    client.message_timer(mode=1)

    print("unterbrochen!")