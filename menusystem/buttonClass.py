# imports
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
