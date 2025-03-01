from PyQt6 import QtWidgets
import cv2
import numpy as np


def reshape_image(image_slices):
  resized_image = cv2.resize(image_slices, (512, 512), interpolation=cv2.INTER_LINEAR)
  rgb_image = np.repeat(resized_image[..., np.newaxis], 3, axis=-1)
  batch_image = rgb_image[np.newaxis, ...]
  return batch_image


def remove_all_children(widget, layout):
  for child in widget.children():
    if isinstance(child, QtWidgets.QWidget):
      layout.removeWidget(child)
      child.deleteLater()


def remove_widget(widget, layout):
  if widget:
    layout.removeWidget(widget)
    widget.deleteLater()
