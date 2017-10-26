#works, suppresses dialog box

import rhinoscriptsyntax as rs
# iterates through layers
layers = rs.LayerNames() 
for layer in layers:
    
    if layer != 'concrete':
    
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
            #cmdstr += " Angle 0.0 AspectRatio 0.0 Distance 0.1 Density 0.1 Grid 0.0 "
            #cmdstr += " enter " 
                    
            #cmdstr += " Enter Enter"
        
        # execute command
        cmd = rs.Command(cmdstr)
        if not(cmd):
            success = False
            
        rs.Command("-_SelNone" )
        rs.Command("Show" )
    
