# imports
import sys
sys.path.insert(0, "../")
sys.path.insert(0, "./")
import globalsettings
# import button handler class
from buttonClass import *
# import menu handler classes
from menuHandlerClass import *
import RPi.GPIO as GPIO

# Button class which is extended by MyButton to include the button handler functions
class Button:
	def __init__(self, pin, lable, action):
		self.GPIO_Pin = pin
		self.lable = lable
		self.action = action
		#initialize gpio pin for input
		GPIO.setup(self.GPIO_Pin,GPIO.IN)

	def buttonPress(self, menu=None, menufunc=None):
		self.action(self, menu=menu, menufunc=menufunc)
		
	#default button handlers
	
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
		#update title
		#menu.display.clearTitle()
		#menu.display.drawTitle(self.titles[globalsettings.selectedMenu])
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

