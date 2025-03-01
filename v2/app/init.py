import sys
from PyQt6.QtWidgets import QApplication
from .windows.main_window import MainWindow


def run() -> int:

  app: QApplication = QApplication(sys.argv)

  with open("./resources/style.qss", "r") as file:
    qss = file.read()
    app.setStyleSheet(qss)

  window: MainWindow = MainWindow()
  window.show()
  return sys.exit(app.exec())
