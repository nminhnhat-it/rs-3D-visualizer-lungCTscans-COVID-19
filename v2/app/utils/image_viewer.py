import pyqtgraph as pg
import numpy as np
import cv2
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsSimpleTextItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QRectF


class ImageViewer(pg.ImageView):
  def __init__(self, image, mask_data=None):
    super().__init__()
    self.ui.roiBtn.setVisible(False)
    self.ui.histogram.setVisible(False)
    self.ui.menuBtn.setVisible(False)

    self.image = image
    self.mask_image = mask_data
    self.legend_items = []

  def load_image(self):
    self.image = cv2.resize(self.image, (512, 512), interpolation=cv2.INTER_AREA)
    self.setImage(self.image)
    if self.mask_image is not None:
      self.mask_item = pg.ImageItem()
      self.view.addItem(self.mask_item)

      lut = np.zeros((256, 4), dtype=np.uint8)

      self.mask_descriptions = {
          2: ("Infection Region", (255, 255, 0, 255)),
          1: ("Lung Region", (0, 200, 200, 255)),
      }

      for value, (name, color) in self.mask_descriptions.items():
        lut[value] = color

      self.mask_item.setLookupTable(lut)

      self.mask_item.setImage(self.mask_image, levels=(0, 255))
      self.mask_item.setZValue(1)
      self.mask_item.setOpacity(0.5)

      self.add_legend_overlay()

  def add_legend_overlay(self):

    x_start, y_start = 10, 10
    box_size = 20
    spacing = 30

    for idx, (value, (label, color)) in enumerate(self.mask_descriptions.items()):
      rect = QGraphicsRectItem(QRectF(x_start, y_start + idx * spacing, box_size, box_size))
      rect.setBrush(QColor(*color))
      rect.setPen(pg.mkPen('black', width=1))

      rect.setZValue(2)
      self.scene.addItem(rect)
      self.legend_items.append(rect)

      text = QGraphicsSimpleTextItem(label)
      text.setBrush(QColor(255, 255, 255))
      text.setPos(x_start + box_size + 5, y_start + idx * spacing)

      text.setZValue(2)
      self.scene.addItem(text)
      self.legend_items.append(text)
