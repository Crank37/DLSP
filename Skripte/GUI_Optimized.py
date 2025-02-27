
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit)
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Klassifikations-Status")
        MainWindow.setGeometry(100, 100, 500, 400)
        
        # Set modern dark theme
        palette = MainWindow.palette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40))
        palette.setColor(QPalette.WindowText, QColor(240, 240, 240))
        MainWindow.setPalette(palette)
        
        # Layout
        self.centralwidget = QWidget(MainWindow)
        main_layout = QVBoxLayout(self.centralwidget)
        
        # Header Label
        self.header_label = QLabel("Klassifikationssystem", self.centralwidget)
        self.header_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.header_label)
        
        # Input Bereich
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self.centralwidget)
        self.input_field.setPlaceholderText("Geben Sie die Daten ein...")
        input_layout.addWidget(self.input_field)
        self.classify_button = QPushButton("Klassifizieren", self.centralwidget)
        self.classify_button.setFont(QFont("Arial", 12))
        input_layout.addWidget(self.classify_button)
        main_layout.addLayout(input_layout)
        
        # Status Label
        self.status_label = QLabel("Status: Unbekannt", self.centralwidget)
        self.status_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("border: 1px solid #555; padding: 10px; background-color: #222; color: #FFD700; border-radius: 5px;")
        main_layout.addWidget(self.status_label)
        
        MainWindow.setCentralWidget(self.centralwidget)

if __name__ == "__main__":
    app = QApplication([])
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec()