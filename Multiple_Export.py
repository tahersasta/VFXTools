def exportAll():
    PATH = "C:/Users/TAHER/Desktop/Houdini/"
    obj = hou.node("/obj")
    children = obj.children()
    for child in children:
        nodeName = child.name()
        finalPath = PATH + nodeName + ".fbx"
        child.parm("sopoutput").set(finalPath)
        child.parm("execute").pressButton()
        