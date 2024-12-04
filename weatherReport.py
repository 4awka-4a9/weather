from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import requests
import json
import datetime
import threading, os

cities = {
1:{"ru":"Варшава", "en":"Warsaw", "latitude":"25.13", "longitude":"21.02"},
2:{"ru":"Минск", "en":"Minsk", "latitude":"53.55", "longitude":"27.33"},
3:{"ru":"Москва", "en":"Moscow", "latitude":"55.44", "longitude":"24.00"}
}

languages = {
1:{"title":"English", "lang":"en"},
2:{"title":"Русский", "lang":"ru"}
}

translate = {
"weather":{"en":"Weather", "ru":"Погода"},
"relhum":{"en":"Relative humidity", "ru":"Относительная влажность"},
"settings":{"en":"Settings", "ru":"Настройки"},

}

city = 1
lang = 1


class Ui_MainWindow(object):

    def changeCity(self, cityID):
        global city
        city = cityID
        ui.retranslateUi(mainWindow)

    def changeLanguage(self, language):
        global lang
        lang = language
        print(lang)
        ui.retranslateUi(mainWindow)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 500)
        MainWindow.setStyleSheet("background-color: rgb(102, 207, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 300, 500))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tempLabel = QtWidgets.QLabel(self.tab)
        self.tempLabel.setGeometry(QtCore.QRect(100, 50, 100, 80))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.tempLabel.setFont(font)
        self.tempLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tempLabel.setObjectName("tempLabel")
        self.countryLabel = QtWidgets.QLabel(self.tab)
        self.countryLabel.setGeometry(QtCore.QRect(110, 10, 80, 20))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.countryLabel.setFont(font)
        self.countryLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.countryLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.countryLabel.setObjectName("countryLabel")
        self.windSpeedLabel = QtWidgets.QLabel(self.tab)
        self.windSpeedLabel.setGeometry(QtCore.QRect(120, 120, 60, 16))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.windSpeedLabel.setFont(font)
        self.windSpeedLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.windSpeedLabel.setTextFormat(QtCore.Qt.AutoText)
        self.windSpeedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.windSpeedLabel.setObjectName("windSpeedLabel")
        self.timeLabel = QtWidgets.QLabel(self.tab)
        self.timeLabel.setGeometry(QtCore.QRect(120, 30, 60, 16))
        self.timeLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.humidityLabel = QtWidgets.QLabel(self.tab)
        self.humidityLabel.setGeometry(QtCore.QRect(80, 150, 140, 20))
        self.humidityLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.humidityLabel.setScaledContents(True)
        self.humidityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.humidityLabel.setObjectName("humidityLabel")
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setGeometry(QtCore.QRect(90, 140, 121, 71))
        self.progressBar.setMinimum(0)
        self.progressBar.setProperty("value", 89)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.combobox = QtWidgets.QComboBox(self.tab_2)
        self.combobox.setGeometry(100, 50, 100, 20)

        self.changeLanguages = QtWidgets.QComboBox(self.tab_2)
        self.changeLanguages.setGeometry(100, 100, 100, 20)

        for number, language in enumerate(languages):
            self.changeLanguages.addItem(languages[language]["title"])

        for index, value in enumerate(cities):
            self.combobox.addItem(cities[index + 1][languages[lang]["lang"]])


        self.combobox.currentIndexChanged.connect(self.on_combobox_changed)
        self.changeLanguages.currentIndexChanged.connect(self.on_language_changet)

        self.autoUpdate(MainWindow)

        QMainWindow.closeEvent = self.closeEvent

    def closeEvent(self, value):
        os._exit(1)

    def on_combobox_changed(self, value):

        self.changeCity(value + 1)

    def on_language_changet(self, language):
            self.changeLanguage(language + 1)

            for index, CITY in enumerate(cities):
                self.combobox.setItemText(index, cities[city][languages[lang]["lang"]])


    def retranslateUi(self, MainWindow):

        current_time = datetime.datetime.now().time()
        ct = str(current_time).split(":")

        print(lang)


        obj = self.getWeather(cities[city]["latitude"], cities[city]["longitude"])
        time_str = str(obj["hourly"]["time"][0])[-5:]



        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tempLabel.setText(_translate("MainWindow", str(obj["hourly"]["temperature_2m"][int(ct[0])]) + "°C"))
        self.windSpeedLabel.setText(_translate("MainWindow", str(obj["hourly"]["wind_speed_10m"][int(ct[0])]) + " KM/H"))
        self.countryLabel.setText(_translate("MainWindow", cities[city][languages[lang]["lang"]]))
        self.timeLabel.setText(_translate("MainWindow", ct[0] + ":" + ct[1]))
        self.humidityLabel.setText(_translate("MainWindow", translate["relhum"][languages[lang]["lang"]] + str(obj["hourly"]["relative_humidity_2m"][int(ct[0])]) + "%"))
        self.progressBar.setProperty("value", obj["hourly"]["relative_humidity_2m"][int(ct[0])])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", translate["weather"][languages[lang]["lang"]]))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", translate["settings"][languages[lang]["lang"]]))

        print(str(obj["hourly"]["temperature_2m"][int(ct[0])]) + "°C")
        print(city)

    def autoUpdate(self, MainWindow):
        current_time = datetime.datetime.now().time()
        ct = str(current_time).split(":")
        seconds = float(ct[2])
        seconds = int(seconds)

        if seconds == 0:
            self.retranslateUi(MainWindow)

        self.timer = threading.Timer(1, self.autoUpdate, [MainWindow], {})
        self.timer.start()

    def getWeather(self, latitude, longitude):
        session = requests.Session()
        response = session.get("https://api.open-meteo.com/v1/forecast?latitude="+latitude+"&longitude="+longitude+"&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
        obj = json.loads(response.text)
        return(obj)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
