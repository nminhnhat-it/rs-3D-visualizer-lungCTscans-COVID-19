import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtCore import QSettings, QSize, QPoint

from src.windows.main_window import MainWindow


class App(QApplication):
  def __init__(self, argv):
    super().__init__(argv)
    self.setWindowIcon(QIcon("assets/images/app_icon.png"))
    self.load_settings()
    self.main_window = MainWindow(self.settings)
    self.main_window.show()

  def load_settings(self):
    self.settings = QSettings("CTU", "Lung CT Scan Viewer")

    if not self.settings.contains("window/size"):
      self.settings.setValue("window/size", QSize(1024, 768))

    if not self.settings.contains("window/position"):
      x, y = self.getCenterPos()
      self.settings.setValue("window/position", QPoint(x, y))

  def getCenterPos(self):
    screen_geometry = QApplication.primaryScreen().geometry()
    size = self.settings.value("window/size")
    center_x = (screen_geometry.width() - size.width()) // 2
    center_y = (screen_geometry.height() - size.height()) // 2
    return center_x, center_y
