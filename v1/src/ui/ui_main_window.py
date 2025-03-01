from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from src.widgets.image_viewer import ImageViewer


class Ui_MainWindow(object):
  def setupUi(self, MainWindow):
    self.label = QLabel("Drag and drop file here", self)
    self.label.setObjectName("label1")
    self.label.setStyleSheet("font-size: 16px;")
    self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self.layout = QVBoxLayout()
    self.layout.addWidget(self.label)

    self.central_widget = QWidget()
    self.central_widget.setLayout(self.layout)
    self.setCentralWidget(self.central_widget)

    self.setAcceptDrops(True)
    self.retranslateUi(MainWindow)

  def displayImageViewer(self, file_path):
    if hasattr(self, 'viewer') and self.viewer is not None:
      self.layout.removeWidget(self.viewer) 
      self.viewer.deleteLater()

    self.viewer = ImageViewer(file_path)
    self.viewer.load_image()  

    self.layout.addWidget(self.viewer)

  def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))