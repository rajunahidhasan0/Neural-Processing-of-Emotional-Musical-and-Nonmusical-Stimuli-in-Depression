import os
import shutil

for file in os.listdir(os.getcwd()+'/extracted'):
	if 'bold' in file:
		shutil.move(os.getcwd()+'/extracted/'+file, os.getcwd()+'/extracted/func/'+file)
	elif 'T1' in file:
		shutil.move(os.getcwd()+'/extracted/'+file, os.getcwd()+'/extracted/anat/'+file) 