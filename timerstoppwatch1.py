import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, QDateTime, Qt

class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stoppuhr und Timer")
        self.setStyleSheet("background-color: rgb(77, 77, 77); color: white;")

        self.initUI()

    def initUI(self):
        # Weltuhr
        world_clock_layout = QVBoxLayout()
        self.world_clock_label = QLabel("Weltuhr")
        self.world_clock_label.setStyleSheet("font-size: 20px;")
        world_clock_layout.addWidget(self.world_clock_label)
        self.country_combo = QComboBox()
        self.country_combo.addItems(["Deutschland", "USA", "Japan"])
        self.country_combo.currentIndexChanged.connect(self.updateWorldTime)
        world_clock_layout.addWidget(self.country_combo)
        self.world_time_label = QLabel()
        self.world_time_label.setStyleSheet("font-size: 16px;")
        world_clock_layout.addWidget(self.world_time_label)
        world_clock_layout.addStretch()

        # Timer
        timer_layout = QVBoxLayout()
        self.timer_label = QLabel("Timer")
        self.timer_label.setStyleSheet("font-size: 20px;")
        timer_layout.addWidget(self.timer_label)
        self.timer_time_label = QLabel()
        self.timer_time_label.setStyleSheet("font-size: 16px;")
        timer_layout.addWidget(self.timer_time_label)
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Zeit eingeben")
        timer_layout.addWidget(self.time_input)
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Sekunden", "Minuten", "Stunden"])
        timer_layout.addWidget(self.unit_combo)
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.startTimer)
        timer_layout.addWidget(self.start_button)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stopTimer)
        self.stop_button.hide()
        timer_layout.addWidget(self.stop_button)
        self.resume_button = QPushButton("Weiter")
        self.resume_button.clicked.connect(self.resumeTimer)
        self.resume_button.hide()
        timer_layout.addWidget(self.resume_button)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.resetTimer)
        timer_layout.addWidget(self.reset_button)
        timer_layout.addStretch()

        # Stoppuhr
        stopwatch_layout = QVBoxLayout()
        self.stopwatch_label = QLabel("Stoppuhr")
        self.stopwatch_label.setStyleSheet("font-size: 20px;")
        stopwatch_layout.addWidget(self.stopwatch_label)
        self.stopwatch_time_label = QLabel("00:00:00:000")
        self.stopwatch_time_label.setStyleSheet("font-size: 24px;")
        stopwatch_layout.addWidget(self.stopwatch_time_label)
        self.stopwatch_start_button = QPushButton("Start")
        self.stopwatch_start_button.clicked.connect(self.startStopwatch)
        stopwatch_layout.addWidget(self.stopwatch_start_button)
        self.stopwatch_stop_button = QPushButton("Stop")
        self.stopwatch_stop_button.clicked.connect(self.stopStopwatch)
        self.stopwatch_stop_button.hide()
        stopwatch_layout.addWidget(self.stopwatch_stop_button)
        self.stopwatch_reset_button = QPushButton("Reset")
        self.stopwatch_reset_button.clicked.connect(self.resetStopwatch)
        stopwatch_layout.addWidget(self.stopwatch_reset_button)
        stopwatch_layout.addStretch()

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(world_clock_layout)
        main_layout.addLayout(timer_layout)
        main_layout.addLayout(stopwatch_layout)

        self.setLayout(main_layout)

        # Timer for updating world time
        self.world_timer = QTimer()
        self.world_timer.timeout.connect(self.updateWorldTime)
        self.world_timer.start(1000)

        # Stopwatch variables
        self.stopwatch_timer = QTimer()
        self.stopwatch_timer.timeout.connect(self.updateStopwatch)
        self.stopwatch_milliseconds = 0
        self.stopwatch_seconds = 0
        self.stopwatch_minutes = 0
        self.stopwatch_hours = 0

    def updateWorldTime(self):
        country = self.country_combo.currentText()
        if country == "Deutschland":
            time = QDateTime.currentDateTime().toString("hh:mm:ss")

    def startTimer(self):
        time_input = int(self.time_input.text())
        unit = self.unit_combo.currentText()
        if unit == "Minuten":
            time_input *= 60
        elif unit == "Stunden":
            time_input *= 3600

        self.time_remaining = time_input
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(1000)
        self.updateTimer()
        self.start_button.hide()
        self.stop_button.show()

    def stopTimer(self):
        self.timer.stop()
        self.resume_button.show()
        self.start_button.hide()
        self.stop_button.hide()

    def resumeTimer(self):
        self.timer.start(1000)
        self.resume_button.hide()
        self.start_button.hide()
        self.stop_button.show()

    def resetTimer(self):
        self.timer.stop()
        self.start_button.show()
        self.stop_button.hide()
        self.resume_button.hide()
        self.timer_time_label.setText("")

    def updateTimer(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_time_label.setText(f"{minutes} Minuten {seconds} Sekunden")
        self.time_remaining -= 1

        if self.time_remaining < 0:
            self.timer.stop()
            self.timer_time_label.setText("Zeit abgelaufen!")
            self.start_button.hide()
            self.stop_button.hide()
            self.resume_button.hide()

    def startStopwatch(self):
        self.stopwatch_timer.start(10)
        self.stopwatch_start_button.hide()
        self.stopwatch_stop_button.show()

    def stopStopwatch(self):
        self.stopwatch_timer.stop()
        self.stopwatch_start_button.show()
        self.stopwatch_stop_button.hide()

    def resetStopwatch(self):
        self.stopwatch_timer.stop()
        self.stopwatch_milliseconds = 0
        self.stopwatch_seconds = 0
        self.stopwatch_minutes = 0
        self.stopwatch_hours = 0
        self.stopwatch_time_label.setText("00:00:00:000")
        self.stopwatch_start_button.show()

    def updateStopwatch(self):
        self.stopwatch_milliseconds += 1
        if self.stopwatch_milliseconds >= 100:
            self.stopwatch_milliseconds = 0
            self.stopwatch_seconds += 1
        if self.stopwatch_seconds >= 60:
            self.stopwatch_seconds = 0
            self.stopwatch_minutes += 1
        if self.stopwatch_minutes >= 60:
            self.stopwatch_minutes = 0
            self.stopwatch_hours += 1
        formatted_time = f"{self.stopwatch_hours:02}:{self.stopwatch_minutes:02}:{self.stopwatch_seconds}"
        self.stopwatch_time_label.setText(formatted_time)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Stopwatch()
    window.show()
    sys.exit(app.exec_())