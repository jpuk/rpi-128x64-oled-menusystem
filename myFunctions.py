# functions which are called by function handlers when button 2 is pushed
		
def myFunction1():
	print("This is myFunction1")

def myFunction2():
	print("This is myFunction2")


# dictionary to hold function handlers
functionHandlersDictionary = { "myFunction1":  [myFunction1, "My function 1"], "myFunction2": [myFunction2, "My Function 2"]}
