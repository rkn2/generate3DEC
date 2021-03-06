"""
ENSURE THAT THE DENSITIES ARE CORRECT FOR THE DEFORMABLE OBJECTS SUCH AS CONCRETE VS MORTAR VS INFILL

"""

import sys
import glob
import os

path1 = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
sys.path.insert(0, path1) #navigate to function folder

import generate3DECfunc as gen

file_path = 'C:/Users/Rebecca Napolitano/Documents/datafiles/Romanbondingcourses/2017_10_20_simulations/' #where data files are


"""
THE BEGINNING OF THIS FILE IS WHERE TO INPUT THE VARIABLES FOR THE SIMULATION
"""
finalOutput = '2017_10_20_3DEC_FILE.3ddat' #write a name here that your 3dec script will be called
gravity = '0 0 -10 '
# ;m/s2'
densitystone = '2713 '
#units for density ;kg/m3 given by mike granite, cut, rough material editor'
dampLocal = 'true' #use lowercase
facetri = 'false'

jkn1 = '1e9 '
jks1 = '1e9 '
jfric1 = '30 '
#; units are N/m3
numCycles = '10000 '
densitymortar = '1540 ' #; kg/m3 https://www.simetric.co.uk/si_materials.htm
ymod = ' 18e9 '
numCycloops = '10 '
boundload = '-480004.7 '
#dont forget the negative sign
#area of load = 2.785m^2
#20psf from mike = 0.137895 MPa
#total weight = 0.137895MPa * 2.785m^2 = 0.384 E6 N divide by 8 for vertices = 480004.7
densitybrick = '2000 ' #brick wikipedia
densityinfill = '1800 ' #check this with mike
#;source https://www.academia.edu/1214963/The_toughness_of_Imperial_Roman_concrete
arraysize = '1000000 '
#movieInterval = str(int(int(numCycles) * int(numCycloops) / 10))
movieInterval = '10000 '

solveRatio = '4' #remember it goes until the one before this, so if you want 5 make this 6

os.chdir(file_path)

fileHandles_concrete = glob.glob('*_concrete.3ddat')

for file in fileHandles_concrete:
    os.remove(file)
    

function_path = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\' #where function scripts are

# generateFile will always include 'base' first;

#blockList = ['deformable',
#              'mortar',
#              'brick',
#              'stone',
#              'frame',
#              'infill',
#              'loadblock',
#              'outofplane',
#              'sidewall']

blockTypes = []
blockTypes.append('deformable')
#blockTypes.append('mortar')
blockTypes.append('brick')
blockTypes.append('stone')
#blockTypes.append('frame')
#blockTypes.append('infill')
#blockTypes.append('loadblock')
blockTypes.append('outofplane')
#blockTypes.append('sidewall')

blockParams = {} # COMMENT OUT GEOMETRY YOU DO NOT HAVE, TO ADD A NEW TYPE OF MATERIAL, ADD IT HERE AND IN DEF GEN3dec
blockParams['deformable'] = '\ngen edge 100 \ngroup block deformable \nprop mat 2 dens ' + densityinfill + ' ymod ' + ymod + '\n'
#blockParams['mortar'] = '\ngen edge 100 \ngroup block mortar \nprop mat 2 dens ' + densitymortar + ' ymod ' + ymod + '\n'
blockParams['brick'] = '\nprop mat 3 dens ' + densitybrick + '\n'
blockParams['stone'] = '\nprop mat 1 dens ' + densitystone + '\n\nprop jmat 1 jkn ' + jkn1 + ' jks ' + jks1 +  ' jfric ' + jfric1 + '\n'
#blockParams['frame'] = '\n;they are the same as the stone parameters\n'
#blockParams['infill'] = '\n;they are the same as the mortar parameters\n'
#blockParams['loadblock'] = '\n;they are the same as the stone parameters\n'
blockParams['outofplane'] = '\n;they are the same as the stone parameters\n'
#blockParams['sidewall'] = '\n;they are the same as the stone parameters\n'


functions = '\n@setup \n;@normals \n@neighbors \n@initial_centroid \n@initial_vertex \n@getvol \n;@getstoneid \n@movieSetup \n@makeMoviePlots \n@cycloop \n@plot_cracks \n@makeCrackPlots \n@plotCrackPlot \n@displacement \n@final_centroid \n@final_vertex \n@get_stress \n@clearPlots'


# make a list of blockGroup objects
blockGroups = []
for blockType in blockTypes:
    if blockType == 'infill':
        blockGroups.append(gen.infillGroup(blockType,blockParams[blockType])) 
    else:
        blockGroups.append(gen.blockGroup(blockType,blockParams[blockType]))


genFile = gen.generateFile(file_path,blockTypes,blockGroups,
                           finalOutput=finalOutput,
                           gravity=gravity,
                           boundload=boundload,
                           function_path=function_path,
                           numCycloops=numCycloops,
                           numCycles=numCycles,
                           arraysize=arraysize,
                           movieInterval = movieInterval, 
                           dampLocal = dampLocal, 
                           functions = functions, 
                           solveRatio = solveRatio)
# genFile.fileHandles()

# genFile(finalOutput, gravity, densitystone,jkn1, jks1, jfric1, numCycles, densitymortar,ymod,numCycloops,boundload,densitybrick, densityinfill, arraysize, file_path, function_path)

