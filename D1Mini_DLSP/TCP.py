from machine import Timer
from machine import I2C
from machine import Pin

import network
import gc
import struct

import time
from imu import MPU6050
import usocket as socket

class TCPClient(object):

    """
    
    Klasse mit Initialisierungargumenten (host_id, port, Netzwerk_ssid, Netzwerk_Passwort)
    
    """

    #Initialisierung des Client Sockets und Timers
    def __init__(self, host = "127.0.0.1", port = 12345, ssid = "abc", pw = "abc"):
        #Netwerk
        self.host = host
        self.port = port
        self.ssid = ssid
        self.pw = pw
        self.connected = False

        #Listen Werte
        self.__accel_x = []
        self.__accel_y = []
        self.__accel_z = []
        self.__datastring = ''
        self.iter = 0

        #Timer
        self.tim = Timer(-1)
        self.sampletime = 0

        #TCP Socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(10)  # Timeout auf 10 Sekunden setzen

        #Schnittstelle IMU mit Beschleunigungswerten
        i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
        mpu6050 = MPU6050(i2c)
        self.accel = mpu6050.accel

    #---------------------------------------------- Verbindung ------------------------------------------------------

    #Netzwerkverbindung
    def connect_to_wifi(self):
        wlan = network.WLAN(network.STA_IF)  # Station-Modus für die Verbindung zu einem WLAN
        wlan.active(True)  # WLAN aktivieren

        if not wlan.isconnected():
            print("Connecting to WiFi...")
            wlan.connect(self.ssid, self.pw)  # Verbindung herstellen
            while not wlan.isconnected():
                print("Waiting for connection...")
                time.sleep(1)
                
    #Verbindung TCPServer
    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to server at {self.host}:{self.port}")
        except OSError as e:
            print(f"Connection failed: {e}")
            self.close()

    #---------------------------------------------- Nachricht ------------------------------------------------------

    #periodisches Triggern nachricht
    def message_timer(self, sampletime, mode = 1):
        """
        
        sampletime in ms und mode 0 (128) oder 1 (256) Werte (je beschlunigungsachse) in einem Datenpaket zum versenden
        
        """

        #Abfangen richtiger Moduswert
        if mode < 0 or mode > 1:
            raise ValueError(f"Ungültiger Wert: {mode}.")
        self.mode = mode

        #Anzahl Werte limitieren für ein Datenpaket
        if self.mode == 0:
            self.limit = 128
        else:
            self.limit = 256

        if self.connected:
            self.tim.init(mode=Timer.PERIODIC, period = sampletime, callback=self.send_message)
            
    #Nachricht senden
    def send_message(self, t):
        #Start des Timers
        start = time.ticks_ms()

        if self.connected:
            try:
                self.data_int()
            except OSError as e:
                print(f"Communication failed: {e}")
                self.close()
        
        #Ende des Timers
        end = time.ticks_ms()
        elapsed = time.ticks_diff(end, start)
        print(elapsed)
    
    #Empfangen vom Server
    def get_time(self):
        print("1-------------------------------")
        self.client_socket.bind((self.host, self.port))
        print("2")
        self.client_socket.listen()
        print("3")

        while True:
            conn, addr = self.client_socket.accept()
            with conn:
                try:
                    self.sampletime = conn.recv()
                except:
                    self.sampletime = 10
                    print("Zeitintervall wurde auf 10ms gesetzt")
                
                break

        #falls nichts weitergegeben wurde
        if self.sampletime == "":
            self.sampletime = 10

        print(f'Zeit auf {self.sampletime} ms gesetzt!')


    #---------------------------------------------- Datenstrukturierung ------------------------------------------------------

    #Datenpaket zusammenpacken in ein String
    def data_string(self):
        if self.iter >= self.limit:
            self.client_socket.sendall(self.__datastring.encode())
            self.__datastring.clear()
            self.iter = 0

        before = gc.mem_free()
        self.__datastring += '{0:3.5f},{1:3.5f},{2:3.5f}\n'.format(self.accel.x,self.accel.y,self.accel.z)
        after = gc.mem_free()

        # Speicherverbrauch berechnen
        used_memory = before - after
        print(f"Speicherverbrauch der Variable: {used_memory} Bytes")

        self.iter += 1


    def data_int(self):

        if self.iter >= self.limit:
            chunk_size = self.limit / 4
            packed_data = b''
            print(f"Länge der Listen x {len(self.__accel_x)}, y {len(self.__accel_y)}, z{len(self.__accel_z)} ")
            combined_data = zip(self.__accel_x, self.__accel_y, self.__accel_z)

            # Gesamtlänge der Daten
            total_samples = self.limit
            self.client_socket.send(struct.pack('I', total_samples))  # Gesamtlänge der Daten senden

            for i, (x, y, z) in enumerate(combined_data): #0 bis i
                # Packe jedes Tripel von Floats in Binärdaten
                packed_data += struct.pack('fff', x, y, z)

                # Sende, wenn ein Chunk voll ist oder die Daten vollständig sind
                if (i + 1) % chunk_size == 0 or (i + 1) == total_samples: 
                    # Länge des gepackten Chunks senden
                    self.client_socket.send(struct.pack('I', len(packed_data)))
                    # Chunk-Daten senden
                    self.client_socket.sendall(packed_data)  
                    print(f"gesendet Länge : {len(packed_data)}")

                    packed_data = b''

            self.iter = 0
            self.__accel_x.clear()
            self.__accel_y.clear()
            self.__accel_z.clear()
        
        self.__accel_x.append(self.accel.x)
        self.__accel_y.append(self.accel.y)
        self.__accel_z.append(self.accel.z)

        self.iter += 1

    

    #---------------------------------------------- Verbindung schließen ------------------------------------------------------

    #Client Verbindung schließen    
    def close(self):
        try:
            self.tim.deinit()
            self.client_socket.close()
        except OSError:
            pass
        self.connected = False
        print("Socket closed and timer stopped")




