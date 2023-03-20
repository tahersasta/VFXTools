########################################################################################################################
#
#ToolEngine main module
#this main module provides functions to create the main panels
#
########################################################################################################################
import nuke 
import ToolEngine.src.toolhelper as toolhelper
import ToolEngine.src.config as config
import os 
import json

def add_toolset():
	"""
		create new toolset 
		return: None
	"""
	sel = nuke.selectedNodes()
	print(sel)
	if (len(sel) == 0):
		nuke.message("Please select some nodes")
		return 
	p = nuke.Panel("Add Tool Set")
	p.setWidth(400)
	p.addSingleLineInput("Name: ","")
	category_default = "----select_one_category----"
	categories=toolhelper.get_tools(toolhelper.load_settings()["tools_root"])
	categories.insert(0,category_default)
	categories.append(config.TOOLS_TEMP.upper())
	p.addEnumerationPulldown("Category: "," ".join(categories))


	if p.show():
		if p.value("Name: ")!="":
			if p.value("Category: ") != category_default:
				toolset_full_path = os.path.join(toolhelper.load_settings()['tools_root'],p.value("Category: "),"{}.nknc".format(p.value("Name: ")))
				print(toolset_full_path)
				if os.path.isfile(toolset_full_path):
					if not nuke.ask("The toolset '{}' already exists. Do you want to overwrite it?".format(toolset_full_path)):
						return
				#write toolset 
				nuke.nodeCopy(toolset_full_path)
				nuke.message("Successfully added toolset '{}/{}'".format(p.value("Category: "),p.value("Name: ")))
				toolhelper.reload_tools_menu(notify=False)
			else:
				nuke.message("Please choose a category")
		else:
			nuke.message("Please enter a toolset name")

def show_settings():
	"""
		show settintgs window
		return: None
	"""
	settings = toolhelper.load_settings()
	p=nuke.Panel("Tool Engine Settings")
	p.setWidth(600)
	p.addFilenameSearch("tools root: ",settings['tools_root'])

	if p.show():
		settings['tools_root'] = p.value("tools root: ")

		with open(config.PATH_SETTINGS_FILE,'w') as f:
			json.dump(settings,f)

		toolhelper.reload_tools_menu(notify=False)

def show_info():
	"""
		show info window 
		return:None
	"""
	info_file = os.path.normpath(os.path.join(os.path.dirname(__file__),"../","data","info.json"))

	if not os.path.isfile(info_file):
		print("ToolEngine: info file doesnt exist")
		return 
	with open(info_file,"r") as f:
		info_data = json.load(f)

	logo = os.path.normpath(os.path.join(os.path.dirname(__file__),"../","img","logo.png"))
	nuke.message("<img src='{}' style = 'float:right;'/><h1>Tool Enginev{}</h1>\n\n{}".format(logo,info_data["version"],info_data["info"]))

