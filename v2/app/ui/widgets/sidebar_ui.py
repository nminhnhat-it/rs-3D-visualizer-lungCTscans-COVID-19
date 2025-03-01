from PyQt6.QtCore import QTimer
from PyQt6 import QtCore, QtWidgets, QtGui
from ...utils.utils import remove_all_children


class Ui_SideBar(QtWidgets.QScrollArea):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setMinimumWidth(132)
    self.setMaximumWidth(132)
    self.setObjectName("Ui_SideBar")
    self.setStyleSheet("border: none;")

    self.gridLayout = QtWidgets.QGridLayout(parent=self)
    self.gridLayout.setContentsMargins(0, 0, 0, 0)
    self.gridLayout.setObjectName("gridLayout")

    self.scrollArea = QtWidgets.QScrollArea()
    self.scrollArea.setAutoFillBackground(False)
    self.scrollArea.setStyleSheet("border: none;")
    self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.scrollArea.setObjectName("scrollArea")
    self.scrollArea.setWidgetResizable(True)
    self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

    self.scrollAreaWidgetContents = QtWidgets.QWidget()
    self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
    self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
    self.verticalLayout.setContentsMargins(0, 0, 0, 0)
    self.verticalLayout.setSpacing(0)
    self.verticalLayout.setObjectName("verticalLayout")

    label = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
    label.setText("You have not open any files")
    label.setObjectName("label")
    label.setMinimumHeight(50)
    label.setWordWrap(True)
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
    self.verticalLayout.addWidget(label)

    pushButton = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
    pushButton.setObjectName("openFileButton")
    pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
    pushButton.setText("Open File")
    pushButton.clicked.connect(self.choose_file)
    self.verticalLayout.addWidget(pushButton)

    spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
    self.verticalLayout.addItem(spacerItem)

    QtCore.QMetaObject.connectSlotsByName(self)

  def displayFileList(self, file_list):
    self.removeStart()
    for file in file_list:
      pushButton = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents)
      pushButton.setObjectName("pushButton")
      pushButton.setText(file["name"])
      pushButton.setProperty("image", file["image"])
      if "mask" in file:
        pushButton.setProperty("mask", file["mask"])
      pushButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
      pushButton.clicked.connect(lambda _, button=pushButton: self.change_button_color(button))
      pushButton.installEventFilter(self)
      self.verticalLayout.addWidget(pushButton)

    spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
    self.verticalLayout.addItem(spacerItem)
    first_but = self.verticalLayout.itemAt(0).widget()
    first_but.setProperty("clicked", True)
    first_but.setStyleSheet("background-color: rgb(98, 132, 164);")
    self.parent().parent().displayImage(first_but.property("image"), first_but.property("mask"))

  def change_button_color(self, tg_button):
    for button in self.scrollAreaWidgetContents.findChildren(QtWidgets.QPushButton):
      button.setStyleSheet("background-color: rgb(37, 37, 38);")
      button.setProperty("clicked", False)
    tg_button.setStyleSheet(f"background-color: rgb(98, 132, 164);")
    tg_button.setProperty("clicked", True)
    self.parent().parent().displayImage(tg_button.property("image"), tg_button.property("mask"))

  def eventFilter(self, obj, event):
    if isinstance(obj, QtWidgets.QPushButton) and not obj.property("clicked"):
      if event.type() == QtCore.QEvent.Type.Enter:
        obj.setStyleSheet("background-color: rgb(55, 55, 61);")
      elif event.type() == QtCore.QEvent.Type.Leave:
        if not obj.hasFocus():
          obj.setStyleSheet("background-color: rgb(37, 37, 38);")
    return super().eventFilter(obj, event)

  def removeStart(self):
    remove_all_children(self.scrollAreaWidgetContents, self.verticalLayout)
    item = self.verticalLayout.takeAt(0)
    del item

  def choose_file(self):
    self.parent().parent().open_file()
