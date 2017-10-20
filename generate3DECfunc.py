# #==============================================================================
# # FUNCTION STUFF
# #==============================================================================
#==============================================================================

import glob
import os
import re

class blockGroup:
    def __init__(self,name,params):
        self.name = name
        self.params = params
        
    def writeToFile(self,i,outfile,file_path,prevBlockTypes, fileHandles):
        self.writeGeometry(i,outfile,file_path, fileHandles)
        self.writeParams(i,outfile,prevBlockTypes)
        
    def writeGeometry(self,i,outfile,file_path, fileHandles):
        #this adds the contents of one file to the end of that one
        blockType = self.name
        if blockType not in fileHandles.keys():
            return
        if len(fileHandles[blockType]) == 0:
            return
        openBlock = open(file_path + fileHandles[blockType][i], 'r')
        dataBlock = openBlock.read()
        openBlock.close()
        outfile.write('\n;--------------------------------%s GEOMETRY-----------------------------------\n'%self.name.upper())
        outfile.write(dataBlock)
        
    def writeParams(self,i,outfile,prevBlockTypes):
        #generate mesh parameters
        outfile.write('\n;--------------------------------%s PARAMETERS-----------------------------------\n'%self.name.upper())
        outfile.write(self.params)
        for blockType in prevBlockTypes:
            outfile.write('\nhide range group %s'%blockType)
        if len(prevBlockTypes) > 0:
            outfile.write('\ngroup block %s \nshow \n'%self.name)

class infillGroup(blockGroup):
    def writeGeometry(self,i,outfile,file_path, fileHandles):
        #this adds the contents of one file to the end of that one
        blockType = self.name
        for j in range (len(fileHandles[self.name])):
            if blockType not in fileHandles.keys():
                return
            if len(fileHandles[blockType]) == 0:
                return
            openBlock = open(file_path + fileHandles[blockType][i], 'r')
            dataBlock = openBlock.read()
            openBlock.close()
            outfile.write('\n;--------------------------------%s GEOMETRY-----------------------------------\n'%self.name.upper())
            outfile.write(dataBlock)

class generateFile:
    def __init__(self, file_path, blockTypes, blockGroups, movieInterval,dampLocal,
                 finalOutput = None,
                 gravity = None, boundload = None,
                 function_path=None, numCycloops=0, numCycles=0, arraysize=0):
        self.file_path = file_path
        self.finalOutput = finalOutput
        self.blockTypes = blockTypes
        self.blockGroups = blockGroups
        self.fileHandles = self.genFileHandles()
        self.gravity = gravity
        self.boundload = boundload
        self.function_path = function_path
        self.numCycloops = numCycloops
        self.numCycles = numCycles
        self.arraysize = arraysize
        self.movieInterval = movieInterval
        self.dampLocal = dampLocal
        
        self.gen3DEC()
        
    def import_3ddat_files(self,blockType,maxFiles=None):
        os.chdir(self.file_path)
        fileHandles = glob.glob('*_'+blockType+'.3ddat')
        if len(fileHandles) == 0:
            print('There are no '+blockType+' files')
        if maxFiles is not None and len(fileHandles) > maxFiles:
            print('Number of %s files exceeds max (%d > %d)'%(blockType,len(fileHandles),maxFiles))
        return fileHandles        
        
    def genFileHandles(self):
        fileHandles = {}
        # there will always be a 'base' blockType
        fileHandles['base'] = self.import_3ddat_files('base')
        self.maxFiles = len(fileHandles['base'])
        for blockType in self.blockTypes:
            if blockType == 'base':
                continue
            fileHandles[blockType] = self.import_3ddat_files(blockType)
        return fileHandles

    def grav(self):
        self.outfile.write('\ngravity ' + self.gravity + ' \n')
    
    def loadBlock(self):    
        self.outfile.write('\nhide \nshow range group loadblock \n')
        self.outfile.write('\nbound zload ' + self.boundload + 'range group loadblock \nshow \n')

    def baseGeometry(self,i):
        openBase = open(self.file_path + self.fileHandles['base'][i], 'r')
        dataBase = openBase.read()
        openBase.close()
        self.outfile.write('\n;--------------------------------BASE GEOMETRY-----------------------------------\n')
        self.outfile.write('\nhide')
        self.outfile.write(dataBase)                 

    def fixBlocks(self,prevBlockTypes):
        self.outfile.write('\n;--------------------------------BASE PARAMETERS-----------------------------------\n')
#        for blockType in prevBlockTypes:
#            if blockType == 'base':
#                continue
#            self.outfile.write('\nshow')
#            self.outfile.write('\nhide range group %s'%blockType)
        self.outfile.write('\ngroup block bases \nfix \nshow \n')

    def hideFrontBlocks(self,prevBlockTypes):
        if 'outofplane' in prevBlockTypes:
            self.outfile.write('\nhide range group outofplane \n')

    def writeFunctions(self):
        os.chdir(self.function_path)
        functionFiles = glob.glob('*_func.txt')
        numFunctions = len(functionFiles)
        os.chdir(self.file_path)
        self.outfile.write('\n;--------------------------------FUNCTIONS-----------------------------------\n')
         
        for i in range(numFunctions):
            functionOpen = open(self.function_path + functionFiles[i])
            functiondata = functionOpen.read()
            functionOpen.close()
            saveCyc = 'cycstate_' + self.fileName
            if self.dampLocal != 'true':
                functiondata = re.sub(r'\bDAMP LOCAL\b', '' , functiondata)

            functiondata = re.sub(r'\bnumCycloops\b', self.numCycloops, functiondata)
            functiondata = re.sub(r'\bnumCycles\b', self.numCycles, functiondata)
            functiondata = re.sub(r'\bsaveCyc\b', saveCyc, functiondata)
            functiondata = re.sub(r'\barraysize\b', self.arraysize, functiondata )
            self.outfile.write(functiondata)
            self.outfile.write('\n')
             
        os.chdir(self.function_path)
        setupFiles = glob.glob('*_setup.txt')
        os.chdir(self.file_path)
        self.outfile.write('\n;--------------------------------SETUP-----------------------------------\n')
        setupOpen = open(self.function_path + setupFiles[0])
        setupData = setupOpen.read()
        setupOpen.close()
        setupData = re.sub(r'\bINSERT PATH HERE\b', self.file_path, setupData)
        setupData = re.sub(r'\bINSERT RUN NAME HERE\b', self.fileName, setupData)
        setupData = re.sub(r'\bINSERT MOVIE INTERVAL HERE\b', self.movieInterval, setupData)
        self.outfile.write(setupData)
        self.outfile.write('\n;---------------------------------RUNTIME-----------------------------------\n')
        self.outfile.write('\n@setup \n@neighbors \n@initial_centroid \n@initial_vertex \n@getvol \n@getstoneid \n;@getblockgroup \n@movieSetup \n@cycloop \n@displacement \n@final_centroid \n@final_vertex \n@get_stress')

    def joinFiles(self,i):
        #join all the files together for one massive three dec script
        output = self.file_path + self.fileName + '.3ddat'
        print('writing to %s'%output)
        outputOpen = open(output, 'r')
        fullData = outputOpen.read()
        outputOpen.close()
        if i == 0:
            mode = 'w+'
        else:
            mode = 'a+'
        outputOpen = open(self.file_path + self.finalOutput, mode)
        fullData = re.sub(r'\bret\b','',fullData)
        outputOpen.write(fullData)
        outputOpen.write('\n\n\n\n\n\n')
        outputOpen.close()        

    def gen3DEC(self):
        for i in range(self.maxFiles):
            self.fileName = self.fileHandles['base'][i][0:-11] 
            writefile = self.fileName + '.3ddat'
            output = self.file_path + writefile
            self.outfile = open(output,'w+')
              
            self.outfile.write('\n;-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            self.outfile.write('new\n' + ';This is file ' + str(i) + '\n')
            
            prevBlockTypes = []
            for blockGroup in self.blockGroups:
                # find corresponding blockGroup entry
                for j in range(len(self.fileHandles[blockGroup.name])):
                    if self.fileHandles[blockGroup.name][j].replace(blockGroup.name,'base') == self.fileHandles['base'][i]:
                        break
                try:
                    if self.fileHandles[blockGroup.name][j].replace(blockGroup.name,'base') != self.fileHandles['base'][i]:
                        print(self.fileHandles['base'][i],self.fileHandles[blockGroup.name][j])
                except:
                    print(len(self.fileHandles['base']),len(self.fileHandles[blockGroup.name]))
                blockGroup.writeToFile(j,self.outfile,self.file_path,prevBlockTypes,self.fileHandles)
                if len(self.fileHandles[blockGroup.name]) > 0:
                    prevBlockTypes.append(blockGroup.name)
              
            self.outfile.write('\n;-------------------------------- PARAMETERS-----------------------------------\n')
            self.outfile.write('\nhide \n')
            #assign properties                
            stoneMatList = ['stone', 'frame', 'loadblock', 'outofplane', 'sidewall']
            mortarMatList = ['mortar', 'infill', 'deformable']
            brickMatList = ['brick']
              
            for entry in stoneMatList:
                if entry in prevBlockTypes:
                    self.outfile.write('\nshow range group ' + entry)
            self.outfile.write('\nchange mat 1 \nshow \nhide \n')
              
            for entry in mortarMatList: 
                if entry in prevBlockTypes:
                    self.outfile.write('\nshow range group ' + entry)
            self.outfile.write('\nchange mat 2 \nshow \nhide \n')
              
            for entry in brickMatList: 
                if entry in prevBlockTypes:
                    self.outfile.write('\nshow range group ' + entry)
            self.outfile.write('\nchange mat 3 \nshow \nhide \n')

            if( self.gravity ):
                self.grav()
            if( self.boundload and 'loadblock' in prevBlockTypes ):
                self.loadBlock()
            
            self.baseGeometry(i)
            self.fixBlocks(prevBlockTypes)
            self.hideFrontBlocks(prevBlockTypes)
            
            if( self.function_path ):
                self.writeFunctions()
            
            self.outfile.close()
            
            self.joinFiles(i)
            
#==============================================================================
