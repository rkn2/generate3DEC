import sys
import numpy as np

path1 = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
sys.path.insert(0, path1) #navigate to function folder

import generate_3decCurrent as gen

#============================================================
#INPUT SCRIPT
# set up experiment
filePath= 'C:/Users/Rebecca Napolitano/Documents/datafiles/Romanbondingcourses/2018_2_15_varyheight/' #slashes must be this direction or it breaks
functionPath = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
outFileName = 'TEST'
iterator = ['stone','brick', 'concrete'] #can iterate over base or load or stone
cycChoice = 'ratio' #can be ratio or loop or test
solveRat = 1e-5
solveRatio = np.log(1e-0/solveRat)/np.log(2)

#______________________________________________________________

# define functions and movies
#options = 'getDisplacement', 'getStress', 'getCracks', 'getFinalCentroid', 'getVolume', 'getInitCentroid',
#           'getInitVert', 'getFinalVert', 'getNeighbors'
# cycle choice is either cycloop or cycratio
functionHandles = ['getDisplacement', 'getStress', 'getCracks', 'getFinalCentroid', 'getVolume', 'getInitCentroid',
                   'getInitVert', 'getFinalVert', 'getNeighbors']

#options = 'makeMoviePlots', 'makeCrackPlots'
movieHandles = ['makeMoviePlots', 'makeCrackPlots']

# list movie plots you want 
#options: 'displacement', 'xdisplacement', 'ydisplacement', 'zdisplacement', 'smaximum', 'sminimum'
plots = ['displacement', 'smaximum']

#______________________________________________________________

# define materials(dens, edge, fixity, hide, ymod, join)
#mortar = material({'dens':2200, 'edge':100, 'hide':True})
stone = gen.material({'dens':2560})
fixedstone = gen.material({'dens':2560,'fixity':'fix'})
brick = gen.material({'dens':2000})
concrete = gen.material({'dens':1800, 'ymod':18e9, 'edge':0.3})
#______________________________________________________________

# pass input variables 
#for loadLocation, it goes bound VALUE range YYY; where YYY can be 'group GROUPNAME', 'x XCOORD y YCOORD z ZCOORD'
#sample of all the variables that can be included
my_experiment = gen.experiment(filePath, functionPath, outFileName, iterator, cycChoice, functionHandles, movieHandles, plots, solveRatio,
                           movieInterval = 10000, numCycLoops = 100, numCycles = 100, arraySize = 3000000, threshold = 0.001)
# define joint materials
mortar_stone = gen.jointMaterial({'jkn':1.0e9, 'jks':1.0e9, 'jfric': 30})

#______________________________________________________________

# add geometries to experiment
my_experiment.addGeometry('base', fixedstone, mortar_stone)
my_experiment.addGeometry('brick', brick, mortar_stone)
#my_experiment.addGeometry('mortar', mortar, mortar_stone)
my_experiment.addGeometry('concrete', concrete, mortar_stone)
my_experiment.addGeometry('stone', stone, mortar_stone)

# write geometries to 3dec file
my_experiment.write3DECFile()