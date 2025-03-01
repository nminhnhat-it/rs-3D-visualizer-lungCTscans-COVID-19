import cv2
import pyqtgraph as pg


class ImageViewer(pg.ImageView):
  def __init__(self, image_path):
    super().__init__()
    self.ui.roiBtn.setVisible(False)
    self.ui.histogram.setVisible(False)
    self.ui.menuBtn.setVisible(False)

    self.image_path = image_path

  def load_image(self):
    image_data = cv2.imread(self.image_path)
    image_data = cv2.rotate(image_data, cv2.ROTATE_90_COUNTERCLOCKWISE)
    self.setImage(image_data)

  def load_nii(self):
    print("Loaded nifty file")
