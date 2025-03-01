import nibabel as nib
import numpy as np
import cv2


def to_uint8(data):
  if data.min() == data.max():
    return np.zeros_like(data, dtype=np.uint8)
  data -= data.min()
  data /= data.max()
  data *= 255
  return data.astype(np.uint8)


def load_nii_file(file_path):
  nii_image = nib.load(file_path)
  image_data = nii_image.get_fdata()
  image_slices = [{'name': f'Slice {i + 1}', 'image': np.rot90(to_uint8(image_data[:, :, i]), k=1, axes=(1, 0))} for i in range(image_data.shape[2])]
  num_slice = len(image_slices)
  return (image_slices, num_slice)