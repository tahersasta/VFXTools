#########################################################################################################################################
#
#
#
#########################################################################################################################################


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_ProjectList(object):
    def setupUi(self, ProjectList):
        """
            Sets all the items that are going to be added to the widget
        """
        ProjectList.setObjectName("ProjectList")
        ProjectList.resize(262, 364)
        self.verticalLayoutWidget = QtWidgets.QWidget(ProjectList)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 240, 340))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ProjLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ProjLabel.setObjectName("ProjLabel")
        self.verticalLayout.addWidget(self.ProjLabel)
        self.projList = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.projList.setObjectName("projList")
        self.verticalLayout.addWidget(self.projList)
        self.lowSample = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.lowSample.setObjectName("lowSample")
        self.verticalLayout.addWidget(self.lowSample)
        self.highSample = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.highSample.setObjectName("highSample")
        self.verticalLayout.addWidget(self.highSample)
        self.okBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.okBtn.setObjectName("okBtn")
        self.verticalLayout.addWidget(self.okBtn)

        self.retranslateUi(ProjectList)
        QtCore.QMetaObject.connectSlotsByName(ProjectList)

    def retranslateUi(self, ProjectList):
        _translate = QtCore.QCoreApplication.translate
        ProjectList.setWindowTitle(_translate("ProjectList", "Form"))
        self.ProjLabel.setText(_translate("ProjectList", "Select The Project :"))
        self.lowSample.setText(_translate("ProjectList", "Low Sample"))
        self.highSample.setText(_translate("ProjectList", "High Sample"))
        self.okBtn.setText(_translate("ProjectList", "OK"))
