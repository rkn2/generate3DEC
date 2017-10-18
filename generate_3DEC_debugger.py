#script stuff
import sys
import glob
import os
import re


path1 = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
sys.path.insert(0, path1) #navigate to function folder

import generate3DECfunc_debugger as gen

file_path = 'C:/Users/Rebecca Napolitano/Documents/datafiles/Romanbondingcourses/2017_10_16_simulations/' #where data files are
finalOutput = 'testy123_3DEC_FILE.3ddat'

blockTypes = []
blockTypes.append('deformable')
#blockTypes.append('mortar')
blockTypes.append('brick')
blockTypes.append('stone')
#blockTypes.append('frame')
#blockTypes.append('infill')
#blockTypes.append('loadblock')
blockTypes.append('outofplane')

blockGroups = []
for blockType in blockTypes:
    blockGroups.append(gen.blockGroup(blockType)


genFile = gen.generateFile(file_path,blockTypes,blockGroups, finalOutput=finalOutput)

