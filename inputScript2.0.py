import sys
import numpy as np

path1 = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
sys.path.insert(0, path1) #navigate to function folder

import generate_3decCurrent as gen

#============================================================
#INPUT SCRIPT
# set up experiment
filePath= 'C:/Users/Rebecca Napolitano/Documents/datafiles/labWalls/A_simulations/2018_5_10_diffusionMaps/'  
functionPath = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
outFileName = '2018_5_10_Dif_3DEC'
iterator = ['base','load'] #can iterate over base or load or stone ; always put base first for naming conventions, not load
cycChoice = 'ratio' #can be ratio or loop or test
solveRat = 1e-5
solveRatio = np.log(1e-0/solveRat)/np.log(2)

#______________________________________________________________

# define functions and movies
#options = 'getDisplacement', 'getStress', 'getCracks', 'getFinalCentroid', 'getVolume', 'getInitCentroid',
#           'getInitVert', 'getFinalVert', 'getNeighbors', 'getCrackData'
# cycle choice is either cycloop or cycratio
functionHandles = ['getInitVert', 'getFinalVert']

#options = 'makeMoviePlots', 'makeCrackPlots'
movieHandles = []

# list movie plots you want 
#options: 'displacement', 'xdisplacement', 'ydisplacement', 'zdisplacement', 'smaximum', 'sminimum'
plots = []

#______________________________________________________________

# define materials(dens, edge, fixity, hide, ymod, join)
#mortar = material({'dens':2200, 'edge':100, 'hide':True})
fixedstone = gen.material({'dens':2500,'fixity':'fix'})
brick = gen.material({'dens':2508.67})

#______________________________________________________________

#define loads
loadTypes = ['pt'] #can be 'eq','pt', or 'none' right now
#if you choose 'eq' then you need to provide the following: 
#eqDStart, eqDIncrement, eqDEnd for the direction the load will be applied. 0 is x and to the left, 90 is y into the page, etc
#eqDStart = 0 #always in radians
#eqDIncrement = np.pi/2
#eqDEnd = np.pi
#eqDList = list(np.arange(eqDStart, eqDEnd + eqDIncrement, eqDIncrement))
##eqVert, eqFw, eqSStart, eqSIncrement, eqSEnd for the calcuation of the load; eqS is scale of the eq ranging generally from 0 to 0.3g
#eqVertVal = 744
#eqFwVal = 2183.15
#eqSStart = 0
#eqSIncrement = 0.1
#eqSEnd = 0.1
#eqSList = list(np.arange(eqSStart, eqSEnd + eqSIncrement, eqSIncrement)) #cant calculate eqBoundLoad outhere since it will change with each eqS
#if you choose 'pt' then you need to provide the following:
#ptVStart, ptVIncrement, ptVEnd for the value of the load thatwill be applied
ptVStart = -200
ptVIncrement = 100
ptVEnd = 200
ptVList = list(np.arange(ptVStart, ptVEnd + ptVIncrement, ptVIncrement)) 
#ptLList = [] is a list of string locations in the format: range x -1000 1000; can be written in another python script but not here bc too much variation
ptLList = [['x', 'range bid 31'],
            ['y', 'range z 0.55 0.6']]

#______________________________________________________________

# pass input variables 
#for loadLocation, it goes bound VALUE range YYY; where YYY can be 'group GROUPNAME', 'x XCOORD y YCOORD z ZCOORD'
#sample of the variables that can be included see readme for more information
my_experiment = gen.experiment(filePath, functionPath, outFileName, iterator, cycChoice, functionHandles, movieHandles, plots, solveRatio, loadTypes,
                               #eqVert = eqVertVal, eqFw = eqFwVal, eqD = eqDList, eqS = eqSList, 
                               ptV = ptVList, ptL = ptLList,
                               numCycLoops = 1, numCycles = 100, arraySize = 3000000)

# define joint materials
mortar_stone = gen.jointMaterial({'jkn':1e9, 'jks':1e9, 'jfric': 30})

#______________________________________________________________

# add geometries to experiment
my_experiment.addGeometry('base', fixedstone, mortar_stone)
my_experiment.addGeometry('brick', brick, mortar_stone)
#my_experiment.addGeometry('mortar', mortar, mortar_stone)

# write geometries to 3dec file
my_experiment.write3DECFile()