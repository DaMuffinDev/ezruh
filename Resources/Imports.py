from Resources.required_modules import pymodules
pymodules.install(pymodules.presets.resources("imports"))

from PyQt5.QtWidgets import \
    QApplication as App, QWidget as Widget, \
    QLabel as Label, QPushButton as Button, \
    QMainWindow as MainWindow, QProgressBar as ProgressBar, \
    QFrame as Frame, QHBoxLayout as HBoxLayout, \
    QVBoxLayout as VBoxLayout

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon as Icon

__all__ = [
    "MainWindow",
    "App",
    "Widget",
    "Label",
    "Button",
    "ProgressBar",
    "Frame",
    "HBoxLayout",
    "VBoxLayout",

    "QSize",
    "QTimer",
    "Qt",

    "Icon"
]