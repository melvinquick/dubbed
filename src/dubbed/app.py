"""
Username generator that never leaves your machine.
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QSizePolicy,
)

from .dubbed import UsernameGenerator
from .yaml_file_handler import YamlFileHandler

config_file = YamlFileHandler("resources/configs/config.yaml")
config = config_file.load_yaml_file()

themes_file = YamlFileHandler("resources/configs/themes.yaml")
themes = themes_file.load_yaml_file()


class Dubbed(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.show()

        # * Set window default settings
        self.setWindowTitle(config["window_title"])
        self.setFixedSize(
            config["window_size"]["width"], config["window_size"]["height"]
        )

        # * Create end user widgets and apply settings to them
        self.generate_username = QPushButton("Generate and Copy Username")
        self.generate_username.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.username = QLabel(
            " ", alignment=Qt.AlignmentFlag.AlignCenter, wordWrap=False
        )
        self.username.setFixedWidth(560)

        self.theme_toggle = QPushButton("Dark")
        self.theme_toggle.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # * Define button connections and/or actions
        self.generate_username.pressed.connect(self.get_username)
        self.generate_username.pressed.connect(self.copy_text)
        self.theme_toggle.pressed.connect(self.toggle_theme)

        # * Create layouts
        page = QHBoxLayout()
        inputs = QVBoxLayout()
        outputs = QHBoxLayout()

        # * Add widgets to layouts
        inputs.addWidget(self.generate_username)
        inputs.addWidget(self.theme_toggle)

        outputs.addWidget(self.username)

        # # * Wrap inputs in a widget and constrain its height
        # inputs_widget = QWidget()
        # inputs_widget.setLayout(inputs)
        # inputs_widget.setMaximumHeight(config["window_size"]["height"])

        # * Setup overall page layout and set default window theme
        page.addLayout(inputs)
        page.addLayout(outputs)

        gui = QWidget()
        gui.setLayout(page)

        self.setCentralWidget(gui)

        self.apply_theme(self.theme_toggle.text().lower())
        self.set_font()

    def get_username(self):
        username = UsernameGenerator().generate_username()
        self.username.setText(username)
        self.set_font_username()

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.username.text())

    def toggle_theme(self):
        if self.theme_toggle.text() == "Dark":
            self.theme_toggle.setText("Light")
            theme = self.theme_toggle.text()
        else:
            self.theme_toggle.setText("Dark")
            theme = self.theme_toggle.text()

        self.apply_theme(theme.lower())

    def apply_theme(self, theme):
        self.main_stylesheet = f"""
            background-color: {themes[theme]["background-color"]};
            color: {themes[theme]["color"]};
            border: {themes[theme]["border"]};
            border-radius: {themes["general"]["border-radius"]};
            padding: {themes["general"]["padding"]};
            """
        self.widget_stylesheet = f"""
            background-color: {themes[theme]["widget-background-color"]};
            """
        self.setStyleSheet(self.main_stylesheet)
        self.username.setStyleSheet(self.widget_stylesheet)
        self.generate_username.setStyleSheet(self.widget_stylesheet)
        self.theme_toggle.setStyleSheet(self.widget_stylesheet)

        (
            self.theme_toggle.setText("Dark")
            if theme == "dark"
            else self.theme_toggle.setText("Light")
        )

    def set_font(self):
        font = QFont("Commit Mono Nerd Font", 9)

        self.setFont(font)
        self.generate_username.setFont(font)
        self.theme_toggle.setFont(font)

    def set_font_username(self):
        min_font_size = 11
        current_font_size = 65
        font = QFont("Commit Mono Nerd Font")

        while current_font_size >= min_font_size:
            font.setPointSize(current_font_size)
            metrics = QFontMetrics(font)

            fits_width = (
                metrics.horizontalAdvance(self.username.text())
                < self.username.width() - 10
            )
            fits_height = metrics.height() <= self.username.height()

            if fits_width and fits_height:
                self.username.setFont(font)
                return

            current_font_size -= 1


def main():
    app = QApplication(sys.argv)
    main_window = Dubbed()  # noqa: F841
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
