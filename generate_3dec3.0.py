import re
import glob

class material():
    # stores all metadata about a material
    def __init__(self, properties):
        self.properties = properties
        self.idx = None

    def write(self):
        # write mat properties to string;
        propertyString = ''
        for aProperty in self.properties:
            if aProperty == 'edge': 
                propertyString += '\ngen edge ' + str(self.properties[aProperty]) 
        propertyString += '\nprop mat ' + str(self.idx) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for aProperty in self.properties:
            if aProperty != 'edge' and aProperty != 'fixity' and aProperty != 'hide':
                propertyString += ' %s %s '%(aProperty,self.properties[aProperty])
            if aProperty == 'fixity':
                propertyString += '\nfix '
        return propertyString
            

class jointMaterial():
    #stores all metadata about a joint material
    def __init__(self, jointProperties):
        self.jointProperties = jointProperties
        self.jidx = None

    def write(self):
        # write joint properties to string;
        jPropertyString = '\nprop jmat INSERT NUMBER HERE'
        for jointProperty in self.jointProperties:
            jPropertyString += ' %s %s '%(jointProperty,self.jointProperties[jointProperty])
        return jPropertyString

class geometry():
    # holds all the geometry data for a certain type of block
    def __init__(self, label, mat, jmat):
        self.label = label
        self.material = mat
        self.jointMaterial = jmat

class experiment():
    # holds all the necessary objects to run an experiment
    def __init__(self, filePath, functionPath, outFileName, iterator, functionHandles, movieHandles, plots, load_min = 0, load_max = 0, load_iterator = 0, 
                 movieInterval = 0, dampBool = None, faceTriBool = None, numCycLoops = 0, numCycles = 0, solveRatio = 0, arraySize = 0, threshold = 0):
        self.filePath = filePath
        self.functionPath = functionPath
        self.geometries = []
        self.materials = []
        self.jointMaterials = []
        self.outFileName = outFileName
        self.iterator = iterator
        self.functionHandles = functionHandles
        self.movieHandles = movieHandles
        self.plots = plots
        self.load_min = load_min
        self.load_max = load_max
        self.load_iterator = load_iterator
        self.movieInterval = movieInterval
        self.dampBool = dampBool
        self.faceTriBool = faceTriBool
        self.numCycLoops = numCycLoops
        self.numCycles = numCycles
        self.solveRatio = solveRatio
        self.arraySize = arraySize
        self.threshold = threshold

    # used to bring inputs into specific formats
    def addGeometry(self, label, mat, jmat):
        # create a new geometry object
        newGeo = geometry(label, mat, jmat)
        # only add it to the list if not already present
        if newGeo not in self.geometries:
            self.geometries.append(newGeo)
        if mat not in self.materials:
            self.materials.append(mat)
        if jmat not in self.jointMaterials:
            self.jointMaterials.append(jmat)

    def writeParams(self, outfile, geom):
        outfile.write('\n;--------------------------------%s PARAMETERS-----------------------------------\n'%geom.label.upper())
        outfile.write('\n')
        outfile.write(geom.material.write())
        outfile.write('\n')
        outfile.write(geom.jointMaterial.write())
        outfile.write('\ngroup range block ' + geom.label + '\nhide' )

    #used in writegeometrybymat
    def writeGeometry(self,j,outfile, geom):
        #figures out an index for iteration based on the iterator and the geometry
        if self.iterator == 'base' and geom.label == 'base':
            index = j
        else:
            index = 0

        #uses information about the iterator to make the index
        openBlock = open(self.fileHandles[geom.label][index])
        dataBlock = openBlock.read()
        openBlock.close()
        outfile.write('\n;--------------------------------%s GEOMETRY-----------------------------------\n'%geom.label.upper())
        outfile.write(dataBlock)

    #used in write3decfile to write geometry for materials
    def writeGeomandParam(self, i, outfile):
        #this writes geometry for any deformable materials
        for geom in self.geometries:
            keys = geom.material.properties.keys()
            if 'edge' in keys:
                self.writeGeometry(i, outfile, geom)
                self.writeParams(outfile, geom)

        #this writes geometry for any rigid materials
        for geom in self.geometries:
            keys = geom.material.properties.keys()
            if 'edge' not in keys:
                self.writeGeometry(i, outfile, geom)
                self.writeParams(outfile, geom)
   
    #this function is called by write3decfile to assign material properties
    def assignMat(self, outfile):
        outfile.write('\n;--------------------------------ASSIGN MATERIALS-----------------------------------\n')  
        outfile.write('\nhide')
        for geom in self.geometries:
            outfile.write('\nshow range group ' + geom.label)
            outfile.write('\nchange mat ' + str(geom.material.idx))
            outfile.write('\nchange jmat ' + str(geom.jointMaterial.jidx))
            outfile.write('\nhide')
        outfile.write('\nshow')
            
    #this function is called by write3decfile to hide blocks that need to be hidden
    def hideBlocks(self, outfile):
        for geom in self.geometries:
            keys = geom.material.properties.keys()
            if 'hide' in keys:
                outfile.write('\n\n;--------------------------------HIDING SELECTED BLOCKS------------------------------------')
                outfile.write('\nhide range group ' + geom.label)
    
    #This is used in write functions
    def writemakeMoviePlots(self, outfile):
        moviePlotsOpen = open(self.filePath + 'makeMoviePlots.txt', 'w+')
        moviePlotsOpen.write('\n;This is a function to create movie plots.')
        moviePlotsOpen.write('\ndef makeMoviePlots \n\tcommand ')
        #takes the place of movie_setup_func
        moviePlotsOpen.write('\n\t\tplot set movieactive false \n\t\tplotset movieprefix @runName' + 
                             '\n\t\tplot set moviein @movieInterval \n\t\tplot set index 1' + 
                             '\n\t\tplot set movieactive true')
        
        #takes the place of makemovieplots       
        for plotName in plots: 
            if plotName == 'displacement' or plotName == 'xdisplacement' or plotName == 'ydisplacement' or plotName == 'zdisplacement':
                specifier = 'contour '
            if plotName == 'smaximum' or plotName == 'sminimum':
                specifier = 'blockcontour '                
            moviePlotsOpen.write('\n\t\tplot create \n\t\tplot rename ' + plotName + 
                                 '\n\t\tplot clear \n\t\tplot add ' + specifier + plotName)
        moviePlotsOpen.write('\n\tendcomand \nend')
        moviePlotsOpen.close()
        moviePlotFile = open(self.filePath + 'makeMoviePlots.txt', 'r')
        moviePlotText = moviePlotFile.read()
        moviePlotFile.close()
        outfile.write(moviePlotText)            
        
    def writemakeCrackPlots(self, outfile):
        crackPlotsOpen = open(self.filePath + 'makeCrackPlots.txt', 'w+')
        crackPlotsOpen.write('\n;This is a function to create crack plots.')
        crackPlotsOpen.write('\ndef makeCrackPlots \n\tcommand ')
        crackPlots = ['ndisplacement', 'nstress']
        for crackPlot in crackPlots:
            #rewrite as if statement if you ever have any other specifiers
            specifier = 'jointcontour '
            crackPlotsOpen.write('\n\t\tplot create \n\t\tplot rename ' + crackPlot + 
                                 '\n\t\tplot add ' + specifier + crackPlot)
        crackPlotsOpen.write('\n\tendcommand') 
        for crackPlot in crackPlots:
            crackPlotsOpen.write('\n\t' + crackPlot + 'File = saveCyc_' + crackPlot + '.png')
            crackPlotsOpen.write('\n\tcommand \n\t\tplot bitmap plot ' + crackPlot + 
                             ' filename ' + '@' + crackPlot + 'File \n\tencommand \nend')     
        crackPlotsOpen.close()
        crackPlotFile = open(self.filePath + 'makeCrackPlots.txt', 'r')
        crackPlotText = crackPlotFile.read()
        crackPlotFile.close()
        outfile.write(crackPlotText)    
        
        
    def writeMovieFunctions(self,outfile):
        #make sure you write the individual functions like makeMoviePlots, makeCrackPlots, clearPlots, plotCrackPlots
        if 'makeMoviePlots' in self.movieHandles:
            print('makemovieplots is here')
            self.writemakeMoviePlots(outfile)
            
        #add other specialty functions
        if 'makeCrackPlots' in self.movieHandles:
            print('makecrackplots is here')
            self.writemakeCrackPlots(outfile)
        
        
    def writeClearPlots(self, outfile):
        clearPlotsOpen = open(self.filePath + 'clearPlots.txt', 'w+')
        clearPlotsOpen.write('\n;this is a function that destroys all plots')
        clearPlotsOpen.write('\ndef clearPlots \n\tcommmand')
        for function in self.functionHandles:
            function = function
            clearPlotsOpen.write('\n\t\tplot destroy plot ' + function)
        for function in self.movieHandles:
            clearPlotsOpen.write('\n\t\tplot destroy plot ' + function)
        clearPlotsOpen.write('\n\tendcommand \nend')
        
        clearPlotsOpen.close()
        clearPlotsFile = open(self.filePath + 'clearPlots.txt', 'r')
        clearPlotsText = clearPlotsFile.read()
        clearPlotsFile.close()
        outfile.write(clearPlotsText)
    
    #this function is called by write3decfile to write all the functions and their calls
    def writeFunctions(self, outfile):
     
        functionCall = '\n'
        #functionList = {}
        outfile.write('\n;;--------------------------------FUNCTIONS------------------------------------\n')
        
        self.writeMovieFunctions(outfile)
       
        for function in self.functionHandles:
            functionFull = functionPath + function + '.txt'
            openFunction = open(functionFull, 'r')
            dataFunction = openFunction.read()
            openFunction.close()
            outfile.write('\n')
            outfile.write(dataFunction)   
            functionCall += '@' + function + '\n'
            #function = function.replace('.txt', '') 
            #functionList[function] = keyNumber
        #defining setup variables
        overwrites = {'movieInterval' : self.movieInterval, 'dampBool': self.dampBool, 'faceTriBool' : self.faceTriBool, 
                      'numCycLoops' : self.numCycLoops, 'numCycles' : self.numCycles, 'solveRatio' : self.solveRatio, 
                      'arraySize' : self.arraySize, 'threshold' : self.threshold}
        #start writing setup
        setupFull = functionPath + 'SETUP_setup.txt'    
        openSetup = open(setupFull, 'r')
        dataSetup = openSetup.read()
        openSetup.close()
        outfile.write('\n;--------------------------------SETUP------------------------------------\n')
        #WORKING HERE!!!!!!!!!!!!!!!!!!!!!!!!!
        for overwrite in overwrites:
            insertString = 'insert' + overwrite
            dataSetup = re.sub(insertString, str(overwrites[overwrite]), dataSetup)
        #filePath = self.filePath
        #filePath = re.sub("\\", replace, filePath)
        #print(filePath)
        #dataSetup = re.sub(r'\binsertpath\b',filePath, dataSetup)
        #dataSetup = re.sub('insertrunName', self.fileName, dataSetup)
        #dont forget to do saveCyc = 'cycstate' + fileName
        outfile.write('\n' + dataSetup)
        if self.movieHandles != []:
            self.writeClearPlots(outfile)
        outfile.write('\n;--------------------------------FUNCTION CALLS------------------------------------\n')
        outfile.write('\n@setup')
        outfile.write(functionCall)
        if self.movieHandles != []:
            outfile.write('\n@clearPlots')
        
        
    #used in write3decfile to grab all of the pertinent files
    def getFileHandles(self):
        self.fileHandles = {}
        #gets all the fileHandles
        for geom in self.geometries:
            self.fileHandles[geom.label] = glob.glob(self.filePath + '*_' + geom.label + '.3ddat')
            #SHOULD PROBABLY INCLUDE SOME ERROR CHECKING

    #used in write3dec file to change index and insertion for filename based on iterator
    def setupSimulationBase(self,j):
        self.runIndex = j
        self.insertion = ''

    #used in write3dec file to change index and insertion for filename based on iterator
    def setupSimulationLoad(self, j):
        self.runIndex = 0
        self.insertion = '_' + str(j*self.load_iterator)

    #main function
    def write3DECFile(self):
        # first assign indices to unique materials
        for i in range(len(self.materials)):
            self.materials[i].idx = i + 1
        for k in range(len(self.jointMaterials)):
            self.jointMaterials[k].jidx = k + 1

        # next we need to get a list of the files so we can call them for writing
        # so lets make a list called fileHandles, we can do that in a different function above
        self.getFileHandles()

        if iterator == 'base':
            self.numSimulations = len(self.fileHandles['base'])
        elif iterator == 'load':
            self.numSimulations = int((self.load_max-self.load_min)/self.load_iterator)
        else:
            print('Iterator must be either base or load')

        for j in range(self.numSimulations):
            print ('This is iteration number ' + str(j))
            if iterator == 'base':
                self.setupSimulationBase(j)
            if iterator == 'load':
                self.setupSimulationLoad(j)
            self.fileName = self.fileHandles['base'][self.runIndex]
            self.fileName = self.fileName.replace('.3ddat', '').replace(self.filePath, '').replace('_base','')
            writeFile = self.fileName + self.insertion +'.3ddat'
            output = self.filePath + writeFile
            #open the file and writing
            outfile = open(output, 'w+')
            outfile.write('\n;-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            outfile.write('new\n' + ';This is file ' + str(j) + '\n')
            #open the file and write the geometry and parameters
            self.writeGeomandParam(j, outfile)
            
            #assign material properties
            self.assignMat(outfile)
            
            #when last geom and param are written, make sure to hide the blocks that need to be hidden
            self.hideBlocks(outfile)
                        
            #write the functions that can be called
            self.writeFunctions(outfile)
            
            #write the moviefunctions
            
            
            outfile.close()


#============================================================

# set up experiment
filePath= 'C:\\Users\\Rebecca Napolitano\\Documents\\datafiles\\test\\'
functionPath = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'
outFileName = 'TEST_3DEC_INPUT'
iterator = 'load' #can iterate over base or load
#if iterator = 'load' the following parameters need to be specified

# define functions and movies
#options = getDisplacement, getStres, getCracks, getFinalCentroid, getVolume, getInitCentroid,
#           getInitVert, getFinalVert, getNeighbors
functionHandles = ['getstress', 'cycloop', 'getCracks']
#options = 'makeMoviePlots', 'makeCrackPlots'
movieHandles = ['makeMoviePlots', 'makeCrackPlots']

# list movie plots you want 
#options: displacement, xdisplacement, ydisplacement, zdisplacement, smaximum, sminimum
plots = ['displacement', 'smaximum']

# define materials(dens, edge, fixity, hide, ymod)
mortar = material({'dens':2200., 'edge':100., 'hide':True})
stone = material({'dens':2400.})
fixedstone = material({'dens':2400.,'fixity':'fix'})

# pass input variables   
#sample of all the variables that can be included
my_experiment = experiment(filePath, functionPath, outFileName, iterator, functionHandles, movieHandles, plots, load_min = 0., 
                           load_max = 1000., load_iterator = 250., movieInterval = 1000., dampBool = True, faceTriBool = True, 
                           numCycLoops = 10., numCycles = 1000., solveRatio = 5., arraySize = 30000., threshold = 0.001)

# define joint materials
mortar_stone = jointMaterial({'jkn':1.0e9, 'jks':1.0e9, 'jfric': 37.})

# add geometries to experiment
my_experiment.addGeometry('base', fixedstone, mortar_stone)
my_experiment.addGeometry('loadblock', stone, mortar_stone)
my_experiment.addGeometry('mortar', mortar, mortar_stone)
my_experiment.addGeometry('stone', stone, mortar_stone)

# write geometries to 3dec file
my_experiment.write3DECFile()
