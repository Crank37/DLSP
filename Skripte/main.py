from TCP import TCPServer_MDB

if __name__ == "__main__":
    server = TCPServer_MDB(host = "192.168.2.81", port = 53563, MDB_clientaddr_port = "localhost:27017")
    try:
        #Datenbank erzeugen
        server.create_opendb()
        #TCP Server starten
        server.start()

    except KeyboardInterrupt:
        print("Server geschlossen!")
        server.stop()