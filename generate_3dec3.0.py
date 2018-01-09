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
        propertyString += '\nprop mat INSERT NUMBER HERE'
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
    def __init__(self, label, material, jointMaterial):
        self.label = label
        self.material = material
        self.jointMaterial = jointMaterial

class experiment():
    # holds all the necessary objects to run an experiment
    def __init__(self, filePath, outFileName, iterator, load_min = 0, load_max = 0, load_iterator = 0):
        self.filePath = filePath
        self.geometries = []
        self.materials = []
        self.jointMaterials = []
        self.outFileName = outFileName
        self.iterator = iterator
        self.load_min = load_min
        self.load_max = load_max
        self.load_iterator = load_iterator

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

    def writeParams(self, outfile, geometry):
        print(geometry.label)
        outfile.write('\n;--------------------------------%s PARAMETERS-----------------------------------\n'%geometry.label.upper())
        #WILL NEED TO ADD PROP NUMBER IN HERE LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        outfile.write('\n')
        outfile.write(geometry.material.write())
        #WILL NEED TO ADD JMAT NUMBER IN HERE LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        outfile.write('\n')
        outfile.write(geometry.jointMaterial.write())

    #used in writegeometrybymat
    def writeGeometry(self,j,outfile, geometry):
        #figures out an index for iteration based on the iterator and the geometry
        if self.iterator == 'base' and geometry.label == 'base':
            index = j
        else:
            index = 0

        #uses information about the iterator to make the index
        openBlock = open(self.fileHandles[geometry.label][index])
        dataBlock = openBlock.read()
        openBlock.close()
        outfile.write('\n;--------------------------------%s GEOMETRY-----------------------------------\n'%geometry.label.upper())
        outfile.write(dataBlock)

    #used in write3decfile to write geometry for materials
    def writeAllGeometries(self, i, outfile):
        #this writes geometry for any deformable materials
        for geometry in self.geometries:
            keys = geometry.material.properties.keys()
            #keys = list(geometry.material.properties.keys())
            if 'edge' in keys:
                self.writeGeometry(i, outfile, geometry)
                #make sure to add gen edge in here later... something like
                #outfile.write('\n gen edge ' + str(geometry.materials['edge'])
                self.writeParams(outfile, geometry)

        #this writes geometry for any rigid materials
        for geometry in self.geometries:
            #keys = list(geometry.material.properties.keys())
            keys = geometry.material.properties.keys()
            if 'edge' not in keys:
                self.writeGeometry(i, outfile, geometry)
                self.writeParams(outfile, geometry)

#        for geometry in self.geometries:
#            self.writeParams(outfile, geometry)

    #used in write3decfile to grab all of the pertinent files
    def getFileHandles(self):
        self.fileHandles = {}
        #gets all the fileHandles
        for geometry in self.geometries:
            self.fileHandles[geometry.label] = glob.glob(self.filePath + '*_' + geometry.label + '.3ddat')
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SHOULD PROBABLY INCLUDE SOME ERROR CHECKING

    #used in write3dec file to change index and insertion for filename based on iterator
    def setupSimulationBase(self,j):
        #self.numSimulations = len(self.fileHandles['base'])
        self.runIndex = j
        self.insertion = ''

    #used in write3dec file to change index and insertion for filename based on iterator
    def setupSimulationLoad(self, j):
        #self.numSimulations = int((self.load_max-self.load_min)/self.load_iterator)
        self.runIndex = 0
        self.insertion = '_' + str(j*load_iterator)

    #main function
    def write3DECFile(self):
        # first assign indices to unique materials
        for i in range(len(self.materials)):
            self.materials[i].idx = i
        for k in range(len(self.jointMaterials)):
            self.jointMaterials[k].jidx = k

        # next we need to get a list of the files so we can call them for writing
        # so lets make a list called fileHandles, we can do that in a different function above
        self.getFileHandles()

        if iterator == 'base':
            self.numSimulations = len(self.fileHandles['base'])
        elif iterator == 'load':
            self.numSimulations = int((self.load_max-self.load_min)/self.load_iterator)
        else:
            print('Iterator must be either base or load')

        print('this is num simulations ' + str(self.numSimulations))

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
            outfile.write('new\n' + ';This is file ' + str(i) + '\n')

            #open the file and write the geometry
            self.writeAllGeometries(j, outfile)

#============================================================

# set up experiment
filePath= 'C:\\Users\\Rebecca Napolitano\\Documents\\datafiles\\test\\'
outFileName = 'TEST_3DEC_INPUT'
iterator = 'load' #can iterate over base or load
#if iterator = 'load' the following parameters need to be specified
load_min = 0
load_max = 1000
load_iterator = 250
my_experiment = experiment(filePath, outFileName, iterator, load_min, load_max, load_iterator)

# define materials(dens, edge, fixity, hide, ymod)
mortar = material({'dens':2200, 'edge':100})
stone = material({'dens':2400})
fixedstone = material({'dens':2400,'fixity':'fix'})

# define joint materials
mortar_stone = jointMaterial({'jkn':1e9, 'jks':1e9, 'jfric': 37})

# add geometries to experiment
my_experiment.addGeometry('base', fixedstone, mortar_stone)
my_experiment.addGeometry('loadblock', stone, mortar_stone)
my_experiment.addGeometry('mortar', mortar, mortar_stone)
my_experiment.addGeometry('stone', stone, mortar_stone)

# write geometries to 3dec file
my_experiment.write3DECFile()
