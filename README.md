# rpi-128x64-oled-menusystem
# Project goal: Creat a simple python 3 library for creating a menu driven interface on 128x64 OLED displays for 
# the Raspberry Pi's

##  See menusystem-example.py for skeleton project template for python main() ##

# Description
This library allows you to quickly create menu driven interfaces for the Raspberry Pi and SSD1306 compatible 
128x64 OLED displays using the SPI bus and at least two button.

(The GPIO pins for the buttons and SPI bus can be configured from within globalsetting.py)

How it work:
The menu system consists of a number of "screens".

Each screen is defined by creating a file menu.XX in the folder specified in MENU_FOLDER in globalsetting.py

The library will read in each menu file in alphabetical order with the first menu file read being screen0.

example;
menu.00 - Screen0
menu.01 - Screen1
-- snip
menu.99 - Screen99

Each menu file has a very simple CSV file structure which defines the text/menus displayed on the screen. 

Each menu file should not contain more than either 8 items or lines of text.
The structure of the file is as such;
Text,Flag,Type

Text is the line of text to be displayed. This string should not be longer than would be displayed on one 
line of the OLED screen. How many charecters will depend on the font size selected.

Flag is an integer which either points to the screen which would be selected if the execute button was 
pushed. For example for the screen loaded in Screen1 you would set this value to 1.

Flag can also be set to one of several special values which tell the menu system to treat this line differently.

Currently to special flags exist, flag 999 tells the menu system that this line is purely for informational
display and is not a selectable menu option.

The second is flag 998 which tells the menu system that this item is not a link to another menu screen but 
should execute and python function which we can declare in myFunction.py.

Type should be set to the string "Menu" unless flag 998 is also used in which case it should contain the name
of the function defined in myFunctions.py

Here is a simple example of a simple set of menus;

#menu.00 - Screen0
"Player",1,"Menu"
"Help",2,"Menu"

#menu.01 - Screen1
"Stop",998,"stopPlayer"
"Start",998,"startPlayer"
"Forward 30 sec",998,"forward30"
"Backwards 30 sec",998,"backwards30"
"Back",0,"Menu"

# menu.02 - Screen2
"This is the",999,"Menu"
"help page....",999,"Menu"
"Back",0,"Menu"

On startup the first menu loaded (Screen0) will be loaded and displayed. 

This will display two menu items which can be skipped through by pressing button 1 and selected with button 2.

If the first menu item on Screen0 is selected the flag value is checked and the screen is changed to the screen 
with the same value, in this example, 1, so screen1 is selected.

On screen1 the first 4 items are not links to other screens but have flag 998 set which denotes these
are function handlers which will call the function named in the type feild.

These function are defined in the myFunction.py file and will be covered later.

The final item on Screen1 is a link back to the start page, Screen0.

Screen2 shows use of the 999 flag which denotes that the first two lines of text are just to be displayed on 
the screen with no link or associated function handler.

myFunctions.py contains function definitions for each function handlers and a python dictionary named 
functionHandlersDictionary which contains one item for each function handler.

Example myFunctions.py;

def myFunction1():
	print("This is myFunction1")

def myFunction2():
	print("This is myFunction2")


# dictionary to hold function handlers
functionHandlersDictionary = { "myFunction1":  [myFunction1, "My function 1"], "myFunction2": [myFunction2, "My Function 2"]}

and the coresponding menu file to call these functions when selected with button 2
#menu.XX
"Execute myFunction1",998,"myFunction1"
"Execute myFunction2",998,"myFunction2"

