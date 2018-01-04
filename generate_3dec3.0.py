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
    def writeGeometry(self):        
        # first assign indices to unique materials
        for i in range(len(self.materials)):
            self.materials[i].idx = i
        # write base geometry first
        
        # then loop over other geometries

#============================================================

# set up experiment
filePath= 'C:\\test\\file\\path\\'
my_experiment = experiment(filePath)

# define materials
brick = material({'dens':2000})
concrete = material({'dens':2200})
stone = material({'dens':2400})

# create a copy of stone but add fixity
fixedStone = material(dict(stone.properties))
fixedStone['fixity'] = True

# add geometries to experiment
my_experiment.addGeometry('base', fixedStone)
my_experiment.addGeometry('brick', brick)
my_experiment.addGeometry('concrete', concrete)
my_experiment.addGeometry('stone', stone)

# write geometries to 3dec file
my_experiment.writeGeometry()