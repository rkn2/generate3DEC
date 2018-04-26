import glob
import os
import numpy as np

file_path = 'C:/Users/Rebecca Napolitano/Documents/datafiles/labWalls/A_simulations/2018_4_25_eqL2_settle/test/'

os.chdir(file_path)
fileHandles = glob.glob('*.3ddat')

for fileName in fileHandles:
    if 'settle3' in fileName:
        file = fileName.replace('.3ddat','').replace('settle3A_','') #remove extra characters
        file = np.fromstring(file,sep='_')[:]
        if file[3] == 0 and file[4] == 0 and file[5] == 0:
            print('yay')
        else: 
            if file[3] == file[4] and file[4] == file[5] or file[3] != 0 and file[4] != 0 and file[5] != 0:
                os.remove(fileName) 
                print('removing one')
    if 'settle2' in fileName:
        file = fileName.replace('.3ddat','').replace('settle2A_','') #remove extra characters
        file = np.fromstring(file,sep='_')[:]
        if file[2] == 0 and file[1] == 0: 
            print('yay')
        else:
            if file[2] == file[1] or file[1] != 0 and file[2] != 0:
                os.remove(fileName)
                print('removing one')            
    
    #2389 before, 1363 now.. that's great!