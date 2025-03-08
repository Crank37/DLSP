from TCP import TCPClient
import gc

if __name__ == "__main__":
    print("Frei verfügbarer Speicher:", gc.mem_free())  

    client = TCPClient(host = "xxx", port = 53565, ssid='xxx', pw='xxx', samplemode = 1)
    client.connect_to_wifi()
    client.connect()
    client.get_time()
    client.set_rtc_time()
    client.message_timer()

    print("unterbrochen!")