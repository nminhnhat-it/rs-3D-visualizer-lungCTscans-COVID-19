import sys
import numpy as np
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6.QtGui import QGuiApplication, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

from src.ui.ui_main_window import Ui_MainWindow
# from src.ui.ui import Ui_MainWindow


class MainWindow(QMainWindow):
  def __init__(self, settings):
    super(MainWindow, self).__init__()
    self.settings = settings

    self.setWindowTitle("Lung CT Scan Viewer")

    self.resize(self.settings.value("window/size"))
    self.move(self.settings.value("window/position"))

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

  def closeEvent(self, event):
    """Save the window size and position when the window is closed."""
    self.settings.setValue("window/size", self.size())
    self.settings.setValue("window/position", self.pos())
    # self.settings.clear()
    super().closeEvent(event)

  def dragEnterEvent(self, event):
    if event.mimeData().hasUrls():
      event.accept()
    else:
      event.ignore()

  def dropEvent(self, event):
    if event.mimeData().hasUrls():
      file_path = event.mimeData().urls()[0].toLocalFile()

    if file_path.endswith(".png"):
      self.label.setText(f"Loaded file: {file_path}")
      self.displayImageViewer(file_path)

    else:
      self.label.setText("Invalid file")
