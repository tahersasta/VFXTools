#############################################################################################################################################
#
#The Main Widget that appears when the function is executed
#
#############################################################################################################################################

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        """
            Sets all the items that are going to be added to the widget
        """
        Form.setObjectName("Form")
        Form.resize(745, 530)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(230, 0, 261, 61))
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.listView = QtWidgets.QListWidget(Form)
        self.listView.setGeometry(QtCore.QRect(30, 90, 211, 301))
        self.listView.setObjectName("listView")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 60, 151, 16))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(56, 404, 151, 41))
        self.pushButton.setObjectName("pushButton")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(76,387,151,41))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setHidden(True)
        self.checkBox.setChecked(True)
        self.checkLabel = QtWidgets.QLabel(Form)
        self.checkLabel.setGeometry(QtCore.QRect(96,387,151,41))
        self.checkLabel.setObjectName("checkLabel")
        self.checkLabel.setHidden(True)


        self.checkBox_1 = QtWidgets.QCheckBox(Form)
        self.checkBox_1.setGeometry(QtCore.QRect(286,387,151,41))
        self.checkBox_1.setObjectName("checkBox_1")
        self.checkBox_1.setHidden(True)
        self.checkLabel_1 = QtWidgets.QLabel(Form)
        self.checkLabel_1.setGeometry(QtCore.QRect(306,387,151,41))
        self.checkLabel_1.setObjectName("checkLabel_1")
        self.checkLabel_1.setHidden(True)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(286, 404, 151, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.listView_2 = QtWidgets.QListWidget(Form)
        self.listView_2.setGeometry(QtCore.QRect(260, 90, 211, 301))
        self.listView_2.setObjectName("listView_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(270, 60, 171, 16))
        self.label_3.setObjectName("label_3")
        self.listView_3 = QtWidgets.QListWidget(Form)
        self.listView_3.setGeometry(QtCore.QRect(490, 90, 211, 301))
        self.listView_3.setObjectName("listView_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(500, 60, 171, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(516, 404, 151, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(286, 454, 151, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(56, 454, 151, 41))
        self.pushButton_5.setObjectName("pushButton_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Render Setup Menu"))
        self.checkLabel.setText(_translate("Form","Set Render Layer"))
        self.checkLabel_1.setText(_translate("Form","Set Visible Layer"))
        self.label_2.setText(_translate("Form", "List of existing Render Layers"))
        self.pushButton.setText(_translate("Form", "Create New Render Layer"))
        self.pushButton_2.setText(_translate("Form", " Edit Existing Layer"))
        self.label_3.setText(_translate("Form", "List of existing exisiting collections"))
        self.label_4.setText(_translate("Form", "List of Overrides on the collection "))
        self.pushButton_3.setText(_translate("Form", "Automate"))
        self.pushButton_4.setText(_translate("Form", "Add a Collection"))
        self.pushButton_5.setText(_translate("Form","Set Show Specific"))
