import glob
import os
import numpy as np

file_path = 'C:/Users/Rebecca Napolitano/Documents/datafiles/labWalls/2018_4_25_settlement/'

os.chdir(file_path)
fileHandles = glob.glob('*.3ddat')

for fileName in fileHandles:
    if 'settle3' in fileName:
        file = fileName.replace('.3ddat','').replace('settle3_','') #remove extra characters
        file = np.fromstring(file,sep='_')[:]
        if file[3] == file[4] and file[4] == file[5]:
            os.remove(fileName)
    if 'settle2' in fileName:
        file = fileName.replace('.3ddat','').replace('settle2_','') #remove extra characters
        file = np.fromstring(file,sep='_')[:]
        if file[2] == file[1]:
            os.remove(fileName)
    
    #2384 before, 2208 now.. not much of a difference but still something 