# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Benutzeroberflaeche.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QRadioButton, QSizePolicy,
    QStatusBar, QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(629, 301)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.bRecData = QPushButton(self.centralwidget)
        self.bRecData.setObjectName(u"bRecData")
        self.bRecData.setGeometry(QRect(450, 130, 151, 32))
        self.bStop = QPushButton(self.centralwidget)
        self.bStop.setObjectName(u"bStop")
        self.bStop.setGeometry(QRect(450, 160, 151, 32))
        self.bSim = QPushButton(self.centralwidget)
        self.bSim.setObjectName(u"bSim")
        self.bSim.setGeometry(QRect(450, 100, 151, 32))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 151, 16))
        self.bMan = QRadioButton(self.centralwidget)
        self.bMan.setObjectName(u"bMan")
        self.bMan.setGeometry(QRect(250, 130, 99, 20))
        self.bRealt = QRadioButton(self.centralwidget)
        self.bRealt.setObjectName(u"bRealt")
        self.bRealt.setGeometry(QRect(250, 160, 99, 20))
        self.tSampletime = QLineEdit(self.centralwidget)
        self.tSampletime.setObjectName(u"tSampletime")
        self.tSampletime.setGeometry(QRect(10, 110, 113, 21))
        self.tSampletime.setMaxLength(3)
        self.tLabel = QLineEdit(self.centralwidget)
        self.tLabel.setObjectName(u"tLabel")
        self.tLabel.setGeometry(QRect(10, 150, 113, 21))
        self.tLabel.setMaxLength(30)
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(10, 40, 151, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 629, 37))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.bRecData.setText(QCoreApplication.translate("MainWindow", u"Daten empfangen", None))
        self.bStop.setText(QCoreApplication.translate("MainWindow", u"Stoppen", None))
        self.bSim.setText(QCoreApplication.translate("MainWindow", u"Simulation", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Waschmachine", None))
        self.bMan.setText(QCoreApplication.translate("MainWindow", u"Manuell", None))
        self.bRealt.setText(QCoreApplication.translate("MainWindow", u"Echtzeit", None))
        self.tSampletime.setPlaceholderText(QCoreApplication.translate("MainWindow", u"10", None))
        self.tLabel.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Stillstand", None))
    # retranslateUi

