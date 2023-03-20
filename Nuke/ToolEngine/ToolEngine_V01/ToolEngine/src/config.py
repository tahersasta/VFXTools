import os 
#################################################################################
#
#User config file 
#
#################################################################################
#
#
#TOOLS_TEMP
#This is the folder and menu name for the temp tools as it will be displayed in nuke's menu 
TOOLS_TEMP = "TEMP"
#
#PATH SETTINGS FILE
#This is the path where we can find the ToolsEngines seeting json file 
PATH_SETTINGS_FILE = os.path.join(os.path.expanduser('~'),'.nuke','ToolEngine','settings.json')
#
#
#TOOLSDIR_IGNORE
#ignore these folders when building tools menu 
TOOLSDIR_IGNORE = []