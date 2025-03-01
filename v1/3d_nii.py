import nibabel as nib
import numpy as np
from vedo import Volume, Axes, Plotter

nifti_file = 'MedSeg Covid Dataset 2/lung_ct_masks.nii.gz'
nifti_img = nib.load(nifti_file)
data = nifti_img.get_fdata()

class_1_mask = (data == 1)
class_2_mask = (data == 2)

volume_class_1 = Volume(class_1_mask.astype(np.uint8)).color('green')
volume_class_2 = Volume(class_2_mask.astype(np.uint8)).color('yellow')

plt = Plotter()
plt += volume_class_1
plt += volume_class_2

vaxes = Axes(plt, xygrid=False)


def show_class_1(obj, evt):
  obj.switch()
  if (obj.status() == 'Lung Off'):
    volume_class_1.alpha(0)
  if (obj.status() == 'Lung On'):
    volume_class_1.alpha(0.1)
  plt.render()


def show_class_2(obj, evt):
  obj.switch()
  if (obj.status() == 'Infection Off'):
    volume_class_2.alpha(0)
  if (obj.status() == 'Infection On'):
    volume_class_2.alpha(2)
  plt.render()


plt.add_button(show_class_1,
               states=('Lung On', 'Lung Off'),
               c=('w', 'w'),
               bc=('green4', 'red4'),
               pos=(0.5, 0.1),)
plt.add_button(show_class_2,
               states=('Infection On', 'Infection Off'),
               c=('w', 'w'),
               bc=('green4', 'red4'),
               pos=(0.7, 0.1),)

plt.show(__doc__, vaxes, axes=14, viewup='z')
