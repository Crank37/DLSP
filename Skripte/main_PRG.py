import sys
from PySide6.QtCore import Signal, QObject, QTimer
from PySide6 import  QtWidgets
from PySide6.QtWidgets import QVBoxLayout
from GUI_from_Designer import Ui_Datenerfassung
from TCP import TCPServer_MDB
from Simulation import Simulation
import urllib 

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

#Zustände
#0: Aus - Stillstand
#2: Hin und Her drehen zum Waschen (Wasser mit Waschüulver) bzw Einweichen   - Waschen
#3: Abpumpen des Schmutzwassers + Zufügen neues Wasser zum Abspülen  -  Spülen
#4: Schleudervorgang - Schleudern
#i: Spülen mit Schleudern (große Schwingungen durch hohe Unwuchten)  -  Spülschleudern

#---------------------------------------------- Instanz mit TCP und Simulationsklasse ------------------------------------------------------

#Klasse zur Kopplung Elemente aus Benutzeroberfläche mit TCPServer_MDB Klasse (Start,Stopp Server)
class ServerController(QObject):
    """
    host, port: IP-Adresse und Port, worüber der TCP Server läuft
    cloud: 0 lokal, 1 nur cloud, 2 cloud und lokal
    dbcloudurl: URL des Servers
    dbinstance: Name DB (Gilt für das Hochladen Daten und für Abrufen (Simulation))
    MLModelname: Name des ML-Models (Im selben Pfad)
    simspeed: Simulationsgeschwindigkeit Zyklus in s

    """

    # Signal zur Kommunikation mit der GUI
    message_received = Signal(str)

    def __init__(self, host, port, cloud, dbcloudurl, dbinstance, MLModelname, simspeed):
        super().__init__()

        #Variable zum Umschalten Textfeld zwischen TCP und Simulation
        self.TCPActive = False
        self.SimActive = False

        self.server = TCPServer_MDB(host, port)

        #Simulation mit Klassifikiation
        self.sim = Simulation(MLModelname, dbcloudurl, dbinstance, simspeed)

        #Verbindung zu Mongo DB herstellen und Datenbank erzeugen 
        self.server.create_opendb(dbinstance, MDB_clientaddr_port="localhost:27017", MDB_cloud_addr=dbcloudurl, cloud=cloud)

    def Status_Updater(self):
        #Bestimmung, ob Textfeld durch Simulation oder TCP Server ersetzt werden soll
        if self.TCPActive:
            text = self.server.get_statustext()
        else:
            text = self.sim.get_statustext()
        return str(text)

    def Graph_Updater(self):
        #Werte für die Darstellung des Frequenzspektrums
        if self.SimActive:
            xf, list = self.sim.get_values_formatplotlib() #eine Liste

            #Damit 128 Elemente immer gefüllt werden (da am Anfang keine Elemente)
            if len(list) == 0:
                list = [0] * 128
            return xf, list
        return [0] * 128, [0] * 128


    def Receive_data(self, label: str, time: str):
        self.TCPActive = True
        #TCP Server starten
        if not self.SimActive:
            self.server.start(label=label, time=time)

    def start_sim(self):
        if not (self.SimActive or self.TCPActive):
            self.sim.start()
        self.SimActive = True
        
    def stop_sim_server(self):
        if self.TCPActive:
            self.server.stop()
            self.TCPActive = False
        self.sim.stop()
        self.SimActive = False

#---------------------------------------------- Aktionen über GUI ------------------------------------------------------

#Benutzeroberfläche (Layout in Ui_MainWindow, erstellt mit Qt Designer)
class MainWindow(QtWidgets.QMainWindow, Ui_Datenerfassung):
    def __init__(self, server_controller):
        super().__init__()
        self.setupUi(self)

        self.server_controller = server_controller

        #Funktionen Triggern
        self.bRecData.clicked.connect(lambda: self.server_controller.Receive_data(self.tLabel.text(), str(self.tSampletime.text())))

        self.bStop.clicked.connect(lambda: self.server_controller.stop_sim_server())

        self.bSim.clicked.connect(lambda: self.server_controller.start_sim())

        # Matplotlib-Widget in Qt Creator UI einfügen
        self.layout = QVBoxLayout(self.widgetplot)  # `widgetplot` ist dein Platzhalter-Widget
        self.plot_widget = MatplotlibWidget(self.widgetplot)  # Matplotlib in `widgetplot` einfügen
        self.layout.addWidget(self.plot_widget)  # Matplotlib-Widget zum Layout hinzufügen
        self.plot_widget.plot_data([0] * 128, [0] * 128)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(300)  

    def update_status(self):
        """Aktualisiert den Status-Text regelmäßig"""
        self.StatusText.setText(self.server_controller.Status_Updater())

        #Plot
        xf, liste = self.server_controller.Graph_Updater()
        # Beispiel-Plot zeichnen

        self.plot_widget.plot_data(xf, liste)


#---------------------------------------------- Matplot als Widget ------------------------------------------------------


class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure, self.ax = plt.subplots()
        super().__init__(self.figure)
        self.setParent(parent)

    def plot_data(self, x, y):
        """Passt Matplotlib exakt an das Qt-Widget an, macOS-kompatibel."""
        self.ax.clear()

        # Daten plottens
        self.ax.plot(x, y, label="128 Sensorwerte", color='r', linewidth=1)

        # Statische Achsenbereiche
        self.ax.set_xlim(0, 55)
        self.ax.set_ylim(0, 0.0005)

        # Achsenbeschriftungen
        self.ax.set_xlabel("Frequenz (Hz)", fontsize=10, fontweight="bold", labelpad=5)
        self.ax.set_ylabel("Normierte Amplitude", fontsize=10, fontweight="bold", labelpad=5)
        self.ax.set_title("FFT Beschleunigungsbeträge", fontsize=12, fontweight="bold", pad=10)

        # Achsenticks
        self.ax.tick_params(axis='both', which='major', labelsize=6)

        # Raster für bessere Lesbarkeit
        self.ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

        # Legende positionieren
        self.ax.legend(loc="upper right", fontsize=6, frameon=True)

        # Layout optimieren, damit alles sichtbar bleibt
        self.figure.tight_layout()

        # Neu zeichnen
        self.draw()

#---------------------------------------------- Ausführung ------------------------------------------------------

if __name__ == "__main__":
    #Fenster Benutzeroberfläche
    app = QtWidgets.QApplication(sys.argv)

    #Cloud
    username = urllib.parse.quote_plus('mongo')
    password = urllib.parse.quote_plus('mongo')
    srv_url = f'mongodb+srv://{username}:{password}@cluster21045.2xlz5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster21045' 

    serverController = ServerController(host = "xxx", port = 53565, cloud=2, dbcloudurl=srv_url, dbinstance = "Messung01_03", MLModelname="LightGBM_model.pkl", simspeed = 0.5)

    #Benutzeroberfläche starten
    window = MainWindow(serverController)
    window.show()
    sys.exit(app.execs())

