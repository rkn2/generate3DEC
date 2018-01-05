import glob

class material():
    # stores all metadata about a material
    def __init__(self, properties):
        self.properties = properties
        self.idx = None
    def write(self):
        # write properties to string
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
    def __init__(self, filePath):
        self.filePath = filePath
        self.geometries = []
        self.materials = []
    def addGeometry(self, label, mat):
        # create a new geometry object
        newGeo = geometry(label, mat)
        # only add it to the list if not already present
        if newGeo not in self.geometries:
            self.geometries.append(newGeo)
        if mat not in self.materials:
            self.materials.append(mat)
    
    def getFileHandles(self):
        fileHandles = {}
        #gets all the fileHandles
        for geometry in self.geometries:
            fileHandles[geometry.label] = glob.glob(self.filePath + '*_' + geometry.label + '.3ddat')
            #checks to make sure all input geometries have correponding files
            if fileHandles == []:
                print('There are no geometry files of type ' + geometry.label)
        print(fileHandles)      
        
    def writeGeometry(self):        
        # first assign indices to unique materials
        for i in range(len(self.materials)):
            self.materials[i].idx = i
        
        # next we need to get a list of the files so we can call them for writing
        # so lets make a list called fileHandles, we can do that in a different function above
        
        self.getFileHandles()
        
        


#============================================================

# set up experiment
filePath= 'C:\\Users\\Rebecca Napolitano\\Documents\\datafiles\\test\\'
my_experiment = experiment(filePath)

# define materials
mortar = material({'dens':2200})
stone = material({'dens':2400})
fixedstone = material({'dens':2400,'fixity':True}) #could not copy to work

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