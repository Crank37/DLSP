import sys
from PySide6.QtCore import Signal, QObject, QTimer
from PySide6 import  QtWidgets
from GUI_from_Designer import Ui_MainWindow
from TCP import TCPServer_MDB
from Simulation import Simulation
import urllib 

#Zustände
#0: Aus - Stillstand
#1: Wasser Pumpvorgang (zu Beginn) und ggf. Heizvorgang (60° Wäsche)  -  Pumpvorgang
#2: Hin und Her drehen zum Waschen (Wasser mit Waschüulver) bzw Einweichen   - Waschen
#3: Abpumpen des Schmutzwassers + Zufügen neues Wasser zum Abspülen  -  Spülen
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

    def __init__(self, host, port, cloud, dbcloudurl, dbinstance, MLModelname):
        super().__init__()

        #Variable zum Umschalten Textfeld zwischen TCP und Simulation
        self.TCPActive = False
        self.SimActive = False

        self.server = TCPServer_MDB(host, port)

        #Simulation mit Klassifikiation
        self.sim = Simulation(MLModelname, dbcloudurl, dbinstance)

        #Verbindung zu Mongo DB herstellen und Datenbank erzeugen 
        self.server.create_opendb(dbinstance, MDB_clientaddr_port="localhost:27017", MDB_cloud_addr=dbcloudurl, cloud=cloud)

    def Status_Updater(self):
        #Bestimmung, ob Textfeld durch Simulation oder TCP Server ersetzt werden soll
        if self.TCPActive:
            text = self.server.get_statustext()
        else:
            text = self.sim.get_statustext()
        return str(text)

    def Receive_data(self, label: str, time: str):
        self.TCPActive = True
        #TCP Server starten
        if not self.SimActive:
            self.server.start(label=label, time=time)

    def start_sim(self):
        if not (self.SimActive and self.TCPActive):
            self.sim.start()
        self.SimActive = True
        
    def stop_server(self):
        if self.TCPActive:
            self.server.stop()
            self.TCPActive = False
        self.sim.stop()
        self.SimActive = False


#Benutzeroberfläche (Layout in Ui_MainWindow, erstellt mit Qt Designer)
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, server_controller):
        super().__init__()
        self.setupUi(self)

        self.server_controller = server_controller

        self.bRecData.clicked.connect(lambda: self.server_controller.Receive_data(self.tLabel.text(), str(self.tSampletime.text())))

        self.bStop.clicked.connect(lambda: self.server_controller.stop_server())

        self.bSim.clicked.connect(lambda: self.server_controller.start_sim())

        # Timer zur regelmäßigen Aktualisierung des Status
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(500)  

    def update_status(self):
        """Aktualisiert den Status-Text regelmäßig"""
        self.StatusText.setText(self.server_controller.Status_Updater())





if __name__ == "__main__":
    #Fenster Benutzeroberfläche
    app = QtWidgets.QApplication(sys.argv)

    #Cloud
    username = urllib.parse.quote_plus('mongo')
    password = urllib.parse.quote_plus('mongo')
    srv_url = f'mongodb+srv://{username}:{password}@cluster21045.2xlz5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster21045' 

    serverController = ServerController(host = "192.168.2.107", port = 53565, cloud=1, dbcloudurl=srv_url, dbinstance = "Messung2", MLModelname="LightGBM_model.pkl")

    #Benutzeroberfläche starten
    window = MainWindow(serverController)
    window.show()
    sys.exit(app.exec())

