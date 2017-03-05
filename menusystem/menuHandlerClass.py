# imports
import os
from os import walk
#import pathlib
import sys
import glob
import csv
## import functions for menufunc handlers
sys.path.insert(0, "../")
sys.path.insert(0, "./")
import globalsettings
from myFunctions import *

# input getter
class InputGetter:
	def __init__(self):
		if (globalsettings.DEBUGFLAG >= 1):
			print("InputGetter class initialised")
		
# menu items for each screen
class Menu:
	def __init__(self, items, length):
		self.length = length
		self.items = items
		self.menuTitle = ""
		self.selected = 0
		
# read in files for each menu screen
class MenuReader:
	def __init__(self, folder):
		#check menu folder
		if (globalsettings.DEBUGFLAG >= 1):
			print("Menu Reader class initialized")
		if os.path.isdir(folder):
			self.folder = folder
			if (globalsettings.DEBUGFLAG >= 1):
				print("Menus will be read from ", folder)
		else:
			if (globalsettings.DEBUGFLAG >= 1):
				print("Folder for menu files does not exist")
		
		#check that title file exists
		if os.path.isfile(os.path.join(self.folder,"titles.lst")):
			self.titlesFile = os.path.join(self.folder,"titles.lst")
		else:
			if (globalsettings.globalsettings.DEBUGFLAG >= 1):
				print("File with Menu titles does not exist")
						
		# init array to hold menus in
		self.menus = []
		self.menuFiles = []
		self.Titles = []
		# load list of files in menu directory in to object
		self.getMenuFiles()
			
	def processTitlesFile(self):
		if (globalsettings.DEBUGFLAG >= 1):
			print("Processing titles file", self.titlesFile)
		n= 0
		with open(self.titlesFile, 'rt') as titlesfile:
			for line in titlesfile:
				self.Titles.append(line)
				if (globalsettings.DEBUGFLAG >= 1):
					print("Title entered in to list position,",[n, self.Titles[n]])
				#print("Line ", line)
				n += 1
		return self.Titles
				
	def getMenuFiles(self):
		self.menuFiles = glob.glob( os.path.join(self.folder,"menu.*"))
		
	def processMenuFiles(self):
		i = 0
		j = 0
		listOfMenus = [[]]
		self.menuFiles.sort()
		for f in self.menuFiles:
			if (globalsettings.DEBUGFLAG >= 1):
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
class MenuFunc(MenuFunc_Base):
	def __init__(self, folder):
		#print("Menu func init")
		#check that functions file exists
		self.folder = folder
		if os.path.isfile(os.path.join(self.folder,"functions.lst")):
			self.functionsFile = os.path.join(self.folder,"functions.lst")
		else:
			if (globalsettings.DEBUGFLAG >= 1):
				print("File with Functions does not exist")
		self.function = None
		self.lable = None
		self.funcHandler = []
		self.Functions = {}
		self.functionHandlersDictionary = None
		self.processFunctionsFile()
		self.registerFunctions(self.Functions)  #(self.functionHandlersDictionary)
		
	def processFunctionsFile(self):
		if (globalsettings.DEBUGFLAG >= 1):
			print("Processing functions file", self.functionsFile)
		with open(self.functionsFile, 'rt') as csvfile:
			menudata = csv.reader(csvfile, delimiter=',', quotechar='"')
			i  = 0
			listofFunctions = {}
			for row in menudata:
				# make sure second item is brought in as int
				k = 0
				curr = []
				for r in row:
					if (k == 0):
						curr.append(str(r))
					if (k == 1):
						curr.append(str(r))
					if (k == 2):
						curr.append(str(r))
					k += 1
				#print(row)
				if (globalsettings.DEBUGFLAG >= 1):
					print("creating dictionary object with key ", [curr[0], curr])
				listofFunctions[curr[0]] = (curr[1], curr[2])

				i += 1
				self.Functions = listofFunctions
				if (globalsettings.DEBUGFLAG >= 1):
					print("self.functions =", self.Functions)
		return listofFunctions
		
	def registerFunctions(self, funcHandler):
		if (globalsettings.DEBUGFLAG >= 1):
			print("Registering functions")
		for lable in funcHandler.items():
			if (globalsettings.DEBUGFLAG >= 1):
				print("Function handler registered:", lable[1][1])
		self.funcHandler = funcHandler

	def returnFunctionHandler(self, lable):
		if (globalsettings.DEBUGFLAG >= 1):
			print("Return function handler for", self.funcHandler[0])
		#return self.funcHandler[lable][0]
	
	def returnFunctionHandlerLable(self, lable):
		if (globalsettings.DEBUGFLAG >= 1):
			print("Return function handler lable for", lable)
		return self.funcHandler[lable][1]
		
	def executeFunctionHandler(self, lable):
		if (globalsettings.DEBUGFLAG >= 1):
			print("Executing function handler", self.Functions[lable][0])
		func = getattr(MenuFunc_Base, self.Functions[lable][0])
		func()
