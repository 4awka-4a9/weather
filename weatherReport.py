from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import requests
import json
import datetime
import threading, os


cities = [
    {"ru":"Варшава", "en":"Warsaw", "pl":"Warszawa", "latitude":"52.22", "longitude":"21.01"},
    {"ru":"Минск", "en":"Minsk", "pl":"Minsk","latitude":"53.55", "longitude":"27.33"},
    {"ru":"Москва", "en":"Moscow", "pl":"Moskwa" ,"latitude":"55.44", "longitude":"24.00"},
    {"ru":"Стокгольм", "en":"Stockholm", "pl":"Sztokholm", "latitude":"59.2", "longitude":"18.04"},
    {"ru":"Берлин", "en":"Berlin", "pl":"Berlin", "latitude":"52.3", "longitude":"13.2"},
    {"ru":"Стамбул", "en":"Istanbul", "pl":"Stambuł", "latitude":"41.0", "longitude":"28.5"},
]

languages = [
    {"title":"English", "lang":"en"},
    {"title":"Русский", "lang":"ru"},
    {"title":"Polski", "lang":"pl"}
]

translate = {
    "weather":{
        "en":"Weather",
        "ru":"Погода",
        "pl":"Pogoda"
    },
    "relhum":{
        "en":"Relative humidity",
        "ru":"Относительная влажность",
        "pl":"Wilgotność względna"
    },
    "settings":{
        "en":"Settings",
        "ru":"Настройки",
        "pl":"Opcje"
    },
    "donate":{
        "en":"Donate",
        "ru":"Потдержка",
        "pl":"Wsparcie"
    },
}

city = 0
lang = 0


class Ui_MainWindow(object):


    def change_city(self, cityID):
        global city
        city = cityID
        ui.retranslateUi(mainWindow)

    def change_language(self, language):
        global lang
        lang = language
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

        self.cityLabel = QtWidgets.QLabel(self.tab)
        self.cityLabel.setGeometry(QtCore.QRect(0, 10, 300, 20))

        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)

        self.cityLabel.setFont(font)
        self.cityLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.cityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.cityLabel.setObjectName("cityLabel")

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
        self.humidityLabel.setGeometry(QtCore.QRect(50, 150, 200, 20))
        self.humidityLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.humidityLabel.setScaledContents(True)
        self.humidityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.humidityLabel.setObjectName("humidityLabel")

        self.humProgressBar = QtWidgets.QProgressBar(self.tab)
        self.humProgressBar.setGeometry(QtCore.QRect(90, 140, 120, 70))
        self.humProgressBar.setMinimum(0)
        self.humProgressBar.setProperty("value", 89)
        self.humProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.humProgressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.humProgressBar.setObjectName("humProgressBar")

        self.hourlyTemp = QtWidgets.QLabel(self.tab)
        self.hourlyTemp.setGeometry(QtCore.QRect(20, 190, 125, 10))
        self.hourlyTemp.setStyleSheet("color: rgb(255, 255, 255);")
        self.hourlyTemp.setAlignment(QtCore.Qt.AlignCenter)
        self.hourlyTemp.setObjectName("hourlyTemp")

        self.tabWidget.addTab(self.tab, "")

        self.extendedWeather = QtWidgets.QWidget()
        self.extendedWeather.setObjectName("extended_weather")

        self.settingsTab = QtWidgets.QWidget()
        self.settingsTab.setObjectName("settingsTab")

        self.donateTab = QtWidgets.QWidget()
        self.donateTab.setObjectName("donateTab")

        self.tabWidget.addTab(self.extendedWeather, "")
        self.tabWidget.addTab(self.settingsTab, "")
        self.tabWidget.addTab(self.donateTab, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.cityChange = QtWidgets.QComboBox(self.settingsTab)
        self.cityChange.setGeometry(100, 50, 100, 20)

        self.changeLanguages = QtWidgets.QComboBox(self.settingsTab)
        self.changeLanguages.setGeometry(100, 100, 100, 20)

        self.BTCtext = QLabel(self.donateTab)
        self.BTCtext.setGeometry(10, 25, 100, 20)
        self.BTCtext.setText("BTC:")

        self.ETHtext = QLabel(self.donateTab)
        self.ETHtext.setGeometry(10, 75, 100, 20)
        self.ETHtext.setText("ETH:")

        self.USDTTtext = QLabel(self.donateTab)
        self.USDTTtext.setGeometry(10, 125, 100, 20)
        self.USDTTtext.setText("USDT TRC 20:")

        self.USDTEtext = QLabel(self.donateTab)
        self.USDTEtext.setGeometry(10, 175, 100, 20)
        self.USDTEtext.setText("USDT ERC 20:")

        self.BTCcopy = QLineEdit(self.donateTab)
        self.BTCcopy.setGeometry(10, 50, 270, 20)
        self.BTCcopy.setText("bc1qml9r2f7qud0zsatjf3kh4c6v9yetd8zer52t97")
        self.BTCcopy.setReadOnly(True)

        self.ETHcopy = QLineEdit(self.donateTab)
        self.ETHcopy.setGeometry(10, 100, 270, 20)
        self.ETHcopy.setText("0xc3006CD922641337053BfB34a919299754002Fa6")
        self.ETHcopy.setReadOnly(True)

        self.USDTTcopy = QLineEdit(self.donateTab)
        self.USDTTcopy.setGeometry(10, 150, 270, 20)
        self.USDTTcopy.setText("TJ1Zc5Y2SsNLMaQKzdy9XFT5iLAZHx7zGZ")
        self.USDTTcopy.setReadOnly(True)

        self.USDTEcopy = QLineEdit(self.donateTab)
        self.USDTEcopy.setGeometry(10, 200, 270, 20)
        self.USDTEcopy.setText("0xc3006CD922641337053BfB34a919299754002Fa6")
        self.USDTEcopy.setReadOnly(True)

        for l in languages:
            self.changeLanguages.addItem(l["title"])

        for index, value in enumerate(cities):
            self.cityChange.addItem(cities[index][languages[lang]["lang"]])

        self.cityChange.currentIndexChanged.connect(self.on_city_changed)
        self.changeLanguages.currentIndexChanged.connect(self.on_language_changed)


        self.auto_update(MainWindow)

        QMainWindow.closeEvent = self.close_event


    def close_event(self, value):
        os._exit(1)

    def on_city_changed(self, value):

        self.change_city(value)

    def on_language_changed(self, language):
            self.change_language(language)

            for index, CITY in enumerate(cities):
                self.cityChange.setItemText(index, cities[index][languages[lang]["lang"]])


    def retranslateUi(self, MainWindow):

        it = 5

        current_time = datetime.datetime.now().time()
        ct = str(current_time).split(":")

        obj = self.get_weather(cities[city]["latitude"], cities[city]["longitude"])
        time_str = str(obj["hourly"]["time"][0])[-5:]

        if ct[0] == "-0":
            ct[0] = "0"


        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.tempLabel.setText(_translate("MainWindow", str(obj["hourly"]["temperature_2m"][int(ct[0])]) + "°C"))

        self.windSpeedLabel.setText(_translate("MainWindow", str(obj["hourly"]["wind_speed_10m"][int(ct[0])]) + " KM/H"))

        self.cityLabel.setText(_translate("MainWindow", cities[city][languages[lang]["lang"]]))

        self.timeLabel.setText(_translate("MainWindow", ct[0] + ":" + ct[1]))

        self.humidityLabel.setText(_translate("MainWindow", translate["relhum"][languages[lang]["lang"]] + " " + str(obj["hourly"]["relative_humidity_2m"][int(ct[0])]) + "%"))

        self.humProgressBar.setProperty("value", obj["hourly"]["relative_humidity_2m"][int(ct[0])])

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", translate["weather"][languages[lang]["lang"]]))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsTab), _translate("MainWindow", translate["settings"][languages[lang]["lang"]]))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.extendedWeather), _translate("MainWindow","24H"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.donateTab), _translate("MainWindow", translate["donate"][languages[lang]["lang"]]))

        for index in range(int(ct[0]), int(ct[0]) + 24):

            time = obj["hourly"]["time"][index].split("T")
            it += 18

            hl = QtWidgets.QLabel(self.extendedWeather)
            hl.setGeometry(20, it, 120, 15)
            hl.setStyleSheet("background-color: rgb(89, 192, 230);")
            hl.setAlignment(QtCore.Qt.AlignCenter)
            hl.setText(time[-1])

            hw = QtWidgets.QLabel(self.extendedWeather)
            hw.setGeometry(150, it, 120, 15)
            hw.setStyleSheet("background-color: rgb(89, 192, 230);")
            hw.setAlignment(QtCore.Qt.AlignCenter)
            hw.setText(str(obj["hourly"]["temperature_2m"][index]) + "°C")





    def auto_update(self, MainWindow):

        current_time = datetime.datetime.now().time()
        ct = str(current_time).split(":")
        seconds = float(ct[2])
        seconds = int(seconds)

        if seconds == 0:
            self.retranslateUi(MainWindow)

        self.timer = threading.Timer(1, self.auto_update, [MainWindow], {})
        self.timer.start()

    def get_weather(self, latitude, longitude):
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
