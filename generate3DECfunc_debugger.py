# #==============================================================================
# # FUNCTION STUFF
# #==============================================================================
#==============================================================================

import glob
import os
import re

class blockGroup:
    def __init__(self,name):
        self.name = name
       
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
        openBlock = open(file_path + fileHandles[blockType][0], 'r')
        dataBlock = openBlock.read()
        openBlock.close()
        outfile.write('\n;--------------------------------%s GEOMETRY-----------------------------------\n'%self.name.upper())
        outfile.write(dataBlock)
        

class generateFile:
    def __init__(self, file_path, blockTypes, blockGroups,
                 finalOutput = None):
        self.file_path = file_path
        self.finalOutput = finalOutput
        self.blockTypes = blockTypes
        self.blockGroups = blockGroups
        self.fileHandles = self.genFileHandles()
        
        
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
                blockGroup.writeToFile(i,self.outfile,self.file_path,prevBlockTypes,self.fileHandles)
                if len(self.fileHandles[blockGroup.name]) > 0:
                    prevBlockTypes.append(blockGroup.name)
              
            
            
            if( self.function_path ):
                self.writeFunctions()
            
            self.outfile.close()
            
            self.joinFiles(i)
            
#==============================================================================
