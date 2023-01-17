
from Qt import QtWidgets, QtCore, QtGui
from maya import cmds
import pprint
import contLibrary


class ControllerLibraryUI(QtWidgets.QDialog):

    def __init__(self):
        # super is an interesting function
        # It gets the class that our class is inheriting from
        # This is called the superclass
        # The reason is that because we redefined __init__ in our class, we no longer call the code in the super's init
        # So we need to call our super's init to make sure we are initialized like it wants us to be
        super(ControllerLibraryUI, self).__init__()

        # We set our window title
        self.setWindowTitle('Controller Library UI')

        # We store our library as a variable that we can access from inside us
        self.library = contLibrary.ControllerLibrary()

        # Finally we build our UI
        self.buildUI()

    def buildUI(self):
        # Just like we made a column layout in the last UI, in Qt we have a vertical box layout
        # We tell it that we want to apply the layout to this class (self)
        layout = QtWidgets.QVBoxLayout(self)

        # We want to make another widget to store our controls to save the controller
        # A widget is what we call a UI element
        saveWidget = QtWidgets.QWidget()
        # Every widget needs a layout. We want a Horizontal Box Layout for this one, and tell it to apply to our widget
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        # Finally we add this widget to our main widget
        layout.addWidget(saveWidget)

        # Our first order of business is to have a text box that we can enter a name
        # In Qt this is called a LineEdit
        self.saveNameField = QtWidgets.QLineEdit()
        # We will then add this to our layout for our save controls
        saveLayout.addWidget(self.saveNameField)

        # We add a button to call the save command
        saveBtn = QtWidgets.QPushButton('Save')
        # When the button is clicked it fires a signal
        # A signal can be connected to a function
        # So when the button is called, it will call the function that is given.
        # In this case, we tell it to call the save method
        saveBtn.clicked.connect(self.save)
        # and then we add it to our save layout
        saveLayout.addWidget(saveBtn)

        # Now we'll set up the list of all our items
        # The size is for the size of the icons we will display
        size = 64
        # First we create a list widget, this will list all the items we give it
        self.listWidget = QtWidgets.QListWidget()
        # We want the list widget to be in IconMode like a gallery so we set it to a mode
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        # We set the icon size of this list
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        # then we set it to adjust its position when we resize the window
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        # Finally we set the grid size to be just a little larger than our icons to store our text label too
        self.listWidget.setGridSize(QtCore.QSize(size+12, size+12))
        # And finally, finally, we add it to our main layout
        layout.addWidget(self.listWidget)

        # Now we need a layout to store our buttons
        # So first we create a widget to store this layout
        btnWidget = QtWidgets.QWidget()
        # We create another horizontal layout and tell it to apply to our btn widdget
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        # And we add this widget to our main UI
        layout.addWidget(btnWidget)

        # Similar to above we create three buttons
        importBtn = QtWidgets.QPushButton('Import!')
        # And we connect it to the relevant functions
        importBtn.clicked.connect(self.load)
        # And finally we add them to the button layout
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

        # After all that, we'll populate our UI
        self.populate()

    def load(self):
        # We will ask the listWidget what our currentItem is
        currentItem = self.listWidget.currentItem()

        # If we don't have anything selected, it will tell us None is selected, so we can skip this method
        if not currentItem:
            return

        # We then get the text label of the current item. This will be the name of our control
        name = currentItem.text()
        # Then we tell our library to load it
        self.library.load(name)

    def save(self):
        # We start off by getting the name in the text field
        name = self.saveNameField.text()

        # If the name is not given, then we will not continue and we'll warn the user
        # The strip method will remove empty characters from the string, so that if the user entered spaces, it won't be valid
        if not name.strip():
            cmds.warning("You must give a name!")
            return

        # We use our library to save with the given name
        self.library.save(name)
        # Then we repopulate our UI with the new data
        self.populate()
        # And finally, lets remove the text in the name field so that they don't accidentally overwrite the file
        self.saveNameField.setText('')

    def populate(self):
        # This function will be used to populate the UI. Shocking. I know.

        # First lets clear all the items that are in the list to start fresh
        self.listWidget.clear()

        # Then we ask our library to find everything again in case things changed
        self.library.find()

        # Now we iterate through the dictionary
        # This is why I based our library on a dictionary, because it gives us all the nice tricks a dictionary has
        for name, info in self.library.items():
            # We create an item for the list widget and tell it to have our controller name as a label
            item = QtWidgets.QListWidgetItem(name)

            # We set its tooltip to be the info from the json
            # The pprint.pformat will format our dictionary nicely
            item.setToolTip(pprint.pformat(info))

            # Finally we check if there's a screenshot available
            screenshot = info.get('screenshot')
            # If there is, then we will load it
            if screenshot:
                # So first we make an icon with the path to our screenshot
                icon = QtGui.QIcon(screenshot)
                # then we set the icon onto our item
                item.setIcon(icon)

            # Finally we add our item to the list
            self.listWidget.addItem(item)

# This is a convenience function to display our UI
def showUI():
    # Create an instance of our UI
    ui = ControllerLibraryUI()
    # Show the UI
    ui.show()
    # Return the ui instance so people using this function can hold on to it
    return ui



