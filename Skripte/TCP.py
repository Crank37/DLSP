import socket
import struct
import certifi
import threading

from pymongo import MongoClient




class TCPServer_MDB(object):
    """
    
    Erzeugung einer Istanz für ein TCP Server und ein Mongo DB Client
    
    """
    #Initialisierung Attribute
    def __init__(self, host = "127.0.0.1", port = 65432):
        self.host = host
        self.port = port
        
        #Beschleunigungswerte
        self.__ax = []
        self.__ay = []
        self.__az = []
        self.__timestamp = []

        #Status innerhalb Benutzeroberfläche updaten
        self._Statustext = "Willkommen! \nWählen Sie eine Aktion aus!"

        #Antrainieren des Modells
        self.label = ""

        #Zeitkonstante an Client
        self.sampletime = ""



    #---------------------------------------------- Server Start,Stopp ------------------------------------------------------
       

    def start(self, label, time):
        """Startet den TCP-Server in einem separaten Thread."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.running = True
        self.label = label      #nur für manuelle Datenaufnahme
        self.sampletime = time  #Abtastrate über GUI

        #Receivedata Funktion im zusätzlichen Thread ausführen, sodass die Benutzeroberfläche parallel funktioniert
        thread = threading.Thread(target=self.receivedata, daemon=True)
        thread.start()

    def stop(self):
        """Stoppt den Server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self._Statustext = "Verbindung geschlossen!"
        print("Verbindung geschlossen!")

    #---------------------------------------------- Nachricht an Client ------------------------------------------------------
    
    def set_time(self, conn):
        """Sendet die eingegebene Zeit an den Client"""

        #falls Feld im GUI freigelassen wurde, automatisch auf 10 setzen
        if self.sampletime == "":
            self.sampletime = "10"
        conn.send(self.sampletime.encode())



    #---------------------------------------------- Daten aufbereiten ------------------------------------------------------

    def receivedata(self):
            
            self._Statustext = "Daten empfangen \n\nVerbindung wird hergestellt ... "

            #Verbindung herstellen
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()

            #Daten
            iter = 0
            while self.running:
                conn, addr = self.server_socket.accept() #blockiert weiteren Code, bis Client eine Verbindung mit server hergesetllt hat

                with conn:
                    print(f"Verbunden mit der Adresse: {addr[0]}")
                    self.set_time(conn) #Zeit senden
                    while self.running:

                        ### Zur Übersichtlichkeit: Ab hier werden Daten empfangen und aufbereitet! ###

                        try:
                            # Gesamtlänge der Daten empfangen
                            total_samples = struct.unpack('I', conn.recv(4))[0]

                            # Daten in Chunks empfangen
                            while len(self.__ax) < total_samples:
                                # Länge des nächsten Chunks empfangen
                                chunk_size = struct.unpack('I', conn.recv(4))[0]
                                # Sicherstellen, dass der vollständige Chunk empfangen wird
                                chunk_data = b''
                                while len(chunk_data) < chunk_size:
                                    chunk_data += conn.recv(chunk_size - len(chunk_data))
                                print(f"Größe Empfangenen Teildaten: {len(chunk_data)}")

                                # Entpacke die Float-Daten
                                floats = struct.unpack(f'{chunk_size // 4}f', chunk_data)

                                # Verteile die Daten auf die drei Listen
                                for i in range(0, len(floats), 3):
                                    self.__ax.append(floats[i])
                                    self.__ay.append(floats[i + 1])
                                    self.__az.append(floats[i + 2])
                            
                            self._Statustext = f"Daten empfangen \n\nVerbunden mit: {addr[0]}\nEmpfangene Datenpakete {iter+1} \n\n{len(self.__ax+self.__ay+self.__az)} Werte von {3*256} erhalten!"
     
                            if iter > 50:
                                print("Verbindung geschlossen")
                                self.running = False
                                break
                            print(f"Daten Nr. {iter} empfangen")

                            self.getindb()

                            iter += 1

                        except (ConnectionResetError, BrokenPipeError):
                            print("Verbindung verloren")
                            break

    #---------------------------------------------- Laden Daten in Mongo DB ------------------------------------------------------

    #DB Instanz erstellen oder aufrufen
    def create_opendb(self, dbinstance = "Acceleration",MDB_clientaddr_port = "localhost:27017", MDB_cloud_addr = "", cloud = 0):
        #Erzeugung Verbindung lokale DB
        self.cloud = cloud
        if self.cloud == 0 or self.cloud == 2:
            self.MD_local = MongoClient(MDB_clientaddr_port)
            self.db_local = self.MD_local[dbinstance]

        #Erzeugung Verbindung zum Cloud
        if self.cloud == 1 or self.cloud == 2:
            self.MD_Cloud = MongoClient(MDB_cloud_addr, tlsCAFile=certifi.where())
            self.db_cloud = self.MD_Cloud[dbinstance]

        print(f"DB Instanz ({dbinstance}) erstellt!")
    
    #Daten in die DB packen und zurücksetzen
    def getindb(self):
        #Packt jedes Element rein als Dictionary
        array = [{'ax': self.__ax, 'ay': self.__ay, 'az': self.__az, "label":self.label}]

        if self.cloud == 0 or self.cloud == 2:
            self.db_local.Accelerations.insert_many(array)
        
        if self.cloud == 1 or self.cloud == 2:
            self.db_cloud.Accelerations.insert_many(array)

        #arrays leeren
        self.__ax.clear()
        self.__ay.clear()
        self.__az.clear()

        print("Durch")


    #---------------------------------------------- getter ------------------------------------------------------


    def get_statustext(self):
        """Getter-Methode für Statustext"""
        return self._Statustext
