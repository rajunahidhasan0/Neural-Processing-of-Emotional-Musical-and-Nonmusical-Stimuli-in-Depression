import os
import shutil


PATH = 'G:/nhr/fMRI/timeseries'
OUT = 'G:/nhr/fMRI/restructured/'

def mkdir_if_not_exists(path):
	if(not(os.path.exists(path))):
		os.mkdir(path)


for sub in os.listdir(PATH):
    sub_path = PATH + '/' + sub
    for roi in os.listdir(sub_path):
        
        roi_path = sub_path + '/' + roi
        roi_name = roi.split('-', 1)[1]
        roi_name = roi_name.split('-', 1)[1]
        roi_name = roi_name[:-4]
        
        out_roi = OUT + roi_name + '/'
        mkdir_if_not_exists(out_roi)

        src = roi_path
        dst = out_roi + roi
        print(src)
        print(dst, '\n')
        if(not(os.path.exists(dst))):
            shutil.copyfile(src, dst)
        else:
            print('Skipped!')


