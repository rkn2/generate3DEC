##works, suppresses dialog box
#
#import rhinoscriptsyntax as rs
## iterates through layers
#layers = rs.LayerNames() 
#for layer in layers:
#    
#    # select layer
#    rs.Command("-_SelLayer " + layer)
#    
#    directory = 'C:\\Users\\Rebecca Napolitano\\Documents\\datafiles\\Romanbondingcourses\\2017_10_25_experiments\\test2\\'
#    
#    filename = 'test'
#    filetype = '.wrl'
#    
#    # make cmdstr, include layer if there are multiple layers
#    if len(layers) > 1:
#        path = "\"" + directory + filename + "_" + layer + filetype + "\""
#    else:
#        path = "\"" + directory + filename + filetype + "\""
#    cmdstr = "-_Export " + path
#    if filetype == ".wrl":
#        cmdstr += " Enter"
#        cmdstr += " Angle 0.0 AspectRatio 0.0 Distance 0.1 Density 0.1 Grid 0.0 "
#        cmdstr += " enter " 
#                
#        #cmdstr += " Enter Enter"
#    
#    # execute command
#    cmd = rs.Command(cmdstr)
#    if not(cmd):
#        success = False
#        
#    rs.Command("-_SelNone")
#    
#___________________________________________________________________________________________

import rhinoscriptsyntax as rs
# iterates through layers
layers = rs.LayerNames() 
for layer in layers:
    
    # select layer
    rs.Command("-_SelLayer " + layer)
    
    directory = 'C:\\Users\\Rebecca Napolitano\\Documents\\datafiles\\Romanbondingcourses\\2017_10_25_experiments\\test2\\'
    
    filename = 'test'
    filetype = '.wrl'
    
    # make cmdstr, include layer if there are multiple layers
    if len(layers) > 1:
        path = "\"" + directory + filename + "_" + layer + filetype + "\""
    else:
        path = "\"" + directory + filename + filetype + "\""
    cmdstr = "_Export " + path
    #if filetype == ".wrl":
        #cmdstr += " Enter"
        #cmdstr += " Angle 0.0 AspectRatio 0.0 Distance 0.1 Density 0.1 Grid 0.0 "
        #cmdstr += " enter " 
                
        #cmdstr += " Enter Enter"
    
    # execute command
    cmd = rs.Command(cmdstr)
#    if not(cmd):
#        success = False
#        
    rs.Command("-_SelNone")
    
