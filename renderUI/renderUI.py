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

rs = renderSetup.instance()


def createShader(shaderType,nameShader):
	""" Create a shader of the given type"""
	
	shaderName = cmds.shadingNode(shaderType, asShader=True, n = nameShader )
	sgName = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=(shaderName + "SG"))
	cmds.connectAttr(shaderName + ".outColor", sgName + ".surfaceShader")
	return (shaderName, sgName)
	
class mainUI(QtWidgets.QDialog,main.Ui_Form):
	def layerDisplay(self,*args):
		self.listView.clear()
		children = rs.getChildren()
		for layer in children:
			self.listView.addItem(layer.name())
	def collectionDisplay(self,*args):
		self.listView_2.clear()
		children = rs.getChildren()
		for layer in children:
			if layer.name() == self.listView.currentItem().text():
				collections = layer.getCollections()
				for collection in collections:
					self.listView_2.addItem(collection.name())
	def __init__(self):
		super(mainUI,self).__init__()
		self.setupUi(self)
		self.layerDisplay(self)
		self.pushButton.clicked.connect(self.load)
		self.listView.itemClicked.connect(self.collectionDisplay)
		self.pushButton_2.clicked.connect(self.edit)

	def edit(self):
		if self.listView_2.selectedItems():
			dialog = editUI()
			uin = dialog.exec_()
			return uin
		else:
			QtWidgets.QMessageBox(self,"Error","Please select a layer and a collection")

	def load(self):
		dialog = beautyUI()
		uin = dialog.exec_()
		self.layerDisplay(self)
		return uin 

class editUI(QtWidgets.QDialog,stacked.Ui_Form):		
	def __init__(self):
		super(editUI,self).__init__()
		self.setupUi(self)
		self.layerNameLine.setText()


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
		self.r1 = rs.createRenderLayer(self.form[0])
		rs.switchToLayer(self.r1)
		c1 = self.r1.createCollection(self.form[1])
		obj =""
		for i in self.form[2]:
			obj = obj + " " + i
		c1.getSelector().setPattern(obj)
		o = []
		print(self.form[2][0])
		child = cmds.listRelatives(self.form[2][0])
		print(child)
		return
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
				override.setAttrValue(0)  # override value
				override.setName(self.r1.name()+'_'+aov)
	def createNewCollection(self, *args):
		dialog = collectionUI()
		
		if dialog.exec_():
			obj  = " "
			QtWidgets.QMessageBox.warning(self,"Error","Worked")
			rsult=dialog.createLayerCollection(self)
			c1 = self.r1.createCollection(rsult[0])
			for i in rsult[1]:
				obj = obj + " "+ i
			c1.getSelector().setPattern(obj)
			o1 = []
			child = cmds.listRelatives(rsult[1][0])
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
	def __init__(self):
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
		for s in self.sel:
			if cmds.objectType(s) == "transform":
					self.listWidget.addItem(s)
		allSgs = ['aiStandardSurface','lambert','surfaceShader','Phong','Blinn','aiShadowMatte']
		for a in allSgs:
			self.shaderListCollection.addItem(a)
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
			relObj = cmds.listRelatives(i.text())
			attrs.update(cmds.listAttr(relObj))
		for x in attrs:
			self.attrListCollection.addItem(x)
def showUI():
	ui = mainUI()
	ui.show()
	return ui
