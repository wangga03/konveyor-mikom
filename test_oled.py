import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(board.SCL, board.SDA)

oled = SSD1306_i2C(128, 64, i2c)

oled.fill(0)
oled.show()

width = oled.width
height = oled.height
image = Image.new('1', (width, height))

draw.rectangle((0,0,width, height), outline=0, fill = 0)

text = "hai, wgg"
font = ImageFont.load_default()

draw.text((0,0), text, font=font, fill = 255)

oled.image(image)
oled.show()
