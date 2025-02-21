import sys
from PySide6.QtCore import Signal, QObject
from PySide6 import  QtWidgets
from GUI_from_Designer import Ui_MainWindow
from TCP import TCPServer_MDB
import urllib 

#Zustände
#0: Aus - Stillstand
#1: Wasser Pumpvorgang (zu Beginn) und ggf. Heizvorgang (60° Wäsche)  -  Pumpvorgang
#2: Hin und Her drehen zum Waschen (Wasser mit Waschüulver) bzw Einweichen   - Waschen
#3: Abpumpen des Schmutzwassers + Zufügen neues Wasser zum Absülen  -  Spülen
#4: Schleudervorgang - Schleudern


"""loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)
window = loader.load("Benutzeroberflaeche.ui", None)
window.show()
app.exec()"""

#pyside6-uic Benutzeroberflaeche.ui -o GUI_from_Designer.py 

#Klasse zur Kopplung Elemente aus Benutzeroberfläche mit TCPServer_MDB Klasse (Start,Stopp Server)
class ServerController(QObject):
    """
    host, port: IP-Adresse und Port, worüber der TCP Server läuft
    cloud: 0 lokal, 1 zusätliche Nutzung der Cloud
    dbcloudurl: URL des Servers
    """

    # Signal zur Kommunikation mit der GUI
    message_received = Signal(str)

    def __init__(self, host, port, cloud, dbcloudurl, dbinstance):
        super().__init__()

        self.server = TCPServer_MDB(host, port)

        #Verbindung zu Mongo DB herstellen und Datenbank erzeugen 
        self.server.create_opendb(dbinstance, MDB_clientaddr_port="localhost:27017", MDB_cloud_addr=dbcloudurl, cloud=cloud)


    def Receive_data(self, label: str, time: str):
        #TCP Server starten
        self.server.start(label=label, time=time)
        
    def stop_server(self):
        self.server.stop()

#Benutzeroberfläche (Layout in Ui_MainWindow, erstellt mit Qt Designer)
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, server_controller):
        super().__init__()
        self.setupUi(self)

        self.server_controller = server_controller

        self.bRecData.clicked.connect(lambda: self.server_controller.Receive_data(self.tLabel.text(), str(self.tSampletime.text())))

        self.bStop.clicked.connect(lambda: self.server_controller.stop_server())





if __name__ == "__main__":
    #Fenster Benutzeroberfläche
    app = QtWidgets.QApplication(sys.argv)

    #Cloud
    username = urllib.parse.quote_plus('mongo')
    password = urllib.parse.quote_plus('mongo')
    srv_url = f'mongodb+srv://{username}:{password}@cluster21045.2xlz5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster21045' 

    serverController = ServerController(host = "192.168.2.101", port = 53565, cloud=1, dbcloudurl=srv_url, dbinstance = "Messung21_02")

    #Benutzeroberfläche starten
    window = MainWindow(serverController)
    window.show()
    sys.exit(app.exec())

