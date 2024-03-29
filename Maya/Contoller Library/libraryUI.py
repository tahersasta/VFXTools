################################################################################################################################################
#
#Creates the UI and sets the layout
#
###############################################################################################################################################


from Qt import QtWidgets, QtCore, QtGui
from maya import cmds
import pprint
import contLibrary


class ControllerLibraryUI(QtWidgets.QDialog):

    def __init__(self):

        super(ControllerLibraryUI, self).__init__()
        self.setWindowTitle('Controller Library UI')
        self.library = contLibrary.ControllerLibrary()
        self.buildUI()

    def buildUI(self):
        """
            Creates the Layout of the entire Library
            ;Return:None
        """
        layout = QtWidgets.QVBoxLayout(self)
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)
        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)
        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)
        size = 64
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size + 12, size + 12))
        layout.addWidget(self.listWidget)
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import!')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)
        self.populate()

    def load(self):
        """
            Loads the selected controller to the scene
            ;Returns:None
        """
        currentItem = self.listWidget.currentItem()

        if not currentItem:
            return

        name = currentItem.text()
        self.library.load(name)

    def save(self):
        """
            Saves a newly created controller/asset on the click of a button 
            ;return : None
        """
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("You must give a name!")
            return
        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')

    def populate(self):
        """
            Lists the available controllers
            ;return:None
        """
        self.listWidget.clear()
        self.library.find()
        for name, info in self.library.items():

            item = QtWidgets.QListWidgetItem(name)

            item.setToolTip(pprint.pformat(info))

            screenshot = info.get('screenshot')

            if screenshot:
                icon = QtGui.QIcon(screenshot)

                item.setIcon(icon)

            self.listWidget.addItem(item)


def showUI():
    """
        Displays the Ui when the program is executed
        ;return ui:the object of the class so the widget keeps running
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui
