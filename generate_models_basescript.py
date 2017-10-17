#makes walls with roman bonding courses


import sys
import os
import shutil
import rhinoscriptsyntax as rs
#file_path = location of usemasonrycommands.py
file_path = 'C:\\Users\\Rebecca Napolitano\\Documents\\functions\\'    
sys.path.append(file_path)
import useMasonryCmds as umc
#import NoBondingCourseWall as nobc
#import BondingCourseWallv2 as bc


directory = "C:\\Users\\Rebecca Napolitano\\Documents\\datafiles\\Romanbondingcourses\\2017_10_16_simulations\\"

#def buildBondingCourseWall(wallWidth, wallHeight, wallDepth, stoneHeight, stoneWidth, brickHeight="Enter", brickWidth="", firstCourse="", brickRow="", bondingCourses="", settleWidth="Enter", settleDepth=""):

    
wallWidth = 7   
wallHeight = 3.3
wallDepth = 2
stoneHeight = 0.3 
stoneWidth = 0.5
brickHeight = 0.1
brickWidth = 0.3
firstCourse = 0.9
brickRow = 3
sideBaseWidth = 0.4
TOL = 1e-5

meshValue = '0.5 '

i = 0 #number of bonding courses
j = 0 #width
k = 0 #settlement depth   

iList = [1, 2]
jList = [0.5, 2, 3,4]
kList = [0.01, 0.05, 0.1]


umc.new()
  
while i <= len(iList) - 1 :
    while j <= len(jList) - 1 :
        while k <= len(kList) - 1 :
            iEntry = iList[i]
            jEntry = jList[j]
            kEntry = kList[k]
            
            umc.buildBondingCourseWallv2(wallWidth, wallHeight, wallDepth, stoneHeight, stoneWidth, brickHeight, brickWidth, firstCourse, brickRow, iEntry, jEntry, kEntry, sideBaseWidth)
            filename = "bc_r" + str(iEntry) + "-w" + str(jEntry) + "-s" + str(kEntry)  
            success = umc.exportLayers(directory, filename, ".wrl")
            if not (success):
                break  
            
            meshValue = '0.5 '
            
            os.chdir(directory)
                        
            #meshcommands
            angle = ' _angle=0'
            aspectratio =' _aspectratio=0' 
            distance = ' _distance=0'
            grid = ' _grid=0'
            maxedgelength = ' _maxedgelength=' + meshValue
            maxedgelengthstr= maxedgelength
            minedgelength = ' _minedgelength=' + meshValue
            minedgelengthstr = minedgelength
            
            advOptions = angle + aspectratio + distance + grid + maxedgelengthstr + minedgelengthstr
            
            #gsurfcommands
            
            mode = '_mode=tri'
            minedgelength = '_minedgelength=' + meshValue
            maxedgelength = '_maxedgelength=' + meshValue
            ridgeangle = '_ridgeangle=20'
            maxgradation = '_maxgradation=1'
            deleteinput = '_deleteinput=Yes'
            
            gsurfOptions = mode + minedgelength + maxedgelength + ridgeangle + maxgradation + deleteinput
            
            #gvol options
            mode = '_mode=test '
            outputformat = '_outputformat=3DEC '
            
            gvolOptions = mode + outputformat
            
            layers = rs.LayerNames()
            for layer in layers:
                if layer == 'concrete':
                                   
                    rs.Command("-_SelLayer " + layer)
                    rs.Command("_Enter")
                    rs.Command("-_Mesh _DetailedOptions _AdvancedOptions " + advOptions + '_Enter _Enter')
                    rs.Command("-_SelMesh")
                    rs.Command("-_Gsurf " + gsurfOptions + '_Enter _Enter')
                    rs.Command("-_SelMesh")
                    rs.Command("-_Gvol " + gvolOptions + '_Enter _Enter')
                    
            #save filename
 
 
            shutil.move('Gvol.3ddat', filename + '_deformable.3ddat')

            success = umc.saveAs(directory, filename, ".3dm")
            if not (success):
                break

#            #open a new file
            if i < len(iList) + 1:                             
                success = umc.new()
                #rs.Command('_Enter')
                if not (success):
                    break
            k = k + 1
        j = j + 1
        k = 0
    i = i + 1
    j = 0
    
i = 0 #number of bonding courses
j = 0 #width
k = 0 #settlement depth   

iList = [1, 2]
jList = [0.5, 2, 3,4]
kList = [0.01, 0.05, 0.1]

    
umc.new()            
while j <= len(jList) - 1 :
    while k <= len(kList) - 1 :
        #iEntry = iList[i]
        jEntry = jList[j]
        kEntry = kList[k]
        umc.buildNOBC(wallWidth, wallHeight, wallDepth, stoneHeight, stoneWidth, jEntry, kEntry, sideBaseWidth)
        filename = "nobc-w" + str(jEntry) + "-s" + str(kEntry) 
        success = umc.exportLayers(directory, filename, ".wrl")
        if not (success):
            break
        
        meshValue = '0.5 '
            
        os.chdir(directory)
                    
        #meshcommands
        angle = ' _angle=0'
        aspectratio =' _aspectratio=0' 
        distance = ' _distance=0'
        grid = ' _grid=0'
        maxedgelength = ' _maxedgelength=' + meshValue
        maxedgelengthstr= maxedgelength
        minedgelength = ' _minedgelength=' + meshValue
        minedgelengthstr = minedgelength
        
        advOptions = angle + aspectratio + distance + grid + maxedgelengthstr + minedgelengthstr
        
        #gsurfcommands
        
        mode = '_mode=tri'
        minedgelength = '_minedgelength=' + meshValue
        maxedgelength = '_maxedgelength=' + meshValue
        ridgeangle = '_ridgeangle=20'
        maxgradation = '_maxgradation=1'
        deleteinput = '_deleteinput=Yes'
        
        gsurfOptions = mode + minedgelength + maxedgelength + ridgeangle + maxgradation + deleteinput
        
        #gvol options
        mode = '_mode=test '
        outputformat = '_outputformat=3DEC '
        
        gvolOptions = mode + outputformat
        
        layers = rs.LayerNames()
        for layer in layers:
            if layer == 'concrete':
                               
                rs.Command("-_SelLayer " + layer)
                rs.Command("_Enter")
                rs.Command("-_Mesh _DetailedOptions _AdvancedOptions " + advOptions + '_Enter _Enter')
                rs.Command("-_SelMesh")
                rs.Command("-_Gsurf " + gsurfOptions + '_Enter _Enter')
                rs.Command("-_SelMesh")
                rs.Command("-_Gvol " + gvolOptions + '_Enter _Enter')
    
        #save filename
          
        shutil.move('Gvol.3ddat', filename + '_deformable.3ddat')

        success = umc.saveAs(directory, filename, ".3dm")
        if not (success):
            break

        #umc.meshing(meshValue)
        #open a new file
        if k < len(kList) + 1:
            success = umc.new()
            if not (success):
                break
        k = k + 1
    j = j + 1
    k = 0

             
