from PyQt6 import QtCore, QtWidgets, QtGui
from ...utils.utils import remove_all_children


class Ui_ImageViewer(QtWidgets.QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setObjectName("Ui_ImageViewer")
    self.setStyleSheet("background-color: black;")

    self.gridLayout = QtWidgets.QGridLayout(self)
    self.gridLayout.setContentsMargins(0, 0, 0, 0)
    self.gridLayout.setSpacing(0)
    self.gridLayout.setObjectName("gridLayout")

    label = QtWidgets.QLabel(parent=self)
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    self.gridLayout.addWidget(label)

  def removeViewer(self):
    remove_all_children(self, self.gridLayout)
