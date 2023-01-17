from maya import cmds

from gearCreatorClass import Gear
from tweennerUI import tween

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


class tweenerUI(baseWindow):
    windowName = "TweenerUI"

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use this slider to set the tween amount")

        rows = cmds.rowLayout(numberOfColumns=2)

        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)

        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)

        cmds.button(label="Close", command=self.closeUI)

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit=True, value=50)


class gearUI(baseWindow):
    windowName = "GearUI"
    gear = None

    def buildUI(self):
        column = cmds.columnLayout()

        cmds.text("Use this slider to modify a gear")

        rows = cmds.rowLayout(numberOfColumns=4)

        self.side_label=cmds.text(label="10")

        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand=self.modifyGear)

        cmds.button(label="Make Gear", command=self.gearC)

        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)

        cmds.button(label="Close", command=self.closeUI)

    def modifyGear(self, teeth):
        if self.gear:
            self.gear.changeTeeth(teeth=teeth)

        cmds.text(self.side_label,edit=True,label=teeth)

    def gearC(self, *args):
        teeth = cmds.intSlider(self.slider, query=True, value=True)

        self.gear = Gear()

        self.gear.createGear(teeth=teeth)

    def reset(self, *args):
        self.gear = None
        self.slider=cmds.intSlider(self.slider,edit=True,value=10)
        cmds.text(self.side_label,edit=True,label="10")
