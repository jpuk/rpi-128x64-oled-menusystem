# to do
# implement system to allow user functions to create virtual screen or buffers which can be displayed on the screen
# one method could be to provide a structure which can be overwritten before being called by a special flag
# another could be to add a virtual item to the screens list
# implement loading mechanism from file for user buttons
# implement error handling for file operations
# implement command key to safely shut down
# implement menu flag to shutdown

# imports

# global setting file
import globalsettings
import pdb
import sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)	

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

# look at myFunctions.py, myClasses.py and globalsettings.py to configure options


def main():
	
	menusystem = MenuSystem()
	
	while True:
		menusystem.checkButtons()
		menusystem.checkScreenSaver()
		menusystem.updateScreen()
	
	# clean up GPIO		
	GPIO.cleanup()
	return 0


		
if __name__ == "__main__":
	main()

