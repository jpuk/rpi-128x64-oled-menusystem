#class to control the screen and disply information
# global setting file
import sys
sys.path.insert(0, "../")
import globalsettings
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

########
#globals
# Raspberry Pi pin configuration:
RST  = globalsettings.RST
# Note the following are only used with SPI:
DC = globalsettings.DC
SPI_PORT = globalsettings.SPI_PORT
SPI_DEVICE = globalsettings.SPI_DEVICE

#screen configuration
# height of each text line in pixels
TEXT_LINE_X = globalsettings.TEXT_LINE_X
TEXT_Y_OFFSET = globalsettings.TEXT_Y_OFFSET
# this oled has two sections, 16 pixel yellow bar at the top and then the remaining 48 pixels are blue
# this var marks the start of the main section of the screen and anything to be displayed in it should be offset by it
MAIN_X = globalsettings.MAIN_X
MAX_ITEM_PERSCREEN = globalsettings.MAX_ITEM_PERSCREEN
SECOND_SCREEN = globalsettings.SECOND_SCREEN



class Display:
	def __init__(self):
		self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
		self.disp.begin()
		self.disp.clear()
		self.disp.display()
		self.width = self.disp.width
		self.height = self.disp.height
		self.image = Image.new('1', (self.width, self.height))
		self.draw = ImageDraw.Draw(self.image)
		self.font = ImageFont.truetype(globalsettings.FONT_NAME, globalsettings.FONT_SIZE)

	#draw title in the header section of the oled
	def drawTitle(self, text):
		self.draw.rectangle((0,0,self.width,MAIN_X), outline=0, fill=1)
		self.draw.text((3, 3),    text, font=self.font, fill=0)
		self.disp.image(self.image)
		self.disp.display()

	def drawTextLine(self, text, line, selected=False):
		#print("about to write to screen, ", text)
		if (selected == True):
			line_x = (MAIN_X + (TEXT_LINE_X * line))
			self.draw.rectangle((0,line_x, self.width, (line_x + TEXT_LINE_X) ), outline=0, fill=255)
			self.draw.text((TEXT_Y_OFFSET, (MAIN_X + (TEXT_LINE_X * line))),    text, font=self.font, fill=0)		
		else:
			self.draw.text((TEXT_Y_OFFSET, (MAIN_X + (TEXT_LINE_X * line))),    text, font=self.font, fill=255)
		self.disp.image(self.image)
		self.disp.display()
	
	#clear the main section of the screen leaving the header intact
	def clearMainScreen(self):
		self.draw.rectangle((0,MAIN_X, self.width, 64 ), outline=0, fill=0)
		self.disp.image(self.image)
		self.disp.display()
	

	def overwriteSelection(self, x):
		line_x = x - TEXT_LINE_X
		self.draw.rectangle((0,line_x, self.width, (line_x + TEXT_LINE_X) ), outline=0, fill=0)
		self.disp.image(self.image)
		self.disp.display()
	
	def clearDisplay(self):
		self.disp.clear()
		self.disp.image(self.image)
		self.disp.display()
