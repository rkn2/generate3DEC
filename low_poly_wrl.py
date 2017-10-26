import rhinoscriptsyntax as rs
# iterates through layers

    
# select all in current layer
rs.Command("-_SelAll ")

directory = 'C:\\Users\\Rebecca Napolitano\\Documents\\datafiles\\Romanbondingcourses\\2017_10_25_experiments\\'

filename = 'test'
filetype = '.wrl'

# make cmdstr, include layer if there are multiple layers
path = "\"" + directory + filename + filetype + "\""
cmdstr = "-_Export " + path
if filetype == ".wrl":
    cmdstr += " Enter"
    cmdstr += " Angle 0.0 AspectRatio 0.0 Distance 0.0 Density 0.0 Grid 0.0 "
    cmdstr += " Enter "
            
    #cmdstr += " Enter Enter"

# execute command
cmd = rs.Command(cmdstr)
if not(cmd):
    success = False
    
rs.Command("-_SelNone")

#
#import rhinoscriptsyntax as rs
## iterates through layers
#layers = rs.LayerNames() 
#for layer in layers:
#    
#    # select layer
#    rs.Command("-_SelLayer " + layer)
#    
#    directory = 'C:\Users\Rebecca Napolitano\Documents\datafiles\Romanbondingcourses\2017_10_25_experiments\'
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
#        cmdstr += " Angle 0.0 AspectRatio 0.0 Distance 0.0 Density 0.0 Grid 0.0 "
#        cmdstr += " enter 
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
