import gzip
import shutil
import os

for dir in os.listdir(os.getcwd()+'/datasets'):
	for file in os.listdir(os.getcwd()+'/datasets/'+dir):
		if file.endswith('.nii'):
			shutil.move(os.getcwd()+'/datasets/'+dir+'/'+file, os.getcwd()+'/extracted/'+file)