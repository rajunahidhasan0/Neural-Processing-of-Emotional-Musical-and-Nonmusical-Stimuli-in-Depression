import nibabel as nb

functional = nb.load('')
anatomical = nb.load('')

print('Functional - ', functional.shape)
print('Anatomical - ', anatomical.shape)

print('Anatomical - ', functional.header)