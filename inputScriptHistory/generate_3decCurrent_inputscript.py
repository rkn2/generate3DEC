import sys
import numpy as np

path1 = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
sys.path.insert(0, path1) #navigate to function folder

import generate_3decCurrent as gen

#============================================================
#INPUT SCRIPT
# set up experiment
filePath= "C:/Users/Rebecca Napolitano/Documents/datafiles/mike/baptistery/2018/rigid_simplified/existing/" 
functionPath = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
outFileName = 'TEST3_3DEC_INPUT'
iterator = 'base' #can iterate over base or load
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
stone = gen.material({'dens':2400, 'ymod': 1e9, 'edge':100})
fixedstone = gen.material({'dens':2400,'fixity':'fix'})

#______________________________________________________________

# pass input variables 
#for loadLocation, it goes bound VALUE range YYY; where YYY can be 'group GROUPNAME', 'x XCOORD y YCOORD z ZCOORD'
#sample of all the variables that can be included
my_experiment = gen.experiment(filePath, functionPath, outFileName, iterator, cycChoice, functionHandles, movieHandles, plots, solveRatio,
                           load_min = 0, load_max = 1000, load_iterator = 1000, movieInterval = 1000,
                           numCycLoops = 300, numCycles = 1000, arraySize = 3000000, threshold = 0.001, edge = 100, 
                           boundLoad = [], loadLocation = [], loadOrientation = [])
# define joint materials
mortar_stone = gen.jointMaterial({'jkn':1.0e9, 'jks':1.0e9, 'jfric': 37})

#______________________________________________________________

# add geometries to experiment
my_experiment.addGeometry('base', fixedstone, mortar_stone)
my_experiment.addGeometry('loadblock', stone, mortar_stone)
#my_experiment.addGeometry('mortar', mortar, mortar_stone)
my_experiment.addGeometry('stone', stone, mortar_stone)

# write geometries to 3dec file
my_experiment.write3DECFile()