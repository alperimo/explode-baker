import mset

mywindow = mset.UIWindow("Explode Baker")
mywindow.width = 600

suffixes_lowpoly = ["_LP", "_lowpoly", "_low"]
suffixes_highpoly = ["_HP", "_highpoly", "_high"]

previousSliderValue = 0

bakeGroups = {}

def moveToBakeGroup(bakeProject, obj, polyType):
    global bakeGroups
    
    groupName = obj.name
    if (groupName not in bakeGroups):
        bakeGroups[groupName] = bakeProject.addGroup(groupName)
        
    bakeGroup = bakeGroups[groupName]
    low_high_objects = bakeGroup.getChildren()
        
    if polyType == "low":
        subdivision_level_for_lowpoly = subDivisionLevel.value
        
        low_poly_object = low_high_objects[1]
        obj.subdivisionLevel = subdivision_level_for_lowpoly
        obj.parent = low_poly_object
    else:
        high_poly_object = low_high_objects[0]
        obj.parent = high_poly_object

def prepareGroups():
    global bakeGroups
    bakeGroups = {}
    
    def checkIfObjectIsPoly(obj):
        for suffix in suffixes_lowpoly:
            if (suffix in obj.name):
                return True
            
        for suffix in suffixes_highpoly:
            if (suffix in obj.name):
                return True
            
        return False
    
    subdivision_level_for_lowpoly = subDivisionLevel.value
    
    # Create a bake project
    bakeProject = mset.BakerObject()
    bakeProject.name = "Bake Project"
    
    # Get the selected objects
    objects = mset.getAllObjects()
    for obj in objects:
        if (type(obj) == mset.MeshObject and checkIfObjectIsPoly(obj)):
            splittedName = obj.name.split("_")
            if (splittedName[0] not in bakeGroups):
                bakeGroups[splittedName[0]] = bakeProject.addGroup(splittedName[0])
                
            bakeGroup = bakeGroups[splittedName[0]]
            low_high_objects = bakeGroup.getChildren()
                
            obj_suffix = "_"+splittedName[-1]
            print(obj_suffix)
            if (obj_suffix in suffixes_lowpoly):
                low_object = low_high_objects[1]
                obj.subdivisionLevel = subdivision_level_for_lowpoly
                obj.parent = low_object
                
            elif (obj_suffix in suffixes_highpoly):
                high_object = low_high_objects[0]
                obj.parent = high_object
                
def prepareFromBakeProject():
    global bakeGroups
    bakeGroups = {}
    
    all_scene_objects = mset.getAllObjects()
    for obj in all_scene_objects:
        if (type(obj) == mset.BakerObject):
            bakerProject = obj
            bakeGroup = bakerProject.getChildren()[0]
            low_high_objects = bakeGroup.getChildren()
            low_poly_objects = low_high_objects[0].getChildren()
            high_poly_objects = low_high_objects[1].getChildren()
            
            for low_poly_object in low_poly_objects:
                moveToBakeGroup(bakerProject, low_poly_object, "low")
                
            for high_poly_object in high_poly_objects:
                moveToBakeGroup(bakerProject, high_poly_object, "high")
                
            break

def explodeAll():
    global previousSliderValue
    sliderValueDiff = sliderFloat.value - previousSliderValue
    previousSliderValue = sliderFloat.value
    print(sliderValueDiff)
    
    all_scene_objects = mset.getAllObjects()
    for obj in all_scene_objects:
        if (type(obj) == mset.BakerObject):
            bakeGroups = obj.getChildren()
            
            totalBakeGroups = len(bakeGroups)
            translation = []
            
            min = 0
            if (totalBakeGroups % 2 == 0):
                min = -sliderValueDiff * (totalBakeGroups / 2)
                totalBakeGroups += 1
            else:
                min = -sliderValueDiff * ((totalBakeGroups - 1) / 2)
            
            for i in range(0, totalBakeGroups):
                translation.append(min)
                min += sliderValueDiff
            
            if len(bakeGroups) % 2 == 0:
                middleElementIndex = len(translation) // 2
                del translation[middleElementIndex]
            
            for index, bakeGroup in enumerate(bakeGroups):
                pos = bakeGroup.position
                bakeGroup.position = [pos[0] + translation[index], pos[1], pos[2]]
    
subDivisionLevel = mset.UITextFieldInt()
subDivisionLevel.value = 1

collector = mset.UIButton("From suffixs")
collector.onClick = prepareGroups

collectorType2 = mset.UIButton("From High/Low Project")
collectorType2.onClick = prepareFromBakeProject

sliderFloat = mset.UISliderFloat()
sliderFloat.min = 0
sliderFloat.max = 1000
sliderFloat.value = previousSliderValue
sliderFloat.onChange = explodeAll

#add the button to the window
mywindow.addElement( collector )
mywindow.addElement( collectorType2 )
mywindow.addElement( subDivisionLevel )
mywindow.addElement( sliderFloat )
