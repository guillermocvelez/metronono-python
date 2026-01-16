
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSlider, QComboBox, QFrame)
from PyQt6.QtCore import Qt, QTimer
from src.core.metronome import Metronome
from src.ui.styles import STYLESHEET

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Metrónomo Pro")
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet(STYLESHEET)
        
        self.metronome = Metronome()
        self.metronome.beat_signal.connect(self.on_beat)
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title_label = QLabel("METRÓNOMO")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #89b4fa; letter-spacing: 2px;")
        layout.addWidget(title_label)

        # BPM Display
        self.bpm_label = QLabel(f"{self.metronome.bpm}")
        self.bpm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bpm_label.setStyleSheet("font-size: 72px; font-weight: bold; color: #cdd6f4;")
        layout.addWidget(self.bpm_label)

        bpm_unit = QLabel("BPM")
        bpm_unit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bpm_unit.setStyleSheet("font-size: 18px; color: #a6adc8;")
        layout.addWidget(bpm_unit)

        # Visual Beat Indicator
        self.beat_indicator = QFrame()
        self.beat_indicator.setFixedSize(20, 20)
        self.beat_indicator.setStyleSheet("background-color: #45475a; border-radius: 10px;")
        # Centering indicator
        indicator_layout = QHBoxLayout()
        indicator_layout.addStretch()
        indicator_layout.addWidget(self.beat_indicator)
        indicator_layout.addStretch()
        layout.addLayout(indicator_layout)

        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(40, 220)
        self.slider.setValue(self.metronome.bpm)
        self.slider.valueChanged.connect(self.update_bpm)
        layout.addWidget(self.slider)

        # Controls Layout
        controls_layout = QHBoxLayout()
        
        # Time Signature
        self.time_sig_combo = QComboBox()
        self.time_sig_combo.addItems(["4/4", "3/4", "2/4", "6/8"])
        self.time_sig_combo.currentIndexChanged.connect(self.update_time_signature)
        controls_layout.addWidget(self.time_sig_combo)

        # Play Button
        self.play_btn = QPushButton("PLAY")
        self.play_btn.setFixedSize(120, 50)
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.clicked.connect(self.toggle_metronome)
        controls_layout.addWidget(self.play_btn)

        layout.addLayout(controls_layout)
        
        # Spacer
        layout.addStretch()

    def update_bpm(self, value):
        self.metronome.set_bpm(value)
        self.bpm_label.setText(str(value))

    def update_time_signature(self, index):
        text = self.time_sig_combo.currentText()
        numerator = int(text.split('/')[0])
        self.metronome.set_time_signature(numerator)

    def toggle_metronome(self):
        if self.metronome.playing:
            self.metronome.stop()
            self.play_btn.setText("PLAY")
            self.play_btn.setStyleSheet("") # Reset or set specific stop style
        else:
            self.metronome.start()
            self.play_btn.setText("STOP")
            self.play_btn.setStyleSheet("background-color: #f38ba8; border-color: #f38ba8;")

    def on_beat(self, beat_num):
        # Flash the indicator
        # High beat (1) is different color?
        if beat_num == 1:
             self.beat_indicator.setStyleSheet("background-color: #a6e3a1; border-radius: 10px;") # Green for downbeat
        else:
             self.beat_indicator.setStyleSheet("background-color: #89b4fa; border-radius: 10px;") # Blue for others
        
        # Reset color after 100ms
        QTimer.singleShot(100, self.reset_indicator)

    def reset_indicator(self):
        self.beat_indicator.setStyleSheet("background-color: #45475a; border-radius: 10px;")

    def closeEvent(self, event):
        self.metronome.stop()
        event.accept()
