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
	#user defined button handlers here
	#def button3Handler(self, menu=None, menufunc=None):

# List of buttons and associated handlers
myButtonsList = [myButton(5,"Button1", myButton.button1Handler),myButton(6, "Button2", myButton.button2Handler)]


#extentions to MenuFunc class go here
# function handlers
class MyMenuFunc(MenuFunc):
	def __init__(self, functionHandlersDictionary):
		self.functionHandlersDictionary = functionHandlersDictionary
		#print("init my menu func")
		MenuFunc.__init__(self, self.functionHandlersDictionary)
