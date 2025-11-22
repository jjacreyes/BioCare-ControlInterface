import sys
import qtawesome as qta
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QListWidget, QFrame

from PyQt6.QtCore import Qt

APP_STYLE = """
QWidget {
    background-color: #1A1A1A;  /* Main background */
    color: #EAEAEA;             /* Default text */
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 15px;
}

/* Sidebar */
QFrame#sidebar {
    background-color: #000000;
}

/* Sidebar buttons */
QPushButton {
    background-color: transparent;
    border: none;
    padding: 8px 12px;
    text-align: left;
    color: #EAEAEA;
}
QPushButton:hover {
    background-color: #CC0000;   /* Carleton Red on hover */
    border-radius: 6px;
}
QPushButton:pressed {
    background-color: #990000;   /* Darker red on press */
}

/* Titles */
QLabel#title {
    font-size: 20px;
    font-weight: bold;
    color: #CC0000;  /* Carleton red headings */
}

/* Cards / panels */
QFrame#card {
    background-color: #262626;
    border-radius: 8px;
    padding: 12px;
    margin: 8px 0;
}

/* Selected items (lists) */
QListWidget::item:selected {
    background-color: #CC0000;
    color: #FFFFFF;
    border-radius: 6px;
}
"""

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BioCare Prosthetic Control Dashboard")
        self.setMinimumSize(1200, 700)

        # ---------------- Main Container ----------------
        container = QWidget()
        layout = QHBoxLayout(container)

        # ---------------- Sidebar ----------------
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar_frame)

        self.btn_presets  = QPushButton("  Preset Manager", icon=qta.icon("mdi.bookmark"))
        self.btn_ble      = QPushButton("  BLE Manager", icon=qta.icon("mdi.bluetooth"))
        self.btn_live     = QPushButton("  Live Sensor Display", icon=qta.icon("mdi.chart-line"))
        self.btn_settings = QPushButton("  Settings", icon=qta.icon("mdi.cog"))

        for btn in [self.btn_presets, self.btn_ble, self.btn_live, self.btn_settings]:
            btn.setFixedHeight(50)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # ---------------- Pages ----------------
        self.pages = QStackedWidget()


        # Build Pages
        self.presets_page = self.build_presets_page()
        self.ble_page = self.build_ble_page()
        self.sensors_page = self.build_live_sensor_page()
        self.settings_page = self.build_settings_page()

        # Add Pages to Widgets
        self.pages.addWidget(self.presets_page)
        self.pages.addWidget(self.ble_page)
        self.pages.addWidget(self.sensors_page)
        self.pages.addWidget(self.settings_page)

        layout.addWidget(sidebar_frame, 1)
        layout.addWidget(self.pages, 4)

        self.setCentralWidget(container)

        # ---------------- Connect Buttons ----------------
        self.btn_presets.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.btn_ble.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.btn_live.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        self.btn_settings.clicked.connect(lambda: self.pages.setCurrentIndex(3))


        # ================ Preset Page ======================
    def build_presets_page(self):
        page = QWidget()
        main_layout = QHBoxLayout(page)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(25)

        # ---------------- Left Panel: Preset List ----------------
        left_panel = QFrame()
        left_panel.setObjectName("card")
        left_panel.setStyleSheet("""
        QFrame#card {
            background-color: #2b2b2b;
            border-radius: 12px;
            border: 1px solid #3c3c3c;
        }
        """)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(15)

        # Title
        title = QLabel("Preset Manager")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffffff")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        left_layout.addWidget(title)


        # Presets List
        self.preset_list = QListWidget()
        self.preset_list.setFixedWidth(250)
        self.preset_list.setStyleSheet("background-color: #262626; border: 1px solid #dcdcdc;")
        left_layout.addWidget(self.preset_list)

        # Create | Edit | Delete Buttons
        btn_layout = QHBoxLayout()
        btn_create = QPushButton("Create")
        btn_edit   = QPushButton("Edit")
        btn_delete = QPushButton("Delete")
        for b in [btn_create, btn_edit, btn_delete]:
            b.setFixedHeight(35)
            btn_layout.addWidget(b)
        left_layout.addLayout(btn_layout)

        # ---------------- Right Panel: Preset Details ----------------
        right_panel = QFrame()
        right_panel.setObjectName("card")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_layout.setSpacing(10)
        

        # ------ 
        details_title = QLabel("Preset Details")
        details_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        details_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        right_layout.addWidget(details_title)

        self.details_display = QLabel("Select a preset to view details here...")
        self.details_display.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.details_display.setWordWrap(True)
        right_layout.addWidget(self.details_display)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

        return page
    
    def build_ble_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("BLE Manager")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        btn_scan = QPushButton("Scan for ESP32")
        btn_connect = QPushButton("Connect")
        btn_disconnect = QPushButton("Disconnect")
        for b in [btn_scan, btn_connect, btn_disconnect]:
            b.setFixedHeight(40)
            layout.addWidget(b)

        layout.addStretch()
        return page

    

    # ---------------- Live Sensor Page ----------------
    def build_live_sensor_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Live Sensor Data")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Live data placeholder..."))
        layout.addStretch()
        return page

    # ---------------- Settings Page ----------------
    def build_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)
        layout.addStretch()
        return page



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())
