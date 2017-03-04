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
		#set GPIO mode
			GPIO.setmode(GPIO.BCM)	

			#create display object
			self.display = Display()

			#create menu object
			# if menu link value is 999 this mean this ot is not a selectable option, if 998 it's a function handler
			# init menu reader object
			self.menuReader = MenuReader(globalsettings.MENU_FOLDER)
			# load list of files in menu directory in to object
			self.menuReader.getMenuFiles()
			#create array of menu objects from files
			self.menus = self.menuReader.processMenuFiles()
			
			# call registerFunctions() from myfunctions.py which contains function handlers and definitions
			# functionHandlersDictionary is in myfucntions.py
			self.myMenuFunctions = MyMenuFunc(functionHandlersDictionary)
			

			# create 2 button objects
			self.buttons = myButtonsList

			self.display.drawTitle("Menu system")

			#button handler / main loop
			self.changedFlipFlop = True
			self.lastItem = None
			self.freshPass = True
			print ("Initialising MenuSystem object")
			
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
						print("scrolling past end of screen")
						if ( globalsettings.SECOND_SCREEN == True ):
							globalsettings.SECOND_SCREEN = False
						if ( globalsettings.SECOND_SCREEN == False ):
							globalsettings.SECOND_SCREEN = True
						print("SECOND SCREEN = ", globalsettings.SECOND_SCREEN)				
					if (self.menus[globalsettings.selectedMenu].selected == 0 or self.menus[globalsettings.selectedMenu].selected == 4):
						print("selected ", self.menus[globalsettings.selectedMenu].selected)
						self.display.clearDisplay()
						self.display.clearMainScreen()
				
				#if button 2 pressed		
				if (button.lable == "Button2"):
					self.display.clearDisplay()
					self.display.clearMainScreen()
					self.freshPass = True
					#call button handler
					button.buttonPress(menu=self.menus[globalsettings.selectedMenu],menufunc=self.myMenuFunctions)
				time.sleep(globalsettings.BUTTON_SLEEP_TIME)	
					
	def updateScreen(self):						
		if ( self.changedFlipFlop == True ):
			i = 0
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
								#print(i - globalsettings.MAX_ITEM_PERSCREEN)
								j = ((i - globalsettings.MAX_ITEM_PERSCREEN) * globalsettings.TEXT_LINE_X) + (globalsettings.MAIN_X)
						else:
							if ( i < globalsettings.MAX_ITEM_PERSCREEN):
								j = (i * globalsettings.TEXT_LINE_X) + (globalsettings.MAIN_X)								
						self.display.overwriteSelection( j )
						if ( globalsettings.SECOND_SCREEN == True):
							
							if ( i >= globalsettings.MAX_ITEM_PERSCREEN+1):
								#print(i - globalsettings.MAX_ITEM_PERSCREEN)
								self.display.drawTextLine(self.lastItem[0], (i - 4)-1, selected=False)
						else:
							if ( i < globalsettings.MAX_ITEM_PERSCREEN):
								self.display.drawTextLine(self.lastItem[0], i -1, selected=False)
					#if wrapping round to first item remove highligting from last item

					if ( globalsettings.SECOND_SCREEN == True):
						
						if ( i >= globalsettings.MAX_ITEM_PERSCREEN):
							#print(i - globalsettings.MAX_ITEM_PERSCREEN)
							self.display.drawTextLine(item[0], i - 4, selected=True)
					else:
						if ( i < globalsettings.MAX_ITEM_PERSCREEN):
							self.display.drawTextLine(item[0], i, selected=True)
					self.changedFlipFlop = False
				#else this item isn't selected so draw text without highlighting
				else:
					if ( globalsettings.SECOND_SCREEN == True ):
						
						if ( i >= globalsettings.MAX_ITEM_PERSCREEN):
							#print(i - globalsettings.MAX_ITEM_PERSCREEN)
							self.display.drawTextLine(item[0], i - 4, selected=False)
					else:
						if ( i < globalsettings.MAX_ITEM_PERSCREEN):
							self.display.drawTextLine(item[0], i, selected=False)
					self.changedFlipFlop = False
				i = i + 1
				self.lastItem = item
			self.freshPass = False
			
######
