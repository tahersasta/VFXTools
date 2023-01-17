from maya import cmds

#Dictionary to derive names from
SUFFIXES = {
    "mesh":"gem",
    "joint":"jnt",
    "camera": None,
    "directionalLight":"dlgt",
    "ambientLight":"algt"
}

DEFAULT_SUFFIX = "grp"

def ren(selection=False):
    """
    This function will rename any objects to have the correct suffix
    Args:
        selection: Whether or not we use the current selection

    Returns:
        A list of all the objects we operated on
    """
    #list all the commands , selection tells whether an object is selected and visible in the ouliner and lists their long name

    objects = cmds.ls(selection =selection, dag=True, long=True)

    # this function cannot run if there is no selection and no objects
    # spits error in case the user return selection True without selecting anything
    if selection and not objects:
        raise RuntimeError("You diont have anything selected! How dare you?!")
    # iterates through the list of selection to find the object name and type
    for obj in objects:
        shortName = (obj.split("|")[-1])
        # to find the children of objects when they are parented
        children = cmds.listRelatives(obj , children = True, fullPath = True) or []

        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)
        #gets the suffix of the obj depending on its type
        suffix = SUFFIXES.get(objType,DEFAULT_SUFFIX)

        #incase of cameras
        if not suffix:
            continue

        #incase it already has a suffix
        if obj.endswith('_' + suffix):
            continue

        #adding the new name to the old name
        newName = "%s_%s" % (shortName, suffix)
        cmds.rename(obj,newName)

        index =objects.index(obj)
        objects[index] = obj.replace(shortName,newName)

    return objects