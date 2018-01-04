import glob

#____________________FUNCTIONS__________________________

class block():
    # holds all the block data
    def __init__(self, label, density=2000, y_mod=18e9, jkn=1e9, jks=1e9, jfric=37, genEdge=False, fixity=False):
        self.label = label
        self.density = density
        self.y_mod = y_mod
        self.jkn = jkn
        self.jks = jks
        self.jfric = jfric
        self.genEdge = genEdge
        self.fixity = fixity

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
    def __init__(self,
                 data_path = 'C:/Users/Rebecca Napolitano/Documents/datafiles/test/'):
        self.data_path = data_path
        
    def generateFile(self,blocks, maxFiles=None):
        for block in blocks:
            # look in a directory and grab anything that is a .3ddat file
            fileHandles = glob.glob(self.data_path + '*_' + block.label + '.3ddat')
            # check how many files there are for each, if one is zero, print warning
            if len(fileHandles) == 0:
                print('There are no ' + block + ' files!')
            #check how many base files there are 
            maxFiles = len(fileHandles['base'])
            for i in range(maxFiles):
                fileName = fileHandles['base'][i].replace()
        
    
#___________________CALL FROM INPUT SCRIPT______________    

loadblock = block('loadblock')
mortar = block('mortar', genEdge=True)
stone = block('stone')
base = baseBlock()
blocks = [mortar, stone, loadblock, base] # only write the ones you want

my_simulation = simulation() #instantiating the class, simulation so it can be used to access importGeometry
    