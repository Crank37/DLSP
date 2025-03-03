import joblib
import pandas as pd
import numpy as np
import certifi
from pymongo import MongoClient
import threading
import time



from bson.json_util import dumps
from bson.json_util import loads

from sklearn.preprocessing import StandardScaler
import lightgbm as lgb

#Optionen
#1: Trainingsdaten 23_02, Validierungsdaten 27_02
#2: Trainingsdaten 23_02, Validierungsdaten 23_02_128 (Hier wurden Werte H)



#---------------------------------------------- Ab hier:  Funktionen aus Jupyter ------------------------------------------------------

#Funktion zur Druchführung FFT mit Tiefpassfilter
def calcFFT(accel, cutoff=50, fss = 100):
    n = accel.size
    freq = np.fft.rfftfreq(n, d=1/fss)  # Frequenzachse berechnen

    accel_without_mean = accel-np.mean(accel) #Subtract mean
    yfreq = np.fft.rfft(accel_without_mean,n,norm='ortho')

    # Tiefpassfilter anwenden (hohe Frequenzen entfernen)
    yfreq[freq > cutoff] = 0
    
    yfreq = np.abs(yfreq)
    yfreq[0]=0.0 #Suppress DC Offset
    yfreq = yfreq/n
    return yfreq


def calcAGes(ax,ay,az):
    return np.sqrt(ax*ax+ay*ay+az*az)

#Objekt aus Datenbank in ein pd Frame umwandeln mit Betrag Beschleunigungen
def create_df_Ages(df, obj, n):
    ind = int((n/2) +1)
    #Listen
    ax_list = []
    ay_list = []
    az_list = []

    #arrays
    df_list = np.zeros(n)
    df_add = np.zeros(ind-1)
    
    #BSON in JSON umwandeln
    dictionary = dumps(obj)
    objs = loads(dictionary)

    df["label"] = df["label"].astype(str)


    #Durchiterieren Objekte
    for ind, teilobj in enumerate(objs):
        ax_list = teilobj["ax"]
        ay_list = teilobj["ay"]
        az_list = teilobj["az"]
        
        #Innerhalb Objetkte auf beschleunigungs zugreifen und berechnet in die Liste einfpgen
        for i in range(n):
            df_list[i] = calcAGes(ax_list[i], ay_list[i], az_list[i])

        #Frequenztransformation durchführen
        df_add = calcFFT(df_list)

        #in die Liste hinzufügen
        df.loc[len(df)] = df_add
        df.loc[ind, "label"] = teilobj["label"]
    return df

#---------------------------------------------- Bis hier:  Funktionen aus Jupyter ------------------------------------------------------


class Simulation(object):
    """
    
    Erzeugung einer Istanz um ein Simulationsbetrieb der Klassifikation durchzuführen
    
    """

    def __init__(self, modelname, MDB_cloud_addr, dbinstance):
        #Klassifikator laden
        self.model = joblib.load(modelname)  # Laden des gespeicherten Modells

        #Initialisierung MongoDB
        self.MDB_cloud_addr = MDB_cloud_addr
        self.dbinstance = dbinstance
        self._Statustext = "Willkommen! \nWählen Sie eine Aktion aus!"

        #Initialisierung für FFT
        self.n_sample = 256

        self.fs = 100 # Hz
        self.period = 1/self.fs

        end_freq = self.fs/2      #fs:Nyquist 50Hz

        self.xf=np.linspace(0,int(end_freq),int(self.n_sample/2))

        #Für Matplotlib Widget
        self.values = []

        #Leeres Format für df erzeugen
        self.df = pd.DataFrame(columns=range(int(self.n_sample/2)))
        self.df['label'] = 0
        #self.df["label"] = self.df["label"].astype(str)

        #Zyklus für Datenabfrage (Klassifikation nacheinander)
        self.interval = 0.5
        
        self.bStop = False


    #---------------------------------------------- Simulation starten ------------------------------------------------------
       

    def start(self):
        """Startet den TCP-Server in einem separaten Thread."""

        self._Statustext = "Simulation startet ..."

        self.running = True

        #Receivedata Funktion im zusätzlichen Thread ausführen, sodass die Benutzeroberfläche parallel funktioniert
        thread = threading.Thread(target=self.cycle, daemon=True)
        thread.start()
    
    #Programmduchlauf
    def cycle(self):
        self.get_dataDB()

        last_time = time.perf_counter()  # Startzeitpunkt erfassen

        #Aufteilung
        Xtest,ylabel = self.get_Xtest_ylabel()

        scaler = StandardScaler()
        X_test_scaled = scaler.fit_transform(Xtest)    

        #Itereation mit Zählung tatsächliche Werte
        i = 0
        counttrue = 0

        count0 = 0  #Stillstand richtig klazzifiziert zählen
        count1 = 0  #Schleudern richtig klazzifiziert zählen
        count2 = 0  #Waschen richtig klazzifiziert zählen
        count3 = 0  #Spülen richtig klazzifiziert zählen

        sum0 = (ylabel == "Stillstand").sum()
        sum1 = (ylabel == "Schleudern").sum()
        sum2 = (ylabel == "Waschen").sum()
        sum3 = (ylabel == "Spülen").sum()


        while i < len(Xtest):
            current_time = time.perf_counter()

            #Für Plotten auf der GUI
            self.values = Xtest.iloc[i,0 :128].values.tolist() 
            
            if current_time - last_time >= self.interval:
                last_time = current_time  # Zeitstempel aktualisieren

                # Einzelne Zeile für Vorhersage nehmen
                #sample = X_test_scaled.iloc[i].values.reshape(1, -1)
                sample = X_test_scaled[i].reshape(1, -1)
                prediction = self.model.predict(sample)[0]  # Vorhersage des Modells


                if prediction == 1:
                    prediction = "Schleudern"
                elif prediction == 2:
                    prediction = "Waschen"
                elif prediction == 3:
                    prediction = "Spülen"
                else:
                    prediction = "Stillstand"

                # Vergleich mit dem echten Label
                true_label = ylabel[i]

                #Zählen richtige Klassifikationen
                if true_label == prediction:
                    counttrue += 1

                    if true_label == "Stillstand":
                        count0 += 1
                    elif true_label == "Schleudern":
                        count1 += 1
                    elif true_label == "Waschen":
                        count2 += 1
                    else:
                        count3 += 1 

                self._Statustext = f"Simulation \n\nKlassifikation Nr. {i+1} von {len(Xtest)} \nVorhersage = {prediction} \nWahres Label = {true_label} \n\nRichtige Ergebnisse: {counttrue}"

                if i == len(Xtest)-1:
                    self._Statustext = (
                        f"Simulation - Resultat\n\n"
                        f"Stillstand: {count0} von {sum0} richtig\n"
                        f"Schleudern: {count1} von {sum1} richtig\n"
                        f"Waschen:    {count2} von {sum2} richtig\n"
                        f"Spülen:     {count3} von {sum3} richtig\n"
                        f"Insgesamt:  {counttrue} von {len(Xtest)} richtig!"
)
                i += 1

            
            # Weitere Logik hier, um die CPU-Auslastung gering zu halten
            time.sleep(0.01)  # Kleine Verzögerung für Effizienz

            if self.bStop:
                self.bStop = False
                break


    def stop(self):
        self.bStop = True
        self._Statustext = "Willkommen! \nWählen Sie eine Aktion aus!"

        #Leeren des Dataframes
        self.df.drop(self.df.index, inplace=True)


    #---------------------------------------------- Daten Aufbereitung ------------------------------------------------------

    def get_Xtest_ylabel(self):
        Xtest = self.df.drop(columns=['label'])
        ylabel = self.df['label']
        return Xtest, ylabel

    #---------------------------------------------- Daten aus DB holen ------------------------------------------------------

    #Daten aus Datenbank in Dataframe gepackt
    def get_dataDB(self):
        """Empfangen der Daten aus der Datenbank"""

        #Erzeugung Verbindung zum Cloud
        MD_Cloud = MongoClient(self.MDB_cloud_addr, tlsCAFile=certifi.where())
        db_cloud = MD_Cloud[self.dbinstance]

        #Db abrufen und df befüllen
        Objekte = db_cloud.Accelerations.find()
        self.df = create_df_Ages(self.df, Objekte, self.n_sample)

    #---------------------------------------------- getter ------------------------------------------------------


    def get_statustext(self):
        """Getter-Methode für Statustext"""
        return self._Statustext
    
    def get_values_formatplotlib(self):
        """Getter-Methode für Statustext"""
        return self.xf, self.values