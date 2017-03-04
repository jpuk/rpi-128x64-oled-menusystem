# todo
#

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

# look at myFunctions.py, myClasses.py and globalsettings.py to configure options


def main():
	menusystem = MenuSystem()
	
	while True:
		menusystem.checkButtons()
		menusystem.updateScreen()
	
	# clean up GPIO		
	GPIO.cleanup()
	return 0


		
if __name__ == "__main__":
	main()

