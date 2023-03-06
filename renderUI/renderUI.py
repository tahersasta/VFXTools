from Qt import QtWidgets,QtCore,QtGui 
from PySide2 import QtWidgets,QtCore,QtGui 
from maya import cmds 
import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup

import main
import stacked
import importlib
importlib.reload(stacked)
import stackedCollection
importlib.reload(stackedCollection)
importlib.reload(main)
import showSpecific
importlib.reload(showSpecific)

rs = renderSetup.instance()


def createShader(shaderType,nameShader):
	""" Create a shader of the given type"""
	
	shaderName = cmds.shadingNode(shaderType, asShader=True, n = nameShader )
	sgName = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=(shaderName + "SG"))
	cmds.connectAttr(shaderName + ".outColor", sgName + ".surfaceShader")
	return (shaderName, sgName)
	
class mainUI(QtWidgets.QDialog,main.Ui_Form):	
	def __init__(self):
		super(mainUI,self).__init__()
		self.setupUi(self)
		self.layerDisplay(self)
		self.pushButton.clicked.connect(self.load)
		self.listView.itemClicked.connect(self.collectionDisplay)
		self.listView_2.itemClicked.connect(self.overrideDisplay)
		self.pushButton_2.clicked.connect(self.edit)
		self.pushButton_3.clicked.connect(self.confirmation)
		self.listView.itemClicked.connect(self.show_checkBox)
		self.checkBox.stateChanged.connect(self.setRender)
		self.pushButton_4.clicked.connect(self.addCollection)
		self.checkBox_1.stateChanged.connect(self.setVisibleRender)
		self.pushButton_5.clicked.connect(self.showSpecific)		

		for i in range(self.listView.count()):
			r1 = rs.getRenderLayer(self.listView.item(i).text())
			if r1.isRenderable():
				self.listView.item(i).setBackground(QtGui.QColor('Green'))
			else:
				self.listView.item(i).setBackground(QtGui.QColor('Red'))
	
			

	def confirmation(self, *args):
		reply = QtWidgets.QMessageBox.question(self,"Confirmation", "For this code to work your scene should be setup a certian way , where your objects have to be inside a group called 'geo' , your environments objects such as projection planes should be inside a group called 'env' and all your lights should be inside a group called 'lgt' . Have you organised yout Scene")
		if reply == QtWidgets.QMessageBox.Yes:
			checkList = ['geo', 'env' , 'lgt']
			sel = cmds.ls(type='transform')
			if set(checkList).issubset(set(sel)):
				self.automate(self)
			else:
				QtWidgets.QMessageBox.warning(self,"Error","Please arrange the scene as stated in the instructions")
		elif reply == QtWidgets.QMessageBox.No:
			pass

	def layerDisplay(self,*args):
		self.listView.clear()
		children = rs.getChildren()
		for layer in children:
			self.listView.addItem(layer.name())
		for i in range(self.listView.count()):
			r1 = rs.getRenderLayer(self.listView.item(i).text())
			if r1.isRenderable():
				self.listView.item(i).setBackground(QtGui.QColor('Green'))
			else:
				self.listView.item(i).setBackground(QtGui.QColor('Red'))

	def collectionDisplay(self,*args):
		self.listView_2.clear()
		children = rs.getRenderLayer(self.listView.currentItem().text())
		collections = children.getCollections()
		for collection in collections:
			self.listView_2.addItem(collection.name())
	def overrideDisplay(self,*args):
		self.listView_3.clear()
		r1 = rs.getRenderLayer(self.listView.currentItem().text())
		c1 = r1.getCollections()
		for c in c1:
			if c.name() == self.listView_2.currentItem().text():
				c2 = c.getCollections()
				o1 = []
				for sub in c2:
					o1.append(sub.getOverrides())
				o2 = []
				for o in o1:
					for i in o:
						o2.append(i.name())
				try :
					self.listView_3.addItems(o2)
				except:
					self.listView_3.clear()
		
	def addCollection(self, *args):
		if self.listView.selectedItems():
			initvalues=[False]
			dialog = collectionUI(initvalues)
			if dialog.exec_():
				obj  = " "
				QtWidgets.QMessageBox.warning(self,"Message","Worked")
				rsult=dialog.createLayerCollection(self)
				r1 = rs.getRenderLayer(self.listView.currentItem().text())
				c1 = r1.createCollection(rsult[0])
				for i in rsult[1]:
					obj = obj + " "+ i
				c1.getSelector().setPattern(obj)
				o1 = []
				child = cmds.listRelatives(rsult[1][0],ad=True)
				l = dialog.lenAttr(self)
				for i in range(l):
					o1.append(c1.createAbsoluteOverride(child[0],rsult[2][i]))
					o1[i].setAttrValue(True)
				s = dialog.shaderSelected(self)
				if s:
					createShader(rsult[3],rsult[4])
					so = c1.createOverride(rsult[4],"shaderOverride")
					so.setShader(rsult[4])
				self.collectionDisplay()
		
		else:
			QtWidgets.QMessageBox.warning(self,"Error","Please select a Layer to add the collection")	
	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Delete:
			current_item = self.listView.currentItem()
			current_collection = self.listView_2.currentItem()
			current_override = self.listView_3.currentItem()
			r1 = rs.getRenderLayer(current_item.text())
			if current_item is not None and current_collection is None:
				self.listView.takeItem(self.listView.row(current_item))
				renderLayer.delete(r1)
				self.listView_2.clear()
			elif current_collection is not None and current_override is None:
				self.listView_2.takeItem(self.listView_2.row(current_collection))
				c1 = r1.getCollections()
				c = [x for x in c1 if x.name() == current_collection.text()]
				collection.delete(c[0])
			elif current_override is not None:
				self.listView_3.takeItem(self.listView_3.row(current_override))
				o1 = []
				c1 = r1.getCollections()
				for c in c1:
					if c.name() == self.listView_2.currentItem().text():
						c2 = c.getCollections()
						for sub in c2:
							o1=sub.getOverrides()
							for o in o1:
								if o.name() == current_override.text():
									override.delete(o)

	def setRender(self,*args):
		r1 = rs.getRenderLayer(self.listView.currentItem().text())
		if not self.checkBox.isChecked():
			r1.setRenderable(False)
			r1.setLabelColor('Red')
			self.listView.currentItem().setBackground(QtGui.QColor('Red'))
		else:
			r1.setRenderable(True)
			r1.setLabelColor('Green')
			self.listView.currentItem().setBackground(QtGui.QColor('Green'))
	def setVisibleRender(self, *args):
		r1 = rs.getRenderLayer(self.listView.currentItem().text())
		if self.checkBox_1.isChecked():
			rs.switchToLayer(r1)


	def show_checkBox(self,*args):
		self.checkBox.setHidden(False)
		self.checkLabel.setHidden(False)
		self.checkBox_1.setHidden(False)
		self.checkLabel_1.setHidden(False)
		
		r1 = rs.getRenderLayer(self.listView.currentItem().text())
		if r1.isRenderable():
			self.checkBox.setChecked(True)
		else:
			self.checkBox.setChecked(False)
		if r1.isVisible():
			self.checkBox_1.setChecked(True)
		else:
			self.checkBox_1.setChecked(False)
		self.pushButton.setGeometry(QtCore.QRect(56, 424, 151, 41))
		self.pushButton_2.setGeometry(QtCore.QRect(286, 424, 151, 41))
		self.pushButton_3.setGeometry(QtCore.QRect(516, 424, 151, 41))
		self.pushButton_4.setGeometry(QtCore.QRect(286, 474, 151, 41))
		self.pushButton_5.setGeometry(QtCore.QRect(56, 474, 151, 41))
	def edit(self):
		if self.listView_2.selectedItems():
			initvalues=[True,self.listView.currentItem().text(),self.listView_2.currentItem().text()]
			dialog = collectionUI(initvalues)
			if dialog.exec_():
				obj  = " "
				QtWidgets.QMessageBox.warning(self,"Message","Collection Created")
				rsult=dialog.createLayerCollection(self)
				r1 = rs.getRenderLayer(self.listView.currentItem().text())
				oldCollection = r1.getCollections()
				for c in oldCollection:
					if c.name() == self.listView_2.currentItem().text():
						collection.delete(c)
				c1 = r1.createCollection(rsult[0])
				for i in rsult[1]:
					obj = obj + " "+ i
				c1.getSelector().setPattern(obj)
				o1 = []
				child = cmds.listRelatives(rsult[1][0],ad=True)
				l = dialog.lenAttr(self)
				for i in range(l):
					o1.append(c1.createAbsoluteOverride(child[0],rsult[2][i]))
					o1[i].setAttrValue(True)
				s = dialog.shaderSelected(self)
				if s:
					createShader(rsult[3],rsult[4])
					so = c1.createOverride(rsult[4],"shaderOverride")
					so.setShader(rsult[4])
				self.collectionDisplay()
		
		else:
			QtWidgets.QMessageBox.warning(self,"Error","Please select a collection to be edited")

	def automate(self,*args):
		aovs = cmds.ls(type="aiAOV")
		for a in aovs:
			cmds.setAttr(a+'.enabled',0)
		r1 = rs.createRenderLayer('Beauty')
		c1 = r1.createCollection('geo')
		c1.getSelector().setPattern('geo')
		c2=r1.createCollection('lgts')
		c2.getSelector().setPattern('lgt')
		c3=r1.createCollection('env')
		c3.getSelector().setPattern('env')
		rel1 = cmds.listRelatives('env',ad=1)
		o=c3.createAbsoluteOverride(rel1[0],'primaryVisibility')
		o.setAttrValue(False)
		

		aov_collection = r1.aovCollectionInstance()
		aov_name = cmds.ls(type="aiAOV")
		for a in range(len(aov_name)):
			aov = aov_name[a][6:]
			sub_colle = collection.create(r1.name()+'_'+aov, collection.AOVChildCollection.kTypeId, aovName=aov)
			aov_collection.appendChild(sub_colle)
			override = sub_colle.createAbsoluteOverride('aiAOV_'+aov, 'enabled')  #(aov name, attr name)
			override.setAttrValue(1)  # override value
			override.setName(r1.name()+'_'+aov)


		r2 = rs.createRenderLayer('Shadow')
		c4 = r2.createCollection('geo')
		c4.getSelector().setPattern('geo')
		rel = cmds.listRelatives('geo',ad=1)
		o1 = c4.createAbsoluteOverride(rel[0],'primaryVisibility')
		o1.setAttrValue(False)
		c5=r2.createCollection('lgts')
		c5.getSelector().setPattern('lgt')
		c6=r2.createCollection('env')
		c6.getSelector().setPattern('env')
		createShader('aiShadowMatte','shadow')
		so = c6.createOverride('shadow',"shaderOverride")
		so.setShader('shadow')
		rel1 = cmds.listRelatives('env',ad=1)
		o2=c6.createAbsoluteOverride(rel1[0],'primaryVisibility')
		o2.setAttrValue(True)



		r3 = rs.createRenderLayer('Reflection')
		c7 = r3.createCollection('geo')
		c7.getSelector().setPattern('geo')
		rel = cmds.listRelatives('geo',ad=1)
		o3 = c7.createAbsoluteOverride(rel[0],'primaryVisibility')
		o3.setAttrValue(False)
		c8=r3.createCollection('lgts')
		c8.getSelector().setPattern('lgt')
		c9=r3.createCollection('env')
		c9.getSelector().setPattern('env')
		createShader('aiStandardSurface','reflect')
		so1 = c9.createOverride('reflect',"shaderOverride")
		so1.setShader('reflect')
		rel1 = cmds.listRelatives('env',ad=1)
		o4=c9.createAbsoluteOverride(rel1[0],'primaryVisibility')
		o4.setAttrValue(True)
		cmds.setAttr('reflect.baseColor',0 , 0 ,0,type = 'double3')


		r4 = rs.createRenderLayer('Occlusion')
		c10 = r4.createCollection('geo')
		c10.getSelector().setPattern('geo')
		o5 = c10.createAbsoluteOverride(rel[0], 'primaryVisibility')
		o5.setAttrValue(False)
		c11 = r4.createCollection('env')
		c11.getSelector().setPattern('env')
		createShader('aiAmbientOcclusion', 'occlusion')
		so1 = c11.createOverride('occlusion', "shaderOverride")
		so1.setShader('occlusion')
		rel1 = cmds.listRelatives('env',ad=1)
		o6=c11.createAbsoluteOverride(rel[0],'primaryVisibility')
		o6.setAttrValue(True)

		r1.setLabelColor('Green')
		r2.setLabelColor('Green')
		r3.setLabelColor('Green')
		r4.setLabelColor('Green')
		self.layerDisplay(self)
	def load(self):
		dialog = beautyUI()
		uin = dialog.exec_()
		self.layerDisplay(self)
		return uin 
	def showSpecific(self, *args):
		projDict = {
		"Stranger Things" : {"width" : 1080,"height":1920},
		"Black Panther" : {"width" : 1080,"height":2048},
		"Wednesday" : {"width" : 900,"height":1440},
		"Superman" : {"width":3840 , "height":2160},
		}
		dialog = projList()
		if dialog.exec_():
			item,check = dialog.load()
			cmds.setAttr("defaultRenderGlobals.imageFilePrefix" ,"<scene>/<version>/<RenderPass>",type = "string")
			cmds.setAttr( 'defaultArnoldDriver.ai_translator', 'exr', type='string' )
			cmds.setAttr('defaultResolution.width',projDict[item]['width'])
			cmds.setAttr('defaultResolution.height',projDict[item]['height'])
			cmds.setAttr('defaultArnoldRenderOptions.motion_blur_enable',1)
			cmds.setAttr('frontShape.renderable', False)
			cmds.setAttr('perspShape.renderable', False)
			cmds.setAttr('sideShape.renderable', False)
			cmds.setAttr('topShape.renderable', False)
			cmds.setAttr('shotCamShape.renderable', True)
			if check == "Low":
				cmds.setAttr("defaultArnoldRenderOptions.AASamples",4)
				cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples",1)
				cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples",1)
				cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples",1)
				cmds.setAttr("defaultArnoldRenderOptions.GISssSamples",1)
				cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples",1)
			elif check == "High":
				cmds.setAttr("defaultArnoldRenderOptions.AASamples",6)
				cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples",2)
				cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples",2)
				cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples",2)
				cmds.setAttr("defaultArnoldRenderOptions.GISssSamples",2)
				cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples",2)

class projList(QtWidgets.QDialog,showSpecific.Ui_ProjectList):
	def __init__(self):
		super(projList,self).__init__()
		self.setupUi(self)
		projects = ['Stranger Things','Black Panther','Wednesday','Superman']
		self.projList.addItems(projects)	
		self.okBtn.clicked.connect(self.load)	
	def load (self,*args):
		if self.projList.currentItem() is not None and (self.lowSample.isChecked() or self.highSample.isChecked()) :
			self.accept()
			item = self.projList.currentItem().text()
			if self.lowSample.isChecked():
				check = "Low"
			elif self.highSample.isChecked():
				check="High"
			self.accept()
			return item,check
		else:
			QtWidgets.QMessageBox.warning(self,"Error","Please select both Project and Sample Settings")

class beautyUI(QtWidgets.QDialog,stacked.Ui_Form):
	def __init__(self):
		super(beautyUI,self).__init__()
		self.setupUi(self)
		self.nextpage1.clicked.connect(self.next)
		self.nextpage2.clicked.connect(self.next)
		self.nextpage3.clicked.connect(self.next)
		self.nextpage4.clicked.connect(self.next)
		self.finishBtn.clicked.connect(self.next)
		self.backpage2.clicked.connect(self.back)
		self.backpage3.clicked.connect(self.back)
		self.backpage4.clicked.connect(self.back)
		self.backpage5.clicked.connect(self.back)
		self.count = 0 
		self.search.textChanged.connect(self.Search)
		self.attrSearch.textChanged.connect(self.searchAttr)
		self.shaderSearch.textChanged.connect(self.searchShader)
		self.sel = cmds.ls(sl=0,dag=True)
		allSgs = ['aiStandardSurface','lambert','surfaceShader','Phong','Blinn','aiShadowMatte']
		for a in allSgs:
			self.shaderList.addItem(a)
		for s in self.sel:
			if cmds.objectType(s) == "transform":
					self.listView.addItem(s)
		self.form = []



	def back(self):
		if self.count == 1:
			self.count = self.count - 1
			self.stackedWidget.setCurrentIndex(self.count)
		elif self.count == 2:
			self.count = self.count - 1
			self.stackedWidget.setCurrentIndex(self.count)
		elif self.count == 3:
			self.count = self.count - 1
			self.stackedWidget.setCurrentIndex(self.count)
		elif self.count == 4:
			self.count = self.count - 1
			self.stackedWidget.setCurrentIndex(self.count)
		elif self.count == 5:
			self.count = self.count - 1
			self.stackedWidget.setCurrentIndex(self.count)
	def next(self):
		if self.count == 0:
			if self.layerNameLine.text() == "":
				QtWidgets.QMessageBox.warning(self,"Error","Please Enter a Layer Name")
			else:
				children = rs.getChildren()
				for layer in children:
					if layer.name() == self.layerNameLine.text():
						QtWidgets.QMessageBox.warning(self,"Error","A layer with the following name already exists")
						self.layerNameLine.setText(self.layerNameLine.text()+"1")
						return
				self.count = self.count + 1
				self.stackedWidget.setCurrentIndex(self.count)
				self.form.append(self.layerNameLine.text())
				return
		elif self.count == 1: 
			if self.collectionNameLine.text() == "":
				QtWidgets.QMessageBox.warning(self,"Error","Please Enter a collection Name")
			else:
				self.count = self.count + 1 
				self.stackedWidget.setCurrentIndex(self.count)
				self.form.append(self.collectionNameLine.text())
				return
		elif self.count ==2:
			if  not  self.listView.selectedItems():
				QtWidgets.QMessageBox.warning(self,"Error","Please select atleast one item to addd to the collection")
			else:
				self.count = self.count + 1 
				self.stackedWidget.setCurrentIndex(self.count)
				self.attr_List()
				sel = self.listView.selectedItems()
				shapes = []
				for i in sel:
					shapes.append(i.text())
				self.form.append(shapes)
				return
		elif self.count == 3:
			self.count = self.count + 1 
			self.stackedWidget.setCurrentIndex(self.count)
			ovs = self.attrList.selectedItems()
			overrides = []
			for i in ovs:
				overrides.append(i.text())
			self.form.append(overrides)
			return
		elif self.count == 4:
			if self.shaderList.selectedItems():
				self.form.append(self.shaderList.currentItem().text())
				if self.nameShader.text() == "":
					QtWidgets.QMessageBox.warning(self,"Error","Please Provide a name for the shader")
					return
				else:
					self.createLayerCollectionClose(self)
					reply = QtWidgets.QMessageBox.question(self,"Create Further Collection", "Do you want to create further collections for this layer?")
					if reply == QtWidgets.QMessageBox.Yes:
						self.createNewCollection(self)
					elif reply == QtWidgets.QMessageBox.No:
						QtWidgets.QDialog.close(self)
			else:
				self.createLayerCollectionClose(self)
				reply = QtWidgets.QMessageBox.question(self,"Create Further Collection", "Do you want to create further collections for this layer?")
				if reply == QtWidgets.QMessageBox.Yes:
					self.createNewCollection(self)
				elif reply == QtWidgets.QMessageBox.No:
						QtWidgets.QDialog.close(self)

	def createLayerCollectionClose(self, *args):
		children = rs.getChildren()
		for layer in children:
			if layer.name() == self.form[0]:
				return	

		aovs = cmds.ls(type="aiAOV")
		for a in aovs:
			cmds.setAttr(a+'.enabled',0)
		self.r1 = rs.createRenderLayer(self.form[0])
		self.r1.setLabelColor('Green')
		rs.switchToLayer(self.r1)
		c1 = self.r1.createCollection(self.form[1])
		obj =""
		for i in self.form[2]:
			obj = obj + " " + i
		c1.getSelector().setPattern(obj)
		o = []
		child = cmds.listRelatives(self.form[2][0],ad=True)

		for i in range(len(self.attrList.selectedItems())):
			o.append(c1.createAbsoluteOverride(child[0],self.form[3][i]))
			o[i].setAttrValue(True)
		if self.shaderList.selectedItems():
			createShader(self.form[4],self.nameShader.text())
			so = c1.createOverride(self.nameShader.text(),"shaderOverride")
			so.setShader(self.nameShader.text())
		if self.check.isChecked():
			aov_collection = self.r1.aovCollectionInstance()
			aov_name = cmds.ls(type="aiAOV")
			for a in range(len(aov_name)):
				aov = aov_name[a][6:]
				sub_colle = collection.create(self.r1.name()+'_'+aov, collection.AOVChildCollection.kTypeId, aovName=aov)
				aov_collection.appendChild(sub_colle)
				override = sub_colle.createAbsoluteOverride('aiAOV_'+aov, 'enabled')  #(aov name, attr name)
				override.setAttrValue(1)  # override value
				override.setName(self.r1.name()+'_'+aov)
	def createNewCollection(self, *args):
		initvalues = [False]
		dialog = collectionUI(initvalues)
		
		if dialog.exec_():
			obj  = " "
			QtWidgets.QMessageBox.warning(self,"Message","Collection Created")
			rsult=dialog.createLayerCollection(self)
			c1 = self.r1.createCollection(rsult[0])
			for i in rsult[1]:
				obj = obj + " "+ i
			c1.getSelector().setPattern(obj)
			o1 = []
			child = cmds.listRelatives(rsult[1][0],ad=True)
			l = dialog.lenAttr(self)
			for i in range(l):
				o1.append(c1.createAbsoluteOverride(child[0],rsult[2][i]))
				o1[i].setAttrValue(True)
			s = dialog.shaderSelected(self)
			if s:
				createShader(rsult[3],rsult[4])
				so = c1.createOverride(rsult[4],"shaderOverride")
				so.setShader(rsult[4])
		
		
	def searchShader(self,text):
		for i in range(self.shaderList.count()):
			if text.lower() in self.shaderList.item(i).text().lower():
				self.shaderList.item(i).setHidden( False)
			else:
				self.shaderList.item(i).setHidden(True)

	def Search(self,text):
		for i in range(self.listView.count()):
			if text.lower() in self.listView.item(i).text().lower():
				self.listView.item(i).setHidden( False)
			else:
				self.listView.item(i).setHidden(True)
	def searchAttr(self,text):
		for i in range(self.attrList.count()):
			if text.lower() in self.attrList.item(i).text().lower():
				self.attrList.item(i).setHidden( False)
			else:
				self.attrList.item(i).setHidden(True)

	def attr_List(self, *args):
		attrs = set()
		for i in self.listView.selectedItems():
			relObj = cmds.listRelatives(i.text(),ad=True)
			attrs.update(cmds.listAttr(relObj[0]))
		for x in attrs:
			self.attrList.addItem(x)




class collectionUI(QtWidgets.QDialog,stackedCollection.Ui_Form):
	def __init__(self,initvalues):
		super(collectionUI,self).__init__()
		self.setupUi(self)
		
		self.nextpage2.clicked.connect(self.next)
		self.nextpage3.clicked.connect(self.next)
		self.nextpage4.clicked.connect(self.next)
		self.finishBtn.clicked.connect(self.next)
		self.finishBtn.clicked.connect(self.accept)
		self.backpage3.clicked.connect(self.back)
		self.backpage4.clicked.connect(self.back)
		self.backpage5.clicked.connect(self.back)
		self.count = 0 
		self.formC=[]
		self.sel = cmds.ls(sl = 0 , dag=True)
		self.search.textChanged.connect(self.Search)
		self.attrSearch.textChanged.connect(self.searchAttr)
		self.shaderSearch.textChanged.connect(self.searchShader)
		self.values = initvalues
		for s in self.sel:
			if cmds.objectType(s) == "transform":
					self.listWidget.addItem(s)
		allSgs = ['aiStandardSurface','lambert','surfaceShader','Phong','Blinn','aiShadowMatte']
		for a in allSgs:
			self.shaderListCollection.addItem(a)
		if initvalues[0]:
			r1 = rs.getRenderLayer(initvalues[1])
			c1 = r1.getCollections()
			for c in c1:
				if c.name() == initvalues[2] :
					self.collectionNameLine.setText(initvalues[2])
					target_collection = renderSetup.instance().getRenderLayer(initvalues[1]).getCollectionByName(initvalues[2])
					objects_in_collection = target_collection.getSelector().getPattern()
					print(objects_in_collection)
					for i in range(self.listWidget.count()):
						if objects_in_collection.strip() == self.listWidget.item(i).text():
							self.listWidget.setCurrentItem(self.listWidget.item(i))
					c2 = c.getCollections()
					for sub in c2:
						if sub.name()[-15:] == '_shadingEngines':
							o1 = sub.getOverrides()
							o1Text=[]
							for o in o1 :
								o1Text.append(o.name())
							for i in range(len(o1Text))	:
								if o1Text[i][-1].isdigit():
									o1Text[i] = o1Text[i][:-1]
								theNode = cmds.nodeType(o1Text[0])
								for i in range(self.shaderListCollection.count()):
									if theNode == self.shaderListCollection.item(i).text():
										self.shaderListCollection.setCurrentItem(self.shaderListCollection.item(i))

		
	def lenAttr(self,*args):
		return len(self.attrListCollection.selectedItems())
	def shaderSelected(self,*args):
		return self.shaderListCollection.selectedItems()
	def next(self, *args):
		if self.count == 0:
			if self.collectionNameLine.text() == "":
				QtWidgets.QMessageBox.warning(self,"Error","Please Enter a Layer Name")
			else:
				self.count = self.count + 1
				self.stackedWidget.setCurrentIndex(self.count)
				self.formC.append(self.collectionNameLine.text())
				return
		elif self.count == 1:
			if  not  self.listWidget.selectedItems():
				QtWidgets.QMessageBox.warning(self,"Error","Please select atleast one item to addd to the collection")
			else:
				self.count = self.count + 1 
				self.stackedWidget.setCurrentIndex(self.count)
				self.attr_List()
				sel = self.listWidget.selectedItems()
				shapes = []
				for i in sel:
					shapes.append(i.text())
				self.formC.append(shapes)
				return
		elif self.count==2:
			self.count = self.count + 1 
			self.stackedWidget.setCurrentIndex(self.count)
			ovs = self.attrListCollection.selectedItems()
			overrides = []
			for i in ovs:
				overrides.append(i.text())
			self.formC.append(overrides)
			return
		elif self.count == 3:
			self.count = self.count + 1 
			self.stackedWidget.setCurrentIndex(self.count)
			if self.shaderListCollection.selectedItems():
				self.formC.append(self.shaderListCollection.currentItem().text())
				if self.nameShaderCollection.text() == "":
					QtWidgets.QMessageBox.warning(self,"Error","Please Provide a name for the shader")
					return
				else:
					self.formC.append(self.nameShaderCollection.text())
					self.createLayerCollection(self)

	def createLayerCollection(self,*args):
		return self.formC
		
	def back (self, *args):
		if self.count == 1:
			self.count = self.count - 1
			self.stackedWidget.setCurrentIndex(self.count)
		elif self.count == 2:
			self.count = self.count - 1
			self.stackedWidget.setCurrentIndex(self.count)
		elif self.count == 3:
			self.count = self.count - 1
			self.stackedWidget.setCurrentIndex(self.count)
		elif self.count == 4:
			self.count = self.count - 1
			self.stackedWidget.setCurrentIndex(self.count)
		elif self.count == 5:
			self.count = self.count - 1
			self.stackedWidget.setCurrentIndex(self.count)

	def searchShader(self,text):
		for i in range(self.shaderListCollection.count()):
			if text.lower() in self.shaderListCollection.item(i).text().lower():
				self.shaderListCollection.item(i).setHidden( False)
			else:
				self.shaderListCollection.item(i).setHidden(True)

	def Search(self,text):
		for i in range(self.listWidget.count()):
			if text.lower() in self.listWidget.item(i).text().lower():
				self.listWidget.item(i).setHidden( False)
			else:
				self.listWidget.item(i).setHidden(True)
	def searchAttr(self,text):
		for i in range(self.attrListCollection.count()):
			if text.lower() in self.attrListCollection.item(i).text().lower():
				self.attrListCollection.item(i).setHidden( False)
			else:
				self.attrListCollection.item(i).setHidden(True)
	def attr_List(self, *args):
		attrs = set()
		for i in self.listWidget.selectedItems():
			relObj = cmds.listRelatives(i.text(),ad=1)
			attrs.update(cmds.listAttr(relObj[0]))
		for x in attrs:
			self.attrListCollection.addItem(x)
		if self.values[0]:
			r1 = rs.getRenderLayer(self.values[1])
			c1 = r1.getCollections()
			for c in c1:
				if c.name() == self.values[2] :
					c2 = c.getCollections()
					for sub in c2:
						if sub.name()[-7:] == '_shapes':
							o1 = sub.getOverrides()
							o1Text=[]
							for o in o1 :
								o1Text.append(o.name())
							for i in range(len(o1Text))	:
								if o1Text[i][-1].isdigit():
									o1Text[i] = o1Text[i][:-1]

							print (o1Text)
							for i in range(self.attrListCollection.count()):
								item = self.attrListCollection.item(i)
								if item.text() in o1Text:
									print(item.text())
									item.setSelected(True)

def showUI():
	ui = mainUI()
	ui.show()
	return ui
