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
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(629, 301)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.bRecData = QPushButton(self.centralwidget)
        self.bRecData.setObjectName(u"bRecData")
        self.bRecData.setGeometry(QRect(450, 10, 151, 32))
        self.bStop = QPushButton(self.centralwidget)
        self.bStop.setObjectName(u"bStop")
        self.bStop.setGeometry(QRect(450, 50, 151, 32))
        self.bSim = QPushButton(self.centralwidget)
        self.bSim.setObjectName(u"bSim")
        self.bSim.setGeometry(QRect(450, 90, 151, 32))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 151, 16))
        font = QFont()
        font.setPointSize(21)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.tSampletime = QLineEdit(self.centralwidget)
        self.tSampletime.setObjectName(u"tSampletime")
        self.tSampletime.setGeometry(QRect(20, 150, 113, 21))
        self.tSampletime.setMaxLength(3)
        self.tLabel = QLineEdit(self.centralwidget)
        self.tLabel.setObjectName(u"tLabel")
        self.tLabel.setGeometry(QRect(20, 200, 113, 21))
        self.tLabel.setMaxLength(30)
        self.StatusText = QTextBrowser(self.centralwidget)
        self.StatusText.setObjectName(u"StatusText")
        self.StatusText.setGeometry(QRect(20, 60, 251, 61))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 130, 151, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(150, 150, 31, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 180, 151, 16))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(320, 150, 301, 71))
        self.label_5.setAcceptDrops(False)
        self.label_5.setWordWrap(True)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 40, 151, 16))
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
        self.tSampletime.setPlaceholderText(QCoreApplication.translate("MainWindow", u"10", None))
        self.tLabel.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Stillstand", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Abtastintervall", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"ms ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"label", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Vor dem start den Abtastintervall (mind. 10ms) w\u00e4hlen. Das Label nur f\u00fcr das Antrainieren des Modells verwendet!", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Status", None))
    # retranslateUi

