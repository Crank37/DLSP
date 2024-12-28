import sys
from PySide6.QtWidgets import QApplication, QLabel, QPushButton
from PySide6.QtCore import Slot

@Slot()
def StartVerb():
    print(True)
    return True

def CloseConn():
    print(False)
    return True

# Create the Qt Application
app = QApplication(sys.argv)
# Create a button, connect it and show it
button = QPushButton("Verbindung starten")
button2 = QPushButton("Verbindung schließen")
button.clicked.connect(StartVerb)
button2.clicked.connect(CloseConn)
button.show()
# Run the main Qt loop
app.exec()

