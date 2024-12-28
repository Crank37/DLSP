from TCP import TCPServer_MDB
import urllib 

if __name__ == "__main__":

    #Eingangsdaten Cloud
    username = urllib.parse.quote_plus('mongo')
    password = urllib.parse.quote_plus('mongo')
    srv_url = f'mongodb+srv://{username}:{password}@cluster21045.2xlz5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster21045' 
    
    server = TCPServer_MDB(host = "192.168.2.81", port = 53565)
    try:
        #Verbindung zu Mongo DB herstellen und Datenbank erzeugen (0: nur lokal, 1: mit cloud)
        server.create_opendb(cloud=1, MDB_clientaddr_port="localhost:27017", MDB_cloud_addr=srv_url, labeling="Schleudern")
        #TCP Server starten
        server.start()

    except KeyboardInterrupt:
        print("Server geschlossen!")
        server.stop()