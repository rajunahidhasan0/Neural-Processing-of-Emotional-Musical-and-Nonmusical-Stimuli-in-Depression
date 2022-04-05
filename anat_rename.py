import os

for file in os.listdir(os.getcwd()+'/extracted/anat'):
	if file.endswith('T1w.nii'):
		os.rename(os.getcwd()+'/extracted/anat/'+file, os.getcwd()+'/extracted/anat/'+file[:13]+'_T1w_defaced.nii')