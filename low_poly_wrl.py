#works, suppresses dialog box

import rhinoscriptsyntax as rs
# iterates through layers
layers = rs.LayerNames() 
for layer in layers:
    
    if layer != 'concrete': #can be altered to exclude anything in deformablekeys! 
    
        # select layer
        rs.Command("-_SelLayer " + layer)
        
        rs.Command("-_Mesh DetailedOptions SimplePlane=Yes Enter")
           
        directory = 'C:\\Users\\Rebecca Napolitano\\Documents\\datafiles\\Romanbondingcourses\\2017_10_26_experiments\\'
        
        filename = 'test'
        filetype = '.wrl'
        
        # make cmdstr, include layer if there are multiple layers
        if len(layers) > 1:
            path = "\"" + directory + filename + "_" + layer + filetype + "\""
        else:
            path = "\"" + directory + filename + filetype + "\""
        
        rs.Command("-_SelNone ")
        rs.Command("-_SelLayer " + layer)
        rs.Command("-_Invert ")
        rs.Command("Hide Enter")
        rs.Command("-_SelMesh ")
        cmdstr = "-_Export " + path
        if filetype == ".wrl":
            cmdstr += " Enter Enter"
        
        # execute command
        cmd = rs.Command(cmdstr)
        if not(cmd):
            success = False
            
        rs.Command("-_SelNone" )
        rs.Command("Show" )
    
