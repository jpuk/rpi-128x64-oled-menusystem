# imports
import os
from os import walk
#import pathlib
import sys
import glob
import csv

# menu items for each screen
class Menu:
	def __init__(self, items, length):
		self.length = length
		self.items = items
		self.selected = 0
		
# read in files for each menu screen
class MenuReader:
	def __init__(self, folder):
		print("Menu Reader class initialized")
		if os.path.isdir(folder):
			self.folder = folder
			print("Menus will be read from ", folder)
		else:
			print("Folder for menu files does not exist")
		# init array to hold menus in
		self.menus = []
		self.menuFiles = []
		
	def getMenuFiles(self):
		self.menuFiles = glob.glob( os.path.join(self.folder,"menu.*"))
	
	def processMenuFiles(self):
		i = 0
		j = 0
		listOfMenus = [[]]
		self.menuFiles.sort()
		for f in self.menuFiles:
			print("Processing menu file ", f)
			with open(f, 'rt') as csvfile:
				j = 0
				listOfMenus.append([])
				menudata = csv.reader(csvfile, delimiter=',', quotechar='"')
				for row in menudata:
					# make sure second item is brought in as int
					k = 0
					curr = []
					for r in row:
						if (k == 0):
							curr.append(str(r))
						if (k == 1):
							curr.append(int(r))
						if (k == 2):
							curr.append(str(r))
						k += 1
					listOfMenus[i].append(curr)
					j += 1
			i += 1

		menus = []
		for m in listOfMenus:
			menus.append(Menu(m, len(m)))
		return menus
		
# class to deal with function handler calls
class MenuFunc:
	def __init__(self, funcHandler):
		#print("Menu func init")
		self.function = None
		self.lable = None
		self.funcHandler = None 
		self.registerFunctions(funcHandler)
		
	def registerFunctions(self, funcHandler):
		print("Registering functions")
		for lable in funcHandler.items():
			print("Function handler registered:", lable[1][1])
		self.funcHandler = funcHandler

	def returnFunctionHandler(self, lable):
		print("Return function handler for", self.funcHandler[lable][1])
		return self.funcHandler[lable][0]
	
	def returnFunctionHandlerLable(self, lable):
		print("Return function handler for", lable)
		return self.funcHandler[lable][1]
		
	def executeFunctionHandler(self, lable):
		print("Executing function handler", self.funcHandler[lable][1])
		self.funcHandler[lable][0]()
