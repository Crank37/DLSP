from machine import Timer
from machine import I2C
from machine import Pin
from machine import RTC
import ntptime

import network
import struct

import time
from imu import MPU6050
import usocket as socket

class TCPClient(object):

    """
    
    Klasse mit Initialisierungargumenten (host_id, port, Netzwerk_ssid, Netzwerk_Passwort, samplemode)
    
    """

    #Initialisierung des Client Sockets und Timers
    def __init__(self, host = "127.0.0.1", port = 12345, ssid = "abc", pw = "abc", samplemode = 0):
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
        self.__timestamps = []
        self.iter = 0

        # Echtzeituhr im Mikrocontroller initialisieren
        self.rtc = RTC()

        #Timer
        self.tim = Timer(-1)
        self.sampletime = 10 #ms
        self.samplemode = samplemode

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
    def message_timer(self):
        """
        
        sampletime in ms und mode 0 (128) oder 1 (256) Werte (je beschlunigungsachse) in einem Datenpaket zum versenden
        
        """

        #Abfangen richtiger Moduswert
        if self.samplemode < 0 or self.samplemode > 1:
            raise ValueError(f"Ungültiger Wert: {self.samplemode}.")

        #Anzahl Werte limitieren für ein Datenpaket
        if self.samplemode == 0:
            self.limit = 128
        else:
            self.limit = 256

        if self.connected:
            self.tim.init(mode=Timer.PERIODIC, period = self.sampletime, callback=self.send_message)
            
    #Nachricht senden
    def send_message(self, t):
        #Start des Timers
        start = time.ticks_ms()

        if self.connected:
            try:
                self.data_struct_send()
            except OSError as e:
                print(f"Communication failed: {e}")
                self.close()
        
        #Ende des Timers
        end = time.ticks_ms()
        elapsed = time.ticks_diff(end, start)
        print(elapsed)
    
    #Empfangen vom Server
    def get_time(self):
        self.sampletime = int(self.client_socket.recv(256).decode())
        print(f'Zeit auf {self.sampletime} ms gesetzt!')


    #---------------------------------------------- Datenstrukturierung ------------------------------------------------------

    def data_struct_send(self):

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

    #---------------------------------------------- Zeitsynchronisation [Verworfen] ------------------------------------------------------

    def set_rtc_time(self):
        """Synchronisieren RTC einmalig über NTP-Server"""
        try:
            ntptime.host = "pool.ntp.org"  
            ntptime.settime()  # Zeit von NTP-Server holen und RTC setzen
        except Exception as e:
            print("Fehler bei NTP-Synchronisation:", e)
            return

        #Korrektur Zeitzone von UTC zur lokale Zeit (MEZ)
        GMT_OFFSET = 3600  # MEZ = UTC+1
        local_time = time.localtime(time.time() + GMT_OFFSET)  # Lokale Zeit berechnen


        # RTC mit lokaler Zeit setzen (Jahr, Monat, Tag,Wochentag , Stunde, Minute, Sekunde, Mikrosekunden)
        self.rtc.datetime((local_time[0], local_time[1], local_time[2], local_time[6], local_time[3], local_time[4], local_time[5], 0))
        print(self.get_unix_timestamp())

    def get_unix_timestamp(self):
        """Berechnet den aktuellen UNIX-Zeitstempel aus der RTC."""
        rtc_time = self.rtc.datetime()
        
        # **Manuelle Unix-Zeit-Berechnung**
        unix_timestamp = (rtc_time[0] - 1970) * 31536000  # Jahre in Sekunden
        unix_timestamp += (rtc_time[1] - 1) * 2678400    # Monate (vereinfachte Annahme: 31 Tage/Monat)
        unix_timestamp += (rtc_time[2] - 1) * 86400      # Tage in Sekunden
        unix_timestamp += rtc_time[4] * 3600             # Stunden in Sekunden
        unix_timestamp += rtc_time[5] * 60               # Minuten in Sekunden
        unix_timestamp += rtc_time[6]                    # Sekunden

        return unix_timestamp

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