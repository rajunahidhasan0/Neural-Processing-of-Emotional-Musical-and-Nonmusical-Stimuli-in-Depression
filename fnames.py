import os

outfile = open('fnames.txt', 'w')
for dir in os.listdir(os.getcwd()+'/extracted'):
	for file in os.listdir(os.getcwd()+'/extracted/'+dir):
		if dir=='anat':
			outfile.write(file.replace('_T1w_defaced.nii', '')+'\n')
