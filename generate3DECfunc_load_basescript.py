"""
ENSURE THAT THE DENSITIES ARE CORRECT FOR THE DEFORMABLE OBJECTS SUCH AS CONCRETE VS MORTAR VS INFILL

"""

import sys
#import glob
import os
import math

path1 = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
sys.path.insert(0, path1) #navigate to function folder

import generate3DECfunc as gen

file_path = 'C:/Users/Rebecca Napolitano/Documents/datafiles/Romanbondingcourses/2017_11_15_lowfric_persistent/bc/' #where data files are


"""
THE BEGINNING OF THIS FILE IS WHERE TO INPUT THE VARIABLES FOR THE SIMULATION
"""
finalOutput = '2017_11_16_bc_jfric30_persistent_3DEC_FILE.3ddat' #write a name here that your 3dec script will be called
gravity = '0 0 -10 '
# ;m/s2
densitystone = '2560 '
# kg/m3 medium density limestone http://www.natural-stone.com/limestone.html
dampLocal = 'true' #use lowercase
facetri = 'true'

jkn1 = '1e9 ' #lemos pronaos
jks1 = '1e9 ' #lemos pronaos
jfric1 = '30 ' #where did this come from?
#; units are N/m3
numCycles = '10000 '
densitymortar = '1540 ' #; kg/m3 https://www.simetric.co.uk/si_materials.htm
ymod = ' 18e9 '
#jcoh = '0.375e6 '
# n/m2 Sarhosis et al (2014) Identification of material parameters for low bond strength masonry table 3
#jten = '0.10e6 '
# n/m2 Sarhosis et al (2014) Identification of material parameters for low bond strength masonry table 3
#jfric2 = '36.8 '
# degrees Sarhosis et al (2014) Identification of material parameters for low bond strength masonry table 3
#jkn2 = '25e9 '
# n/m2 Sarhosis et al (2014) Identification of material parameters for low bond strength masonry table 3
#jks2 = '1.1e10 '
#jkn/2.3 n/m2 Sarhosis et al (2014) Identification of material parameters for low bond strength masonry table 3


numCycloops = '10 '
boundload = '-480004.7 '
maxLoad = 1000 #N
interval = 500 #N
#dont forget the negative sign
#area of load = 2.785m^2
#20psf from mike = 0.137895 MPa
#total weight = 0.137895MPa * 2.785m^2 = 0.384 E6 N divide by 8 for vertices = 480004.7
densitybrick = '2000 ' #brick wikipedia and sarhosis paper: http://www.sciencedirect.com/science/article/pii/S014102961400755X#f0005
densityinfill = '1800 ' #check this with mike
#;source https://www.academia.edu/1214963/The_toughness_of_Imperial_Roman_concrete
arraysize = '1000000 '
#movieInterval = str(int(int(numCycles) * int(numCycloops) / 10))
movieInterval = '10000 '

endRatio = -6

#solveRatio = str(math.ceil((math.log10(math.pow(1,-1)/math.pow(1,endRatio)/math.log10(2)))))
solveRatio = ' 18' #remember it goes until the one before this, so if you want 5 make this 6 HARDCODED

os.chdir(file_path)

#fileHandles_concrete = glob.glob('*_concrete.3ddat')

#for file in fileHandles_concrete:
#    os.remove(file)
#    

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
#blockTypes.append('deformable')
blockTypes.append('concrete')
#blockTypes.append('mortar')
blockTypes.append('brick')
blockTypes.append('stone')
#blockTypes.append('frame')
#blockTypes.append('infill')
#blockTypes.append('loadblock')
#blockTypes.append('outofplane')
#blockTypes.append('sidewall')





blockParams = {} # COMMENT OUT GEOMETRY YOU DO NOT HAVE, TO ADD A NEW TYPE OF MATERIAL, ADD IT HERE AND IN DEF GEN3dec
#blockParams['deformable'] = '\ngen edge 0.3 \ngroup block deformable \nprop mat 2 dens ' + densityinfill + ' ymod ' + ymod + '\n'
blockParams['concrete'] = '\ngen edge 0.3 \ngroup block concrete \nprop mat 2 dens ' + densityinfill + ' ymod ' + ymod  #'\nprop jmat 2 jkn ' + jkn2 + ' jks ' + jks2 + ' jfric ' + jfric2 + ' jcoh ' + jcoh + ' jten ' + jten + '\n'
#blockParams['mortar'] = '\ngen edge 100 \ngroup block mortar \nprop mat 2 dens ' + densitymortar + ' ymod ' + ymod + '\n'
blockParams['brick'] = '\nprop mat 3 dens ' + densitybrick + '\n'
blockParams['stone'] = '\nprop mat 1 dens ' + densitystone + '\n\nprop jmat 1 jkn ' + jkn1 + ' jks ' + jks1 +  ' jfric ' + jfric1 + '\n'
#blockParams['frame'] = '\n;they are the same as the stone parameters\n'
#blockParams['infill'] = '\n;they are the same as the mortar parameters\n'
#blockParams['loadblock'] = '\n;they are the same as the stone parameters\n'
#blockParams['outofplane'] = '\n;they are the same as the stone parameters\n'
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
                           solveRatio = solveRatio, 
                           facetri = facetri, 
                           maxLoad = maxLoad, 
                           interval = interval)
# genFile.fileHandles()

# genFile(finalOutput, gravity, densitystone,jkn1, jks1, jfric1, numCycles, densitymortar,ymod,numCycloops,boundload,densitybrick, densityinfill, arraysize, file_path, function_path)

