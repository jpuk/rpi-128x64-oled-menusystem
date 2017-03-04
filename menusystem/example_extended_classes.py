# sample extended classes for menu system
# integrate these examples in to your own code

###main.py###

#imports
# global setting file
import globalsettings
import pdb
import sys
import RPi.GPIO as GPIO

# import project files
sys.path.insert(0, "./menusystem/")
# import functions for menufunc handlers
from myFunctions import *
# import graphics class
from displayClass import *
# import button handler class
from buttonClass import *
# import menu handler classes
from menuHandlerClass import *
# import menu system class
from menuSystemClass import *
# import extended classes
from myClasses import *




def main():
	menusystem = MenuSystem()
	
	while True:
		menusystem.execute()
	
	# clean up GPIO		
	GPIO.cleanup()
	return 0

if __name__ == "__main__":
	main()

##end main.py###################


##myFunctions.py##########
## holds handler functions for when button is pushed
		
def myFunction1():
	print("Executing myFunction1")

def myFunction2():
	print("Executing myFunction2")


# dictionary to hold function handlers
functionHandlersDictionary = { "myFunction1":  [myFunction1, "My function 1"], "myFunction2": [myFunction2, "My Function 2"]}

##end myFunctions.py#############


##myClasses.py#################
## holds extended class definitions
#imports
import sys
sys.path.insert(0, "../")
sys.path.insert(0, "./")
import globalsettings
# import button handler class
from buttonClass import *
# import menu handler classes
from menuHandlerClass import *

#extended button class with button handler functions
class myButton(Button):
	def __init__(self, pin, lable, action):
		Button.__init__(self, pin, lable, action)
	def button1Handler(self, menu=None, menufunc=None):
		global SECOND_SCREEN
		print("Button 1 handler ") 
		if (menu.selected < (menu.length )):
			menu.selected += 1
		if (menu.selected == menu.length ):
			print("selected has overflowed ", menu.selected)
			SECOND_SCREEN = False
			menu.selected = 0

	def button2Handler(self, menu=None, menufunc=None):
		print("Button 2 handler")
		print("selecting menu screen ", menu.items[menu.selected][1])
		#if status 998 call function handler
		if ( menu.items[menu.selected][1] == 998 ):
			functionLable = str(menu.items[menu.selected][2])
			print("Call to menu function handler")
			print("Looking for match for ", functionLable)
			#new function handler code
			print(menufunc.returnFunctionHandler(functionLable))
			menufunc.executeFunctionHandler(functionLable)
		else:
			globalsettings.selectedMenu = menu.items[menu.selected][1]
			globalsettings.SECOND_SCREEN = False
			menu.selected = 0
		

#extend class to hold the menu function handlers for each action with a function
# function handlers
class MyMenuFunc(MenuFunc):
	def __init__(self, functionHandlersDictionary):
		self.functionHandlersDictionary = functionHandlersDictionary
		#print("init my menu func")
		MenuFunc.__init__(self, self.functionHandlersDictionary)
		
##end myClasses.py########

##globalsettings.py#########
## holds global vars 
########
#globals
# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

#screen configuration
# height of each text line in pixels
TEXT_LINE_X = 10
TEXT_Y_OFFSET = 5
# this oled has two sections, 16 pixel yellow bar at the top and then the remaining 48 pixels are blue
# this var marks the start of the main section of the screen and anything to be displayed in it should be offset by it
MAIN_X = 16
MAX_ITEM_PERSCREEN = 4
SECOND_SCREEN = False

# var to track selected menu 
selectedMenu = 0
############

##end globalsettings.py##########
