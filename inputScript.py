import sys
import numpy as np

path1 = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
sys.path.insert(0, path1) #navigate to function folder

import generate_3decCurrent as gen

#============================================================
#INPUT SCRIPT
# set up experiment
filePath = "C:/Users/Rebecca Napolitano/Documents/datafiles/mike/baptistery/2018/all_deform/noMortar/" 
functionPath = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
outFileName = '2018_5_4_NoMortar'
iterator = ['base'] #can iterate over base or load or stone
cycChoice = 'ratio' #can be ratio or loop or test
solveRat = 1e-5
solveRatio = np.log(1e-0/solveRat)/np.log(2)

#______________________________________________________________

# define functions and movies
#options = 'getDisplacement', 'getStress', 'getCracks', 'getFinalCentroid', 'getVolume', 'getInitCentroid',
#           'getInitVert', 'getFinalVert', 'getNeighbors'
# cycle choice is either cycloop or cycratio
functionHandles = ['getDisplacement', 'getStress']

#options = 'makeMoviePlots', 'makeCrackPlots'
movieHandles = ['makeMoviePlots', 'makeCrackPlots']

# list movie plots you want 
#options: 'displacement', 'xdisplacement', 'ydisplacement', 'zdisplacement', 'smaximum', 'sminimum'
plots = ['displacement', 'smaximum']

#______________________________________________________________

# define materials(dens, edge, fixity, hide, ymod, join)
#mortar = material({'dens':2200, 'edge':100, 'hide':True})
stone = material({'dens':2300, 'edge': 100, 'ymod':52e9}) #ymod from https://www.engineeringtoolbox.com/young-modulus-d_417.html
fixedstone = material({'dens':2400,'fixity':'fix'})
loadblock = material({'dens':2300})

#______________________________________________________________

# pass input variables 
#for loadLocation, it goes bound VALUE range YYY; where YYY can be 'group GROUPNAME', 'x XCOORD y YCOORD z ZCOORD'
#sample of all the variables that can be included
my_experiment = experiment(filePath, functionPath, outFileName, iterator, cycChoice, functionHandles, movieHandles, plots, load_min = 0, 
                           load_max = 1000, load_iterator = 1000, movieInterval = 1000,
                           numCycLoops = 10, numCycles = 1000, solveRatio = 5, arraySize = 3000000, threshold = 0.001,
                           boundLoad = [-131200, -146000, -125000], loadLocation = ['group loadblock1', 'group loadblock2', 'group loadblock3'], loadOrientation = ['z','z','z']) 

# define joint materials
mortar_stone = jointMaterial({'jkn':1e10, 'jks':1e10, 'jfric': 37, 'jcoh': 1e-6, 'jten': 0.35e6}) #jcoh and jten from parameters file

#______________________________________________________________

# add geometries to experiment
my_experiment.addGeometry('base', fixedstone, mortar_stone)
my_experiment.addGeometry('loadblock1', loadblock, mortar_stone)
my_experiment.addGeometry('loadblock2', loadblock, mortar_stone)
my_experiment.addGeometry('loadblock3', loadblock, mortar_stone)
my_experiment.addGeometry('stone', stone, mortar_stone)

# write geometries to 3dec file
my_experiment.write3DECFile()