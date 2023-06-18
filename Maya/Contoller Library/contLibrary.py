######################################################################################################################################################
#
#Adds the Functionality to the UI 
#
#########################################################################################################################################################

from maya import cmds
import os
import json
import pprint


USERAPPDIR = cmds.internalVar(userAppDir=True)

DIRECTORY = os.path.join(USERAPPDIR, 'contLibrary')



def createDirectory(directory=DIRECTORY):
    """
    Creates a directory if it doesn't exist
    :param directory: The directory to create

    """
    if not os.path.exists(directory):
        os.mkdir(directory)
        print("Library Created")

class ControllerLibrary(dict):
        
    def save(self,name,directory=DIRECTORY,screenshot=True, **info):
        """
            Saves the selected contoller to the device 
            :param dict: Dictionary with the name and path 
        """
        createDirectory(directory)
        path=os.path.join(directory,'%s.ma' %name)
        infoFile = os.path.join(directory,'%s.json' %name )
        info['name'] = name
        info['path'] = path

        cmds.file(rename=path)
        if cmds.ls(selection=True):
            cmds.file(force=True,type='mayaAscii',exportSelected=True)
        else:
            cmds.file(save=True, type='mayaAscii',force=True)

        if screenshot:
            info['screenshot']=self.saveScreenshot(name,directory)

        with open(infoFile,'w') as f:
            json.dump(info,f,indent=4)

        self[name]=info

    def find(self,directory=DIRECTORY):
        """
            To check whether a file exists 
            ;param directory: The directory of the controller
            ;return:None
        """
        self.clear()

        if not os.path.exists(directory):
            return

        files = os.listdir(directory)

        mayaFiles = [f for f in files if f.endswith('.ma')]


        for ma in mayaFiles:

            name,ext = os.path.splitext(ma)
            path = os.path.join(directory,ma)
            infoFile = '%s.json' %name
            if infoFile in files:
                infoFile = os.path.join(directory,infoFile)

                with open(infoFile,'r') as f:
                    info = json.load(f)

            else:
                info ={}

            info['name'] = name
            info['path']=path

            screenshot = '%s.jpg' %name

            if screenshot in files:
                info['screenshot'] = os.path.join(directory,name)
            self[name]=info



    def load(self,name):
        """
            Load the file that is selected by the user 
            ;param name:name of the controller to be loaded
            ;return:None
        """
        path= self[name]['path']
        cmds.file(path,i=True, usingNamespaces=False)

    def saveScreenshot(self,name,directory=DIRECTORY):
        """
            Saves a screenshot of the controller to be loaded in the UI 
            ;param name:Name of the controller 
            ;param directory:Directory of the controller
            ;return the path of the screenshot
        """
        path = os.path.join(directory,'%s.jpg' %name)
        cmds.viewFit()
        cmds.setAttr("defaultRenderGlobals.imageFormat",8)
        cmds.playblast(completeFilename=path, forceOverwrite = True, format='image',
                       width = 200, height = 200, showOrnaments = False ,
                       startTime = 1, endTime =1,viewer=False)

        return path
