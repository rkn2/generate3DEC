import glob

class material():
    # stores all metadata about a material
    def __init__(self, properties):
        self.properties = properties
        self.idx = None
    def write(self):
        # write properties to string !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! LATER I WILL NEED FIXITY, HIDING, AND GEN EDGE TO BE NEW LINES AND APART FROM OTHERS...
        s = ''
        for p in self.properties:
            s += '%s %s'%(p,self.properties[p])
        return s

class geometry():
    # holds all the geometry data for a certain type of block
    def __init__(self, label, material):
        self.label = label
        self.material = material
        
class experiment():
    # holds all the necessary objects to run an experiment
    def __init__(self, filePath, outFileName, iterator, load_min = None, load_max = None, load_iterator = None):
        self.filePath = filePath
        self.geometries = []
        self.materials = []
        self.outFileName = outFileName
        self.iterator = iterator
        self.load_min = load_min
        self.load_max = load_max
        self.load_iterator = load_iterator
        
    def addGeometry(self, label, mat):
        # create a new geometry object
        newGeo = geometry(label, mat)
        # only add it to the list if not already present
        if newGeo not in self.geometries:
            self.geometries.append(newGeo)
        if mat not in self.materials:
            self.materials.append(mat)
    
    def getFileHandles(self):
        
        self.fileHandles = {}
        #gets all the fileHandles
        for geometry in self.geometries:
            self.fileHandles[geometry.label] = glob.glob(self.filePath + '*_' + geometry.label + '.3ddat')
            #checks to make sure only base has multiple files !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ERROR HERE.. DOES NOT ACCEPT MULTIPLE BASE FILES
            length = len(self.fileHandles[geometry.label])
            if geometry.label != 'base':
                continue
            else:
                if length > 1:
                    print('There are too many ' + geometry.label + ' files!')
            #removes filepath and suffix from fileHandles
            i = 0
            while i < length:
                self.fileHandles[geometry.label][i] = self.fileHandles[geometry.label][i].replace('.3ddat', '').replace(self.filePath, '')
                i = i + 1
            #checks to make sure all input geometries have correponding files
            if self.fileHandles == []:
                print('There are no geometry files of type ' + geometry.label)
                    
        
    def writeGeometry(self):        
        # first assign indices to unique materials
        for i in range(len(self.materials)):
            self.materials[i].idx = i
        
        # next we need to get a list of the files so we can call them for writing
        # so lets make a list called fileHandles, we can do that in a different function above
        self.getFileHandles()
        
        if iterator == 'base':
            numSimulations = len(self.fileHandles['base'])
            for i in range (numSimulations):
                #get file name    
                self.fileName = self.fileHandles['base'][i].strip('base')
                writeFile = self.fileName + '.3ddat'
                print(writeFile)
                output = self.filePath + writeFile
                #open the file and start writing
                self.outfile = open(output, 'w+')
                self.outfile.write('\n;-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
                self.outfile.write('new\n' + ';This is file ' + str(i) + '\n')                
                self.outfile.close()
            
            
            
            
#        if iterator == 'load':
#            numSimulations = load_max/load_iterator
#            for i in range(numSimulations):
#                fileName = self.fileHandles['base'][0] + 
                    # COMEEEEEEEEEEEEEEEEEEEEEEEE BACCCCCCCCCCCCCCCCKKKKKKKKKK LATERRRRRRRRRRRRRRRRRRRRRR
        

        


#============================================================

# set up experiment
filePath= 'C:\\Users\\Rebecca Napolitano\\Documents\\datafiles\\test\\'
outFileName = 'TEST_3DEC_INPUT'
iterator = 'base' #can iterate over base or load !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! IS THIS HARDCODING..?
#if iterator = 'load' the following parameters need to be specified !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! DEAL WITH THIS AFTER BASE STARTS WORKING
#load_min = 0
#load_max = 1000
#load_iterator = 25 
my_experiment = experiment(filePath, outFileName, iterator)

# define materials
mortar = material({'dens':2200})
stone = material({'dens':2400})
fixedstone = material({'dens':2400,'fixity':'fix'}) #could not copy to work  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! HOW SHOULD I GET FIXITY TO WORK, ITS DIFFERENT THAN OTHER PROPERTIES, NEEDS TO BE OWN LINE AND ONLY SAY "FIX"

## create a copy of stone but add fixity
#fixedStone = material(dict(stone.properties))
#fixedStone['fixity'] = 'True'

# add geometries to experiment
my_experiment.addGeometry('base', fixedstone)
my_experiment.addGeometry('loadblock', stone)
my_experiment.addGeometry('mortar', mortar)
my_experiment.addGeometry('stone', stone)

# write geometries to 3dec file
my_experiment.writeGeometry()