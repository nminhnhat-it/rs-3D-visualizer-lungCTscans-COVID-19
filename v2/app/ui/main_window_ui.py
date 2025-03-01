from PyQt6 import QtCore, QtGui, QtWidgets
from .widgets.sidebar_ui import Ui_SideBar
from .widgets.functionbar_ui import Ui_FunctionBar
from .widgets.image_viewer_ui import Ui_ImageViewer


class Ui_MainWindow(object):
  def setupUi(self, MainWindow):
    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(896, 704)

    self.menuBar = QtWidgets.QMenuBar(parent=MainWindow)
    self.menuBar.setGeometry(QtCore.QRect(0, 0, 896, 24))
    self.menuBar.setObjectName("menuBar")
    self.menuFile = QtWidgets.QMenu(parent=self.menuBar)
    self.menuFile.setObjectName("menuFile")
    self.menuFile.setTitle("File")
    MainWindow.setMenuBar(self.menuBar)

    self.actionNewWindow = QtGui.QAction(parent=MainWindow)
    self.actionNewWindow.setObjectName("actionNewWindow")
    self.actionNewWindow.setText("New Window")
    self.actionNewWindow.triggered.connect(MainWindow.new_window)

    self.actionOpenFile = QtGui.QAction(parent=MainWindow)
    self.actionOpenFile.setObjectName("actionOpenFile")
    self.actionOpenFile.setText("Open File")
    self.actionOpenFile.triggered.connect(MainWindow.open_file)

    self.menuFile.addAction(self.actionNewWindow)
    self.menuFile.addAction(self.actionOpenFile)
    self.menuBar.addAction(self.menuFile.menuAction())

    self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
    self.centralwidget.setObjectName("centralwidget")

    self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
    self.gridLayout.setContentsMargins(0, 0, 0, 0)
    self.gridLayout.setSpacing(0)
    self.gridLayout.setObjectName("gridLayout")

    self.sidebar = Ui_SideBar(parent=self.centralwidget)
    self.gridLayout.addWidget(self.sidebar, 1, 0, 1, 1)

    self.functionbar = Ui_FunctionBar(parent=self.centralwidget)
    self.functionbar.setVisible(False)
    self.gridLayout.addWidget(self.functionbar, 0, 0, 1, 2)

    self.imageviewer = Ui_ImageViewer(parent=self.centralwidget)
    self.gridLayout.addWidget(self.imageviewer, 1, 1, 1, 1)

    MainWindow.setCentralWidget(self.centralwidget)

    QtCore.QMetaObject.connectSlotsByName(MainWindow)
