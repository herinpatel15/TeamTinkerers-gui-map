from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QWidget, QHBoxLayout, \
    QVBoxLayout, QGridLayout, QLabel, \
    QPushButton, QFileDialog, QStackedWidget, \
    QListWidget, QListWidgetItem, QComboBox
import sys
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QFontDatabase, QImage, QPalette, QBrush
from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pandas as pd
import numpy as np
import folium
import pyqtgraph as pg
import os

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()

        self.setWindowTitle("Team Tinkerers")
        self.setGeometry(300, 300, 600, 400)
        self.setIcon()
        self.widgetUi = QWidget()
        self.widgetUi.setStyleSheet("background: #D1D8E4;")
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.navbar()

        self.mainUi()

        self.widgetUi.setLayout(self.layout)
        self.setCentralWidget(self.widgetUi)

        self.showMaximized()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def setIcon(self):
        icon = QIcon("./src/logo.png")
        self.setWindowIcon(icon)

    def mainUi(self):
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.setContentsMargins(0, 0, 0, 0)

        self.filePage()
        self.dasPage()
        self.cusDasPage()

        self.layout.addWidget(self.stackedWidget)

    def navbar(self):
        nav = QWidget()
        nav.setFixedWidth(60)
        nav.setStyleSheet("background: #1F5ED8;")
        navLayout = QVBoxLayout()
        navLayout.setContentsMargins(0, 30, 0, 0)
        navLayout.setAlignment(QtCore.Qt.AlignTop)

        logo = QLabel()
        pix = QPixmap("./src/ttLogo.png")
        logo.setPixmap(pix)
        logo.setFixedSize(pix.width(), pix.height())

        navBtnLayout = QVBoxLayout()
        navBtnLayout.setContentsMargins(0, 20, 0, 0)

        fileLayout = QVBoxLayout()
        fileLayout.setContentsMargins(0, 30, 0, 0)
        self.fileBtn = QPushButton()
        fileIco = QIcon("./src/fileUploadeActiv.png")
        self.fileBtn.setIcon(fileIco)
        self.fileBtn.setStyleSheet("border: 0;")
        self.fileBtn.setIconSize(QtCore.QSize(30, 30))
        self.fileBtn.clicked.connect(lambda: self.filePageClick())
        fileLayout.addWidget(self.fileBtn)

        dasLayout = QVBoxLayout()
        dasLayout.setContentsMargins(0, 30, 0, 0)
        self.dasBtn = QPushButton()
        dasIco = QIcon("./src/dasboard.png")
        self.dasBtn.setIcon(dasIco)
        self.dasBtn.setStyleSheet("border: 0;")
        self.dasBtn.setIconSize(QtCore.QSize(30, 30))
        self.dasBtn.clicked.connect(lambda: self.dasPageClick())
        dasLayout.addWidget(self.dasBtn)

        cusDasLayout = QVBoxLayout()
        cusDasLayout.setContentsMargins(0, 30, 0, 0)
        self.cusDasBtn = QPushButton()
        cusDasIco = QIcon("./src/cusDas.png")
        self.cusDasBtn.setIcon(cusDasIco)
        self.cusDasBtn.setStyleSheet("border: 0;")
        self.cusDasBtn.setIconSize(QtCore.QSize(30, 30))
        self.cusDasBtn.clicked.connect(lambda: self.cusDasPageClick())
        cusDasLayout.addWidget(self.cusDasBtn)

        navBtnLayout.addLayout(fileLayout)
        navBtnLayout.addLayout(dasLayout)
        navBtnLayout.addLayout(cusDasLayout)

        navLayout.addWidget(logo)
        navLayout.addLayout(navBtnLayout)
        

        nav.setLayout(navLayout)

        self.layout.addWidget(nav)

    def filePage(self):
        f_page = QWidget()
        f_page.setStyleSheet("background: url('./src/bg_main1.png'); background-repeat: no-repeat; opacity: 0.5;")

        f_layout = QHBoxLayout()
        
        f_text_layout = QVBoxLayout()

        sayLabel = QLabel("Upload your CSV file .")
        sayLabel.setFont(QFont('Arial', 35))
        sayLabel.setStyleSheet("color: #373D4A; background: #D1D8E4;")
        sayLabel.setAlignment(QtCore.Qt.AlignCenter)

        uploadBtn = QPushButton("Upload File")
        uploadBtn.setFont(QFont('Arial', 20))
        uploadBtn.setStyleSheet("""
            QPushButton{
                padding: 5px; border: 0;
                background: #1F5ED8;
                color: #FAFAFA;
                border-radius: 5px;
            }

            QPushButton:hover{
                background: #174AA9;
            }
        """)
        uploadBtn.clicked.connect(lambda: self.uploadFileClick())

        f_text_layout.addSpacing(50)
        f_text_layout.addWidget(sayLabel)
        f_text_layout.addSpacing(50)
        f_text_layout.addWidget(uploadBtn)

        f_layout.addLayout(f_text_layout)

        f_layout.setAlignment(QtCore.Qt.AlignCenter)
        f_page.setLayout(f_layout)

        self.stackedWidget.addWidget(f_page)

    def dasPage(self):
        d_page = QWidget()
        QFontDatabase.addApplicationFont("./src/Comic_Neue/ComicNeue-Bold.ttf")
        d_page.setStyleSheet("background: white; font-family: 'Comic Neue';")
        d_layout = QGridLayout()
        d_layout.setContentsMargins(0, 0, 0, 0)
        d_layout.setRowStretch(0, 2)
        d_layout.setRowStretch(1, 1)
        d_layout.setRowStretch(2, 1)
        d_layout.setRowStretch(3, 1)
        d_layout.setRowStretch(4, 1)
        d_layout.setRowStretch(5, 1)

        d_layout.setColumnStretch(0, 1)
        d_layout.setColumnStretch(1, 1)
        d_layout.setColumnStretch(2, 1)
        d_layout.setColumnStretch(3, 1)
        d_layout.setColumnStretch(4, 1)
        d_layout.setColumnStretch(5, 1)

        valFont = 20
        self.penWidth = 3
        self.chartBgColor = '#D1D8E4'

        # main Map
        try:
            self.map = QWebEngineView()
            self.map.setStyleSheet("border-radius: 5px;")
            d_layout.addWidget(self.map, 0, 0, 2, 2)
        except Exception as err:
            print(err)

        # main chart
        try:
            self.mainchart = pg.PlotWidget()
            self.mainchart.clear()
            self.mainchart.setBackground(self.chartBgColor)
            self.mainchart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.mainchart.showGrid(True, True, 0.7)
            self.mainchart.plotItem.setMouseEnabled(y=False)
            d_layout.addWidget(self.mainchart, 0, 2, 2, 4)
        except Exception:
            pass


        # All label to show avg value and final value
        try:
            self.avgVol = QLabel("Average Voltage")
            self.avgVol.setStyleSheet("background: #0003AB; color: #FFFFFF; border-radius: 5px;")
            self.avgVol.setFont(QFont('Arial', valFont))
            self.avgVol.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.avgVol, 2, 0, 1, 1)
        except Exception:
            pass

        try:
            self.avgCur = QLabel("Average Current")
            self.avgCur.setStyleSheet("background: #BE2200; color: #FFFFFF; border-radius: 5px;")
            self.avgCur.setFont(QFont('Arial', valFont))
            self.avgCur.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.avgCur, 2, 1, 1, 1)
        except Exception:
            pass

        try:
            self.disChaCap = QLabel("Used Capacity")
            self.disChaCap.setStyleSheet("background: #009758; color: #FFFFFF; border-radius: 5px;")
            self.disChaCap.setFont(QFont('Arial', valFont))
            self.disChaCap.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.disChaCap, 2, 2, 1, 1)
        except Exception:
            pass


        try:
            self.energy = QLabel("Used Energy")
            self.energy.setStyleSheet("background: #A07E00; color: #FFFFFF; border-radius: 5px;")
            self.energy.setFont(QFont('Arial', valFont))
            self.energy.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.energy, 2, 3, 1, 1)
        except Exception:
            pass

        try:
            self.avgPow = QLabel("Average Power")
            self.avgPow.setStyleSheet("background: #C000BA; color: #FFFFFF; border-radius: 5px;")
            self.avgPow.setFont(QFont('Arial', valFont))
            self.avgPow.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.avgPow, 3, 0, 1, 1)
        except Exception:
            pass

        try:
            self.avgSpe = QLabel("Average Speed")
            self.avgSpe.setStyleSheet("background: #00539B; color: #FFFFFF; border-radius: 5px;")
            self.avgSpe.setFont(QFont('Arial', valFont))
            self.avgSpe.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.avgSpe, 3, 1, 1, 1)
        except Exception:
            pass

        try:
            self.maxSpeed = QLabel("Max. Speed")
            self.maxSpeed.setStyleSheet("background: #0088B1; color: #FFFFFF; border-radius: 5px;")
            self.maxSpeed.setFont(QFont('Arial', valFont))
            self.maxSpeed.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.maxSpeed, 3, 2, 1, 1)
        except Exception:
            pass

        try:
            self.distance = QLabel("Distance")
            self.distance.setStyleSheet("background: #0082C8; color: #FFFFFF; border-radius: 5px;")
            self.distance.setFont(QFont('Arial', valFont))
            self.distance.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.distance, 3, 3, 1, 1)
        except Exception:
            pass

        # speed chart 
        try:
            self.speedchart = pg.PlotWidget()
            self.speedchart.clear()
            self.speedchart.setBackground(self.chartBgColor)
            self.speedchart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.speedchart.showGrid(True, True, 0.7)
            self.speedchart.plotItem.setMouseEnabled(y=False)
            d_layout.addWidget(self.speedchart, 2, 4, 2, 2)
        except Exception:
            pass


        # all temp avg
        try:
            self.avgTemp1 = QLabel("Average Temp1")
            self.avgTemp1.setStyleSheet("background: #B02000; color: #FFFFFF; border-radius: 5px;")
            self.avgTemp1.setFont(QFont('Arial', valFont))
            self.avgTemp1.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.avgTemp1, 4, 0, 1, 1)
        except Exception:
            pass

        try:
            self.avgTemp2 = QLabel("Average Temp2")
            self.avgTemp2.setStyleSheet("background: #00864E; color: #FFFFFF; border-radius: 5px;")
            self.avgTemp2.setFont(QFont('Arial', valFont))
            self.avgTemp2.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.avgTemp2, 4, 1, 1, 1)
        except Exception:
            pass

        try:
            self.avgTemp3 = QLabel("Average Temp3")
            self.avgTemp3.setStyleSheet("background: #9A7800; color: #FFFFFF; border-radius: 5px;")
            self.avgTemp3.setFont(QFont('Arial', valFont))
            self.avgTemp3.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.avgTemp3, 5, 0, 1, 1)
        except Exception:
            pass

        try:
            self.avgTemp4 = QLabel("Average Temp4")
            self.avgTemp4.setStyleSheet("background: #007584; color: #FFFFFF; border-radius: 5px;")
            self.avgTemp4.setFont(QFont('Arial', valFont))
            self.avgTemp4.setAlignment(QtCore.Qt.AlignCenter)
            d_layout.addWidget(self.avgTemp4, 5, 1, 1, 1)
        except Exception:
            pass



        # All temp chart
        try:
            self.temp1chart = pg.PlotWidget()
            self.temp1chart.clear()
            self.temp1chart.setBackground(self.chartBgColor)
            self.temp1chart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.temp1chart.showGrid(True, True, 0.7)
            self.temp1chart.plotItem.setMouseEnabled(y=False)
            self.temp1chart.addLegend()
            d_layout.addWidget(self.temp1chart, 4, 2, 1, 2)
        except Exception as err:
            print(err)

        try:
            self.temp2chart = pg.PlotWidget()
            self.temp2chart.clear()
            self.temp2chart.setBackground(self.chartBgColor)
            self.temp2chart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.temp2chart.showGrid(True, True, 0.7)
            self.temp2chart.plotItem.setMouseEnabled(y=False)
            self.temp2chart.addLegend()
            d_layout.addWidget(self.temp2chart, 4, 4, 1, 2)
        except Exception:
            pass

        try:
            self.temp3chart = pg.PlotWidget()
            self.temp3chart.clear()
            self.temp3chart.setBackground(self.chartBgColor)
            self.temp3chart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.temp3chart.showGrid(True, True, 0.7)
            self.temp3chart.plotItem.setMouseEnabled(y=False)
            self.temp3chart.addLegend()
            d_layout.addWidget(self.temp3chart, 5, 2, 1, 2)
        except Exception:
            pass

        try:
            self.temp4chart = pg.PlotWidget()
            self.temp4chart.clear()
            self.temp4chart.setBackground(self.chartBgColor)
            self.temp4chart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.temp4chart.showGrid(True, True, 0.7)
            self.temp4chart.plotItem.setMouseEnabled(y=False)
            self.temp4chart.addLegend()
            d_layout.addWidget(self.temp4chart, 5, 4, 1, 2)
        except Exception:
            pass


        d_page.setLayout(d_layout)

        self.stackedWidget.addWidget(d_page)


    def main_map(self, dataLat, dataLon):
        try:
            m = folium.Map(location=[dataLat.head(1).iloc[0], dataLon.head(1).iloc[0]], zoom_start=15)
            path = folium.PolyLine(locations=list(zip(dataLat, dataLon)), weight=5)
            path.add_to(m)
            m.save('map.html')
            self.map.load(QtCore.QUrl.fromLocalFile(os.getcwd() +"\map.html"))

        except Exception as err:
            print(err)
            # self.map.load('<h1>Map is not load</h1>')


    def main_chart(self, dataV, dataC, time):
        try:
            try:
                self.mainLabel.setText('')
                self.vLineMain.setPen(self.chartBgColor)
            except Exception:
                pass

            self.mainchart.clear()
            self.mainchart.addLegend().clear()

            if np.max(dataV) <= 0 and np.max(dataC) <= 0:
                self.temp4chart.setYRange(0, np.max(dataV)+2)
            
            self.mainchart.addLegend()
            pen1 = pg.mkPen("#0003AB", width=self.penWidth)
            pen2 = pg.mkPen("#BE2200", width=self.penWidth)


            self.mainPlot = self.mainchart.plot(dataV, pen=pen1, name="Voltage")
            self.mainPlot1 = self.mainchart.plot(dataC, pen=pen2, name="Current")

            self.vLineMain = pg.InfiniteLine(pos=5, angle=90, movable=False)
            self.vLineMain.setPen("#000000")
            self.mainchart.addItem(self.vLineMain)

            self.mainLabel = pg.TextItem(anchor=(0, 1))
            self.mainLabel.setColor(QColor("#000000"))
            self.mainchart.addItem(self.mainLabel)

            self.mainchart.scene().sigMouseMoved.connect(self.mouseMovedMain)
            self.mainchart.scene().sigMouseClicked.connect(self.doubleClickedMain)


            self.x_range_mainChart = self.mainchart.plotItem.vb.viewRange()[0]
            self.y_range_mainChart = self.mainchart.plotItem.vb.viewRange()[1]

        except Exception as err:
            pass

    def doubleClickedMain(self, evt):
        if evt.double():
            self.mainchart.getPlotItem().enableAutoRange()

    def mouseMovedMain(self, evt):
        # get mouse position

        pos = evt
        if self.mainchart.sceneBoundingRect().contains(pos):
            x = self.mainchart.plotItem.vb.mapSceneToView(pos).x()
            y = self.mainchart.plotItem.vb.mapSceneToView(pos).y()

            x = max(min(x, max(self.x_range_mainChart)), min(self.x_range_mainChart))
            y = max(min(y, max(self.y_range_mainChart)), min(self.y_range_mainChart))

            # update vertical line position
            self.vLineMain.setPos(x)

            # update label text
            self.mainLabel.setText("x={:.2f}, y={:.2f}".format(x, y))
            self.mainLabel.setPos(x, y)


    def speed_chart(self, data):
        try:

            try:
                self.speedLabel.setText('')
                self.vLineSpeed.setPen(self.chartBgColor)
            except Exception:
                pass

            self.speedchart.clear()
            self.speedchart.addLegend().clear()

            if np.max(data) <= 0:
                self.speedchart.setYRange(0, np.max(data)+2)

            self.speedchart.addLegend()

            pen1 = pg.mkPen("#0088B1", width=self.penWidth)
            self.speedchart.plot(data, pen=pen1, name="Speed")

            self.vLineSpeed = pg.InfiniteLine(pos=5, angle=90, movable=True)
            self.vLineSpeed.setPen("#000000")
            self.speedchart.addItem(self.vLineSpeed)

            self.speedLabel = pg.TextItem(anchor=(0, 1))
            self.speedLabel.setColor(QColor("#000000"))
            self.speedchart.addItem(self.speedLabel)

            self.speedchart.scene().sigMouseMoved.connect(self.mouseMovedSpeed)
            self.speedchart.scene().sigMouseClicked.connect(self.doubleClickedSpeed)

            self.x_range_speedChart = self.speedchart.plotItem.vb.viewRange()[0]
            self.y_range_speedChart = self.speedchart.plotItem.vb.viewRange()[1]

        except Exception as err:
            pass

    def doubleClickedSpeed(self, evt):
        if evt.double():
            self.speedchart.getPlotItem().enableAutoRange()

    def mouseMovedSpeed(self, evt):
        # get mouse position
        pos = evt
        if self.speedchart.sceneBoundingRect().contains(pos):
            x = self.speedchart.plotItem.vb.mapSceneToView(pos).x()
            y = self.speedchart.plotItem.vb.mapSceneToView(pos).y()

            x = max(min(x, max(self.x_range_speedChart)), min(self.x_range_speedChart))
            y = max(min(y, max(self.y_range_speedChart)), min(self.y_range_speedChart))

            # update vertical line position
            self.vLineSpeed.setPos(x)

            # update label text
            self.speedLabel.setText("x={:.2f}, y={:.2f}".format(x, y))
            self.speedLabel.setPos(x, y)


    def temp1_chart(self, data):
        try:

            try:
                self.temp1Label.setText('')
                self.temp1vLine.setPen(self.chartBgColor)
            except Exception:
                pass

            self.temp1chart.clear()
            self.temp1chart.addLegend().clear()

            if np.max(data) <= 0:
                self.temp1chart.setYRange(0, np.max(data)+2)
            
            self.temp1chart.addLegend()
            pen1 = pg.mkPen("#B02000", width=self.penWidth)
            self.temp1chart.plot(data, pen=pen1, name="Temp1")

            self.temp1vLine = pg.InfiniteLine(pos=5, angle=90, movable=True)
            self.temp1vLine.setPen("#000000")
            self.temp1chart.addItem(self.temp1vLine)

            self.temp1Label = pg.TextItem(anchor=(0, 1))
            self.temp1Label.setColor(QColor("#000000"))
            self.temp1chart.addItem(self.temp1Label)

            self.temp1chart.scene().sigMouseMoved.connect(self.mouseMovedTemp1)
            self.temp1chart.scene().sigMouseClicked.connect(self.doubleClickedTemp1)

            self.x_range_temp1 = self.temp1chart.plotItem.vb.viewRange()[0]
            self.y_range_temp1 = self.temp1chart.plotItem.vb.viewRange()[1]

        except Exception as err:
            pass

    def doubleClickedTemp1(self, evt):
        if evt.double():
            self.temp1chart.getPlotItem().enableAutoRange()

    def mouseMovedTemp1(self, evt):
        # get mouse position
        pos = evt
        if self.temp1chart.sceneBoundingRect().contains(pos):
            x = self.temp1chart.plotItem.vb.mapSceneToView(pos).x()
            y = self.temp1chart.plotItem.vb.mapSceneToView(pos).y()

            x = max(min(x, max(self.x_range_temp1)), min(self.x_range_temp1))
            y = max(min(y, max(self.y_range_temp1)), min(self.y_range_temp1))

            # update vertical line position
            self.temp1vLine.setPos(x)

            # update label text
            self.temp1Label.setText("x={:.2f}, y={:.2f}".format(x, y))
            self.temp1Label.setPos(x, y)


    def temp2_chart(self, data):
        try:

            try:
                self.temp2Label.setText('')
                self.temp2vLine.setPen(self.chartBgColor)
            except Exception:
                pass

            self.temp2chart.clear()
            self.temp2chart.addLegend().clear()

            if np.max(data) <= 0:
                self.temp2chart.setYRange(0, np.max(data)+2)
            
            self.temp2chart.addLegend()
            pen1 = pg.mkPen("#00864E", width=self.penWidth)
            self.temp2chart.plot(data, pen=pen1, name="Temp2")

            self.temp2vLine = pg.InfiniteLine(pos=5, angle=90, movable=True)
            self.temp2vLine.setPen("#000000")
            self.temp2chart.addItem(self.temp2vLine)

            self.temp2Label = pg.TextItem(anchor=(0, 1))
            self.temp2Label.setColor(QColor("#000000"))
            self.temp2chart.addItem(self.temp2Label)

            self.temp2chart.scene().sigMouseMoved.connect(self.mouseMovedTemp2)
            self.temp2chart.scene().sigMouseClicked.connect(self.doubleClickedTemp2)

            self.x_range_temp2 = self.temp2chart.plotItem.vb.viewRange()[0]
            self.y_range_temp2 = self.temp2chart.plotItem.vb.viewRange()[1]

        except Exception as err:
            pass

    def doubleClickedTemp2(self, evt):
        if evt.double():
            self.temp2chart.getPlotItem().enableAutoRange()

    def mouseMovedTemp2(self, evt):
        # get mouse position
        pos = evt
        if self.temp2chart.sceneBoundingRect().contains(pos):
            x = self.temp2chart.plotItem.vb.mapSceneToView(pos).x()
            y = self.temp2chart.plotItem.vb.mapSceneToView(pos).y()

            x = max(min(x, max(self.x_range_temp2)), min(self.x_range_temp2))
            y = max(min(y, max(self.y_range_temp2)), min(self.y_range_temp2))

            # update vertical line position
            self.temp2vLine.setPos(x)

            # update label text
            self.temp2Label.setText("x={:.2f}, y={:.2f}".format(x, y))
            self.temp2Label.setPos(x, y)


    def temp3_chart(self, data):
        try:

            try:
                self.temp3Label.setText('')
                self.temp3vLine.setPen(self.chartBgColor)
            except Exception:
                pass

            self.temp3chart.clear()
            self.temp3chart.addLegend().clear()

            if np.max(data) <= 0:
                self.temp3chart.setYRange(0, np.max(data)+2)
            
            self.temp3chart.addLegend()
            pen1 = pg.mkPen("#9A7800", width=self.penWidth)
            self.temp3chart.plot(data, pen=pen1, name="Temp3")

            self.temp3vLine = pg.InfiniteLine(pos=5, angle=90, movable=True)
            self.temp3vLine.setPen("#000000")
            self.temp3chart.addItem(self.temp3vLine)

            self.temp3Label = pg.TextItem(anchor=(0, 1))
            self.temp3Label.setColor(QColor("#000000"))
            self.temp3chart.addItem(self.temp3Label)

            self.temp3chart.scene().sigMouseMoved.connect(self.mouseMovedTemp3)
            self.temp3chart.scene().sigMouseClicked.connect(self.doubleClickedTemp3)

            self.x_range_temp3 = self.temp3chart.plotItem.vb.viewRange()[0]
            self.y_range_temp3 = self.temp3chart.plotItem.vb.viewRange()[1]

        except Exception as err:
            pass

    def doubleClickedTemp3(self, evt):
        if evt.double():
            self.temp3chart.getPlotItem().enableAutoRange()

    def mouseMovedTemp3(self, evt):
        # get mouse position
        pos = evt
        if self.temp3chart.sceneBoundingRect().contains(pos):
            x = self.temp3chart.plotItem.vb.mapSceneToView(pos).x()
            y = self.temp3chart.plotItem.vb.mapSceneToView(pos).y()

            x = max(min(x, max(self.x_range_temp3)), min(self.x_range_temp3))
            y = max(min(y, max(self.y_range_temp3)), min(self.y_range_temp3))

            # update vertical line position
            self.temp3vLine.setPos(x)

            # update label text
            self.temp3Label.setText("x={:.2f}, y={:.2f}".format(x, y))
            self.temp3Label.setPos(x, y)


    def temp4_chart(self, data):
        try:

            try:
                self.temp4Label.setText('')
                self.temp4vLine.setPen(self.chartBgColor)
            except Exception:
                pass

            self.temp4chart.clear()
            self.temp4chart.addLegend().clear()

            if np.max(data) <= 0:
                self.temp4chart.setYRange(0, np.max(data)+2)

            self.temp4chart.addLegend()
            pen1 = pg.mkPen("#007584", width=self.penWidth)
            self.temp4chart.plot(data, pen=pen1, name="Temp4")

            self.temp4vLine = pg.InfiniteLine(pos=5, angle=90, movable=True)
            self.temp4vLine.setPen("#000000")
            self.temp4chart.addItem(self.temp4vLine)

            self.temp4Label = pg.TextItem(anchor=(0, 1))
            self.temp4Label.setColor(QColor("#000000"))
            self.temp4chart.addItem(self.temp4Label)

            self.temp4chart.scene().sigMouseMoved.connect(self.mouseMovedTemp4)
            self.temp4chart.scene().sigMouseClicked.connect(self.doubleClickedTemp4)

            self.x_range_temp4 = self.temp4chart.plotItem.vb.viewRange()[0]
            self.y_range_temp4 = self.temp4chart.plotItem.vb.viewRange()[1]

        except Exception as err:
            pass

    def doubleClickedTemp4(self, evt):
        if evt.double():
            self.temp4chart.getPlotItem().enableAutoRange()

    def mouseMovedTemp4(self, evt):
        # get mouse position
        pos = evt
        if self.temp4chart.sceneBoundingRect().contains(pos):
            x = self.temp4chart.plotItem.vb.mapSceneToView(pos).x()
            y = self.temp4chart.plotItem.vb.mapSceneToView(pos).y()

            x = max(min(x, max(self.x_range_temp4)), min(self.x_range_temp4))
            y = max(min(y, max(self.y_range_temp4)), min(self.y_range_temp4))

            # update vertical line position
            self.temp4vLine.setPos(x)

            # update label text
            self.temp4Label.setText("x={:.2f}, y={:.2f}".format(x, y))
            self.temp4Label.setPos(x, y)


    def allAvgValue(self, data):

        try:
            avgVolSum = round(np.mean(data.Voltage), 2)
            self.avgVol.setText(f"Average Voltage\n{avgVolSum} V")
        except Exception:
            self.avgVol.setText(f"Average Voltage")

        try:
            avgCurSum = round(np.mean(data.Current), 2)
            self.avgCur.setText(f"Average Current\n{avgCurSum} A")
        except Exception:
            self.avgCur.setText(f"Average Current")

        try:
            disChaCapSum = round(data.DischargeCapacity.tail(1).iloc[0], 2)
            self.disChaCap.setText(f"Discharge capacity\n{disChaCapSum} Ah")
        except Exception:
            self.disChaCap.setText(f"Discharge capacity")

        try:
            avgPowSum = round(np.mean(data.Power), 2)
            self.avgPow.setText(f"Average Power\n{avgPowSum} W")
        except Exception:
            self.avgPow.setText(f"Average Power")

        try:
            speedAll = np.array(data.Speed)
            speedFind = np.nonzero(speedAll)
            speedArr = speedAll[speedFind]
            avgSpeSum = round(np.mean(speedArr), 2)
            self.avgSpe.setText(f"Average Speed\n{avgSpeSum} Km/h")
        except Exception:
            self.avgSpe.setText(f"Average Speed")

        try:
            distanceSum = round(data.Distance.tail(1).iloc[0], 2)
            self.distance.setText(f"Distance\n{distanceSum} Km")
        except Exception:
            self.distance.setText(f"Distance")

        try:
            maxSpeedSum = round(np.max(data.Speed))
            self.maxSpeed.setText(f"Max. Speed\n{maxSpeedSum} Km/h")
        except Exception:
            self.maxSpeed.setText(f"Max. Speed")

        try:
            energySum = round(data.DischargeEnergy.tail(1).iloc[0], 2)
            self.energy.setText(f"Discharge Energy\n{energySum} Wh")
        except Exception:
            self.energy.setText(f"Discharge Energy")

        try:
            avgTemp1Sum = round(np.mean(data.Temp1), 2)
            self.avgTemp1.setText(f"Average Temp1\n{avgTemp1Sum} °C")
        except Exception:
            self.avgTemp1.setText(f"Average Temp1")

        try:
            avgTemp2Sum = round(np.mean(data.Temp2), 2)
            self.avgTemp2.setText(f"Average Temp2\n{avgTemp2Sum} °C")
        except Exception:
            self.avgTemp2.setText(f"Average Temp2")

        try:
            avgTemp3Sum = round(np.mean(data.Temp3), 2)
            self.avgTemp3.setText(f"Average Temp3\n{avgTemp3Sum} °C")
        except Exception:
            self.avgTemp3.setText(f"Average Temp3")

        try:
            avgTemp4Sum = round(np.mean(data.Temp4), 2)
            self.avgTemp4.setText(f"Average Temp4\n{avgTemp4Sum} °C")
        except Exception:
            self.avgTemp4.setText(f"Average Temp4")


    def cusDasPage(self):
        try:
            self.cus_page = QWidget()
            self.cus_page.setStyleSheet("background: white;")
            self.cus_layout = QHBoxLayout()
            self.cus_layout.setContentsMargins(0, 0, 0, 0)

            self.yAxisArr = []
            self.xAxis = None

            self.cusOption()

            self.cusDasboard()

            self.cus_layout.setAlignment(QtCore.Qt.AlignLeft)
            self.cus_page.setLayout(self.cus_layout)

            self.stackedWidget.addWidget(self.cus_page)

        except Exception as err:
            print(err)

    def cusOption(self):
        try:
            cusOp = QWidget()
            cusOp.setFixedWidth(300)
            cusOp.setStyleSheet("background: #FAFAFA; font-size: 18px;")
            option_layout = QVBoxLayout()
            option_layout.setContentsMargins(5, 20, 5, 20)

            option_x_layout = QVBoxLayout()
            option_x_layout.setContentsMargins(0, 10, 0, 0)

            mainXaxisTitle = QLabel("X-Axis")
            mainXaxisTitle.setStyleSheet("color: #373D4A")
            option_x_layout.addWidget(mainXaxisTitle)

            self.combo_box_x = QComboBox(self)
            self.combo_box_x.setStyleSheet("border : 1px solid #A3ADBF; border-radius: 5px;")
            option_x_layout.addWidget(self.combo_box_x)

            option_layout.addLayout(option_x_layout)


            option_y_layout = QVBoxLayout()
            option_y_layout.setContentsMargins(0, 10, 0, 0)

            mainYaxisTitle = QLabel("Y-Axis")
            mainYaxisTitle.setStyleSheet("color: #373D4A")
            option_y_layout.addWidget(mainYaxisTitle)

            self.listWidget_y = QListWidget(self)
            self.listWidget_y.setSelectionMode(QListWidget.MultiSelection)
            self.listWidget_y.setStyleSheet("border : 1px solid #A3ADBF; border-radius: 5px;")
            option_y_layout.addWidget(self.listWidget_y)

            option_layout.addLayout(option_y_layout)

            cusOp.setLayout(option_layout)
            self.cus_layout.addWidget(cusOp)

        except Exception as err:
            print("##################################################################")
            print(err)

    def comboBoxItem(self, df):
        try:
            self.combo_box_x.clear()
            comboDataPoint = df.head(0)

            self.data_cus = df

            self.combo_box_x.addItem("-- select --")
            for i in comboDataPoint:
                self.combo_box_x.addItem(i)

            for index in range(self.combo_box_x.count()):
                item = self.combo_box_x.itemText(index)

            self.combo_box_x.activated.connect(self.handle_selection_change)

        except Exception as err:
            print('combo #####################################################################')
            print(err)

    def handle_selection_change(self, index):
        try:
            selected_item_text = self.combo_box_x.itemText(index)
            self.xAxis = selected_item_text
            if self.xAxis != None and self.yAxisArr is not None:
                self.cusChart()

        except Exception as err:
            print(err)

    def listItams(self, df):
        try:
            self.listWidget_y.clear()
            allDataPoints = df.head(0)

            for i in allDataPoints:
                self.allListItem = QListWidgetItem(i)
                self.listWidget_y.addItem(self.allListItem)

            self.listWidget_y.itemSelectionChanged.connect(self.update_array_y)

        except Exception as err:
            print(err)

    def update_array_y(self):
        try:
            self.yAxisArr = [item.text() for item in self.listWidget_y.selectedItems()]
            if self.xAxis != None and self.yAxisArr is not None:
                self.cusChart()

        except Exception as err:
            print(err)

    def cusDasboard(self):
        try:
            cusDasWiget = QWidget()
            cusDas_layout = QGridLayout()

            cusDas_layout.setRowStretch(0, 2)
            cusDas_layout.setRowStretch(0, 1)

            cusDas_layout.setColumnStretch(0, 1)

            self.cusMainChart = pg.PlotWidget()
            self.cusMainChart.clear()
            self.cusMainChart.setBackground('w')
            self.cusMainChart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.cusMainChart.showGrid(True, True, 0.5)
            self.cusMainChart.plotItem.setMouseEnabled(y=False)
            cusDas_layout.addWidget(self.cusMainChart, 0, 0, 1, 1)

            cusDasWiget.setLayout(cusDas_layout)
            self.cus_layout.addWidget(cusDasWiget)

        except Exception as err:
            print("************************************************************")
            print(err)
            print("************************************************************")

    def cusChart(self):
        try:
            self.cusMainChart.clear()
            self.cusMainChart.addLegend().clear()
            self.cusMainChart.addLegend()

            colors = [
                        "#0000FF", "#00FF00", "#FF0000", "#00FFFF", "#FF00FF", "#FFFF00", "#000000",
                        "#FF8000", "#00FF80", "#8000FF", "#007FFF", "#FF007F", "#7FFF00", "#7F00FF",
                        "#FF7F00"
                    ]
            j = 0

            for i in self.yAxisArr:
                color = QColor(colors[j])
                pen = pg.mkPen(color, width=self.penWidth)
                xAxis = self.data_cus[self.xAxis]
                yAxis = self.data_cus[i]
                name = f"cusDasChartPlot{i}"
                name = self.cusMainChart.plot(xAxis, yAxis, pen=pen, name=i)
                j += 1

            self.cusMainChart.scene().sigMouseClicked.connect(self.doubleClickedCusChart)

        except Exception as err:
            print(err)

    def doubleClickedCusChart(self, evt):
        if evt.double():
            self.cusMainChart.getPlotItem().enableAutoRange()

    def uploadFileClick(self):
        file = QFileDialog.getOpenFileName(None, "CSV Files (*.csv)")
        df = pd.read_csv(file[0])

        try:
            self.dasPageClick()
        except Exception:
            pass

        try:
            self.main_map(df.Latitude, df.Longitude)
        except Exception:
            pass

        try:
            self.main_chart(df.Voltage, df.Current, df.Time)
        except Exception:
            self.mainchart.clear()
            self.mainchart.setBackground(self.chartBgColor)
            self.mainchart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.mainchart.showGrid(True, True, 0.7)
            self.mainchart.addLegend()

        try:
            self.allAvgValue(df)
        except Exception:
            pass

        try:
            self.speed_chart(df.Speed)
        except Exception:
            self.speedchart.clear()
            self.speedchart.setBackground(self.chartBgColor)
            self.speedchart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.speedchart.showGrid(True, True, 0.7)
            self.speedchart.addLegend()

        try:
            self.temp1_chart(df.Temp1)
        except Exception:
            self.temp1chart.clear()
            self.temp1chart.setBackground(self.chartBgColor)
            self.temp1chart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.temp1chart.showGrid(True, True, 0.7)
            self.temp1chart.addLegend()

        try:
            self.temp2_chart(df.Temp2)
        except Exception:
            self.temp2chart.clear()
            self.temp2chart.setBackground(self.chartBgColor)
            self.temp2chart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.temp2chart.showGrid(True, True, 0.7)
            self.temp2chart.addLegend()

        try:
            self.temp3_chart(df.Temp3)
        except Exception:
            self.temp3chart.clear()
            self.temp3chart.setBackground(self.chartBgColor)
            self.temp3chart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.temp3chart.showGrid(True, True, 0.7)
            self.temp3chart.addLegend()

        try:
            self.temp4_chart(df.Temp4)
        except Exception:
            self.temp4chart.clear()
            self.temp4chart.setBackground(self.chartBgColor)
            self.temp4chart.plotItem.setContentsMargins(10, 0, 0, 0)
            self.temp4chart.showGrid(True, True, 0.7)
            self.temp4chart.addLegend()

        try:
            self.listItams(df)
        except Exception:
            pass

        try:
            self.comboBoxItem(df)
        except Exception:
            pass

    def filePageClick(self):
        self.fileBtn.setIcon(QIcon("./src/fileUploadeActiv.png"))
        self.dasBtn.setIcon(QIcon("./src/dasboard.png"))
        self.cusDasBtn.setIcon(QIcon("./src/cusDas.png"))
        self.stackedWidget.setCurrentIndex(0)

    def dasPageClick(self):
        self.fileBtn.setIcon(QIcon("./src/file.png"))
        self.dasBtn.setIcon(QIcon("./src/dasboardIconActiv.png"))
        self.cusDasBtn.setIcon(QIcon("./src/cusDas.png"))
        self.stackedWidget.setCurrentIndex(1)

    def cusDasPageClick(self):
        self.fileBtn.setIcon(QIcon("./src/file.png"))
        self.dasBtn.setIcon(QIcon("./src/dasboard.png"))
        self.cusDasBtn.setIcon(QIcon("./src/customDasboardActiv.png"))
        self.stackedWidget.setCurrentIndex(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = window()
    win.show()

    sys.exit(app.exec_())
