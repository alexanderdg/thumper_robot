import time
from ADC import ADC
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess


class Display:
	def __init__(self):
		print("Creating OLED display")
		self.RST = None
		self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=self.RST)
		self.disp.begin()
		self.disp.clear()
		self.disp.display()
		self.image = Image.new('1', (self.disp.width, self.disp.height))
		self.draw = ImageDraw.Draw(self.image)
		self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
		self.font = ImageFont.load_default()
		self.adc = ADC()

	def printDaignosctic(self):
		try:
			self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
			cmd = "hostname -I | cut -d\' \' -f1"
			IP = subprocess.check_output(cmd, shell=True)
			cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
			CPU = subprocess.check_output(cmd, shell=True)
			cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
			MemUsage = subprocess.check_output(cmd, shell=True)

			x = 0
			top = 0

			self.draw.text((x, top), "IP: " + str(IP), font=self.font, fill=255)
			self.draw.text((x, top + 8), str(CPU), font=self.font, fill=255)
			self.draw.text((x, top + 16), str(MemUsage), font=self.font, fill=255)

			self.disp.image(self.image)
			self.disp.display()
			time.sleep(.1)
		except:
			pass

	def printBatStatus(self):
		Batvoltage = self.adc.readVoltage()
		Batcurrent = self.adc.readCurrent()
		self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
		self.draw.text((0, 0), "Batvoltage: %.2fV" % Batvoltage, font=self.font, fill=255)
		self.draw.text((0, 8), "Batcurrent: %.2fA" % Batcurrent, font=self.font, fill=255)
		self.disp.image(self.image)
		self.disp.display()
		time.sleep(0.1)

	def printCloseMessage(self):
		self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)
		self.draw.text((0, 0), "Thumper robot", font=self.font, fill=255)
		self.draw.text((0, 8), "Made by ALDGE", font=self.font, fill=255)
		self.disp.image(self.image)
		self.disp.display()
		time.sleep(0.1)

if __name__ == '__main__':
    display = Display()
    display.printBatStatus()