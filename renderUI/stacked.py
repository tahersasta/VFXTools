

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(559, 348)
        self.stackedWidget = QtWidgets.QStackedWidget(Form)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 0, 551, 341))
        self.stackedWidget.setObjectName("stackedWidget")
        self.layerName = QtWidgets.QWidget()
        self.layerName.setObjectName("layerName")
        self.layerNameLabel = QtWidgets.QLabel(self.layerName)
        self.layerNameLabel.setGeometry(QtCore.QRect(140, 110, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.layerNameLabel.setFont(font)
        self.layerNameLabel.setObjectName("layerNameLabel")
        self.nextpage1 = QtWidgets.QPushButton(self.layerName)
        self.nextpage1.setGeometry(QtCore.QRect(400, 270, 131, 41))
        self.nextpage1.setObjectName("nextpage1")
        self.layerNameLine = QtWidgets.QLineEdit(self.layerName)
        self.layerNameLine.setGeometry(QtCore.QRect(190, 170, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.layerNameLine.setFont(font)
        self.layerNameLine.setText("")
        self.layerNameLine.setObjectName("layerNameLine")
        self.stackedWidget.addWidget(self.layerName)
        self.collectionName = QtWidgets.QWidget()
        self.collectionName.setObjectName("collectionName")
        self.collectionNameLabel = QtWidgets.QLabel(self.collectionName)
        self.collectionNameLabel.setGeometry(QtCore.QRect(134, 92, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.collectionNameLabel.setFont(font)
        self.collectionNameLabel.setObjectName("collectionNameLabel")
        self.backpage2 = QtWidgets.QPushButton(self.collectionName)
        self.backpage2.setGeometry(QtCore.QRect(20, 270, 131, 41))
        self.backpage2.setObjectName("backpage2")
        self.collectionNameLine = QtWidgets.QLineEdit(self.collectionName)
        self.collectionNameLine.setGeometry(QtCore.QRect(190, 140, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.collectionNameLine.setFont(font)
        self.collectionNameLine.setText("")
        self.collectionNameLine.setObjectName("collectionNameLine")
        self.nextpage2 = QtWidgets.QPushButton(self.collectionName)
        self.nextpage2.setGeometry(QtCore.QRect(400, 270, 131, 41))
        self.nextpage2.setObjectName("nextpage2")
        self.stackedWidget.addWidget(self.collectionName)
        self.list = QtWidgets.QWidget()
        self.list.setObjectName("list")
        self.listlabel = QtWidgets.QLabel(self.list)
        self.listlabel.setGeometry(QtCore.QRect(30, 30, 221, 16))
        self.listlabel.setObjectName("listlabel")
        self.backpage3 = QtWidgets.QPushButton(self.list)
        self.backpage3.setGeometry(QtCore.QRect(20, 270, 131, 41))
        self.backpage3.setObjectName("backpage3")
        self.search = QtWidgets.QLineEdit(self.list)
        self.search.setGeometry(QtCore.QRect(20, 220, 501, 21))
        self.search.setObjectName("search")
        self.nextpage3 = QtWidgets.QPushButton(self.list)
        self.nextpage3.setGeometry(QtCore.QRect(390, 270, 131, 41))
        self.nextpage3.setObjectName("nextpage3")
        self.listView = QtWidgets.QListWidget(self.list)
        self.listView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listView.setGeometry(QtCore.QRect(20, 50, 501, 161))
        self.listView.setObjectName("listWidget")
        self.stackedWidget.addWidget(self.list)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.nextpage4 = QtWidgets.QPushButton(self.page_4)
        self.nextpage4.setGeometry(QtCore.QRect(390, 280, 131, 41))
        self.nextpage4.setObjectName("nextpage4")
        self.backpage4 = QtWidgets.QPushButton(self.page_4)
        self.backpage4.setGeometry(QtCore.QRect(20, 280, 131, 41))
        self.backpage4.setObjectName("backpage4")
        self.attrList = QtWidgets.QListWidget(self.page_4)
        self.attrList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.attrList.setGeometry(QtCore.QRect(20, 50, 501, 161))
        self.attrList.setObjectName("attrList")
        self.attrSearch = QtWidgets.QLineEdit(self.page_4)
        self.attrSearch.setGeometry(QtCore.QRect(20, 220, 501, 21))
        self.attrSearch.setObjectName("attrSearch")
        self.listlabel_2 = QtWidgets.QLabel(self.page_4)
        self.listlabel_2.setGeometry(QtCore.QRect(30, 30, 221, 16))
        self.listlabel_2.setObjectName("listlabel_2")
        self.stackedWidget.addWidget(self.page_4)
        self.finish = QtWidgets.QWidget()
        self.finish.setObjectName("finish")
        self.finsishBtn = QtWidgets.QPushButton(self.finish)
        self.finsishBtn.setGeometry(QtCore.QRect(220, 180, 121, 41))
        self.finsishBtn.setObjectName("finsishBtn")
        self.newCollectionBtn = QtWidgets.QPushButton(self.finish)
        self.newCollectionBtn.setGeometry(QtCore.QRect(220, 120, 121, 41))
        self.newCollectionBtn.setObjectName("newCollectionBtn")
        self.backpage5 = QtWidgets.QPushButton(self.finish)
        self.backpage5.setGeometry(QtCore.QRect(20, 280, 131, 41))
        self.backpage5.setObjectName("backpage5")
        self.stackedWidget.addWidget(self.finish)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.layerNameLine, self.nextpage1)
        Form.setTabOrder(self.nextpage1, self.collectionNameLine)
        Form.setTabOrder(self.collectionNameLine, self.nextpage2)
        Form.setTabOrder(self.nextpage2, self.backpage2)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.layerNameLabel.setText(_translate("Form", "Enter name of the layer "))
        self.nextpage1.setText(_translate("Form", "Next"))
        self.layerNameLine.setPlaceholderText(_translate("Form", "Enter name of layer "))
        self.collectionNameLabel.setText(_translate("Form", "Enter name of the Collection"))
        self.backpage2.setText(_translate("Form", "Back"))
        self.collectionNameLine.setPlaceholderText(_translate("Form", "Enter name of collection"))
        self.nextpage2.setText(_translate("Form", "Next"))
        self.listlabel.setText(_translate("Form", "Select the objects for the collection from list"))
        self.backpage3.setText(_translate("Form", "Back"))
        self.search.setPlaceholderText(_translate("Form", "Search the List"))
        self.nextpage3.setText(_translate("Form", "Next"))
        self.nextpage4.setText(_translate("Form", "Next"))
        self.backpage4.setText(_translate("Form", "Back"))
        self.attrSearch.setPlaceholderText(_translate("Form", "Search the List"))
        self.listlabel_2.setText(_translate("Form", "Select the attributes you want to overide "))
        self.finsishBtn.setText(_translate("Form", "Finish Creation"))
        self.newCollectionBtn.setText(_translate("Form", "Create New Collection"))
        self.backpage5.setText(_translate("Form", "Back"))
