

from maya import cmds
from shiboken2 import wrapInstance
import maya.OpenMayaUI as MUI
from PySide2 import QtCore, QtGui, QtWidgets


def maya_main_window():
	
	main_window = MUI.MQtUtil.mainWindow()

class Rename(QtWidgets.QDialog):

	def __init__(self, parent=maya_main_window()):

		super(Rename, self).__init__(parent)

		self.setWindowTitle("Rename")
		self.setMinimumWidth(250)

		self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.buildUI()

	def buildUI(self):

		main_layout = QtWidgets.QGridLayout(self)



		self.searchlabel = QtWidgets.QLabel("Search:")
		self.replacelabel = QtWidgets.QLabel("Replace:")
		self.searchline = QtWidgets.QLineEdit()
		self.replaceline = QtWidgets.QLineEdit()
		self.searchreplacebt = QtWidgets.QPushButton("Replace")
		main_layout.addWidget(self.searchlabel, 0, 0)
		main_layout.addWidget(self.searchline, 0, 1)
		main_layout.addWidget(self.replacelabel, 1, 0)
		main_layout.addWidget(self.replaceline, 1, 1)
		main_layout.addWidget(self.searchreplacebt, 2, 0, 1, 2)
		self.searchreplacebt.clicked.connect(self.creplace)



		self.cprefix_label = QtWidgets.QLabel("Prefix:")
		self.cprefix_lineedit = QtWidgets.QLineEdit()
		self.cprefix_button = QtWidgets.QPushButton("Add Prefix")
		main_layout.addWidget(self.cprefix_label, 3, 0)
		main_layout.addWidget(self.cprefix_lineedit, 3, 1)
		main_layout.addWidget(self.cprefix_button, 4, 0, 1, 2)
		self.cprefix_button.clicked.connect(self.cprefix)



		self.csuffix_label = QtWidgets.QLabel("Suffix:")
		self.csuffix_lineedit = QtWidgets.QLineEdit()
		self.csuffix_button = QtWidgets.QPushButton("Add Suffix")
		main_layout.addWidget(self.csuffix_label, 5, 0)
		main_layout.addWidget(self.csuffix_lineedit, 5, 1)
		main_layout.addWidget(self.csuffix_button, 6, 0, 1, 2)
		self.csuffix_button.clicked.connect(self.csuffix)


	


	def creplace(self):

		

		search = self.searchline.text()
		replace = self.replaceline.text()

		sel = cmds.ls(sl=True)

		if len(sel) == 0:
			cmds.warning("Nothing selected")

		elif search == "":
			cmds.warning("Field is blank!")

		else:
			for s in reversed(sel):
				split_name = s.split("|")
				ser = split_name[-1].replace(search, replace)
				cmds.rename(str(s), str(ser))





	def cprefix(self):

		

		prefix = self.cprefix_lineedit.text()

		sel = cmds.ls(sl=True)

		if len(sel) == 0:
			cmds.warning("Nothing selected")

		elif prefix == "":
			cmds.warning("Field is blank!")

		else:
			for s in reversed(sel):
				split_name = s.split("|")
				cmds.rename(str(s), str(prefix + split_name[-1]))





	def csuffix(self):

		

		suffix = self.csuffix_lineedit.text()

		sel = cmds.ls(sl=True)

		if len(sel) == 0:
			cmds.warning("Nothing selected")

		elif suffix == "":
			cmds.warning("Field is blank!")

		else:
			for s in reversed(sel):
				split_name = s.split("|")
				cmds.rename(str(s), str(split_name[-1] + suffix))




rename = Rename()
rename.show()
