# 2019 - 2020 Eğitim Dönemi Bitirme Projesi

# Python 3.10

# Onur Erikçi

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from comtypes import CLSCTX_ALL
from configparser import RawConfigParser, NoOptionError
from ctypes import cast, POINTER, windll
from datetime import datetime
from keyboard import press
from os import startfile, makedirs, walk, system, getlogin
from psutil import process_iter, Process
from pyautogui import screenshot
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PySide6.QtCore import Qt, QThread, Signal, Slot, QDate
from PySide6.QtGui import QPixmap, QIcon, QTextCursor
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QTextEdit, QPushButton, QSystemTrayIcon, \
    QMenu, QTableWidget, QTableWidgetItem, QHeaderView, QCalendarWidget, QGroupBox, QHBoxLayout
from requests import get, exceptions
from socket import gethostbyname, gethostname
from speech_recognition import Recognizer, Microphone, UnknownValueError
from sqlite3 import connect, OperationalError
from sys import argv, exit
from time import sleep, strftime, time, gmtime, localtime
from variables import *
from win32gui import GetWindowText, GetForegroundWindow
from win32process import GetWindowThreadProcessId
from wmi import WMI


class App(QSystemTrayIcon):
    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        # Uyarı Zamanlayıcısı ==========================================================================================
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.alert, IntervalTrigger(hours=1))
        scheduler.start()
        # SysTray Ana Menü =============================================================================================
        main_menu = QMenu()
        # SysTray Fonksiyonları Görüntüle Menüsü =======================================================================
        show_functions_menu = QMenu("Fonksiyonları Görüntüle")
        # SysTray Komutları Düzenle Menüsü =============================================================================
        edit_commands_menu = QMenu("Komutları Düzenle")
        # SysTray Uygulama Kullanımı İzleyici Menüsü ===================================================================
        application_usage_tracker_menu = QMenu("Uygulama Kullanımı İzleyici")
        # Ekran Fotoğrafı Komutlarını Düzenle SysTray ==================================================================
        edit_screenshot_commands_menu = QMenu("'Ekran Fotoğrafı' Komutları")
        edit_take_a_screenshot = edit_screenshot_commands_menu.addAction("Ekranın Fotoğrafını Çek")
        edit_take_a_screenshot.setIcon(QIcon(take_a_screenshot_icon))
        edit_take_a_screenshot.triggered.connect(self.edit_take_a_screenshot)
        edit_open_screenshot_folder = edit_screenshot_commands_menu.addAction("Ekran Fotoğrafları Klasörünü Aç")
        edit_open_screenshot_folder.setIcon(QIcon(screenshot_folder_icon))
        edit_open_screenshot_folder.triggered.connect(self.edit_open_screenshot_folder)
        # Ekran Parlaklığı Komutlarını Düzenle SysTray =================================================================
        edit_brightness_commands_menu = QMenu("'Ekran Parlaklığı Seviyesi' Komutları")
        edit_brightness_hundred = edit_brightness_commands_menu.addAction("Ekran Parlaklığı Seviyesini '100' Yap")
        edit_brightness_hundred.setIcon(QIcon(brightness_hundred_icon))
        edit_brightness_hundred.triggered.connect(self.edit_brightness_hundred)
        edit_brightness_fifty = edit_brightness_commands_menu.addAction("Ekran Parlaklığı Seviyesini '50' Yap")
        edit_brightness_fifty.setIcon(QIcon(brightness_icon))
        edit_brightness_fifty.triggered.connect(self.edit_brightness_fifty)
        edit_bightness_zero = edit_brightness_commands_menu.addAction("Ekran Parlaklığı Seviyesini '0' Yap")
        edit_bightness_zero.setIcon(QIcon(brightness_zero_icon))
        edit_bightness_zero.triggered.connect(self.edit_brightness_zero)
        edit_brightness_up = edit_brightness_commands_menu.addAction("Ekran Parlaklığı Seviyesini Arttır")
        edit_brightness_up.setIcon(QIcon(brightness_hundred_icon))
        edit_brightness_up.triggered.connect(self.edit_brightness_up)
        edit_brightness_down = edit_brightness_commands_menu.addAction("Ekran Parlaklığı Seviyesini Azalt")
        edit_brightness_down.setIcon(QIcon(brightness_zero_icon))
        edit_brightness_down.triggered.connect(self.edit_brightness_down)
        # Güç Komutlarını Düzenle SysTray ==============================================================================
        edit_power_commands_menu = QMenu("'Güç Seçenekleri' Komutları")
        edit_shutdown_self = edit_power_commands_menu.addAction("Kendini Kapat")
        edit_shutdown_self.setIcon(QIcon(shutdown_self_icon))
        edit_shutdown_self.triggered.connect(self.edit_shutdown_self)
        edit_shutdown_windows = edit_power_commands_menu.addAction("Bilgisayarı Kapat")
        edit_shutdown_windows.setIcon(QIcon(exit_icon))
        edit_shutdown_windows.triggered.connect(self.edit_shutdown_windows)
        edit_restart_windows = edit_power_commands_menu.addAction("Bilgisayarı Yeniden Başlat")
        edit_restart_windows.setIcon(QIcon(restart_icon))
        edit_restart_windows.triggered.connect(self.edit_reboot_windows)
        edit_suspend_windows = edit_power_commands_menu.addAction("Bilgisayarı Uyku Moduna Al")
        edit_suspend_windows.setIcon(QIcon(suspend_icon))
        edit_suspend_windows.triggered.connect(self.edit_suspend_windows)
        edit_lock_windows = edit_power_commands_menu.addAction("Bilgisayarı Kilitle")
        edit_lock_windows.setIcon(QIcon(lock_icon))
        edit_lock_windows.triggered.connect(self.edit_lock_windows)
        # Onay Komutlarını Düzenle SysTray =============================================================================
        edit_confirmation_commands_menu = QMenu("'Onay Seçenekleri' Komutları")
        edit_positive = edit_confirmation_commands_menu.addAction("Onaylıyorum")
        edit_positive.setIcon(QIcon(accept_icon))
        edit_positive.triggered.connect(self.edit_positive)
        edit_negative = edit_confirmation_commands_menu.addAction("Onaylamıyorum")
        edit_negative.setIcon(QIcon(deny_icon))
        edit_negative.triggered.connect(self.edit_negative)
        # Ses Komutlarını Düzenle SysTray ==============================================================================
        edit_volume_commands_menu = QMenu("'Ses Seviyesi' Komutları")
        edit_volume_on = edit_volume_commands_menu.addAction("Ses Akışını Aç")
        edit_volume_on.setIcon(QIcon(volume_icon))
        edit_volume_on.triggered.connect(self.edit_volume_on)
        edit_volume_off = edit_volume_commands_menu.addAction("Ses Akışını Kapat")
        edit_volume_off.setIcon(QIcon(volume_mute_icon))
        edit_volume_off.triggered.connect(self.edit_volume_off)
        edit_volume_hundred = edit_volume_commands_menu.addAction("Ses Seviyesini '100' Yap")
        edit_volume_hundred.setIcon(QIcon(volume_icon))
        edit_volume_hundred.triggered.connect(self.edit_volume_hundred)
        edit_volume_fifty = edit_volume_commands_menu.addAction("Ses Seviyesini '50' Yap")
        edit_volume_fifty.setIcon(QIcon(volume_fifty_icon))
        edit_volume_fifty.triggered.connect(self.edit_volume_fifty)
        edit_volume_zero = edit_volume_commands_menu.addAction("Ses Seviyesini '0' Yap")
        edit_volume_zero.setIcon(QIcon(volume_mute_icon))
        edit_volume_zero.triggered.connect(self.edit_volume_zero)
        edit_volume_up = edit_volume_commands_menu.addAction("Ses Seviyesini Arttır")
        edit_volume_up.setIcon(QIcon(volume_icon))
        edit_volume_up.triggered.connect(self.edit_volume_up)
        edit_volume_down = edit_volume_commands_menu.addAction("Ses Seviyesini Azalt")
        edit_volume_down.setIcon(QIcon(volume_zero_icon))
        edit_volume_down.triggered.connect(self.edit_volume_down)
        # Fonksiyonları Görüntüle ======================================================================================
        show_screenshot_functions = show_functions_menu.addAction("'Ekran Fotoğrafı' Fonksiyonları")
        show_screenshot_functions.setIcon(QIcon(screenshot_icon))
        show_screenshot_functions.triggered.connect(self.show_screenshot_functions)
        show_brightness_functions = show_functions_menu.addAction("'Ekran Parlaklığı Seviyesi' Fonksiyonları")
        show_brightness_functions.triggered.connect(self.show_brightness_functions)
        show_brightness_functions.setIcon(QIcon(brightness_icon))
        show_power_functions = show_functions_menu.addAction("'Güç Seçenekleri' Fonksiyonları")
        show_power_functions.triggered.connect(self.show_power_functions)
        show_power_functions.setIcon(QIcon(power_icon))
        show_confirmation_functions = show_functions_menu.addAction("'Onay Seçenekleri' Fonksiyonları")
        show_confirmation_functions.triggered.connect(self.show_confirmation_functions)
        show_confirmation_functions.setIcon(QIcon(confirmation_icon))
        show_volume_functions = show_functions_menu.addAction("'Ses Seviyesi' Fonksiyonları")
        show_volume_functions.triggered.connect(self.show_volume_functions)
        show_volume_functions.setIcon(QIcon(volume_icon))
        # Komutları Düzenle ============================================================================================
        edit_screenshot_commands = edit_commands_menu.addMenu(edit_screenshot_commands_menu)
        edit_screenshot_commands.setIcon(QIcon(screenshot_icon))
        edit_brightness_commands = edit_commands_menu.addMenu(edit_brightness_commands_menu)
        edit_brightness_commands.setIcon(QIcon(brightness_icon))
        edit_power_commands = edit_commands_menu.addMenu(edit_power_commands_menu)
        edit_power_commands.setIcon(QIcon(power_icon))
        edit_confitmation_commands = edit_commands_menu.addMenu(edit_confirmation_commands_menu)
        edit_confitmation_commands.setIcon(QIcon(confirmation_icon))
        edit_volume_commands = edit_commands_menu.addMenu(edit_volume_commands_menu)
        edit_volume_commands.setIcon(QIcon(volume_icon))
        # SysTray Ana Menü =============================================================================================
        command_sahara = main_menu.addAction("Sahra'ya Komut Ver")
        command_sahara.triggered.connect(self.command_sahara)
        command_sahara.setIcon(QIcon(command_sahara_icon))
        main_menu.addSeparator()
        show_functions = main_menu.addMenu(show_functions_menu)
        show_functions.setIcon(QIcon(show_functions_icon))
        edit_commands = main_menu.addMenu(edit_commands_menu)
        edit_commands.setIcon(QIcon(edit_commands_icon))
        application_usage_tracker = main_menu.addMenu(application_usage_tracker_menu)
        application_usage_tracker.setIcon(QIcon(application_usage_tracker_icon))
        main_menu.addSeparator()
        changelog_sahara = main_menu.addAction("Değişiklikler Listesi")
        changelog_sahara.triggered.connect(self.release_notes)
        changelog_sahara.setIcon(QIcon(release_notes_icon))
        main_menu.addSeparator()
        about_sahara = main_menu.addAction("Hakkında")
        about_sahara.triggered.connect(self.about)
        about_sahara.setIcon(QIcon(about_icon))
        exit_sahara = main_menu.addAction("Çıkış Yap")
        exit_sahara.triggered.connect(self.exit_sahara)
        exit_sahara.setIcon(QIcon(shutdown_self_icon))
        # SysTray Uygulama Kullanımı İzleyici Menüsü ===================================================================
        watch_usages = application_usage_tracker_menu.addAction("Uygulama Kullanımı Verilerini İzle")
        watch_usages.triggered.connect(self.application_usage_data_watch)
        watch_usages.setIcon(QIcon(application_usage_watch_icon))
        show_usages = application_usage_tracker_menu.addAction("Uygulama Kullanımı Verilerini Görüntüle")
        show_usages.triggered.connect(self.application_usage_data_show)
        show_usages.setIcon(QIcon(application_usage_show_icon))
        # SysTray Arayüzü ==============================================================================================
        self.setIcon(QIcon(tray_logo))
        self.setContextMenu(main_menu)
        self.setToolTip("Sahra - Sanal Asistan Araç Kutusu")
        self.activated.connect(self.click_event)
        self.show()
        self.showMessage("Sahra'ya Komut Ver", "Araç Kutusu'na çift tıklayarak komut vermeye başlayabilirsin.", QIcon(command_sahara_icon64), msecs=0)
        # Uygulama Kullanımı İzleyici SysTray Arayüzü ==================================================================
        self.widget1 = QWidget()
        self.widget1.setWindowIcon(QIcon(application_usage_watch_icon))
        self.widget1.setWindowTitle("Uygulama Kullanımı Verilerini İzle")
        self.widget1.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget1.setFixedSize(700, 500)
        self.autlabel = QLabel()
        self.autlabel.setWhatsThis("Canlı veri akışındaki verilerin ne anlama geldiğine dair bilgilendirme.")
        self.autlabel.setText("""[00:00:00] -> Aktivite Durumunun Bildirilme Zamanı\n[Sahra - Sanal Asistan | Sahra.exe] -> Aktivite Durumunun Alındığı Uygulamanın Adı Ve Dosyası\n[00:00:00 | 00:00:00] -> Uygulamanın Mevcut Kullanım Süresi Ve Toplam Kullanım Süresi\n[Aktivite Başladı] -> Aktivitenin Türü""")
        self.autlabel.setAlignment(Qt.AlignCenter)
        self.text_edit1 = QTextEdit()
        self.text_edit1.setWhatsThis("Uygulama kullanımı izleyiciye ait canlı veri akışının görüntülenmesini sağlar.")
        self.text_edit1.setReadOnly(True)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_live = QGroupBox()
        groupbox_live.setTitle("Canlı Veri Akışı")
        groupbox_live.setFlat(True)
        groupbox_live.setStyleSheet("font-weight:bold")
        groupbox_live.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.autlabel)
        vertical_layout.addWidget(groupbox_live)
        vertical_layout.addWidget(self.text_edit1)
        self.widget1.setLayout(vertical_layout)
        font = self.text_edit1.font()
        font.setPointSize(10)
        self.text_edit1.setFont(font)
        # Uygulama Kullanımı İzleyici Thread ===========================================================================
        self.izleyici = UygulamaIzleyici(self)
        self.izleyici.signal.connect(self.application_usage_tracker_watch_print)
        self.izleyici.start()
# Slot Fonksiyonları ===================================================================================================
    @Slot(str)
    def application_usage_tracker_watch_print(self, track):
        self.text_edit1.moveCursor(QTextCursor.End)
        self.text_edit1.insertPlainText(track)
        self.text_edit1.moveCursor(QTextCursor.End)
# SysTray Sahra'ya Komut Ver ===========================================================================================
    # Sahra'ya Komut Ver Arayüzü =======================================================================================
    def command_sahara(self):
        self.think(self.listen())
# ======================================================================================================================
# SysTray Fonksiyonları Görüntüle ======================================================================================
    def show_screenshot_functions(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWhatsThis("'Ekran Fotoğrafı' fonksiyonlarının ne işe yaradığına dair bilgilendirme.")
        self.widget.setWindowIcon(QIcon(screenshot_icon))
        self.widget.setWindowTitle("'Ekran Fotoğrafı' Fonksiyonları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        with open(screenshot_functions_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setText(data)
        self.text_edit.setReadOnly(True)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.text_edit)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.widget.show()
    def show_brightness_functions(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWhatsThis("'Ekran Parlaklığı Seviyesi' fonksiyonlarının ne işe yaradığına dair bilgilendirme.")
        self.widget.setWindowIcon(QIcon(brightness_icon))
        self.widget.setWindowTitle("'Ekran Parlaklığı Seviyesi' Fonksiyonları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        with open(brightness_functions_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setText(data)
        self.text_edit.setReadOnly(True)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.text_edit)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.widget.show()
    def show_power_functions(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWhatsThis("'Güç Seçenekleri' fonksiyonlarının ne işe yaradığına dair bilgilendirme.")
        self.widget.setWindowIcon(QIcon(power_icon))
        self.widget.setWindowTitle("'Güç Seçenekleri' Fonksiyonları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        with open(power_functions_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setText(data)
        self.text_edit.setReadOnly(True)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.text_edit)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.widget.show()
    def show_confirmation_functions(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWhatsThis("'Onay Seçenekleri' fonksiyonlarının ne işe yaradığına dair bilgilendirme.")
        self.widget.setWindowIcon(QIcon(confirmation_icon))
        self.widget.setWindowTitle("'Onay Seçenekleri' Fonksiyonları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        with open(confirmation_functions_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setText(data)
        self.text_edit.setReadOnly(True)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.text_edit)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.widget.show()
    def show_volume_functions(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWhatsThis("'Ses Seviyesi' fonksiyonlarının ne işe yaradığına dair bilgilendirme.")
        self.widget.setWindowIcon(QIcon(volume_icon))
        self.widget.setWindowTitle("'Ses Seviyesi' Fonksiyonları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        with open(volume_functions_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setText(data)
        self.text_edit.setReadOnly(True)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.text_edit)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.widget.show()
# ======================================================================================================================
# SysyTray Komutları Düzenle ===========================================================================================
    # Butonları Etkinleştirme ==========================================================================================
    def enable_buttons(self):
        self.save_button.setEnabled(True)
        self.cancel_button.setEnabled(True)
    # Ekran Fotoğrafı Komutları SysTray Arayüzü =========================================================================
    def edit_take_a_screenshot(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(take_a_screenshot_icon))
        self.widget.setWindowTitle("'Ekranın Fotoğrafını Çek' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ekranın Fotoğrafını Çek' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(take_a_screenshot_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ekranın Fotoğrafını Çek' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ekranın Fotoğrafını Çek' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ekranın Fotoğrafını Çek' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_take_a_screenshot_save)
        self.cancel_button.clicked.connect(self.edit_take_a_screenshot_cancel)
        self.widget.show()
    def edit_take_a_screenshot_save(self):
        data = self.text_edit.toPlainText()
        with open(take_a_screenshot_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ekranın Fotoğrafını Çek', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_take_a_screenshot_cancel(self):
        self.showMessage('Ekranın Fotoğrafını Çek', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_open_screenshot_folder(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(screenshot_folder_icon))
        self.widget.setWindowTitle("'Ekran Fotoğrafları Klasörünü Aç' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ekran Fotoğrafları Klasörünü Aç' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(open_screenshots_folder_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ekran Fotoğrafları Klasörünü Aç' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ekran Fotoğrafları Klasörünü Aç' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ekran Fotoğrafları Klasörünü Aç' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_open_screenshot_folder_save)
        self.cancel_button.clicked.connect(self.edit_open_screenshot_folder_cancel)
        self.widget.show()
    def edit_open_screenshot_folder_save(self):
        data = self.text_edit.toPlainText()
        with open(open_screenshots_folder_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ekran Fotoğrafları Klasörünü Aç', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_open_screenshot_folder_cancel(self):
        self.showMessage('Ekran Fotoğrafları Klasörünü Aç', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    # Ekran Parlaklığı Seviyesi Komutları SysTray Arayüzü ==============================================================
    def edit_brightness_hundred(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(brightness_hundred_icon))
        self.widget.setWindowTitle("'Ekran Parlaklığı Seviyesini 100 Yap' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ekran Parlaklığı Seviyesini 100 Yap' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(brightness_hundred_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ekran Parlaklığı Seviyesini 100 Yap' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ekran Parlaklığı Seviyesini 100 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ekran Parlaklığı Seviyesini 100 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_brightness_hundred_save)
        self.cancel_button.clicked.connect(self.edit_brightness_hundred_cancel)
        self.widget.show()
    def edit_brightness_hundred_save(self):
        data = self.text_edit.toPlainText()
        with open(brightness_hundred_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ekran Parlaklığı Seviyesini 100 Yap', "komutlarında yağtığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_brightness_hundred_cancel(self):
        self.showMessage('Ekran Parlaklığı Seviyesini 100 Yap', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_brightness_fifty(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(brightness_icon))
        self.widget.setWindowTitle("'Ekran Parlaklığı Seviyesini 50 Yap' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ekran Parlaklığı Seviyesini 50 Yap' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(brightness_fifty_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ekran Parlaklığı Seviyesini 50 Yap' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ekran Parlaklığı Seviyesini 50 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ekran Parlaklığı Seviyesini 50 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_brightness_fifty_save)
        self.cancel_button.clicked.connect(self.edit_brightness_fifty_cancel)
        self.widget.show()
    def edit_brightness_fifty_save(self):
        data = self.text_edit.toPlainText()
        with open(brightness_fifty_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ekran Parlaklığı Seviyesini 50 Yap', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_brightness_fifty_cancel(self):
        self.showMessage('Ekran Parlaklığı Seviyesini 50 Yap', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_brightness_zero(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(brightness_zero_icon))
        self.widget.setWindowTitle("'Ekran Parlaklığı Seviyesini 0 Yap' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ekran Parlaklığı Seviyesini 0 Yap' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(brightness_zero_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ekran Parlaklığı Seviyesini 0 Yap' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ekran Parlaklığı Seviyesini 0 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ekran Parlaklığı Seviyesini 0 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_brightness_zero_save)
        self.cancel_button.clicked.connect(self.edit_brightness_zero_cancel)
        self.widget.show()
    def edit_brightness_zero_save(self):
        data = self.text_edit.toPlainText()
        with open(brightness_zero_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ekran Parlaklığı Seviyesini 0 Yap', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_brightness_zero_cancel(self):
        self.showMessage('Ekran Parlaklığı Seviyesini 0 Yap', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_brightness_up(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(brightness_hundred_icon))
        self.widget.setWindowTitle("'Ekran Parlaklığı Seviyesini Arttır' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ekran Parlaklığı Seviyesini Arttır' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(brightness_up_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ekran Parlaklığı Seviyesini Arttır' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ekran Parlaklığı Seviyesini Arttır' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ekran Parlaklığı Seviyesini Arttır' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_brightness_up_save)
        self.cancel_button.clicked.connect(self.edit_brightness_up_cancel)
        self.widget.show()
    def edit_brightness_up_save(self):
        data = self.text_edit.toPlainText()
        with open(brightness_up_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ekran Parlaklığı Seviyesini Arttır', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_brightness_up_cancel(self):
        self.showMessage('Ekran Parlaklığı Seviyesini Arttır', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_brightness_down(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(brightness_zero_icon))
        self.widget.setWindowTitle("'Ekran Parlaklığı Seviyesini Azalt' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ekran Parlaklığı Seviyesini Azalt' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(brightness_down_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ekran Parlaklığı Seviyesini Azalt' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ekran Parlaklığı Seviyesini Azalt' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ekran Parlaklığı Seviyesini Azalt' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_brightness_down_save)
        self.cancel_button.clicked.connect(self.edit_brightness_down_cancel)
        self.widget.show()
    def edit_brightness_down_save(self):
        data = self.text_edit.toPlainText()
        with open(brightness_down_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ekran Parlaklığı Seviyesini Azalt', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_brightness_down_cancel(self):
        self.showMessage('Ekran Parlaklığı Seviyesini Azalt', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    # Güç Seçenekleri Komutları Systray Arayüzü ========================================================================
    def edit_shutdown_self(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(shutdown_self_icon))
        self.widget.setWindowTitle("'Kendini Kapat' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Kendini Kapat' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(shutdown_self_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Kendini Kapat' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Kendini Kapat' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Kendini Kapat' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_shutdown_self_save)
        self.cancel_button.clicked.connect(self.edit_shutdown_self_cancel)
        self.widget.show()
    def edit_shutdown_self_save(self):
        data = self.text_edit.toPlainText()
        with open(shutdown_self_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Kendini Kapat', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_shutdown_self_cancel(self):
        self.showMessage('Kendini Kapat', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_shutdown_windows(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(exit_icon))
        self.widget.setWindowTitle("'Bilgisayarı Kapat' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Bilgisayarı Kapat' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(shutdown_windows_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Bilgisayarı Kapat' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Bilgisayarı Kapat' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Bilgisayarı Kapat' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_shutdown_windows_save)
        self.cancel_button.clicked.connect(self.edit_shutdown_windows_cancel)
        self.widget.show()
    def edit_shutdown_windows_save(self):
        data = self.text_edit.toPlainText()
        with open(shutdown_windows_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Bilgisayarı Kapat', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_shutdown_windows_cancel(self):
        self.showMessage('Bilgisayarı Kapat', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_reboot_windows(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(restart_icon))
        self.widget.setWindowTitle("'Bilgisayarı Yeniden Başlat' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Bilgisayarı Yeniden Başlat' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(reboot_windows_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Bilgisayarı Yeniden Başlat' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Bilgisayarı Yeniden Başlat' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Bilgisayarı Yeniden Başlat' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_reboot_windows_save)
        self.cancel_button.clicked.connect(self.edit_reboot_windows_cancel)
        self.widget.show()
    def edit_reboot_windows_save(self):
        data = self.text_edit.toPlainText()
        with open(reboot_windows_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Bilgisayarı Yeniden Başlat', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_reboot_windows_cancel(self):
        self.showMessage('Bilgisayarı Yeniden Başlat', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_suspend_windows(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(suspend_icon))
        self.widget.setWindowTitle("'Bilgisayarı Uyku Moduna Al' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Bilgisayarı Uyku Moduna Al' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(suspend_windows_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Bilgisayarı Uyku Moduna Al' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Bilgisayarı Uyku Moduna Al' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Bilgisayarı Uyku Moduna Al' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_suspend_windows_save)
        self.cancel_button.clicked.connect(self.edit_suspend_windows_cancel)
        self.widget.show()
    def edit_suspend_windows_save(self):
        data = self.text_edit.toPlainText()
        with open(suspend_windows_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Bilgisayarı Uyku Moduna Al', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_suspend_windows_cancel(self):
        self.showMessage('Bilgisayarı Uyku Moduna Al', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_lock_windows(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(lock_icon))
        self.widget.setWindowTitle("'Bilgisayarı Kilitle' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Bilgisayarı Kilitle' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(lock_windows_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Bilgisayarı Kilitle' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Bilgisayarı Kilitle' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Bilgisayarı Kilitle' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_lock_windows_save)
        self.cancel_button.clicked.connect(self.edit_lock_windows_cancel)
        self.widget.show()
    def edit_lock_windows_save(self):
        data = self.text_edit.toPlainText()
        with open(lock_windows_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Bilgisayarı Kilitle', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_lock_windows_cancel(self):
        self.showMessage('Bilgisayarı Kilitle', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    # Onay Seçenekleri Komutları SysTray Arayüzü =======================================================================
    def edit_positive(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(accept_icon))
        self.widget.setWindowTitle("'Onaylıyorum' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Onaylıyorum' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(yes_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Onaylıyorum' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Onaylıyorum' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Onaylıyorum' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_positive_save)
        self.cancel_button.clicked.connect(self.edit_positive_cancel)
        self.widget.show()
    def edit_positive_save(self):
        data = self.text_edit.toPlainText()
        with open(yes_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Onaylıyorum', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_positive_cancel(self):
        self.showMessage('Onaylıyorum', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_negative(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(deny_icon))
        self.widget.setWindowTitle("'Onaylamıyorum' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Onaylamıyorum' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(no_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Onaylamıyorum' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Onaylamıyorum' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Onaylamıyorum' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_negative_save)
        self.cancel_button.clicked.connect(self.edit_negative_cancel)
        self.widget.show()
    def edit_negative_save(self):
        data = self.text_edit.toPlainText()
        with open(no_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Onaylamıyorum', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_negative_cancel(self):
        self.showMessage('Onaylamıyorum', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    # Ses Seviyesi Komutları SysTray Arayüzü ===========================================================================
    def edit_volume_hundred(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(volume_icon))
        self.widget.setWindowTitle("'Ses Seviyesini 100 Yap' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ses Seviyesini 100 Yap' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(volume_hundred_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ses Seviyesini 100 Yap' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ses Seviyesini 100 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ses Seviyesini 100 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_volume_hundred_save)
        self.cancel_button.clicked.connect(self.edit_volume_hundred_cancel)
        self.widget.show()
    def edit_volume_hundred_save(self):
        data = self.text_edit.toPlainText()
        with open(volume_hundred_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ses Seviyesini 100 Yap', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_volume_hundred_cancel(self):
        self.showMessage('Ses Seviyesini 100 Yap', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_volume_fifty(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(volume_fifty_icon))
        self.widget.setWindowTitle("'Ses Seviyesini 50 Yap' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ses Seviyesini 50 Yap' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(volume_fifty_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ses Seviyesini 50 Yap' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ses Seviyesini 50 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ses Seviyesini 50 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_volume_fifty_save)
        self.cancel_button.clicked.connect(self.edit_volume_fifty_cancel)
        self.widget.show()
    def edit_volume_fifty_save(self):
        data = self.text_edit.toPlainText()
        with open(volume_fifty_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ses Seviyesini 50 Yap', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_volume_fifty_cancel(self):
        self.showMessage('Ses Seviyesini 50 Yap', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_volume_zero(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(volume_mute_icon))
        self.widget.setWindowTitle("'Ses Seviyesini 0 Yap' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ses Seviyesini 0 Yap' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(volume_zero_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ses Seviyesini 0 Yap' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ses Seviyesini 0 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ses Seviyesini 0 Yap' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_volume_zero_save)
        self.cancel_button.clicked.connect(self.edit_volume_zero_cancel)
        self.widget.show()
    def edit_volume_zero_save(self):
        data = self.text_edit.toPlainText()
        with open(volume_zero_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ses Seviyesini 0 Yap', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_volume_zero_cancel(self):
        self.showMessage('Ses Seviyesini 0 Yap', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_volume_on(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(volume_icon))
        self.widget.setWindowTitle("'Ses Akışını Aç' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ses Akışını Aç' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(volume_on_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ses Akışını Aç' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ses Akışını Aç' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ses Akışını Aç' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_volume_on_save)
        self.cancel_button.clicked.connect(self.edit_volume_on_cancel)
        self.widget.show()
    def edit_volume_on_save(self):
        data = self.text_edit.toPlainText()
        with open(volume_on_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ses Akışını Aç', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_volume_on_cancel(self):
        self.showMessage('Ses Akışını Aç', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_volume_off(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(volume_mute_icon))
        self.widget.setWindowTitle("'Ses Akışını Kapat' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ses Akışını Kapat' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(volume_off_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ses Akışını Kapat' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ses Akışını Kapat' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ses Akışını Kapat' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_volume_off_save)
        self.cancel_button.clicked.connect(self.edit_volume_off_cancel)
        self.widget.show()
    def edit_volume_off_save(self):
        data = self.text_edit.toPlainText()
        with open(volume_off_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ses Akışını Kapat', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_volume_off_cancel(self):
        self.showMessage('Ses Akışını Kapat', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_volume_up(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(volume_icon))
        self.widget.setWindowTitle("'Ses Seviyesini Arttır' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ses Seviyesini Arttır' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(volume_up_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ses Seviyesini Arttır' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ses Seviyesini Arttır' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ses Seviyesini Arttır' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_volume_up_save)
        self.cancel_button.clicked.connect(self.edit_volume_up_cancel)
        self.widget.show()
    def edit_volume_up_save(self):
        data = self.text_edit.toPlainText()
        with open(volume_up_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ses Seviyesini Arttır', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_volume_up_cancel(self):
        self.showMessage('Ses Seviyesini Arttır', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
    def edit_volume_down(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(volume_zero_icon))
        self.widget.setWindowTitle("'Ses Seviyesini Azalt' Komutları")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.label = QLabel()
        self.label.setWhatsThis("'Ses Seviyesini Azalt' fonksiyonuna tanımlı komutların nasıl düzenlenmesi gerektiğine dair bilgilendirme.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Komutların tümünün küçük harf olmasına ve her komutun ayrı satırda olmasına dikkat ediniz.")
        with open(volume_down_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("'Ses Seviyesini Azalt' fonksiyonuna tanımlı komutları görüntüleme ve düzenleme imkanı sağlar.")
        self.text_edit.setText(data)
        self.save_button = QPushButton("Kaydet")
        self.save_button.setWhatsThis("Bu butona tıklandığında 'Ses Seviyesini Azalt' fonksiyonuna tanımlı komutlarda yapılan değişiklikler kaydedilir.")
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setWhatsThis("Bu butona tıklandığında 'Ses Seviyesini Azalt' fonksiyonuna tanımlı komutlarda yapılan değişiklikler iptal edilir.")
        self.save_button.setDisabled(True)
        self.cancel_button.setDisabled(True)
        self.text_edit.textChanged.connect(self.enable_buttons)
        self.text_edit.moveCursor(QTextCursor.End)
        groupbox_info = QGroupBox()
        groupbox_info.setTitle("Bilgilendirme")
        groupbox_info.setFlat(True)
        groupbox_info.setStyleSheet("font-weight:bold")
        groupbox_info.setAlignment(Qt.AlignCenter)
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Komutlar")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(groupbox_info)
        vertical_layout.addWidget(self.label)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.text_edit)
        vertical_layout.addWidget(self.save_button)
        vertical_layout.addWidget(self.cancel_button)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.save_button.clicked.connect(self.edit_volume_down_save)
        self.cancel_button.clicked.connect(self.edit_volume_down_cancel)
        self.widget.show()
    def edit_volume_down_save(self):
        data = self.text_edit.toPlainText()
        with open(volume_down_location, 'w', encoding='utf-8') as file:
            file.write(data)
            file.close()
        self.showMessage('Ses Seviyesini Azalt', "komutlarında yaptığın değişiklikleri kaydettim.", QIcon(edit_save_icon64), msecs=0)
        self.widget.close()
    def edit_volume_down_cancel(self):
        self.showMessage('Ses Seviyesini Azalt', "komutlarında yaptığın değişiklikleri iptal ettim.", QIcon(edit_cancel_icon64), msecs=0)
        self.widget.close()
# ======================================================================================================================
# SysTray Uygulama Kullanımı İzleyici ==================================================================================
    # Uygulama Kullanımı Verilerini İzle SysTray Arayüzü ===============================================================
    def application_usage_data_watch(self):
        try:
            self.widget.hide()
        except AttributeError:
            pass
        """widget_geometry = QApplication.desktop().geometry().center()
        x = widget_geometry.x()
        y = widget_geometry.y()
        self.widget1.move(x - self.widget1.geometry().width() / 2.0, y - self.widget1.geometry().height() / 2.0 - 50)"""
        self.widget1.show()
    # Uygulama Kullanımı Verilerini Görüntüle SysTray Arayüzü ==========================================================
    def application_usage_data_show(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(application_usage_show_icon))
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        self.table = QTableWidget()
        self.table.setWhatsThis("Uygulama kullanımı verilerini en fazla kullanılan uygulamadan en az kullanılan uygulamaya göre sıralanmış olarak görüntüler.")
        self.table.setColumnCount(3)
        self.table.setRowCount(5)
        self.table.setHorizontalHeaderLabels(["Uygulama Adı", "Uygulama Dosyası", "Kullanım Süresi"])
        header_horizontal = self.table.horizontalHeader()
        header_horizontal.setSectionResizeMode(0, QHeaderView.Stretch)
        header_horizontal.setSectionResizeMode(1, QHeaderView.Stretch)
        header_horizontal.setSectionResizeMode(2, QHeaderView.Stretch)
        header_horizontal.setDefaultAlignment(Qt.AlignCenter)
        header_vertical = self.table.verticalHeader()
        header_vertical.setDefaultAlignment(Qt.AlignCenter)
        self.calendar = QCalendarWidget()
        self.calendar.setWhatsThis("Hangi tarihe ait uygulama kullanımı verilerinin görüntüleceğinin seçilmesini sağlar.")
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setGridVisible(True)
        data = self.get_min_date()
        self.calendar.setMinimumDate(QDate(int(data[0]), int(data[1]), int(data[2])))
        self.calendar.setMaximumDate(QDate.currentDate())
        self.calendar.setSelectedDate(QDate.currentDate())
        self.widget.setWindowTitle("Uygulama Kullanımı Verilerini Görüntüle")
        vertical_layout = QVBoxLayout()
        vertical_layout2 = QVBoxLayout()
        vertical_layout3 = QVBoxLayout()
        vertical_layout4 = QVBoxLayout()
        vertical_layout5 = QVBoxLayout()
        horizontal_layout1 = QHBoxLayout()
        horizontal_layout2 = QHBoxLayout()
        groupbox_data = QGroupBox()
        groupbox_data.setTitle("Uygulama Kullanımı Verileri")
        groupbox_data.setFlat(True)
        groupbox_data.setStyleSheet("font-weight:bold")
        groupbox_data.setAlignment(Qt.AlignCenter)
        groupbox_most_use = QGroupBox()
        groupbox_most_use.setTitle("En Fazla Kullanılan Uygulama")
        groupbox_most_use.setFlat(True)
        groupbox_most_use.setStyleSheet("font-weight: bold")
        groupbox_most_use.setAlignment(Qt.AlignCenter)
        groupbox_most_use_time = QGroupBox()
        groupbox_most_use_time.setTitle("Kullanım Süresi")
        groupbox_most_use_time.setFlat(True)
        groupbox_most_use_time.setStyleSheet("font-weight: bold")
        groupbox_most_use_time.setAlignment(Qt.AlignCenter)
        groupbox_all_app = QGroupBox()
        groupbox_all_app.setTitle("Toplam Kullanılan Uygulama Sayısı")
        groupbox_all_app.setFlat(True)
        groupbox_all_app.setStyleSheet("font-weight: bold")
        groupbox_all_app.setAlignment(Qt.AlignCenter)
        groupbox_all_time = QGroupBox()
        groupbox_all_time.setTitle("Toplam Kullanım Süresi")
        groupbox_all_time.setFlat(True)
        groupbox_all_time.setStyleSheet("font-weight: bold")
        groupbox_all_time.setAlignment(Qt.AlignCenter)
        groupbox_date = QGroupBox()
        groupbox_date.setTitle("Tarih")
        groupbox_date.setFlat(True)
        groupbox_date.setStyleSheet("font-weight: bold")
        groupbox_date.setAlignment(Qt.AlignCenter)
        self.label2 = QLabel()
        self.label2.setWhatsThis("Seçilen tarihte en fazla hangi uygulamanın kullanılmış olduğunu belirtir.")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label3 = QLabel()
        self.label3.setWhatsThis("Seçilen tarihte en fazla kullanılan uygulamanın kullanım süresini belirtir.")
        self.label3.setAlignment(Qt.AlignCenter)
        self.label = QLabel()
        self.label.setWhatsThis("Seçilen tarihte kullanılan uygulama sayısını belirtir.")
        self.label.setAlignment(Qt.AlignCenter)
        self.label4 = QLabel()
        self.label4.setWhatsThis("Seçilen tarihte kullanılan uygulamaların toplam kullanım süresini belirtir.")
        self.label4.setAlignment(Qt.AlignCenter)
        self.label5 = QLabel()
        self.label5.setWhatsThis("Hangi tarihe ait verilerin görüntülenmekte olduğunu belirtir.")
        self.label5.setAlignment(Qt.AlignCenter)
        vertical_layout2.addWidget(groupbox_most_use)
        vertical_layout2.addWidget(self.label2)
        vertical_layout3.addWidget(groupbox_most_use_time)
        vertical_layout3.addWidget(self.label3)
        vertical_layout4.addWidget(groupbox_all_app)
        vertical_layout4.addWidget(self.label)
        vertical_layout5.addWidget(groupbox_all_time)
        vertical_layout5.addWidget(self.label4)
        horizontal_layout1.addLayout(vertical_layout2)
        horizontal_layout1.addLayout(vertical_layout3)
        horizontal_layout2.addLayout(vertical_layout4)
        horizontal_layout2.addLayout(vertical_layout5)
        vertical_layout.addWidget(groupbox_date)
        vertical_layout.addWidget(self.label5)
        vertical_layout.addLayout(horizontal_layout1)
        vertical_layout.addLayout(horizontal_layout2)
        vertical_layout.addWidget(groupbox_data)
        vertical_layout.addWidget(self.table)
        vertical_layout.addWidget(self.calendar)
        self.widget.setLayout(vertical_layout)
        self.calendar.clicked.connect(self.application_usage_data_show_on_click)
        self.application_usage_data_show_on_click()
        self.widget.show()
    def get_min_date(self):
        dizi = []
        for way, subdirs, files in walk(application_usage_tracker_databases_location):
            for name in files:
                veri = path.join(way, name)
                c1 = "["
                c2 = "]"
                veri_filtreli = veri[veri.find(c1) + 1: veri.find(c2)]
                veri_ters_yil = veri_filtreli.split('-')[2]
                veri_ters_ay = veri_filtreli.split('-')[1]
                veri_ters_gun = veri_filtreli.split('-')[0]
                data = veri_ters_yil + "-" + veri_ters_ay + "-" + veri_ters_gun
                dizi.append(data)
        dizi = sorted(dizi)
        min_date = dizi[0]
        veri_yil = min_date.split('-')[0]
        veri_ay = min_date.split('-')[1]
        veri_gun = min_date.split('-')[2]
        return veri_yil, veri_ay, veri_gun
    def application_usage_data_show_on_click(self):
        try:
            current_date = self.calendar.selectedDate().toString("dd-MM-yyyy")
            db_name = "assets\\application_usages\\" + getlogin() + "[" + current_date + "].aut"
            db = connect(db_name)
            result = db.execute("SELECT application_name, application_executable, application_usage_time, application_usage FROM application_usage_tracker ORDER BY application_usage_time DESC")
            self.table.setRowCount(0)
            usage_time = 0
            for row_number, row_data in enumerate(result):
                self.table.insertRow(row_number)
                if row_number == 0:
                    self.label2.setText(row_data[0])
                    self.label3.setText(row_data[2])
                usage_time = usage_time + int(row_data[3])
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(Qt.ItemIsEnabled)
                    self.table.setItem(row_number, column_number, item)
                    self.label.setText(str(self.table.rowCount()))
            self.label4.setText(strftime('%H:%M:%S', gmtime(usage_time)))
            self.label5.setText(current_date)
            db.close()
        except OperationalError:
            self.table.clear()
            self.table.setRowCount(0)
            self.table.setHorizontalHeaderLabels(["Uygulama Adı", "Uygulama Dosyası", "Kullanım Süresi"])
            self.label.setText("-")
            self.label2.setText("-")
            self.label3.setText("-")
            self.label4.setText("-")
            self.label5.setText(current_date)
            self.showMessage("Uygulama Kullanımı İzleyici", "Bu tarihe ait uygulama kullanımı verisi bulunamadı.", QIcon(no_data_icon64), msecs=0)
# SysTray Değişiklikler Listesi ========================================================================================
    # Değişiklikler Listesi SysTray Arayüzü ============================================================================
    def release_notes(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(release_notes_icon))
        self.widget.setWindowTitle("Değişiklikler Listesi")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(700, 500)
        with open(app_release_notes_location, 'r', encoding='utf-8') as file:
            data = file.read()
            file.close()
        self.label = QLabel()
        self.label.setWhatsThis("Sahra - Sanal Asistan uygulama versiyon numarası.")
        self.label.setText(app_version)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-weight: normal")
        self.label1 = QLabel()
        self.label1.setWhatsThis("Sahra - Sanal Asistan uygulama sürümü tipi.")
        self.label1.setText(app_version_type)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("font-weight: normal")
        self.text_edit = QTextEdit()
        self.text_edit.setWhatsThis("Sahra - Sanal Asistan değşiklikler listesi.")
        self.text_edit.setText(data)
        self.text_edit.setReadOnly(True)
        vertical_layout = QVBoxLayout()
        groupbox_version = QGroupBox()
        groupbox_version.setTitle("Versiyon")
        groupbox_version.setAlignment(Qt.AlignCenter)
        groupbox_version.setFlat(True)
        groupbox_version.setStyleSheet("font-weight: bold")
        groupbox_version_vertical_layout = QVBoxLayout()
        groupbox_version_vertical_layout.addWidget(self.label)
        groupbox_version.setLayout(groupbox_version_vertical_layout)
        groupbox_release = QGroupBox()
        groupbox_release.setTitle("Sürüm")
        groupbox_release.setAlignment(Qt.AlignCenter)
        groupbox_release.setFlat(True)
        groupbox_release.setStyleSheet("font-weight: bold")
        groupbox_release_vertical_layout = QVBoxLayout()
        groupbox_release_vertical_layout.addWidget(self.label1)
        groupbox_release.setLayout(groupbox_release_vertical_layout)
        groupbox_changes = QGroupBox()
        groupbox_changes.setTitle("Değişiklikler")
        groupbox_changes.setAlignment(Qt.AlignCenter)
        groupbox_changes.setFlat(True)
        groupbox_changes.setStyleSheet("font-weight: bold")
        vertical_layout.addWidget(groupbox_version)
        vertical_layout.addWidget(groupbox_release)
        vertical_layout.addWidget(groupbox_changes)
        vertical_layout.addWidget(self.text_edit)
        self.widget.setLayout(vertical_layout)
        font = self.text_edit.font()
        font.setPointSize(10)
        self.text_edit.setFont(font)
        self.widget.show()
# ======================================================================================================================
# SysTray Hakkında =====================================================================================================
    # Hakkında SysTray Arayüzü =========================================================================================
    def about(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(about_icon))
        self.widget.setWindowTitle("Hakkında")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(275, 525)
        self.label = QLabel()
        self.label.setWhatsThis("Sahra - Sanal Asistan uygulama ikonu.")
        pixmap = QPixmap(app_logo)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        groupbox_app_name = QGroupBox()
        groupbox_app_name.setTitle("Uygulama")
        groupbox_app_name.setAlignment(Qt.AlignCenter)
        groupbox_app_name.setFlat(True)
        groupbox_app_name.setStyleSheet("font-weight: bold")
        groupbox_app_name_layout = QVBoxLayout()
        self.label1 = QLabel()
        self.label1.setWhatsThis("Sahra - Sanal Asistan uygulama adı.")
        self.label1.setText(app_name)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("font-weight: normal")
        groupbox_app_name_layout.addWidget(self.label1)
        groupbox_app_name.setLayout(groupbox_app_name_layout)
        groupbox_version = QGroupBox()
        groupbox_version.setTitle("Versiyon")
        groupbox_version.setAlignment(Qt.AlignCenter)
        groupbox_version.setFlat(True)
        groupbox_version.setStyleSheet("font-weight: bold")
        groupbox_version_layout = QVBoxLayout()
        self.label2 = QLabel()
        self.label2.setWhatsThis("Sahra - Sanal Asistan uygulama versiyon numarası.")
        self.label2.setText(app_version)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet("font-weight: normal")
        groupbox_version_layout.addWidget(self.label2)
        groupbox_version.setLayout(groupbox_version_layout)
        groupbox_company = QGroupBox()
        groupbox_company.setTitle("Şirket")
        groupbox_company.setAlignment(Qt.AlignCenter)
        groupbox_company.setFlat(True)
        groupbox_company.setStyleSheet("font-weight: bold")
        groupbox_company_layout = QVBoxLayout()
        self.label3 = QLabel()
        self.label3.setWhatsThis("Sahra - Sanal Asistan uygulama geliştiricisi.")
        self.label3.setText(app_author)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setStyleSheet("font-weight: normal")
        groupbox_company_layout.addWidget(self.label3)
        groupbox_company.setLayout(groupbox_company_layout)
        groupbox_contact = QGroupBox()
        groupbox_contact.setTitle("İletişim")
        groupbox_contact.setAlignment(Qt.AlignCenter)
        groupbox_contact.setFlat(True)
        groupbox_contact.setStyleSheet("font-weight: bold")
        groupbox_contact_layout = QVBoxLayout()
        self.label6 = QLabel()
        self.label6.setWhatsThis("Sahra - Sanal Asistan uygulama geliştiricisine ait iletişim adresi.")
        self.label6.setText(app_author_contact)
        self.label6.setAlignment(Qt.AlignCenter)
        self.label6.setStyleSheet("font-weight: normal")
        groupbox_contact_layout.addWidget(self.label6)
        groupbox_contact.setLayout(groupbox_contact_layout)
        groupbox_release = QGroupBox()
        groupbox_release.setTitle("Sürüm")
        groupbox_release.setAlignment(Qt.AlignCenter)
        groupbox_release.setFlat(True)
        groupbox_release.setStyleSheet("font-weight: bold")
        groupbox_release_layout = QVBoxLayout()
        self.label7 = QLabel()
        self.label7.setWhatsThis("Sahra - Sanal Asistan uygulama sürümü tipi.")
        self.label7.setText(app_version_type)
        self.label7.setAlignment(Qt.AlignCenter)
        self.label7.setStyleSheet("font-weight: normal")
        groupbox_release_layout.addWidget(self.label7)
        groupbox_release.setLayout(groupbox_release_layout)
        vertical_layout_main = QVBoxLayout()
        vertical_layout_main.addWidget(self.label)
        vertical_layout_main.addWidget(groupbox_app_name)
        vertical_layout_main.addWidget(groupbox_version)
        vertical_layout_main.addWidget(groupbox_release)
        vertical_layout_main.addWidget(groupbox_company)
        vertical_layout_main.addWidget(groupbox_contact)
        vertical_layout_main.setAlignment(Qt.AlignCenter)
        self.widget.setLayout(vertical_layout_main)
        self.widget.show()
# ======================================================================================================================
# SysTray Çıkış Yap ====================================================================================================
    # Çıkış Yap SysTray Arayüzü ========================================================================================
    def exit_sahara(self):
        self.widget1.hide()
        self.widget = QWidget()
        self.widget.setWindowIcon(QIcon(shutdown_self_icon))
        self.widget.setWindowTitle("Çıkış Yap")
        self.widget.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.widget.setFixedSize(350, 100)
        vertical_layout = QVBoxLayout()
        label = QLabel()
        label.setWhatsThis("Sahra - Sanal Asistan'ı kapatmak istediğinden emin olmak için bir soru.")
        label.setText("Sahra - Sanal Asistan'dan çıkış yapmak istediğine emin misin?")
        label.setAlignment(Qt.AlignCenter)
        vertical_layout.addWidget(label)
        horizontal_layout = QHBoxLayout()
        yes_button = QPushButton()
        yes_button.setWhatsThis("Bu butona tıklandığında Sahra - Sanal Asistan kapatılır.")
        yes_button.setText("Evet")
        yes_button.clicked.connect(exit)
        no_button = QPushButton()
        no_button.setWhatsThis("Bu butona tıklandığında Sahra - Sanal Asistan çalışmaya devam eder.")
        no_button.setText("Hayır")
        no_button.clicked.connect(self.widget.close)
        horizontal_layout.addWidget(yes_button)
        horizontal_layout.addWidget(no_button)
        vertical_layout.addLayout(horizontal_layout)
        self.widget.setLayout(vertical_layout)
        self.widget.show()
# ======================================================================================================================
# İnternet Kontrolü ====================================================================================================
    def check_connection(self):
        ip = gethostbyname(gethostname())
        if ip == "127.0.0.1":
            return False
        else:
            try:
                get("https://google.com.tr/")
                return True
            except exceptions.ConnectionError or exceptions.ReadTimeout or exceptions.ConnectTimeout:
                return False
# ======================================================================================================================
# Kullanıcıyı Dinleme ==================================================================================================
    def listen(self):
        if self.check_connection() is True:
            recognizer = Recognizer()
            microphone = Microphone()
            self.showMessage("Dinlemeye Başladım", "Komutlarını gerçekleştirmek için sabırsızlanıyorum.", QIcon(listening_start_icon64), msecs=0)
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                #self.showMessage(app_name, "Dinlemeyi Bitirdim.", QIcon(listening_stop_icon64), msecs=0)
            try:
                command = recognizer.recognize_google(audio, language='tr-tr').lower()
                return command
            except UnknownValueError:
                command = "UnknownValueError"
                return command
        else:
            self.showMessage("İnternet Bağlantısı Kesildi", "Komutlarını dinleyebilmem için internet bağlantısına ihtiyacım var.", QIcon(connection_lost_icon64), msecs=0)
            pass
# ======================================================================================================================
# Dinlenen Veriyi Süz ==================================================================================================
    def think(self, command):
        brightness_hundred = open('assets\\commands\\brightness_commands\\brightness_hundred.shr', encoding='utf-8').read().splitlines()
        brightness_fifty = open('assets\\commands\\brightness_commands\\brightness_fifty.shr', encoding='utf-8').read().splitlines()
        brightness_zero = open('assets\\commands\\brightness_commands\\brightness_zero.shr', encoding='utf-8').read().splitlines()
        brightness_up = open('assets\\commands\\brightness_commands\\brightness_up.shr', encoding='utf-8').read().splitlines()
        brightness_down = open('assets\\commands\\brightness_commands\\brightness_down.shr', encoding='utf-8').read().splitlines()
        volume_on = open('assets\\commands\\volume_commands\\volume_on.shr', encoding='utf-8').read().splitlines()
        volume_off = open('assets\\commands\\volume_commands\\volume_off.shr', encoding='utf-8').read().splitlines()
        volume_hundred = open('assets\\commands\\volume_commands\\volume_hundred.shr', encoding='utf-8').read().splitlines()
        volume_fifty = open('assets\\commands\\volume_commands\\volume_fifty.shr', encoding='utf-8').read().splitlines()
        volume_zero = open('assets\\commands\\volume_commands\\volume_zero.shr', encoding='utf-8').read().splitlines()
        volume_up = open('assets\\commands\\volume_commands\\volume_up.shr', encoding='utf-8').read().splitlines()
        volume_down = open('assets\\commands\\volume_commands\\volume_down.shr', encoding='utf-8').read().splitlines()
        lock_windows = open('assets\\commands\\power_commands\\lock_windows.shr', encoding='utf-8').read().splitlines()
        reboot_windows = open('assets\\commands\\power_commands\\reboot_windows.shr', encoding='utf-8').read().splitlines()
        shutdown_windows = open('assets\\commands\\power_commands\\shutdown_windows.shr', encoding='utf-8').read().splitlines()
        suspend_windows = open('assets\\commands\\power_commands\\suspend_windows.shr', encoding='utf-8').read().splitlines()
        take_a_screenshot = open('assets\\commands\\screenshot_commands\\take_a_screenshot.shr', encoding='utf-8').read().splitlines()
        open_screenshots_folder = open('assets\\commands\\screenshot_commands\\open_screenshots_folder.shr', encoding='utf-8').read().splitlines()
        shutdown_self = open('assets\\commands\\power_commands\\shutdown_self.shr', encoding='utf-8').read().splitlines()
        if command in volume_hundred:
            self.volume_hundred()
        elif command in volume_fifty:
            self.volume_fifty()
        elif command in volume_zero:
            self.volume_zero()
        elif command in volume_on:
            self.volume_on()
        elif command in volume_off:
            self.volume_off()
        elif command in volume_down:
            self.volume_down()
        elif command in volume_up:
            self.volume_up()
        elif command in brightness_up:
            self.brightness_up(self.brightness_get())
        elif command in brightness_down:
            self.brightness_down(self.brightness_get())
        elif command in brightness_hundred:
            self.brightness_hundred(self.brightness_get())
        elif command in brightness_fifty:
            self.brightness_fifty(self.brightness_get())
        elif command in brightness_zero:
            self.brightness_zero(self.brightness_get())
        elif command in lock_windows:
            self.lock_windows()
        elif command in suspend_windows:
            self.suspend_windows()
        elif command in reboot_windows:
            self.reboot_windows()
        elif command in shutdown_windows:
            self.shutdown_windows()
        elif command in shutdown_self:
            self.shutdown_self()
        elif command in take_a_screenshot:
            self.take_a_screenshot()
        elif command in open_screenshots_folder:
            self.open_screenshots_folder()
        elif command == "UnknownValueError":
            self.showMessage("Ne Söylediğini Anlamadım", "Söylediklerini anlayabilmem için net bir şekilde söylemen gerekiyor.", QIcon(i_dont_understand_icon64), msecs=0)
        else:
            self.showMessage("Geçersiz Komut Verdin", "'{}.'\nVermiş olduğun bu komut, fonksiyonlarıma tanımlı komutlar ile örtüşmüyor.".format(command.capitalize()), QIcon(unknown_command_icon_64), msecs=0)
# ======================================================================================================================
# Ekran Fotoğrafı Fonksiyonları =========================================================================================
    def take_a_screenshot(self):
        if self.windows_lock_control() == 1:
            pass
        else:
            now = datetime.now()
            datetime_now = now.strftime("[%d-%m-%Y-%H-%M-%S]")
            location = screenshot_location + app_name + datetime_now + ".png"
            if path.exists(screenshot_location) is True:
                sleep(5)
                screenshot().save(location)
                self.showMessage("Ekran Fotoğrafı Fonksiyonları", "Ekranın fotoğrafını çektim.", QIcon(take_a_screenshot_icon64), msecs=0)
                startfile(location)
            else:
                sleep(5)
                makedirs(screenshot_location)
                screenshot().save(location)
                self.showMessage("Ekran Fotoğrafı Fonksiyonları", "Ekranın fotoğrafını çektim.", QIcon(take_a_screenshot_icon64), msecs=0)
                startfile(location)
    def open_screenshots_folder(self):
        if self.windows_lock_control() == 1:
            pass
        else:
            self.showMessage("Ekran Fotoğrafı Fonksiyonları", "Ekran fotoğrafları klasörünü açtım.", QIcon(screenshot_folder_icon64), msecs=0)
            if path.exists(screenshot_location) is False:
                makedirs(screenshot_location)
                startfile(screenshot_location)
            elif path.exists(screenshot_location) is True:
                startfile(screenshot_location)
# ======================================================================================================================
# Ekran Parlaklığı Seviyesi Fonksiyonları ==============================================================================
    def brightness_get(self):
        wmiconnection = WMI(namespace='root/wmi', privileges=["Security"])
        value = wmiconnection.WmiMonitorBrightness()[0].CurrentBrightness
        return value
    def brightness_hundred(self, value):
        wmiconnection = WMI(namespace='root/wmi', privileges=["Security"])
        methods = wmiconnection.WmiMonitorBrightnessMethods()[0]
        if value == 100:
            self.showMessage("Ekran Parlaklığı Seviyesi Fonksiyonları", "Ekran parlaklığı seviyesi zaten 100'de.", QIcon(brightness_hundred_icon64), msecs=0)
        else:
            brightness = 100
            self.showMessage("Ekran Parlaklığı Seviyesi Fonksiyonları", "Ekran parlaklığı seviyesini 100 yaptım.", QIcon(brightness_hundred_icon64), msecs=0)
            methods.WmiSetBrightness(brightness, 0)
    def brightness_fifty(self, value):
        wmiconnection = WMI(namespace='root/wmi', privileges=["Security"])
        methods = wmiconnection.WmiMonitorBrightnessMethods()[0]
        if value == 50:
            self.showMessage("Ekran Parlaklığı Seviyesi Fonksiyonları", "Ekran parlaklığı seviyesi zaten 50'de.", QIcon(brightness_icon64), msecs=0)
        else:
            brightness = 50
            self.showMessage("Ekran Parlaklığı Seviyesi Fonksiyonları", "Ekran parlaklığı seviyesini 50 yaptım.", QIcon(brightness_icon64), msecs=0)
            methods.WmiSetBrightness(brightness, 0)
    def brightness_zero(self, value):
        wmiconnection = WMI(namespace='root/wmi', privileges=["Security"])
        methods = wmiconnection.WmiMonitorBrightnessMethods()[0]
        if value == 0:
            self.showMessage("Ekran Parlaklığı Seviyesi Fonksiyonları", "Ekran parlaklığı seviyesi zaten 0'da.", QIcon(brightness_zero_icon64), msecs=0)
        else:
            brightness = 0
            self.showMessage("Ekran Parlaklığı Seviyesi Fonksiyonları", "Ekran parlaklığı seviyesini 0 yaptım.", QIcon(brightness_zero_icon64), msecs=0)
            methods.WmiSetBrightness(brightness, 0)
    def brightness_up(self, value):
        wmiconnection = WMI(namespace='root/wmi', privileges=["Security"])
        methods = wmiconnection.WmiMonitorBrightnessMethods()[0]
        if value == 100:
            self.showMessage("Ekran Parlaklığı Seviyesi Fonksiyonları", "Ekran parlaklığı seviyesi zaten 100'de.", QIcon(brightness_hundred_icon64), msecs=0)
        else:
            if value <= 75:
                brightness = value + 25
            else:
                brightness = value + (100 - value)
            self.showMessage("Ekran Parlaklığı Seviyesi Fonksiyonları", "Ekran parlaklığı seviyesini arttırdım.", QIcon(brightness_hundred_icon64), msecs=0)
            methods.WmiSetBrightness(brightness, 0)
    def brightness_down(self, value):
        wmiconnection = WMI(namespace='root/wmi', privileges=["Security"])
        methods = wmiconnection.WmiMonitorBrightnessMethods()[0]
        if value == 0:
            self.showMessage("Ekran Parlaklığı Seviyesi Fonksiyonları", "Ekran parlaklığı seviyesi zaten 0'da.", QIcon(brightness_zero_icon64), msecs=0)
        else:
            if value >= 25:
                brightness = value - 25
            else:
                brightness = value - value
            self.showMessage("Ekran Parlaklığı Seviyesi Fonksiyonları", "Ekran parlaklığı seviyesini azalttım.", QIcon(brightness_zero_icon64), msecs=0)
            methods.WmiSetBrightness(brightness, 0)
# ======================================================================================================================
# Güç Seçenekleri Fonksiyonları ========================================================================================
    def windows_lock_control(self):
        if "LogonUI.exe" in (p.name() for p in process_iter()):
            return True
        else:
            return False
    def lock_windows(self):
        if self.windows_lock_control() is True:
            pass
        else:
            yes = open('assets\\commands\\confirmation_commands\\yes.shr', encoding='utf-8').read().splitlines()
            no = open('assets\\commands\\confirmation_commands\\no.shr', encoding='utf-8').read().splitlines()
            if self.check_connection() is True:
                sleep(1)
                self.showMessage("Onay Gerekiyor", "Bilgisayarı kilitleyeceğim.\nOnaylıyor musun?", QIcon(are_you_confirm_icon64), msecs=0)
                while True:
                    recognizer = Recognizer()
                    microphone = Microphone()
                    with microphone as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                    try:
                        answer = recognizer.recognize_google(audio, language='tr-tr').lower()
                    except UnknownValueError:
                        answer = "UnknownValueError"
                    if answer in yes:
                        self.showMessage("Komutu Onayladın", "Bilgisayarı kilitliyorum.", QIcon(accept_icon64), msecs=0)
                        sleep(3)
                        windll.user32.LockWorkStation()
                        break
                    elif answer in no:
                        self.showMessage("Komutu Onaylamadın", "Bilgisayarı kilitlemeyeceğim.", QIcon(deny_icon64), msecs=0)
                        break
                    else:
                        sleep(1.5)
                        self.showMessage("Onay Komutunu Anlamadım", "Bilgisayarı kilitleyeceğim.\nOnaylıyor musun?", QIcon(are_you_confirm_icon64), msecs=0)
            else:
                self.showMessage("İnternet Bağlantısı Kesildi", "'Güç Seçenekleri' fonksiyonlarını gerçekleştirebilmem için internet bağlantısına ihtiyacım var.", QIcon(connection_lost_icon64), msecs=0)
    def suspend_windows(self):
        if self.windows_lock_control() is True:
            pass
        else:
            yes = open('assets\\commands\\confirmation_commands\\yes.shr', encoding='utf-8').read().splitlines()
            no = open('assets\\commands\\confirmation_commands\\no.shr', encoding='utf-8').read().splitlines()
            if self.check_connection() is True:
                sleep(1)
                self.showMessage("Onay Gerekiyor", "Bilgisayarı uyku moduna alacağım.\nOnaylıyor musun?", QIcon(are_you_confirm_icon64), msecs=0)
                while True:
                    recognizer = Recognizer()
                    microphone = Microphone()
                    with microphone as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                    try:
                        answer = recognizer.recognize_google(audio, language='tr-tr').lower()
                    except UnknownValueError:
                        answer = "UnknownValueError"
                    if answer in yes:
                        self.showMessage("Komutu Onayladın", "Bilgisayarı uyku moduna alıyorum.", QIcon(accept_icon64), msecs=0)
                        sleep(3)
                        windll.powrprof.SetSuspendState(False, True, False)
                        break
                    elif answer in no:
                        self.showMessage("Komutu Onaylamadın", "Bilgisayarı uyku moduna almayacağım.", QIcon(deny_icon64), msecs=0)
                        break
                    else:
                        sleep(1.5)
                        self.showMessage("Onay Komutunu Anlamadım", "Bilgisayarı uyku moduna alacağım.\nOnaylıyor musun?", QIcon(are_you_confirm_icon64), msecs=0)
            else:
                self.showMessage("İnternet Bağlantısı Kesildi", "'Güç Seçenekleri' fonksiyonlarını gerçekleştirebilmem için internet bağlantısına ihtiyacım var.", QIcon(connection_lost_icon64), msecs=0)
    def reboot_windows(self):
        if self.windows_lock_control() is True:
            pass
        else:
            yes = open('assets\\commands\\confirmation_commands\\yes.shr', encoding='utf-8').read().splitlines()
            no = open('assets\\commands\\confirmation_commands\\no.shr', encoding='utf-8').read().splitlines()
            if self.check_connection() is True:
                sleep(1)
                self.showMessage("Onay Gerekiyor", "Bilgisayarı yeniden başlatacağım.\nOnaylıyor musun?", QIcon(are_you_confirm_icon64), msecs=0)
                while True:
                    recognizer = Recognizer()
                    microphone = Microphone()
                    with microphone as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                    try:
                        answer = recognizer.recognize_google(audio, language='tr-tr').lower()
                    except UnknownValueError:
                        answer = "UnknownValueError"
                    if answer in yes:
                        self.showMessage("Komutu Onayladın", "Bilgisayarı yeniden başlatıyorum.", QIcon(accept_icon64), msecs=0)
                        sleep(3)
                        system("shutdown /r")
                        break
                    elif answer in no:
                        self.showMessage("Komutu Onaylamadın", "Bilgisayarı yeniden başlatmayacağım.", QIcon(deny_icon64), msecs=0)
                        break
                    else:
                        sleep(1.5)
                        self.showMessage("Onay Komutunu Anlamadım", "Bilgisayarı yeniden başlatacağım.\nOnaylıyor musun?", QIcon(are_you_confirm_icon64), msecs=0)
            else:
                self.showMessage("İnternet Bağlantısı Kesildi", "'Güç Seçenekleri' fonksiyonlarını gerçekleştirebilmem için internet bağlantısına ihtiyacım var.", QIcon(connection_lost_icon64), msecs=0)
    def shutdown_windows(self):
        if self.windows_lock_control() is True:
            pass
        else:
            yes = open('assets\\commands\\confirmation_commands\\yes.shr', encoding='utf-8').read().splitlines()
            no = open('assets\\commands\\confirmation_commands\\no.shr', encoding='utf-8').read().splitlines()
            if self.check_connection() is True:
                sleep(1)
                self.showMessage("Onay Gerekiyor", "Bilgisayarı kapatacağım.\nOnaylıyor musun?", QIcon(are_you_confirm_icon64), msecs=0)
                while True:
                    recognizer = Recognizer()
                    microphone = Microphone()
                    with microphone as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                    try:
                        answer = recognizer.recognize_google(audio, language='tr-tr').lower()
                    except UnknownValueError:
                        answer = "UnknownValueError"
                    if answer in yes:
                        self.showMessage("Komutu Onayladın", "Bilgisayarı kapatıyorum.", QIcon(accept_icon64), msecs=0)
                        sleep(3)
                        system("shutdown /s")
                        break
                    elif answer in no:
                        self.showMessage("Komutu Onaylamadın", "Bilgisayarı kapatmayacağım.", QIcon(deny_icon64), msecs=0)
                        break
                    else:
                        sleep(1.5)
                        self.showMessage("Onay Komutunu Anlamadım", "Bilgisayarı kapatacağım.\nOnaylıyor musun?", QIcon(are_you_confirm_icon64), msecs=0)
            else:
                self.showMessage("İnternet Bağlantısı Kesildi", "'Güç Seçenekleri' fonksiyonlarını gerçekleştirebilmem için internet bağlantısına ihtiyacım var.", QIcon(connection_lost_icon64), msecs=0)
    def shutdown_self(self):
        if self.windows_lock_control() is True:
            pass
        else:
            yes = open('assets\\commands\\confirmation_commands\\yes.shr', encoding='utf-8').read().splitlines()
            no = open('assets\\commands\\confirmation_commands\\no.shr', encoding='utf-8').read().splitlines()
            if self.check_connection() is True:
                sleep(1)
                self.showMessage("Onay Gerekiyor", "Kendimi kapatacağım.\nOnaylıyor musun?", QIcon(are_you_confirm_icon64), msecs=0)
                while True:
                    recognizer = Recognizer()
                    microphone = Microphone()
                    with microphone as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                    try:
                        answer = recognizer.recognize_google(audio, language='tr-tr').lower()
                    except UnknownValueError:
                        answer = "UnknownValueError"
                    if answer in yes:
                        self.showMessage("Komutu Onayladın", "Kendimi kapatıyorum.", QIcon(accept_icon64), msecs=0)
                        sleep(3)
                        exit()
                        break
                    elif answer in no:
                        self.showMessage("Komutu Onaylamadın", "Kendimi kapatmayacağım.", QIcon(deny_icon64), msecs=0)
                        break
                    else:
                        sleep(1.5)
                        self.showMessage("Onay Komutunu Anlamadım", "Kendimi kapatacağım.\nOnaylıyor musun?", QIcon(are_you_confirm_icon64), msecs=0)
            else:
                self.showMessage("İnternet Bağlantısı Kesildi", "'Güç Seçenekleri' fonksiyonlarını gerçekleştirebilmem için internet bağlantısına ihtiyacım var.", QIcon(connection_lost_icon64), msecs=0)
# ======================================================================================================================
# Ses Seviyesi Fonksiyonları ===========================================================================================
    def volume_on(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMute() == 1:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses akışını açtım.", QIcon(volume_icon64), msecs=0)
            volume.SetMute(0, None)
        else:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses akışı zaten açık.", QIcon(volume_icon64), msecs=0)
    def volume_off(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMute() == 0:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses akışını kapattım.", QIcon(volume_mute_icon64), msecs=0)
            volume.SetMute(1, None)
        else:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses akışı zaten kapalı.", QIcon(volume_mute_icon64), msecs=0)
    def volume_hundred(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMasterVolumeLevel() == 0.0:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses seviyesi zaten 100'de.", QIcon(volume_icon64), msecs=0)
        else:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses seviyesini 100 yaptım.", QIcon(volume_icon64), msecs=0)
            volume.SetMasterVolumeLevel(0.0, None)
    def volume_fifty(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMasterVolumeLevel() == -10.329694747924805:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses seviyesi zaten 50'de.", QIcon(volume_fifty_icon64), msecs=0)
        else:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses seviyesini 50 yaptım.", QIcon(volume_fifty_icon64), msecs=0)
            volume.SetMasterVolumeLevel(-10.329694747924805, None)
    def volume_zero(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMasterVolumeLevel() == -65.25:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses seviyesi zaten 0'da.", QIcon(volume_mute_icon64), msecs=0)
        else:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses seviyesini 0 yaptım.", QIcon(volume_mute_icon64), msecs=0)
            volume.SetMasterVolumeLevel(-65.25, None)
    def volume_down(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMasterVolumeLevel() == -65.25:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses seviyesi zaten 0'da.", QIcon(volume_zero_icon64), msecs=0)
        else:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses seviyesini azalttım.", QIcon(volume_zero_icon64), msecs=0)
            for i in range(10):
                press("volume down")
                sleep(0.30)
    def volume_up(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMasterVolumeLevel() == 0.0:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses seviyesi zaten 100'de.", QIcon(volume_icon64), msecs=0)
        else:
            self.showMessage("Ses Seviyesi Fonksiyonları", "Ses seviyesini arttırdım.", QIcon(volume_icon64), msecs=0)
            for i in range(10):
                press("volume up")
                sleep(0.20)
# ======================================================================================================================
    def alert(self):
        self.showMessage("Uzun Süreli Bilgisayar Kullanımı Uyarısı", "Uzun süreli hareketsiz bilgisayar kullanımı fiziksel ve psikolojik sağlığına ciddi zararlar verir. Bilgisayar kullanımına biraz ara ver ve hareket et.", QIcon(walk_icon64), msecs=0)
    def click_event(self, reason):
        if reason is QSystemTrayIcon.ActivationReason.DoubleClick:
            self.think(self.listen())
# ======================================================================================================================
class UygulamaIzleyici(QThread):
    signal = Signal(str)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def run(self):
        i = 0
        last_app = last_exe = ""
        start = None
        while True:
            configfile = RawConfigParser()
            usage_database_location = "assets\\application_usages\\"
            usage_database_filename = getlogin() + "[" + strftime('%d-%m-%Y') + "]" + ".aut"
            db = connect("{}{}".format(usage_database_location, usage_database_filename))
            im = db.cursor()
            im.execute('''CREATE TABLE IF NOT EXISTS application_usage_tracker(application_name TEXT, application_executable TEXT, application_usage INT, application_usage_time TEXT)''')
            active_window = GetForegroundWindow()
            active_window_process_id = GetWindowThreadProcessId(active_window)[-1]
            if active_window_process_id > 0 and len(str(active_window_process_id)) < 6:
                active_window_executable = Process(active_window_process_id).name()
                try:
                    with open(application_usage_tracker_configurations_location, 'r', encoding='utf-8') as f:
                        configfile.read_file(f)
                        active_window_text = configfile.get('Uygulama Başlık Filtreleri', active_window_executable)
                        f.close()
                except NoOptionError:
                    active_window_text = GetWindowText(active_window)
                if last_app != active_window_text and last_exe != active_window_executable and i == 0:
                    start = time()
                    last_app = active_window_text
                    last_exe = active_window_executable
                    i = 1
                    self.signal.emit("• [{}] - [{} | {}] - [Aktivite Başladı]\n".format(strftime("%H:%M:%S", localtime()), last_app, last_exe))
                elif (last_app != active_window_text and last_exe != active_window_executable) or (last_app != active_window_text and last_exe == active_window_executable) and i == 1:
                    stop = time()
                    realtime = stop - start

                    im.execute("SELECT application_executable FROM application_usage_tracker WHERE application_executable=?", (last_exe,))
                    app_exe_exist = im.fetchone() is not None
                    im.execute("SELECT application_name FROM application_usage_tracker WHERE application_name=?", (last_app,))
                    app_name_exist = im.fetchone() is not None
                    if app_name_exist is True and app_exe_exist is True:
                        while True:
                            try:
                                im.execute("SELECT application_usage FROM application_usage_tracker WHERE application_name=? AND application_executable=?", (last_app, last_exe))
                                data = im.fetchone()
                                data = data[0]
                                break
                            except TypeError as error:
                                print(error)
                                pass
                        elapsed_time = realtime + data
                        total_elapsed_time = strftime('%H:%M:%S', gmtime(elapsed_time))
                        im.execute("UPDATE application_usage_tracker SET application_usage=? WHERE application_name=? AND application_executable=?", (elapsed_time, last_app, last_exe))
                        im.execute("UPDATE application_usage_tracker SET application_usage_time=? WHERE application_name=? AND application_executable=?", (total_elapsed_time, last_app, last_exe))
                        db.commit()
                        self.signal.emit("\n• [{}] - [{} | {}] - [{} | {}] - [Aktivite Durdu]\n".format(
                            strftime("%H:%M:%S", localtime()), last_app, last_exe,
                            strftime('%H:%M:%S', gmtime(realtime)), strftime('%H:%M:%S', gmtime(elapsed_time))))
                    else:
                        total_elapsed_time = strftime('%H:%M:%S', gmtime(realtime))
                        im.execute("INSERT INTO application_usage_tracker VALUES (?, ?, ?, ?)",
                                   (last_app, last_exe, realtime, total_elapsed_time))
                        db.commit()
                        self.signal.emit("\n• [{}] - [{} | {}] - [{} | {}] - [Aktivite Durdu]\n".format(
                            strftime("%H:%M:%S", localtime()), last_app, last_exe,
                            strftime('%H:%M:%S', gmtime(realtime)), strftime('%H:%M:%S', gmtime(realtime))))
                    last_app = active_window_text
                    last_exe = active_window_executable
                    self.signal.emit("\n• [{}] - [{} | {}] - [Aktivite Başladı]\n".format(
                        strftime("%H:%M:%S", localtime()), last_app, last_exe))
                    start = time()
                else:
                    pass
            elif len(str(active_window_process_id)) > 5:
                pass
            else:
                pass
            db.close()
            sleep(0.25)


if __name__ == "__main__":
    app = QApplication(argv)
    app.setQuitOnLastWindowClosed(False)
    SysTrayIcon = App()
    SysTrayIcon.show()
    exit(app.exec())