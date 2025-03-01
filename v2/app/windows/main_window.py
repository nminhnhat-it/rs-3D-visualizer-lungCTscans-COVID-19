from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtWidgets import QProgressDialog
from PyQt6.QtWidgets import QApplication
from vedo import Volume, Axes, Plotter
import numpy as np
from ..ui.main_window_ui import Ui_MainWindow
from ..utils.nifty_loader import load_nii_file
from ..utils.image_viewer import ImageViewer
from ..utils.model import build_model, predict_mask


class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.model = build_model((512, 512, 3), 3, "resnet")
    self.model.load_weights("app/AI_models/model.keras")

    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.windowList = []

  def dragEnterEvent(self, event):
    if event.mimeData().hasUrls():
      event.accept()
    else:
      event.ignore()

  def dropEvent(self, event):
    if event.mimeData().hasUrls():
      self.file_path = event.mimeData().urls()[0].toLocalFile()
    self.load_file()

  def load_file(self):
    if self.file_path and self.file_path.endswith(".nii.gz"):
      self.lung_slice_data, self.num_slice = load_nii_file(self.file_path)
      self.ui.sidebar.displayFileList(self.lung_slice_data)
      self.resetFuntionBar()

  def open_file(self):
    dialog = QFileDialog()
    self.file_path, _ = dialog.getOpenFileName(self, "Select a File", ".nii.gz", "NIfTI Files (*.nii.gz)")
    self.load_file()

  def new_window(self):
    new_window = MainWindow()
    new_window.show()
    self.windowList.append(new_window)

  def displayImage(self, data, mask_data=None):
    self.viewer = ImageViewer(data, mask_data)
    self.viewer.load_image()

    self.ui.imageviewer.removeViewer()
    self.ui.imageviewer.gridLayout.addWidget(self.viewer)
    if mask_data is not None:
      self.toggle_mask_visibility()

  def resetFuntionBar(self):
    self.ui.functionbar.setVisible(False)
    self.ui.functionbar.reset_func_btns()
    self.ui.functionbar.setFileDetail(self.file_path, self.num_slice)
    self.ui.functionbar.setVisible(True)

  def view_3d(self):
    self.volume_data = np.stack(self.mask_list, axis=2)
    class_1_mask = (self.volume_data == 1)
    class_2_mask = (self.volume_data == 2)

    volume_class_1 = Volume(class_1_mask.astype(np.uint8)).color('green')
    volume_class_2 = Volume(class_2_mask.astype(np.uint8)).color('yellow')
    plt = Plotter(title='3D Viewer',
                  bg='black',
                  size=(800*2, 600*2),
                  pos=(500, 500))
    plt += volume_class_1
    plt += volume_class_2

    vaxes = Axes(plt, xygrid=False)
    plt.show(__doc__, vaxes, axes=14, viewup='z')

  def toggle_mask_visibility(self):
    if self.ui.functionbar.mask_checkbox.isChecked():
      self.viewer.mask_item.setVisible(True)
    else:
      self.viewer.mask_item.setVisible(False)

  def start_segment(self):
    self.mask_list = []

    total_images = self.num_slice

    progress_dialog = QProgressDialog(
        f"Segmenting {total_images} slices...", "Cancel", 0, total_images, self
    )
    progress_dialog.setWindowTitle("Progress")
    progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
    progress_dialog.setMinimumDuration(0)

    for i in range(0, total_images):
      if progress_dialog.wasCanceled():
        QMessageBox.warning(self, "Canceled", "Segmentation canceled!")
        break

      mask = np.max(predict_mask(self.model, self.lung_slice_data[i]["image"]), axis=2)
      self.lung_slice_data[i]["mask"] = mask
      self.mask_list.append(mask)

      progress_dialog.setValue(i + 1)

    if not progress_dialog.wasCanceled():
      QMessageBox.information(self, "Done", "Segmentation success!")
      self.ui.functionbar.create_func_btns()
      self.ui.sidebar.displayFileList(self.lung_slice_data)
