from maya import cmds
import random
import maya.OpenMaya as om

class cityCreator(object):
	def cityGen(self,selection=False,row=3,col=3, rowG = 10 , colG =10):
		if selection: 
			raise RuntimeError("You diont have anything selected! How dare you?!")
		#get the Translate X Y and Z
		selected = om.MSelectionList()
		om.MGlobal.getActiveSelectionList(selected)
		obj = om.MObject()
		selected.getDependNode(0,obj)
		xTranslate = om.MFnDependencyNode(obj).findPlug("translateX").asFloat()
		self.yScale = om.MFnDependencyNode(obj).findPlug("scaleY").asFloat()
		self.xScale = om.MFnDependencyNode(obj).findPlug("scaleX").asFloat()
		self.zScale = om.MFnDependencyNode(obj).findPlug("scaleZ").asFloat()
		#Initate the random function 
		random.seed()
		#Getting the selected Cube 
		sel = cmds.ls(sl=True)
		cmds.rename('Building1')
		sel = cmds.ls(sl=True)
		#centering the Pivot
		cmds.xform(sel, centerPivots = True)
		#getting the bounding box values and assigning them to a variable
		bounding_box=cmds.xform(sel,q=1,bb=1,ws=1)
		x_min,y_min,z_min,x_max,y_max,z_max = bounding_box
		#Setting the pivot to the bottom 
		cmds.move(y_min, [sel[0]+".scalePivot",sel[0]+".rotatePivot"],y=1, absolute=True)
		#setting the object to world 0 
		cmds.move(y_min*-1,sel[0],r=1,y=1)
		f = int(self.yScale)
		l = int (self.yScale) * 2
		#Generating the Buildings 
		for i in range(row):
			xPos=abs(x_min)+abs(x_max)
			#Setting the distance between buildings
			xPosCh =((i+1)*xPos)-(xTranslate*i)
			#Getting Random Heights for the buildings
			randX = random.randrange(f,l,2)
			#duplicating the buildings
			cmds.duplicate()
			cmds.move(xPosCh,moveX=True)
			cmds.scale(randX,scaleY=True)
		for i in range(col):
			xPos=abs(x_min)+abs(x_max)
			zPos=abs(z_min)+abs(z_max)
			xPosCh =((i+1)*xPos)-(xTranslate*i)
			randZ = random.randrange(f,l,2)
			cmds.duplicate()
			cmds.move(zPos,z=1)
			cmds.move(xPosCh,moveX=True)
			cmds.scale(randZ,scaleY=True)
		cmds.delete('Building1')
		objects = cmds.ls(selection =selection, dag=True, long=True)
		for obj in objects:
			objType=cmds.objectType(obj)
			if objType == "mesh":
					cmds.select(obj,add=True)
		cmds.Group()
		for i in range(colG):
			zPos=abs(z_min)+abs(z_max)
			randGZ = random.randrange(col,col+1,1)
			randSGZ = random.randrange(1,3)
			zVal = zPos * ((i+1)*randGZ)
			cmds.duplicate()
			cmds.move(zVal,z=1)
			cmds.scale(randSGZ,scaleY=True)
		for grp in cmds.ls():
			if self.is_group(grp):
				cmds.select(grp,add=True)
			else:
				pass
		cmds.Group()
		for i in range(rowG):
			xPos=abs(x_min)+abs(x_max)
			randGX = random.randrange(row+3,row+4,1)
			randSGX = random.randrange(1,3)
			xVal = xPos * ((i+1)*randGX)
			cmds.duplicate()
			cmds.move(xVal,moveX=True)
			cmds.scale(randSGX,scaleY=True)
		for grp in cmds.ls():
			if self.is_group(grp):
				cmds.select(grp,add=True)
			else:
				continue
		cmds.Group()
		selG=cmds.ls(sl=1)
		Gbounding_box=cmds.xform(selG,q=1,bb=1,ws=1)
		x_gmin,y_gmin,z_gmin,x_gmax,y_gmax,z_gmax = Gbounding_box
		pWidth = x_gmax+x_gmin + 15 
		pHeight = z_gmax+z_gmin + 15
		cmds.polyPlane(h=pHeight,w=pWidth)
		xpPos = (x_gmax+x_gmin)/2
		zpPos = (z_gmax+z_gmin)/2
		cmds.move(xpPos,zpPos,x=1,z=1)
		self.del_empty()

	def replace_building(self,nob=10):
		if cmds.ls(sl=1):
			sel = cmds.ls(sl=1)
			cmds.delete(sel,constructionHistory = True)
			cmds.rename('Build1')
		else:
			print('You have not selected the replace building. How Dare You?!')
		ch = []
		f = int(self.yScale)
		l=int(self.yScale)*2
		for grp in cmds.ls():
			if self.is_group(grp):
				ch.append(grp)
		for i in range(nob):
			try:
				randNum = random.randrange(2,8)
				randName = 'Building%d' %(randNum)
				rCh = random.choice(ch)
				#|group28|group130|Building2
				r_selName = rCh+'|'+randName
				cmds.xform(r_selName, centerPivots = True)
				bounding_box=cmds.xform(r_selName,q=1,bb=1,ws=1)
				x_min,y_min,z_min,x_max,y_max,z_max = bounding_box
				cmds.delete(r_selName)
				print('deleting %s' %(r_selName))
				#####################
				cmds.select('Build1')
				cmds.duplicate()
				seln = cmds.ls(sl=1)
				print(seln)
				print(cmds.xform(seln, centerPivots = True))
				Nbounding_box=cmds.xform(seln,q=1,bb=1,ws=1)
				x_nmin,y_nmin,z_nmin,x_nmax,y_nmax,z_nmax = Nbounding_box
				cmds.move(y_nmin, [seln[0]+".scalePivot",seln[0]+".rotatePivot"],y=1, absolute=True)
				cmds.move(y_nmin*-1,seln[0],r=1,y=1)
				xPos = (x_max + x_min)/2 
				zPos = (z_max+z_min)/2
				cmds.move(xPos,zPos,x=1,z=1)
				randY = random.randrange(f,l)
				cmds.scale(self.xScale,randY,self.zScale)
			except ValueError:
				continue

	def del_empty(self):
		deleteList=[]
		transforms =  cmds.ls(type='transform')
		for tran in transforms:
			if cmds.nodeType(tran) == 'transform':
				children = cmds.listRelatives(tran, c=True) 
				if children == None:
					print ('%s, has no children' %(tran))
					deleteList.append(tran)
		cmds.delete(deleteList)

	def is_group(self,groupName):
		try:
			children = cmds.listRelatives(groupName , children=True)
			for child in children:
				if not cmds.ls(child, transforms=True):
					return False
			return True
		except:
			return False


class baseWindow(object):
	windowName = "BaseWindow"

	def show(self):
		if cmds.window(self.windowName, query=True, exists=True):
			cmds.deleteUI(self.windowName)
		cmds.window(self.windowName)
		self.buildUI()
		cmds.showWindow()

	def buildUI(self):
		pass
	def reset(self, *args):
		pass
	def closeUI(self, *args):
		cmds.deleteUI(self.windowName)

class city(baseWindow,cityCreator):
	windowName = "CityCreator"
	def buildUI(self):
		column = cmds.columnLayout()
		cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 180), (2, 100)] )
		cmds.text("No.of Rows in city block       ") 
		self.rows = cmds.textField()
		cmds.text("No.of Columns in a city block     ")
		self.cols=cmds.textField()
		cmds.text("No.of Rows in a city      ")
		self.rowG=cmds.textField()
		cmds.text("No.of Columns in a city      ")
		self.colsG=cmds.textField()
		cmds.setParent(column)
		cmds.button(label="Create City", command=self.cityNew)
		cmds.text("Slider to change the number of buildings to replace in the city")
		rows = cmds.rowLayout(numberOfColumns=2)
		self.text= cmds.text(label="10")
		self.slider=cmds.intSlider(min=1,max=30, value=10, step=1, changeCommand =self.repBuild)
		cmds.setParent(column)
		cmds.button(label="Close", command=self.closeUI)
	def repBuild(self,*args):
		nob = cmds.intSlider(self.slider,q=1,value=True)
		self.replace_building(nob=nob)
		cmds.text(self.text,edit=True,label=nob)

	def cityNew(self,*args):
		row = cmds.textField(self.rows,q=1,text=True)
		col = cmds.textField(self.cols,q=1,text=True)
		rowsG = cmds.textField(self.rowG,q=1,text=True)
		colsG = cmds.textField(self.colsG,q=1,text=True)

		self.cityGen(row=int(row),col=int(col), rowG = int(rowsG) , colG=int(colsG))

