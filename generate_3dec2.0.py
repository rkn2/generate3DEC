import glob

#____________________FUNCTIONS__________________________

class block():
    # holds all the block data
    def __init__(self, label, density=2000, y_mod=18e9, jkn=1e9, 
                 jks=1e9, jfric=37, genEdge=False, fixity=False):
        self.label = label
        self.density = density
        self.y_mod = y_mod
        self.jkn = jkn
        self.jks = jks
        self.jfric = jfric
        self.genEdge = genEdge
        self.fixity = fixity
        
    def writeGeometry(self, i, j, outfile, data_path, fileHandles):
        for j in range(len(self.fileHandles[block.label])):
            #this makes sure both i and j are in range. Do we have all the files we are supposed to?
            try:
                if self.fileHandles[block.label][j].replace(baseBlock.label,'base') == self.fileHandles['base'][i]:
                    break
            #if not, tell me how many of each we have
            except:
                print(len(self.fileHandles['base'], self.fileHandles[block.label]))
            
            #this makes sure that the prefixes match, if they dont, it prints that
            if self.fileHandles[block.label][j].replace(baseBlock.label,'base') != self.fileHandles['base'][i]:
                print(self.fileHandles['base'][i] + ' does not match ' + self.fileHandles[block.label][j])
                break        
        #makes sure that the block is one we are looking for and that there are some in there
        blockType = self.label
        if blockType not in fileHandles.keys():
            return
        if len(self.fileHandles[blockType]) == 0:
            return
    
        openBlock = open(self.fileHandles[blockType][i], 'r')
        dataBlock = openBlock.read()
        openBlock.close()
        outfile.write('\n;--------------------------------%s GEOMETRY-----------------------------------\n'%self.block.upper())
        outfile.write(dataBlock)
    
#    def writeParams(self,i,outfile,blocks):
#        outfile.write('\n;--------------------------------%s PARAMETERS-----------------------------------\n'%self.block.upper())
#        outfile.write(self.params) #what is params?
#        for blockType in prevBlockTypes:
#            outfile.write('\nhide range group %s'%blockType)
#        if len(prevBlockTypes) > 0:
#            outfile.write('\ngroup block %s \nshow \n'%self.name)   

class baseBlock():
    # holds base data
    def __init__(self, density=2000, y_mod=18e9, jkn=1e9, jks=1e9, jfric=37, fixity=True):
        self.label = 'base'
        self.density = density
        self.y_mod = y_mod
        self.jkn = jkn
        self.jks = jks
        self.jfric = jfric
        self.fixity = fixity

class simulation():         
    # a simulation holds all the metadata for a set of calculations
    def __init__(self, data_path,
                 function_path = 'C:\\Users\\Rebecca Napolitano\\Documents\\GitHub\\generate3DEC\\'):
        self.function_path = function_path
        self.data_path = data_path

    #this is called by generateFile and it imports the blocks, not the bases
    def import_3ddat_files(self, blockLabel, maxFiles=None):
        fileHandles = glob.glob(self.data_path + '*_' + blockLabel + '.3ddat')
        #checks to make sure the files are actually there
        if len(fileHandles) == 0:
            print('There are no ' + blockLabel + ' files!')
            
        #checks to make sure there are not multiple stone or mortar in one file    
        if maxFiles is not None and len(fileHandles) > maxFiles: 
            print('Number of %s files exceeds max (%d > %d)'%(blockLabel,len(fileHandles),maxFiles))
        return fileHandles
    
   
    #this is called by generateFile; it writes to file
    def writeToFile(self,i,outfile,data_path,blocks, fileHandles):
        self.writeGeometry(i,outfile,data_path, fileHandles)
        #self.writeParams(i,outfile,blocks)
    

     
    #generates the 3dec file    
    def generateFile(self, blocks):
        #make a dictionary
        self.fileHandles = {}
        
        #add bases to the dictionary
        self.fileHandles['base'] = self.import_3ddat_files('base')
        
        #figure out how many bases there are
        self.maxFiles = len(fileHandles['base'])
        
        #for all the rest of the blocks, import them using import_3ddat_file above
        #this skips base since they were already imported
        for block in blocks:
            if block.label =='base': 
                continue
            self.fileHandles[block.label] = self.import_3ddat_files(block.label)
             
        for i in range(self.maxFiles):
            #remove the data_path and suffix from the fileHandles which have been tagged "base")
            fileName = self.fileHandles['base'][i].replace(self.data_path, '').replace('_base.3ddat', '')
            
            #write/append file
            writeFile = fileName + '.3ddat'
            output = self.data_path + writeFile
            self.outfile = open(output, 'w+')
            
            #fileHeader
            outfile.write('\n;-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            self.outfile.write('new\n' + ';This is file ' + str(i) + '\n')
             
            #mark down which blocks are deformable
            deformBlocks = []
            for b in blocks:
                if b.genEdge == True:
                    deformBlocks.append(b)
                
            #write down the deformable blocks first in the output fiels        
            for block in blocks:
                if block in deformBlocks:                
                        block.writeToFile(j,self.outfile, self.data_path, blocks, self.fileHandles)
                        if len(self.fileHandles[block.label]) > 0:
                            blocks.append(block.label)
                                    
            #now write everything else    
            for block in blocks:
                if block is not in deformBlocks:
                    block.writeToFile(j,self.outfile, self.data_path, blocks, self.fileHandles)
                        if len(self.fileHandles[block.label]) > 0:
                            blocks.append(block.label)
                
            #now join the files, do this in a separate function
                

#___________________CALL FROM INPUT SCRIPT______________    

loadblock = block('loadblock')
mortar = block('mortar', genEdge=True)
stone = block('stone')
base = baseBlock()
blocks = [mortar, stone, loadblock, base] # only write the ones you want
data_path = 'C:\\Users\\Rebecca Napolitano\\Documents\\datafiles\\test\\'

my_simulation = simulation(data_path) #instantiating the class, simulation so it can be used to access importGeometry

my_simulation.generateFile(blocks)
    