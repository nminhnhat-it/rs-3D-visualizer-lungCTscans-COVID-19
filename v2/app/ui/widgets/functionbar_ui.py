from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QIcon
from ...utils.utils import remove_widget, remove_all_children
from resources import resources


class Ui_FunctionBar(QtWidgets.QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setObjectName("Ui_FunctionBar")
    self.setMaximumSize(QtCore.QSize(16777215, 42))
    self.setStyleSheet("border: none;")

    self.gridLayout = QtWidgets.QGridLayout(self)
    self.gridLayout.setContentsMargins(0, 0, 0, 0)
    self.gridLayout.setSpacing(0)
    self.gridLayout.setObjectName("gridLayout")

    self.scrollArea = QtWidgets.QScrollArea()
    self.scrollArea.setStyleSheet("border: none;")
    self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setObjectName("scrollArea")
    self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

    self.scrollAreaWidgetContents = QtWidgets.QWidget()
    self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
    self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
    self.horizontalLayout.setContentsMargins(12, 5, 12, 5)
    self.horizontalLayout.setSpacing(12)
    self.horizontalLayout.setObjectName("horizontalLayout")

    QtCore.QMetaObject.connectSlotsByName(self)

  def setFileDetail(self, file_path, num_slice):
    self.fileDetail.setText(f'{file_path} (Total slices: {num_slice})')

  def create_func_btns(self):
    self.mask_checkbox = QtWidgets.QCheckBox(parent=self.scrollAreaWidgetContents)
    self.mask_checkbox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.mask_checkbox.setChecked(True)
    self.mask_checkbox.setObjectName("mask_checkbox")
    self.mask_checkbox.stateChanged.connect(self.parent().parent().toggle_mask_visibility)
    self.mask_checkbox.setToolTip("Show or hide segment masks")
    self.mask_checkbox.setIcon(QIcon(":icons/layers.png"))
    self.mask_checkbox.setIconSize(self.mask_checkbox.size())
    self.horizontalLayout.addWidget(self.mask_checkbox)

    show_3d_btn = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
    show_3d_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    show_3d_btn.setObjectName("show_3d_btn")
    show_3d_btn.setIcon(QIcon(":icons/3d-printer.png"))
    show_3d_btn.setIconSize(show_3d_btn.size())
    show_3d_btn.setToolTip("View all slice in 3D")
    self.horizontalLayout.addWidget(show_3d_btn)
    show_3d_btn.clicked.connect(self.parent().parent().view_3d)

    remove_widget(self.start_segment_btn, self.horizontalLayout)

  def reset_func_btns(self):
    remove_all_children(self.scrollAreaWidgetContents, self.horizontalLayout)

    item = self.horizontalLayout.takeAt(0)
    del item

    self.fileDetail = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
    self.horizontalLayout.addWidget(self.fileDetail)

    spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
    self.horizontalLayout.addItem(spacerItem)

    self.start_segment_btn = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
    self.start_segment_btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    self.start_segment_btn.setObjectName("start_segment_btn")
    self.start_segment_btn.setIcon(QIcon(":icons/play-button-arrowhead.png"))
    self.start_segment_btn.setToolTip("Segment all slices")
    self.start_segment_btn.clicked.connect(self.parent().parent().start_segment)
    self.horizontalLayout.addWidget(self.start_segment_btn)
