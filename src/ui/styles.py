
"""
Styles for the Metronome Application.
Defines colors and QSS for the UI.
"""

DARK_BG = "#1e1e2e"
DARK_SEC = "#252536" 
ACCENT = "#89b4fa"  # Catppuccin Blue-ish
TEXT = "#cdd6f4"
SUBTEXT = "#a6adc8"
RED = "#f38ba8"
GREEN = "#a6e3a1"

STYLESHEET = f"""
QMainWindow {{
    background-color: {DARK_BG};
}}

QLabel {{
    color: {TEXT};
    font-family: 'Segoe UI', sans-serif;
}}

QPushButton {{
    background-color: {DARK_SEC};
    color: {TEXT};
    border: 2px solid {ACCENT};
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
    font-size: 14px;
}}

QPushButton:hover {{
    background-color: {ACCENT};
    color: {DARK_BG};
}}

QPushButton:pressed {{
    background-color: {GREEN};
    border-color: {GREEN};
    color: {DARK_BG};
}}

QSlider::groove:horizontal {{
    border: 1px solid {DARK_SEC};
    height: 8px;
    background: {DARK_SEC};
    margin: 2px 0;
    border-radius: 4px;
}}

QSlider::handle:horizontal {{
    background: {ACCENT};
    border: 1px solid {ACCENT};
    width: 18px;
    height: 18px;
    margin: -5px 0;
    border-radius: 9px;
}}

QComboBox {{
    background-color: {DARK_SEC};
    color: {TEXT};
    border: 1px solid {ACCENT};
    border-radius: 5px;
    padding: 5px;
}}

QComboBox::drop-down {{
    border: 0px;
}}

"""
