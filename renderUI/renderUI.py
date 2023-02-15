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

rs = renderSetup.instance()


class mainUI(QtWidgets.QDialog,main.Ui_Form):
	def __init__(self):
		super(mainUI,self).__init__()
		self.setupUi(self)

		self.pushButton.clicked.connect(self.load)

	def load(self):
		dialog = beautyUI()
		uin = dialog.exec_()
		return uin 

class beautyUI(QtWidgets.QDialog,stacked.Ui_Form):
	def __init__(self):
		super(beautyUI,self).__init__()
		self.setupUi(self)
		self.nextpage1.clicked.connect(self.next)
		self.nextpage2.clicked.connect(self.next)
		self.nextpage3.clicked.connect(self.next)
		self.nextpage4.clicked.connect(self.next)
		self.backpage2.clicked.connect(self.back)
		self.backpage3.clicked.connect(self.back)
		self.backpage4.clicked.connect(self.back)
		self.backpage5.clicked.connect(self.back)
		self.count = 0 
		self.search.textChanged.connect(self.Search)
		self.attrSearch.textChanged.connect(self.searchAttr)

		self.sel = cmds.ls(sl=0,dag=True)

		for s in self.sel:
			if cmds.objectType(s) == "transform":
					self.listView.addItem(s)



	def back(self):
		self.count = self.count - 1
		self.stackedWidget.setCurrentIndex(self.count)
	def next(self):
		if self.count == 0:
			if self.layerNameLine.text() == "":
				QtWidgets.QMessageBox.warning(self,"Error","Please Enter a Layer Name")
			else:
				self.count = self.count + 1
				self.stackedWidget.setCurrentIndex(self.count)
				return
		elif self.count == 1: 
			if self.collectionNameLine.text() == "":
				QtWidgets.QMessageBox.warning(self,"Error","Please Enter a collection Name")
			else:
				self.count = self.count + 1 
				self.stackedWidget.setCurrentIndex(self.count)
				return
		elif self.count ==2:
			if  not  self.listView.selectedItems():
				QtWidgets.QMessageBox.warning(self,"Error","Please select atleast one item to addd to the collection")
			else:
				self.count = self.count + 1 
				self.stackedWidget.setCurrentIndex(self.count)
				self.attr_List()
				return
		else:
			self.count = self.count +1
			self.stackedWidget.setCurrentIndex(self.count)



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
			relObj = cmds.listRelatives(i.text())
			attrs.update(cmds.listAttr(relObj))
		for x in attrs:
			self.attrList.addItem(x)



def showUI():
	ui = mainUI()
	ui.show()
	return ui
