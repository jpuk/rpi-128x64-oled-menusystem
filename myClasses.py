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
	
	# button handlers
	def button1Handler(self, menu=None, menufunc=None):
		globalsettings.SECOND_SCREEN
		print("Button 1 handler ") 
		if (menu.selected < (menu.length )):
			menu.selected += 1
		if (menu.selected == menu.length ):
			print("selected has overflowed ", menu.selected)
			globalsettings.SECOND_SCREEN = False
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
		
		#user defined button handlers here


# List of buttons and associated handlers
myButtonsList = [myButton(5,"Button1", myButton.button1Handler),myButton(6, "Button2", myButton.button2Handler)]


#extentions to MenuFunc class go here
# function handlers
class MyMenuFunc(MenuFunc):
	def __init__(self, functionHandlersDictionary):
		self.functionHandlersDictionary = functionHandlersDictionary
		#print("init my menu func")
		MenuFunc.__init__(self, self.functionHandlersDictionary)
