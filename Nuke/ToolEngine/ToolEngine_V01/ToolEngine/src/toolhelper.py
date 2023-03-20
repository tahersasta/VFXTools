########################################################################################################################
#
#Helper module
#this main module provides functionality for the main module
#
########################################################################################################################

import os 
import ToolEngine.src.config as config
import json 
import nuke

def reload_tools_menu(notify=True):
	"""
		advanced load_toolsfunction
		reload tools directory and scan for new toolsets
		If something is found display a mesaage
		@param notify: Bool if True show message when new tool is found
	"""
	all_tools_before = get_all_tools()
	print(all_tools_before)
	#reload tools dir
	load_tools()

	#save tools in the list after scanning
	all_tools_after = get_all_tools()
	print(all_tools_after)
	dif_list=[tool for tool in all_tools_after if tool not in all_tools_before]
	print(dif_list)
	dif_msg = "\n".join(dif_list)
	print(dif_msg)
	if notify and dif_msg != "":
		nuke.message("{} new tools found:\n\n{}".format(len(dif_list),dif_msg))

def get_all_tools():
	"""
		sacn tools dir and get a list of all the tools 
		assert that all tools are uppercase 
		:return:list of all tools

	"""
	all_tools = [] 

	for item in nuke.menu("Nodes").findItem("ToolEngine").items():
		#checks only for tools that are in uppercase 
		if item.name().isupper():
			#Iterate through each tool menu and save all its tools 
			tool_menu = nuke.menu("Nodes").findItem("{}/{}".format("ToolEngine",item.name()))
			try:
				for tool in tool_menu.items():
					all_tools.append("{}/{}".format(tool_menu.name(),tool.name()))
			except:
				continue
	return all_tools


def load_tools():
	"""
		load tools from root directory
		return : None
	"""
	settings = load_settings()
	build_tools_menu(settings["tools_root"])


def load_settings():
	"""
		load setting file and return values
		if settings file / folder doesnt exist then create it 
		reurns: dict settings data
	"""
	settings_file = config.PATH_SETTINGS_FILE

	if not os.path.isdir(os.path.dirname(settings_file)):
		os.makedirs(os.path.dirname(settings_file))

	if not os.path.isfile(settings_file):
		with open(settings_file,"w") as f:
			f.write('{"tools_root":""}')

	with open(settings_file,"r") as f:
		settings_data = json.load(f)

	return settings_data


def get_tools(tools_root):
	"""
		get a list of all tool categories 
		scan the tools_root for dirs 
		be loaded regarding to the config's TOOLSDIR_IGNORE AND TOOLS_TEMP values
		:param tools_root: String full path of tools root 
		:reutns: list of all categories 
	"""

	if not os.path.isdir(tools_root):
		return []

	tools_categories = [] 

	for item in os.listdir(tools_root):
		item_full_path = os.path.join(tools_root,item)
		if os.path.isdir(item_full_path) and item != config.TOOLS_TEMP and item not in config.TOOLSDIR_IGNORE:
			tools_categories.append(item)

	return tools_categories

def build_tools_menu(tools_root):
	"""
		scan tools_dir and dynamically build tools structure 
		:param tools_root: String full path of tools root 
		:return: None 
	"""
	if not os.path.isdir(tools_root):
		if tools_root == "":
			print("ToolEngine: tools_root not set. You can set it via 'ToolEngine->settings")
		else:
			print("ToolEngine: tools_root'{}' doesnt exist".format(tools_root))
		return
	te_menu = nuke.menu("Nodes").findItem("ToolEngine")
	#scan for tools dir 
	tools_categories= get_tools(tools_root)

	for category in tools_categories:
		category_menu = te_menu.addMenu(category.upper())

		#create toolsets
		item_full_path = os.path.join(tools_root,category)
		for tool in os.listdir(item_full_path):
			if os.path.splitext(tool)[1]==".nknc":
				toolset_path = os.path.join(item_full_path,tool)
				category_menu.addCommand(tool.replace(".nknc",""),lambda toolset_path = toolset_path: insert_toolset(toolset_path,delete=False))
	#temp tools 
	te_menu.addSeparator()
	temp_menu = te_menu.addMenu(config.TOOLS_TEMP.upper())

	#create temp toolsets
	temp_dir = os.path.join(tools_root,config.TOOLS_TEMP)
	if not os.path.isdir(temp_dir):
		os.makedirs(temp_dir)

	for tool in os.listdir(temp_dir):
		if os.path.splitext(tool)[1]==".nknc":
			toolset_path = os.path.join(tools_root,config.TOOLS_TEMP,tool)
			temp_menu.addCommand(os.path.splitext(tool)[0],lambda toolset_path=toolset_path: insert_toolset(toolset_path,delete=True))
def insert_toolset(toolpath,delete=False):

	"""
		insert toolset
		if it is a temp tool then the delete flag is set to True thus it will be removed after inserting 
		:param path: String full path of toolset 
		:param delete: is True delete the toolset after importing; default: False 
		:returns: None
	"""
	if not os.path.isfile(toolpath):
		nuke.message("The tool cannot be found")
		return 

	nuke.nodePaste(toolpath)

	if delete:
		#physically delete the toolset 
		os.remove(toolpath)
		#remove it from the toolset 
		toolset_name = os.path.splitext(os.path.basename(toolpath))[0]
		nuke.menu("Nodes").findItem("{}/{}".format("ToolEngine",config.TOOLS_TEMP.upper())).removeItem(toolset_name)
