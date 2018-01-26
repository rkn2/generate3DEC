# currently this makes simulation suites where the simulations are comprised of 
#1) different loads to the same area
#2) different bases to simulate settlement
# currently this 

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
        
        #join before any thing else happens
        for aProperty in self.properties:
            if aProperty == 'join':
                propertyString += '\njoin '
        for aProperty in self.properties:
            if aProperty == 'edge': 
                propertyString += '\ngen edge ' + str(self.properties[aProperty]) 
        propertyString += '\nprop mat ' + str(self.idx) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for aProperty in self.properties:
            if aProperty != 'edge' and aProperty != 'fixity' and aProperty != 'hide' and aProperty !='join':
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
        jPropertyString = '\nprop jmat ' + str(self.jidx)
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
    def __init__(self, filePath, functionPath, outFileName, iterator, cycChoice, functionHandles, movieHandles, plots, load_min = 0, load_max = 0, load_iterator = 0, 
                 movieInterval = 0, numCycLoops = 0, numCycles = 0, solveRatio = 0, arraySize = 0, threshold = 0,
                 boundLoad = 0, loadLocation = None, loadOrientation = None):
        self.filePath = filePath
        self.functionPath = functionPath
        self.geometries = []
        self.materials = []
        self.jointMaterials = []
        self.outFileName = outFileName
        self.iterator = iterator
        self.cycChoice = cycChoice
        self.functionHandles = functionHandles
        self.movieHandles = movieHandles
        self.plots = plots
        self.load_min = load_min
        self.load_max = load_max
        self.load_iterator = load_iterator
        self.movieInterval = movieInterval
        self.numCycLoops = numCycLoops
        self.numCycles = numCycles
        self.solveRatio = solveRatio
        self.arraySize = arraySize
        self.threshold = threshold
        self.boundLoad = boundLoad
        self.loadLocation = loadLocation
        self.loadOrientation = loadOrientation
        

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
        outfile.write('\ngroup block ' + geom.label + '\nhide' )

    #used in writegeometrybymat
    def writeGeometry(self,j,outfile, geom):
        #figures out an index for iteration based on the iterator and the geometry
        if self.iterator == 'base' and geom.label == 'base':
            index = j 
        elif self.iterator == 'stone' and geom.label == 'stone':
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
        outfile.write('\ngrav 0 0 -10')
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
                print('hiding %s'%geom.label.upper())
                outfile.write('\n\n;--------------------------------HIDING SELECTED BLOCKS------------------------------------')
                outfile.write('\nhide range group ' + geom.label)
    
    #this function is called by write3decfile to load blocks
    def loadBlocks(self, outfile):
        if self.boundLoad != 0 and self.loadLocation != None:
            outfile.write('\n\n;--------------------------------LOADING BLOCKS------------------------------------')
            if len(self.boundLoad) != len(self.loadLocation):
                print('Differnet number of loads and positions')
            numberLoads = len(self.boundLoad)
            loadIndex = 0
            while loadIndex < numberLoads:
                outfile.write('\nbound ' + str(self.loadOrientation[loadIndex]) + 'load ' + str(self.boundLoad[loadIndex]) +' range ' + str(self.loadLocation[loadIndex]))
                loadIndex += 1
    
    #This is used in write functions
    def writemakeMoviePlots(self, outfile):
        moviePlotsOpen = open(self.filePath + 'makeMoviePlots.txt', 'w+')
        moviePlotsOpen.write('\n;This is a function to create movie plots.')
        moviePlotsOpen.write('\ndef makeMoviePlots \n\tcommand ')
        #takes the place of movie_setup_func
        moviePlotsOpen.write('\n\t\tplot set movieactive false ;\n\t\tplot set movieprefix @runName' + 
                             ';\n\t\tplot set moviein @movieInterval ;\n\t\tplot set index 1' + 
                             ';\n\t\tplot set movieactive')
        
        #takes the place of makemovieplots       
        for plotName in self.plots: 
            if plotName == 'displacement' or plotName == 'xdisplacement' or plotName == 'ydisplacement' or plotName == 'zdisplacement':
                specifier = 'contour '
            if plotName == 'smaximum' or plotName == 'sminimum':
                specifier = 'blockcontour '                
            moviePlotsOpen.write('\n\t\tplot create \n\t\tplot rename ' + plotName + 
                                 '\n\t\tplot clear \n\t\tplot add ' + specifier + plotName)
        moviePlotsOpen.write('\n\tendcommand \nend')
        moviePlotsOpen.close()
        moviePlotFile = open(self.filePath + 'makeMoviePlots.txt', 'r')
        moviePlotText = moviePlotFile.read()
        moviePlotFile.close()
        outfile.write(moviePlotText)            
        
    def writemakeCrackPlots(self, outfile):
        crackPlotsOpen = open(self.filePath + 'makeCrackPlots.txt', 'w+')
        crackPlotsOpen.write('\n;This is a function to create crack plots.')
        crackPlotsOpen.write('\ndef makeCrackPlots \n\tcommand ')
        self.crackPlots = ['ndisplacement', 'nstress']
        for crackPlot in self.crackPlots:
            #rewrite as if statement if you ever have any other specifiers
            specifier = 'jointcontour '
            crackPlotsOpen.write('\n\t\tplot create \n\t\tplot rename ' + crackPlot + 
                                 '\n\t\tplot add ' + specifier + crackPlot)
        crackPlotsOpen.write('\n\tendcommand') 
        for crackPlot in self.crackPlots:
            crackPlotsOpen.write('\n\t' + crackPlot + 'File = saveCyc + "_' + crackPlot + '.png"')
            crackPlotsOpen.write('\n\tcommand \n\t\tplot bitmap plot ' + crackPlot + 
                             ' filename ' + '@' + crackPlot + 'File \n\tendcommand')
        crackPlotsOpen.write('\nend')     
        crackPlotsOpen.close()
        crackPlotFile = open(self.filePath + 'makeCrackPlots.txt', 'r')
        crackPlotText = crackPlotFile.read()
        crackPlotFile.close()
        outfile.write(crackPlotText)    
        
    #called in writefunctions    
    def writeMovieFunctions(self,outfile):
        #make sure you write the individual functions like makeMoviePlots, makeCrackPlots, clearPlots, plotCrackPlots
        if 'makeMoviePlots' in self.movieHandles:
            self.writemakeMoviePlots(outfile)
            
        #add other specialty functions
        if 'makeCrackPlots' in self.movieHandles:
            self.writemakeCrackPlots(outfile)
        
    #called in writefunctions    
    def writeClearPlots(self, outfile):
        clearPlotsOpen = open(self.filePath + 'clearPlots.txt', 'w+')
        clearPlotsOpen.write('\n;this is a function that destroys all plots')
        clearPlotsOpen.write('\ndef clearPlots \n\tcommand')
        for plot in self.plots:
            clearPlotsOpen.write('\n\t\tplot destroy plot ' + plot)
        if 'makeCrackPlots' in self.movieHandles:
            for plot in self.crackPlots:
                clearPlotsOpen.write('\n\t\tplot destroy plot ' + plot)
        clearPlotsOpen.write('\n\tendcommand \nend')
        
        clearPlotsOpen.close()
        clearPlotsFile = open(self.filePath + 'clearPlots.txt', 'r')
        clearPlotsText = clearPlotsFile.read()
        clearPlotsFile.close()
        outfile.write(clearPlotsText)
    
    #called in writefunctions    
    def writeFuncCall(self,outfile):
        funcList = []
        funcList.append('setup')
        for eachHandle in self.functionHandles:
            funcList.append(eachHandle)
        for eachHandle in self.movieHandles:
            funcList.append(eachHandle)            
            
        orderedList = ['setup', 'getVolume','getInitCentroid', 'getInitVert', 'getNeighbors', 'makeMoviePlots', 'cycRatio',
                       'cycLoop', 'getStress', 'getDisplacement', 'getFinalCentroid', 'getFinalVert', 'getCracks', 'makeCrackPlots', 'clearPlots']    

        funcDict = {}
        for entry in funcList:
            value = orderedList.index(entry)
            if entry == 'getCracks':
                entry = 'getCracks(' + str(self.threshold) + ')'
            funcDict[entry] = value
        #add clearplots only if there are movies to clear
        if self.movieHandles != []:   
            value = orderedList.index('clearPlots')
            funcDict['clearPlots'] = value
        #add cycle to the Dictionary based on choice
        if self.cycChoice == 'loop':
            value = orderedList.index('cycLoop')
            funcDict['cycLoop'] = value
        if self.cycChoice == 'ratio':
            value = orderedList.index('cycRatio')
            funcDict['cycRatio'] = value
            
        funcCall = []
        results = sorted(funcDict.items(), key = lambda x: x[1])
        for entry in results:
            entryString = '\n@' + entry[0]
            funcCall.append(entryString)
        return(funcCall)
    
    #this function is called by writeFunctions to generate the setup function
    def setupFunction(self, outfile, writeFile):
        #defining setup variables
        overwrites = {'movieInterval' : self.movieInterval, 
                      'numCycLoops' : self.numCycLoops, 'numCycles' : self.numCycles, 'solveRatio' : self.solveRatio, 
                      'threshold' : self.threshold}
        #start writing setup
        setupFull = self.functionPath + 'SETUP_setup.txt'    
        openSetup = open(setupFull, 'r')
        dataSetup = openSetup.read()
        openSetup.close()
        outfile.write('\n;--------------------------------SETUP------------------------------------\n')
        for overwrite in overwrites:
            insertString = 'insert' + overwrite
            dataSetup = re.sub(insertString, str(overwrites[overwrite]), dataSetup)
        filePath = self.filePath
        dataSetup = re.sub(r'\binsertpath\b',filePath, dataSetup)
        writeFile = writeFile.replace(filePath[:-1],'').replace('.3ddat','')[1:]
        dataSetup = re.sub('insertrunName', writeFile, dataSetup)
        
        #dont forget to do saveCyc = 'cycstate' + fileName
        outfile.write('\n' + dataSetup)
        
    #this function is called by write functions to generate the cycle functions    
    def writeCycLoop(self, outfile):
        outfile.write('\ndef cycLoop \n\tloop n(1, numCycloops)'
                      + '\n\t\tsaveFile = saveCyc + "_" + string(n)')
        if self.movieHandles == []:
            self.plots = []
        for plot in self.plots:
            outfile.write('\n\t\t' + plot + 'File = saveFile + ' + '"_' + plot + '" + string(".png")')                                    
        outfile.write('\n\t\tcommand'
                      + '\n\t\t\tDAMP LOCAL \n\t\t\tfacetri rad8 \n\t\t\tcyc @numCycles'
                      + '\n\t\t\tsave @saveCyc')                      
        for plot in self.plots:
            outfile.write('\n\t\t\tplot bitmap plot ' + plot + ' filename @' + plot + 'File')
        
        outfile.write('\n\t\tendcommand \n\tend_loop \nend')
    
    
    def writeRatioLoop(self,outfile):
        outfile.write('\ndef cycRatio \n\trat = float("1e-0") \n\ti = 0'
                      + '\n\tcommand \n\t\tDAMP LOCAL \n\t\tfacetri rad8'
                      + '\n\tendcommand \n\tloop while i < solveRatio'
                      + '\n\t\ti_string = string(i) \n\t\trat = rat/2'
                      + '\n\t\tsaveFile = "saveCyc" + "_" + string(i)')
        if self.movieHandles == []:
            self.plots = []
        for plot in self.plots:
            outfile.write('\n\t\t' + plot + 'File = saveFile + ' + '"_' + plot + '" + string(".png")')
        outfile.write('\n\t\tcommand \n\t\t\tsolve ratio @rat cyc 10000'
                      + '\n\t\t\tsave @saveCyc')
        for plot in self.plots:
            outfile.write('\n\t\t\tplot bitmap plot ' + plot + ' filename @' + plot + 'File')
        outfile.write('\n\t\tendcommand \n\t\ti = i + 1'
                      + '\n\tend_loop \nend')
        
    def writeTest(self, outfile):
        outfile.write('\n;This is only a test run')
    
    #this function is called by write3decfile to write all the functions and their calls
    def writeFunctions(self, outfile, writeFile, j):
     
        outfile.write('\n;;--------------------------------FUNCTIONS------------------------------------\n')
        
        self.writeMovieFunctions(outfile)
        #add in function for cycle
        if self.cycChoice == 'loop':
            self.writeCycLoop(outfile)
        
        if self.cycChoice == 'ratio':
            self.writeRatioLoop(outfile)
            
        if self.cycChoice == 'test':
            self.writeTest(outfile)
        
        #loop through all functions in function handles and write them in.             
        for function in self.functionHandles:
            functionFull = self.functionPath + function + '.txt'
            openFunction = open(functionFull, 'r')
            dataFunction = openFunction.read()
            openFunction.close()
            outfile.write('\n')
            outfile.write(dataFunction)   

        self.setupFunction(outfile, writeFile)
        
        if self.movieHandles != []:
            self.writeClearPlots(outfile)
        outfile.write('\n;--------------------------------FUNCTION CALLS------------------------------------\n')
        self.writeFuncCall(outfile)
        funcCall = self.writeFuncCall(outfile)
        for eachEntry in funcCall:
            outfile.write(eachEntry)


    #join all the files
    def joinFiles(self, filesToJoin):
        #join all the files together for one massive three dec script
        openOutput = open(self.filePath + self.outFileName + '.3ddat', 'w+')
        for file in filesToJoin:
            print('opening ' + file)
            with open(file) as infile:
                print('reading ' + file)
                fullData = infile.read()
                # remove ret
                print('subing in for ret')
                fullData = re.sub(r'\bret\b','', fullData)
                print('subing in for arraysize')
                # subsitute arraysize variable for arraysize, this cannot be done in 3dec bc arrays cannot be dynamically set
                fullData = re.sub(r'\bINSERTarraysize\b',str(self.arraySize), fullData)
                print('writing new lines')
                for line in fullData:
                    openOutput.write(line)
        openOutput.close()

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
        
    #used in write3dec file to change index and insertion for filename based on iterator
    def setupSimulationStone(self, j):
        self.runIndex = j
        self.insertion = ''

    #MAIN FUNCTION
    def write3DECFile(self):
        # first assign indices to unique materials
        for i in range(len(self.materials)):
            self.materials[i].idx = i + 1
        for k in range(len(self.jointMaterials)):
            self.jointMaterials[k].jidx = k + 1

        # next we need to get a list of the files so we can call them for writing
        # so lets make a list called fileHandles, we can do that in a different function above
        self.getFileHandles()

        if self.iterator == 'base':
            self.numSimulations = len(self.fileHandles['base'])
        elif self.iterator == 'load':
            self.numSimulations = int((self.load_max-self.load_min)/self.load_iterator)
        elif self.iterator == 'stone':
            self.numSimulations = len(self.fileHandles['stone'])
        else:
            print('Iterator must be either base or load')
        
        filesToJoin = []
        
        for j in range(self.numSimulations):
            print ('This is iteration number ' + str(j))
            if self.iterator == 'base':
                self.setupSimulationBase(j)
            if self.iterator == 'load':
                self.setupSimulationLoad(j)
            if self.iterator == 'stone':
                self.setupSimulationStone(j)
            print('iterator chosen...')
            fileName = self.fileHandles['base'][self.runIndex]
            print('fileName chosen...')
            fileName = fileName.replace('.3ddat', '').replace(self.filePath, '').replace('_base','')
            print('filename fixing...')
            writeFile = fileName + self.insertion +'.3ddat'
            print('adding this to join list...')
            filesToJoin.append(writeFile)
            output = writeFile
            #open the file and writing
            print('opening the file...')
            outfile = open(output, 'w+')
            outfile.write('\n;-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            outfile.write('new\n' + ';This is file ' + str(j) + '\n')
            #open the file and write the geometry and parameters
            self.writeGeomandParam(j, outfile)
            print('geom and param written')
            #assign material properties
            self.assignMat(outfile)
            print('materials assigned')
            #when last geom and param are written, make sure to hide the blocks that need to be hidden
            self.hideBlocks(outfile)
            print('blocks hidden')            
            #loading is applied
            self.loadBlocks(outfile)
            
            #write the functions that can be called
            self.writeFunctions(outfile, writeFile, j)
                        
            outfile.close()
            
        print('Trying to join....')    
            
        #join all the files together
        self.joinFiles(filesToJoin)
