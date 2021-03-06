# generate3DEC

## Introduction to the input script 
This is a python script that generates a single large input script for 3DEC which is comprised of multiple simulations. This input script uses .3ddat files which can be generated using .wrl files and the script wrl23ddat in generate3decModels. 

If a user has more than one geometry they would like to simulate in the single input script, they can use the iterator input option. For instance, if a user has multiple bases representing differential settlement that they would like to run in conjunction with the same masonry wall on top, they can choose that their iterator is `"base"`. This iterator is taken from the last portion of the file name. So in my folder, I would have a file called test_base.3ddat. If they would like to switch out multiple concrete cores, and stone walls, and bricks and keep the base the same, the iterator input would be `"concrete, stone, brick"`.

A user can choose what type of cycling they want for their simulations. Currently this works with loop which uses cycloop, ratio which is for a solveRatio, and test which is for when you dont actually need it to cycle and you are just testing that your geometry will load in fine. 

`functionHandles = []` defines the auxilary functions you would like to add to your input script. The following are the auxillary functions currently supported:
* `getDisplacement`
* `getStress`
* `getCracks`
* `getFinalCentroid`
* `getVolume`
* `getInitCentroid`
* `getInitVert`
* `getFinalVert`
* `getNeighbors`
* `getCrackData`

`movieHandles = []` defines the auxilary movie functions to add. The following are the auxilary movie files:
* `makeMoviePlots`
* `makeCrackPlots`

`plots = []` defines the plots that can be made so that movies can be generated later. Here are the following supported plot types:
* `displacement`
* `xdisplacement`
* `ydisplacement`
* `zdisplacement`
* `smaximum`
* `sminimum`

The materials, as generated by the material class, are defined in the subsequent section. Here is an example of the input: 
`materialName = gen.material({'dens':2500, 'fixity':fix', 'ymod': 18e9, 'edge':0.3})`.
Here `dens` is density of the material, `fixity` is a binary is it fixed or not, `ymod` is young's modulus for the material, `edge` is used if the material is supposed to be deformable--the specifies what gen edge command should be used. 

The joint materials are added in a similar way: 
`jointMaterialName = gen.jointMaterial({'jkn':1e9, 'jfric':43, 'jks': 1e9, 'jcoh':0.3,'jten':0.3})`.

To pass the variables into the function from the input script, you use the `my_experiment = gen.experiment(...)`
The following variables are positional arguments and must come at the beginnging of the variable pass:
* `filePath`
* `functionPath`
* `outFileName`
* `cycChoice`
* `functionHandles`
* `movieHandles`
* `plots`
* `solveRatio`

The following variables are optional keyword arguments and can come in any order, if at all
* `movieInterval`
* `numCycLoops`
* `numCycles`
* `arraySize`
* `threshold`
* `boundLoad`
* `loadLocation` For loadLocation, it goes bound VALUE range YYY; where YYY can be `group GROUPNAME`or `x XCOORD y YCOORD z ZCOORD`
* `loadOrientation` This refers to x, y, or z.
* `eqVertices` This is how many vertices the load will be applied on

Then the materials are applied to specific geometries using the `my_experiment.addGeometry('nameofGeometry', nameMaterial, nameJointmaterial)`


## How to apply loads in the input script
### Dead load
Dead loads are automatically applied in 3DEC when gravity is turned on. Therefore, nothing else needs to be added. 

###Earthquake load
When passing the keyword arguments into `my_experiment = gen.experiment(...)` you will be using `eqVertices`, `eqFW`, `eqScale`, `eqDirection`. You can just add these keywords to the pass through my_experiment. `eqVertices` is the number of vertices this load will be applied to. You can do this by applying a load of 0 to the area of interest in 3DEC. Then in the console it should say how many vertices it is.`eqFW` is the FW of the building (volume * density * 9.8).The sign of `eqFW`is what denotes the direction of an earthquake. For instance if x is the direction and `eqFW` is positive, it will be applied to the right; if x is the direction and `eqFW` is negative, it will be applied to the left. The same is true for y: `eqFW` positive denotes into the screen, `eqFW` negative denotes out of the screen.  `eqScale` is how you control what scale of an earthquake it is 0.1g or 0.2g for example. You would just put in 0.1 or 0.2 though, the g is accounted for in the `eqFW` calculation. `eqDirection` denotes x or y for in- or out-of-plane earthquake motion. 

###Settlement load
This is done by passing bases with a particular geometry. There are not commands associated with this. 

###Distributed load
At the moment, to apply a distributed load, you need to figure out how many vertices you will be applying it to first. You can do this by applying a load of 0 to the area of interest in 3DEC. Then in the console it should say how many vertices it is. Then you can apply the distributed load using 'group GROUPNAME'or 'x XCOORD y YCOORD z ZCOORD'. 

###Combination load
All of the loads above are already combined with the dead load of the structure. To combine earthquake and settlement, just iterate over the base while you run the earthquake. 
To combine earthquake and distributed load, you can put multiple loads in `boundLoad` as long as they are separated with commas. Then the information corresponding to each load should be found in the same order in `loadLocation` and `loadOrientation`. 
