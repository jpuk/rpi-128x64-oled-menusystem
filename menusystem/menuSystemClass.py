# to do
# implement system to allow user functions to create virtual screen or buffers which can be displayed on the screen
# one method could be to provide a structure which can be overwritten before being called by a special flag
# another could be to add a virtual item to the screens list
# implement loading mechanism from file for user buttons
# implement error handling for file operations
# implement command key to safely shut down
# implement menu flag to shutdown

# imports
import sys
sys.path.insert(0, "../")
sys.path.insert(0, "./")
import globalsettings
import RPi.GPIO as GPIO
import time
## import functions for menufunc handlers
from myFunctions import *
# import graphics class
from displayClass import *
# import button handler class
from buttonClass import *
# import menu handler classes
from menuHandlerClass import *
# import extended classes
from myClasses import *


##menu system class
class MenuSystem:
	def __init__(self):
			if (globalsettings.DEBUGFLAG >= 1):
				print ("Initialising MenuSystem object")
			#set GPIO mode
			GPIO.setmode(GPIO.BCM)	
			#create display object
			self.display = Display()

			#create menu object
			# if menu link value is 999 this mean this ot is not a selectable option, if 998 it's a function handler
			# init menu reader object
			self.menuReader = MenuReader(globalsettings.MENU_FOLDER)
			#create array of menu objects from files
			self.menus = self.menuReader.processMenuFiles()
			self.titles = self.menuReader.processTitlesFile()
			#self.functions = self.menuReader.processFunctionsFile()
			
			# call registerFunctions() from myfunctions.py which contains function handlers and definitions
			# functionHandlersDictionary is in myfucntions.py
			self.myMenuFunctions = MyMenuFunc(globalsettings.MENU_FOLDER)
			
			# create button objects
			self.buttons = myButtonsList

			#initisialise input getter
			self.inputGetter = InputGetter()
			
			#draw title 
			self.display.drawTitle(self.titles[globalsettings.selectedMenu])
			
			#for button handler / main loop
			self.changedFlipFlop = True
			self.lastItem = None
			self.freshPass = True
			
			#set timestamp to be used to measure time between screen changes
			self.screenSaverActive = False
			self.timestamp = int(time.time())
			self.activationTime = None
			
	def updateLastChangeTimestamp(self):
		self.timestamp =  int(time.time())
			
	def checkButtons(self):
		# check buttons to see if they've been pressed and if so call handler function
		for button in self.buttons:
			if GPIO.input(button.GPIO_Pin):
				self.changedFlipFlop = True
				#if button 1 pressed
				if (button.lable == "Button1"):
					#call button handler
					button.buttonPress(menu=self.menus[globalsettings.selectedMenu],menufunc=self.myMenuFunctions)
					if ( self.menus[globalsettings.selectedMenu].selected > (globalsettings.MAX_ITEM_PERSCREEN-1)):
						if (globalsettings.DEBUGFLAG >= 1):
							print("scrolling past end of screen")
						if ( globalsettings.SECOND_SCREEN == True ):
							globalsettings.SECOND_SCREEN = False
						if ( globalsettings.SECOND_SCREEN == False ):
							globalsettings.SECOND_SCREEN = True
						if (globalsettings.DEBUGFLAG >= 1):
							print("SECOND SCREEN = ", globalsettings.SECOND_SCREEN)				
					if (self.menus[globalsettings.selectedMenu].selected == 0 or self.menus[globalsettings.selectedMenu].selected == 4):
						#print("Clearing display")
						self.display.clearDisplay()
						self.display.clearMainScreen()
				
				#if button 2 pressed		
				if (button.lable == "Button2"):
					self.display.clearDisplay()
					self.display.clearMainScreen()
					self.freshPass = True
					#call button handler
					#print(self.menus)
					button.buttonPress(menu=self.menus[globalsettings.selectedMenu],menufunc=self.myMenuFunctions)
					# the selectedMenu variable isn't incered until the button handler is proccessed so we don't upade title until now
					self.display.clearTitle()
					self.display.drawTitle(self.titles[globalsettings.selectedMenu])
				time.sleep(globalsettings.BUTTON_SLEEP_TIME)	
					
	def updateScreen(self):						
		if ( self.changedFlipFlop == True ):
			#update last time stamp
			self.updateLastChangeTimestamp()  
			# disable screensaver if active
			self.disableScreenSaver()
			
			i = 0
			#draw menu items
			for item in self.menus[globalsettings.selectedMenu].items:
				#if current item is selected
				#invese text and highlight background
				# if were about to draw the selected item highlight it unless it has a status of 999 in which case it
				# should be skipped
				if ( self.menus[globalsettings.selectedMenu].selected == i ):
					self.freshPass = True
				if ( item[1] == 999 and self.freshPass == True ):
					self.menus[globalsettings.selectedMenu].selected += 1
				
				j = 0		
				if ( i == self.menus[globalsettings.selectedMenu].selected  and item[1] != 999):
					#if not the first item then remove highlighting from previous item
					if ( self.menus[globalsettings.selectedMenu].selected != 0 ):
						if ( globalsettings.SECOND_SCREEN == True):
							
							if ( i >= globalsettings.MAX_ITEM_PERSCREEN+1):
								j = ((i - globalsettings.MAX_ITEM_PERSCREEN) * globalsettings.TEXT_LINE_X) + (globalsettings.MAIN_X)
						else:
							if ( i < globalsettings.MAX_ITEM_PERSCREEN):
								j = (i * globalsettings.TEXT_LINE_X) + (globalsettings.MAIN_X)								
						self.display.overwriteSelection( j )
						if ( globalsettings.SECOND_SCREEN == True):
							
							if ( i >= globalsettings.MAX_ITEM_PERSCREEN+1):
								self.display.drawTextLine(self.lastItem[0], (i - 4)-1, selected=False)
						else:
							if ( i < globalsettings.MAX_ITEM_PERSCREEN):
								self.display.drawTextLine(self.lastItem[0], i -1, selected=False)
					
					#if wrapping round to first item remove highligting from last item
					if ( globalsettings.SECOND_SCREEN == True):
						
						if ( i >= globalsettings.MAX_ITEM_PERSCREEN):
							self.display.drawTextLine(item[0], i - 4, selected=True)
					else:
						if ( i < globalsettings.MAX_ITEM_PERSCREEN):
							self.display.drawTextLine(item[0], i, selected=True)
					self.changedFlipFlop = False
				#else this item isn't selected so draw text without highlighting
				else:
					if ( globalsettings.SECOND_SCREEN == True ):
						
						if ( i >= globalsettings.MAX_ITEM_PERSCREEN):
							self.display.drawTextLine(item[0], i - 4, selected=False)
					else:
						if ( i < globalsettings.MAX_ITEM_PERSCREEN):
							self.display.drawTextLine(item[0], i, selected=False)
					self.changedFlipFlop = False
				i = i + 1
				self.lastItem = item
			self.freshPass = False
		
	def disableScreenSaver(self):
		if (self.screenSaverActive == True):
			self.screenSaverActive = False
			self.updateLastChangeTimestamp
			self.display.disableScreenSaver()
			self.display.clearDisplay()
			self.display.clearMainScreen()
			self.display.clearTitle()
			self.display.drawTitle(self.titles[globalsettings.selectedMenu])
		return 0
		
	def checkScreenSaver(self):
		self.activationTime = self.timestamp + globalsettings.SCREEN_SAVER_TIMEOUT
		#if (self.screenSaverActive == False):
		if( int(time.time()) >= int(self.activationTime) ):
			self.screenSaverActive = True
			self.display.displayScreenSaver()

				
######
