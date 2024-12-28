import socket
import struct
import certifi

from pymongo import MongoClient




class TCPServer_MDB(object):
    """
    
    Erzeugung einer Istanz ffür ein TCP Server und ein Mongo DB Client
    
    """
    #Initialisierung Attribute
    def __init__(self, host = "127.0.0.1", port = 65432):
        self.host = host
        self.port = port
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #Beschleunigungswerte
        self.__ax = []
        self.__ay = []
        self.__az = []

        #Antrainieren des Modells
        self.label = ""



    #---------------------------------------------- Server Start,Stopp ------------------------------------------------------
       

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        conn, addr = self.server_socket.accept() #blockiert weiteren Code, bis Client eine Verbindung mit server hergesetllt hat
        with conn:
            print(f"Verbunden mit der Adresse: {addr}")
            self.receivedata(conn)

    def stop(self):
        self.server_socket.close()
        print("Verbindung geschlossen!")

    #---------------------------------------------- Daten aufbereiten ------------------------------------------------------

    #Daten Erhalten
    def receivedata(self, conn):
        iter = 0
        while True:
            
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
                print(f"Length chunk data: {len(chunk_data)}")

                # Entpacke die Float-Daten
                floats = struct.unpack(f'{chunk_size // 4}f', chunk_data)

                # Verteile die Daten auf die drei Listen
                for i in range(0, len(floats), 3):
                    self.__ax.append(floats[i])
                    self.__ay.append(floats[i + 1])
                    self.__az.append(floats[i + 2])
                
            if iter > 10:
                print("Verbindung geschlossen")
                break
            print(f"Daten Nr. {iter} empfangen")

            self.getindb()

            iter += 1

    #Beschleunigungswerte ins array packen
    def _getinarray(self, data):
            
        """     for chunk in data:
                    #Splitten des ankommenden Datensatzes (256 DAten gesplittet)
                    data_set = chunk.split('\n')
                    # print(data_set)

                    for nr_data in data_set:
                        #Splitten je Datensatz alle drei Beschleunigungskomponenten in ein Array gespeichert['El1','El2' ...]
                        all_data = nr_data.split(',')

                        #Alle einzelnen Elemente in die Liste gepackt 
                        lengthdata = len(all_data)
                        if lengthdata > 0:
                            if len(all_data[0]) > 1:
                                self.__ax.append(float(all_data[0]))
                        if lengthdata > 1:
                            if len(all_data[1]) > 1:
                                self.__ay.append(float(all_data[1]))
                        if lengthdata > 2:
                            if len(all_data[2]) > 1:
                                self.__az.append(float(all_data[2]))"""
        


    #---------------------------------------------- Laden Daten in Mongo DB ------------------------------------------------------

    #DB Instanz erstellen oder aufrufen
    def create_opendb(self, dbinstance = "Acceleration",MDB_clientaddr_port = "localhost:27017", MDB_cloud_addr = "", cloud = 0, labeling = ""):
        self.cloud = cloud
        self.MD_local = MongoClient(MDB_clientaddr_port)
        self.db_local = self.MD_local[dbinstance]
        self.label = labeling

        #Erzeugung Verbindung zum Cloud
        if self.cloud == 1:
            self.MD_Cloud = MongoClient(MDB_cloud_addr, tlsCAFile=certifi.where())
            self.db_cloud = self.MD_Cloud[dbinstance]

        print(f"DB Instanz ({dbinstance}) erstellt!")
    
    #Daten in die DB packen und zurücksetzen
    def getindb(self):
        #Packt jedes Element rein als Dictionary
        array = [{'ax': self.__ax, 'ay': self.__ay, 'az': self.__az, "label":self.label}]

        self.db_local.Accelerations.insert_many(array)
        
        if self.cloud == 1:
            self.db_cloud.Accelerations.insert_many(array)

        #arrays leeren
        self.__ax.clear()
        self.__ay.clear()
        self.__az.clear()