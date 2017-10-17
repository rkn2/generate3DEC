#==============================================================================
# #==============================================================================
# # SCRIPT STUFF
# #==============================================================================
# """
# THE BEGINNING OF THIS FILE IS WHERE TO INPUT THE VARIABLES FOR THE SCRIPT
# """
# file_path = 'C:/Users/Rebecca Napolitano/Google Drive/Documents/Research/mikehess/palazzo vecchio/2017_9_7_ElementiModels/FoundationModels/ExistingGeometry/test_generator/'
# finalOutput = 'Test_3DEC_FILE.3ddat' #write a name here that your 3dec script will be called
# gravity = '0 0 -10 '
# # ;m/s2'
# densitystone = '2713 '
# #units for density ;kg/m3 given by mike granite, cut, rough material editor'
# jkn1 = '1e9 '
# jks1 = '1e9 '
# jfric1 = '30 '
# #; units are N/m3
# numCycles = '10000 '
# densitymortar = '1800 '
# ymod = ' 18e9 '
# numCycloops = '5 '
# boundload = '-480004.7 '
# #dont forget the negative sign
# #area of load = 2.785m^2
# #20psf from mike = 0.137895 MPa
# #total weight = 0.137895MPa * 2.785m^2 = 0.384 E6 N divide by 8 for vertices = 480004.7
# outofplane1 = '36145 '
# outofplane2 = '36146 '
# densitybrick = '2000 ' #brick wikipedia
# densityinfill = '1800 ' #check this with mike
# #;source https://www.academia.edu/1214963/The_toughness_of_Imperial_Roman_concrete
# arraysize = '10000000 '
# zrange = ' -0.25 -0.002 '
# #==============================================================================
# # FUNCTION STUFF
# #==============================================================================
#==============================================================================

import glob
import os
import re


#function_path = 'C:/Users/Rebecca Napolitano/Documents/functions/Generate_3DEC_Script/'
def import_deformable(file_path):
    os.chdir(file_path)
    fileHandles_deformable = glob.glob('*_deformable.3ddat')
    if len(fileHandles_deformable) == 0 or len(fileHandles_deformable) > 1: 
        deformable_fileHandles = {}
    else: 
        deformable_fileHandles = {'deformable':fileHandles_deformable}
    return deformable_fileHandles
    
def import_mortar(file_path):
    os.chdir(file_path) 
    fileHandles_mortar = glob.glob('*_mortar.3ddat')
    if len(fileHandles_mortar) == 0 or len(fileHandles_mortar) > 1 :
        print('There is an error with mortar files')
        mortar_fileHandles = {}
    else: 
        mortar_fileHandles = {'mortar':fileHandles_mortar}
    return mortar_fileHandles

def import_stone(file_path):    
    os.chdir(file_path) 
    fileHandles_stone = glob.glob('*_stone.3ddat')
    if len(fileHandles_stone) == 0 or len(fileHandles_stone) > 1:
        print('There are no stone files')
        stone_fileHandles = {'empty'}
    else:
        stone_fileHandles = {'stone':fileHandles_stone}
    return stone_fileHandles
        
def import_base(file_path):   
    os.chdir(file_path)    
    fileHandles_base = glob.glob('*_base.3ddat')
    if len(fileHandles_base) == 0:
        print('There are no base files')
        base_fileHandles = {}
    else:
        base_fileHandles = {'base':fileHandles_base}
    return base_fileHandles
    
def import_brick(file_path):
    os.chdir(file_path)
    fileHandles_brick = glob.glob('*_brick.3ddat')
    if len(fileHandles_brick) == 0 :
        print('There are no brick files')
        brick_fileHandles = {}
    else:
        brick_fileHandles = {'brick':fileHandles_brick}
    return brick_fileHandles
        
def import_frame(file_path):
    os.chdir(file_path)
    fileHandles_frame = glob.glob('*_frame.3ddat')
    if len(fileHandles_frame) == 0 or len(fileHandles_frame) > 1:
        print('There is an error with the frame files')
        frame_fileHandles = {}
    else:
        frame_fileHandles = {'frame':fileHandles_frame}
    return frame_fileHandles
    
def import_infill(file_path):
    os.chdir(file_path)
    fileHandles_infill = glob.glob('*_infill.3ddat')
    if len(fileHandles_infill) == 0 :
        print('There are no infill files')
        infill_fileHandles = {}
    else:
        infill_fileHandles = {'infill':fileHandles_infill}
    return infill_fileHandles
    
def import_loadblock(file_path): 
    os.chdir(file_path)       
    fileHandles_loadblock = glob.glob('*_loadblock.3ddat')
    if len(fileHandles_loadblock) == 0 or len(fileHandles_loadblock) > 1:
        print('There are no loadblock files')
        loadblock_fileHandles = {}
    else:
        loadblock_fileHandles = {'loadblock':fileHandles_loadblock}
    return loadblock_fileHandles
        
def import_outofplane(file_path):
    os.chdir(file_path)
    fileHandles_outofplane = glob.glob('*_outofplane.3ddat')
    if len(fileHandles_outofplane) == 0 or len(fileHandles_outofplane) > 1:
        print('There are no outofplane files')
        outofplane_fileHandles = {}
    else:
        outofplane_fileHandles = {'outofplane':fileHandles_outofplane}     
    return outofplane_fileHandles
            
def import_sidewall(file_path):
    os.chdir(file_path)
    fileHandles_sidewall = glob.glob('*_sidewall.3ddat')
    if len(fileHandles_sidewall) == 0 or len(fileHandles_sidewall) > 1:
        print('There are no sidewall files')
        sidewall_fileHandles = {}
    else:
        sidewall_fileHandles = {'sidewall':fileHandles_sidewall}
    return sidewall_fileHandles

 
def createFileHandles(file_path):
    deformable_fileHandles = import_deformable(file_path)
    mortar_fileHandles = import_mortar(file_path)
    stone_fileHandles = import_stone(file_path)
    base_fileHandles = import_base(file_path)
    brick_fileHandles = import_brick(file_path)
    frame_fileHandles = import_frame(file_path)     
    infill_fileHandles = import_infill(file_path)
    loadblock_fileHandles = import_loadblock(file_path)
    outofplane_fileHandles = import_outofplane(file_path)
    sidewall_fileHandles = import_sidewall(file_path)
    #fileHandles = {**mortar_fileHandles, **stone_fileHandles}
    fileHandles = {**deformable_fileHandles, **mortar_fileHandles, **stone_fileHandles, **base_fileHandles, **brick_fileHandles, **frame_fileHandles, **infill_fileHandles,**loadblock_fileHandles, **outofplane_fileHandles, **sidewall_fileHandles}
    # to call, fileHandles['mortar'][1 or other number]
    return fileHandles
    #return[mortar_fileHandles, stone_fileHandles]


class generateFile:
    fileHandles = createFileHandles(file_path)
    maxFiles = len(fileHandles['base']) 

    
    for i in range(maxFiles):
        
        fileName = fileHandles['base'][i][0:-11] 
        writefile = fileName + '.3ddat'
        output = file_path + writefile
        outputOpen = open(output,'w+')
        outputOpen.write('\n;-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
        outputOpen.write('new\n' + ';This is file ' + str(i) + '\n')
        outputOpen.close()
        
        if 'deformable' in fileHandles:
            openDeformable = open(file_path + fileHandles['deformable'][0], 'r')
            dataDeformable = openDeformable.read()
            openDeformable.close()
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------DEFORMABLE GEOMETRY-----------------------------------\n')
            outputOpen.write(dataDeformable)
            outputOpen.close()
            
            #generate mesh parameters
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------DEFORMABLE PARAMETERS-----------------------------------\n')
            #outputOpen.write('\ngen edge 100 \ngroup block mortar \nprop mat 2 dens ' + densitymortar + ' ymod ' + ymod + 'bcoh ' + bcoh + 'bfric ' + bfric + 'bten ' + bten + '\n')
            outputOpen.write('\ngen edge 100 \ngroup block deformable \nprop mat 2 dens ' + densitymortar + ' ymod ' + ymod + '\n')
            outputOpen.close()
        else: 
             print('There are no deformable files')
        
        
        #_____________________________________________________________________________________________________________________________
        if 'mortar' in fileHandles:
            #this adds the contents of one file to the end of that one
            openMortar = open(file_path + fileHandles['mortar'][0], 'r')
            dataMortar = openMortar.read()
            openMortar.close()
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------MORTAR GEOMETRY-----------------------------------\n')
            outputOpen.write(dataMortar)
            outputOpen.close()
            
            #generate mesh parameters
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------MORTAR PARAMETERS-----------------------------------\n')
            #outputOpen.write('\ngen edge 100 \ngroup block mortar \nprop mat 2 dens ' + densitymortar + ' ymod ' + ymod + 'bcoh ' + bcoh + 'bfric ' + bfric + 'bten ' + bten + '\n')
            outputOpen.write('\ngen edge 100 \ngroup block mortar \nprop mat 2 dens ' + densitymortar + ' ymod ' + ymod + '\n')
            outputOpen.close()
        else: 
             print('There are no mortar files')
    #_____________________________________________________________________________________________________________________________
    
        if 'brick' in fileHandles:
            #import the geometry of the bricks
            openBricks = open(file_path + fileHandles['brick'][0], 'r')
            dataBricks = openBricks.read()
            openBricks.close()
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------BRICK GEOMETRY-----------------------------------\n')
            outputOpen.write(dataBricks)
            outputOpen.close()
            
            #add in material properties
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------BRICK PARAMETERS-----------------------------------\n')
            outputOpen.write('\nprop mat 3 dens ' + densitybrick + '\n')
            if 'mortar' in fileHandles:
                outputOpen.write('\nhide range group mortar')
            outputOpen.write('\ngroup block brick \nshow \n')
            outputOpen.close()
        else: 
             print('There are no brick files')        
         #_____________________________________________________________________________________________________________________________
        if 'frame' in fileHandles:
         #import the geometry of the frames
            openFrames = open(file_path + fileHandles['frame'][0], 'r')
            dataFrames = openFrames.read()
            openFrames.close()
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------FRAME GEOMETRY-----------------------------------\n')
            outputOpen.write(dataFrames)
            outputOpen.close()
            
            #add in material properties
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------FRAME PARAMETERS-----------------------------------\n')
            outputOpen.write('\n;they are the same as the stone parameters\n')
            if 'mortar' in fileHandles:
                outputOpen.write('\nhide range group mortar')
            if 'brick' in fileHandles:
                outputOpen.write('\nhide range group brick')
            outputOpen.write('\ngroup block frame \nshow\n')
            outputOpen.close()
        else: 
             print('There are no frame files')
     #_____________________________________________________________________________________________________________________________
        if 'infill' in fileHandles:
            #import the geometry of the infill
            for i in range(fileHandles['infill']):
                openInfill = open(file_path + fileHandles['infill'][i], 'r')
                dataInfill = openInfill.read()
                openInfill.close()
                outputOpen = open(output, 'a+')
                outputOpen.write('\n;--------------------------------INFILL GEOMETRY-----------------------------------\n')
                outputOpen.write(dataInfill)
                outputOpen.close()
            
            #add in material properties
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------INFILL PARAMETERS-----------------------------------\n')
            outputOpen.write('\n;they are the same as the mortar parameters\n')
            if 'mortar' in fileHandles:
                outputOpen.write('\nhide range group mortar')
            if 'brick' in fileHandles:
                outputOpen.write('\nhide range group brick')
            if 'frame' in fileHandles:
                outputOpen.write('\nhide range group frame')
            outputOpen.write('\ngroup block infill \nshow \n')
            outputOpen.close()
        else: 
             print('There are no infill files')           
        #_____________________________________________________________________________________________________________________________
        if 'loadblock' in fileHandles:        
            #import the geometry of the load block
            openLoadBlock = open(file_path + fileHandles['loadblock'][0], 'r')
            dataLoadBlock = openLoadBlock.read()
            openLoadBlock.close()
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------LOAD BLOCK GEOMETRY-----------------------------------\n')
            outputOpen.write(dataLoadBlock)
            outputOpen.close()
            
            #add in material properties
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------LOAD BLOCK PARAMETERS-----------------------------------\n')
            outputOpen.write('\n;they are the same as the mortar parameters\n')
            if 'mortar' in fileHandles:
                outputOpen.write('\nhide range group mortar')
            if 'brick' in fileHandles:
                outputOpen.write('\nhide range group brick')
            if 'frame' in fileHandles:
                outputOpen.write('\nhide range group frame')
            if 'infill' in fileHandles:
                outputOpen.write('\nhide range group infill')
            outputOpen.write('\ngroup block loadblock \nshow \n')
            outputOpen.close()
        else: 
             print('!!!!There are no loadblock files')     
     #_____________________________________________________________________________________________________________________________
        if 'outofplane' in fileHandles:            
        #import the geometry of the out of plane block
            openOutofPlane = open(file_path + fileHandles['outofplane'][0], 'r')
            dataOutofPlane = openOutofPlane.read()
            openOutofPlane.close()
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------OUT OF PLANE GEOMETRY-----------------------------------\n')
            outputOpen.write(dataOutofPlane)
            outputOpen.close()
            
            #add in material properties
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------OUT OF PLANE PARAMETERS-----------------------------------\n')
            outputOpen.write('\n;they are the same as the stone parameters\n')
            if 'mortar' in fileHandles:
                outputOpen.write('\nhide range group mortar')
            if 'brick' in fileHandles:
                outputOpen.write('\nhide range group brick')
            if 'frame' in fileHandles:
                outputOpen.write('\nhide range group frame')
            if 'infill' in fileHandles:
                outputOpen.write('\nhide range group infill')
            if 'loadblock' in fileHandles:
                outputOpen.write('\nhide range group loadblock')
            outputOpen.write('\ngroup block outofplane \nshow \n')
            outputOpen.close()
        else: 
             print('There are no out of plane block files')          
    
    
        #_____________________________________________________________________________________________________________________________
        if 'sidewall' in fileHandles:       
            #import the geometry of the sidewalls
            openSideWalls = open(file_path + fileHandles['sidewall'][0], 'r')
            dataSideWalls = openSideWalls.read()
            openSideWalls.close()
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------SIDEWALL GEOMETRY-----------------------------------\n')
            outputOpen.write(dataSideWalls)
            outputOpen.close()
            
            #add in material properties
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------SIDEWALL PARAMETERS-----------------------------------\n')
            outputOpen.write('\n;they are the same as the stone parameters\n')
            if 'mortar' in fileHandles:
                outputOpen.write('\nhide range group mortar')
            if 'brick' in fileHandles:
                outputOpen.write('\nhide range group brick')
            if 'frame' in fileHandles:
                outputOpen.write('\nhide range group frame')
            if 'infill' in fileHandles:
                outputOpen.write('\nhide range group infill')
            if 'loadblock' in fileHandles:
                outputOpen.write('\nhide range group loadblock')
            if 'outofplane' in fileHandles:
                outputOpen.write('\nhide range group outofplane')
            outputOpen.write('\ngroup block sidewall \nshow \n')
            outputOpen.close()
        else: 
             print('There are no sidewall files')          
                
         #_____________________________________________________________________________________________________________________________
        if 'stone' in fileHandles:           
            #import the geometry of the stones
            openStones = open(file_path + fileHandles['stone'][0], 'r')
            dataStones = openStones.read()
            openStones.close()
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------STONE GEOMETRY-----------------------------------\n')
            outputOpen.write(dataStones)
            outputOpen.close()
            
            #add in material properties
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------STONE PARAMETERS-----------------------------------\n')
            outputOpen.write('\nprop mat 1 dens ' + densitystone + '\n\nprop jmat 1 jkn ' + jkn1 + ' jks ' + jks1 +  ' jfric ' + jfric1 + '\n')
            if 'mortar' in fileHandles:
                outputOpen.write('\nhide range group mortar')
            if 'brick' in fileHandles:
                outputOpen.write('\nhide range group brick')
            if 'frame' in fileHandles:
                outputOpen.write('\nhide range group frame')
            if 'infill' in fileHandles:
                outputOpen.write('\nhide range group infill')
            if 'loadblock' in fileHandles: 
                outputOpen.write('\nhide range group loadblock')
            if 'outofplane' in fileHandles:
                outputOpen.write('\nhide range group outofplane')
            if 'sidewall' in fileHandles:
                outputOpen.write('\nhide range group sidewall')
            outputOpen.write('\ngroup block stone \nshow \n')
            outputOpen.close()
        else: 
             print('!!!There are no stone files')             


#_____________________________________________________________________________
        #general properties and material assignment
        outputOpen = open(output, 'a+')
        outputOpen.write('\n;-------------------------------- PARAMETERS-----------------------------------\n')
            #assign properties
        outputOpen.write('\ngravity ' + gravity + ' \n')
        outputOpen.write('\nhide')
        if 'stone' in fileHandles:  
            outputOpen.write('\nshow range group stone')
        if 'frame' in fileHandles:  
            outputOpen.write('\nshow range group frame') 
        if 'loadblock' in fileHandles:  
            outputOpen.write('\nshow range group loadblock')
        if 'outofplane' in fileHandles:  
            outputOpen.write('\nshow range group outofplane') 
        if 'sidewall' in fileHandles:  
            outputOpen.write('\nshow range group sidewall')            
        outputOpen.write('\nchange mat 1 \nshow \nhide \n')
        if 'mortar' in fileHandles:  
            outputOpen.write('\nshow range group mortar')
            outputOpen.write('\nchange mat 2 \nshow \n')            
        if 'brick' in fileHandles:  
            outputOpen.write('\nhide \nshow range group brick')        
            outputOpen.write('\nchange mat 3 \nshow \n')
            #load blocks
        if 'loadblock' in fileHandles:  
            #load blocks            
            outputOpen.write('\nhide \nshow range group loadblock \n')
            outputOpen.write('\nbound zload ' + boundload + 'range z ' + zrange + '\nshow \n')
        outputOpen.close()
#_____________________________________________________________________________
          #import the geometry of the base
        if 'base' in fileHandles: 
            openBase = open(file_path + fileHandles['base'][i], 'r')
            dataBase = openBase.read()
            openBase.close()
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------BASE GEOMETRY-----------------------------------\n')
            outputOpen.write(dataBase)
            outputOpen.close()
        else: 
            print('!!!There are no bases!!!')
#_____________________________________________________________________________            
            #fix the blocks 
        if 'base' in fileHandles: 
            outputOpen = open(output, 'a+')
            outputOpen.write('\n;--------------------------------BASE PARAMETERS-----------------------------------\n')
            
            if 'mortar' in fileHandles: 
                outputOpen.write('\nhide range group mortar')
            if 'frame' in fileHandles: 
                outputOpen.write('\nhide range group frame')
            if 'brick' in fileHandles: 
                outputOpen.write('\nhide range group brick')                
            if 'loadblock' in fileHandles: 
                outputOpen.write('\nhide range group loadblock')   
            if 'outofplane' in fileHandles: 
                outputOpen.write('\nhide range group outofplane') 
            if 'sidewall' in fileHandles: 
                outputOpen.write('\nhide range group sidewall')
            if 'stone' in fileHandles: 
                outputOpen.write('\nhide range group stone')  
        
            outputOpen.write('\ngroup block bases \nfix \nshow \n')
            outputOpen.close()
#_____________________________________________________________________________            
            #hide front blocks
        if 'outofplane' in fileHandles:
            outputOpen = open(output, 'a+')             
            outputOpen.write('\nhide range group outofplane \n')
            outputOpen.close()
#_____________________________________________________________________________           
#functions
        os.chdir(function_path)
        functionFiles = glob.glob('*_func.txt')
        numFunctions = len(functionFiles)
        os.chdir(file_path)
        outputOpen = open(output, 'a+')
        outputOpen.write('\n;--------------------------------FUNCTIONS-----------------------------------\n')
        
        for i in range(numFunctions):
            functionOpen = open(function_path + functionFiles[i])
            functiondata = functionOpen.read()
            functionOpen.close()
            saveCyc = 'cycstate_' + fileName
            functiondata = re.sub(r'\bnumCycloops\b', numCycloops, functiondata)
            functiondata = re.sub(r'\bnumCycles\b', numCycles, functiondata)
            functiondata = re.sub(r'\bsaveCyc\b', saveCyc, functiondata)
            functiondata = re.sub(r'\barraysize\b', arraysize, functiondata )
            outputOpen.write(functiondata)
            outputOpen.write('\n')
            
        os.chdir(function_path)
        setupFiles = glob.glob('*_setup.txt')
        os.chdir(file_path)
        outputOpen = open(output, 'a+')
        outputOpen.write('\n;--------------------------------SETUP-----------------------------------\n')
        setupOpen = open(function_path + setupFiles[0])
        setupData = setupOpen.read()
        setupOpen.close()
        setupData = re.sub(r'\bINSERT PATH HERE\b', file_path, setupData)
        setupData = re.sub(r'\bINSERT RUN NAME HERE\b', fileName, setupData)
        callFile = fileName + '.3ddat'
        outputOpen.write(setupData)
        outputOpen.write('\n;---------------------------------RUNTIME-----------------------------------\n')
        outputOpen.write('\n@setup \n@neighbors \n@initial_centroid \n@initial_vertex \n@getvol \n@getstoneid \n;@getblockgroup \nhist unbal \n@cycloop \n@displacement \n@final_centroid \n@final_vertex \n@get_stress')
        outputOpen.close()
    
#_____________________________________________________________________________           

#join all the files together for one massive three dec script
        outputOpen = open(output, 'r')
        fullData = outputOpen.read()
        outputOpen.close()
        outputOpen = open(file_path + finalOutput, 'a+')
        fullData = re.sub(r'\bret\b','',fullData)
        outputOpen.write(fullData)
        outputOpen.write('\n\n\n\n\n\n')
        outputOpen.close()
