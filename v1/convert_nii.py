import os
import re
import numpy as np
import nibabel as nib
from imageio import imread

png_dir = "MedSeg Covid Dataset 2/lung_ct_masks"


def extract_slice_number(filename):
  match = re.search(r"_(\d+)\.png", filename)
  return int(match.group(1)) if match else None


png_files = sorted(
    [f for f in os.listdir(png_dir) if f.endswith(".png")], key=extract_slice_number
)

slices = []
for png_file in png_files:
  img = imread(os.path.join(png_dir, png_file))
  slices.append(img)

volume_data = np.stack(slices, axis=-1)

nifti_img = nib.Nifti1Image(volume_data, affine=np.eye(4))

output_nifti_file = "lung_ct_masks.nii.gz"
nib.save(nifti_img, output_nifti_file)
print(f"Saved NIfTI file as {output_nifti_file}")
