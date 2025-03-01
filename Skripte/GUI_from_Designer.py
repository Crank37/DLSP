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

class Ui_Datenerfassung(object):
    def setupUi(self, Datenerfassung):
        if not Datenerfassung.objectName():
            Datenerfassung.setObjectName(u"Datenerfassung")
        Datenerfassung.resize(803, 463)
        Datenerfassung.setAnimated(True)
        self.centralwidget = QWidget(Datenerfassung)
        self.centralwidget.setObjectName(u"centralwidget")
        self.bRecData = QPushButton(self.centralwidget)
        self.bRecData.setObjectName(u"bRecData")
        self.bRecData.setGeometry(QRect(520, 300, 181, 32))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setBold(True)
        self.bRecData.setFont(font)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.NetworkWireless))
        self.bRecData.setIcon(icon)
        self.bStop = QPushButton(self.centralwidget)
        self.bStop.setObjectName(u"bStop")
        self.bStop.setGeometry(QRect(520, 360, 181, 32))
        palette = QPalette()
        brush = QBrush(QColor(38, 74, 125, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        self.bStop.setPalette(palette)
        self.bStop.setFont(font)
        self.bStop.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.bStop.setAutoFillBackground(False)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ProcessStop))
        self.bStop.setIcon(icon1)
        self.bSim = QPushButton(self.centralwidget)
        self.bSim.setObjectName(u"bSim")
        self.bSim.setGeometry(QRect(520, 330, 181, 32))
        self.bSim.setFont(font)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))
        self.bSim.setIcon(icon2)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 0, 251, 31))
        font1 = QFont()
        font1.setPointSize(21)
        self.label.setFont(font1)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.tSampletime = QLineEdit(self.centralwidget)
        self.tSampletime.setObjectName(u"tSampletime")
        self.tSampletime.setGeometry(QRect(522, 230, 181, 21))
        self.tSampletime.setMaxLength(3)
        self.tLabel = QLineEdit(self.centralwidget)
        self.tLabel.setObjectName(u"tLabel")
        self.tLabel.setGeometry(QRect(520, 270, 181, 21))
        self.tLabel.setMaxLength(30)
        self.StatusText = QTextBrowser(self.centralwidget)
        self.StatusText.setObjectName(u"StatusText")
        self.StatusText.setGeometry(QRect(520, 60, 251, 131))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(520, 210, 151, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(710, 230, 31, 16))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(520, 250, 151, 16))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(520, 40, 151, 16))
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 40, 151, 16))
        self.widgetplot = QWidget(self.centralwidget)
        self.widgetplot.setObjectName(u"widgetplot")
        self.widgetplot.setGeometry(QRect(30, 70, 441, 291))
        Datenerfassung.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Datenerfassung)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 803, 37))
        Datenerfassung.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Datenerfassung)
        self.statusbar.setObjectName(u"statusbar")
        Datenerfassung.setStatusBar(self.statusbar)

        self.retranslateUi(Datenerfassung)

        QMetaObject.connectSlotsByName(Datenerfassung)
    # setupUi

    def retranslateUi(self, Datenerfassung):
        Datenerfassung.setWindowTitle(QCoreApplication.translate("Datenerfassung", u"MainWindow", None))
        self.bRecData.setText(QCoreApplication.translate("Datenerfassung", u"Daten empfangen", None))
        self.bStop.setText(QCoreApplication.translate("Datenerfassung", u"Stoppen", None))
        self.bSim.setText(QCoreApplication.translate("Datenerfassung", u"Simulation", None))
        self.label.setText(QCoreApplication.translate("Datenerfassung", u"Beschleuingungsmessung", None))
        self.tSampletime.setPlaceholderText(QCoreApplication.translate("Datenerfassung", u"10", None))
        self.tLabel.setPlaceholderText(QCoreApplication.translate("Datenerfassung", u"Stillstand", None))
        self.label_2.setText(QCoreApplication.translate("Datenerfassung", u"Abtastintervall", None))
        self.label_3.setText(QCoreApplication.translate("Datenerfassung", u"ms ", None))
        self.label_4.setText(QCoreApplication.translate("Datenerfassung", u"label", None))
        self.label_6.setText(QCoreApplication.translate("Datenerfassung", u"Status", None))
        self.label_7.setText(QCoreApplication.translate("Datenerfassung", u"Frequenzspektrum", None))
    # retranslateUi

