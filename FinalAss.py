#Jackson Heystek
#Student ID 5847605
#Intel Edison Final Assessment

from TH02 import TH02 #import Temp and Humidity sensor
import mraa,time #import time, mraa for gpIO
import thingspeak #import thingspeak api for external data

channel_id = "175387"
write_key = "YUQJ29J2FZ8ZTLD7"
channel = thingspeak.Channel(id=channel_id,write_key=write_key)

def LCDInstruction(instruction):
        LCD.writeReg(0x80,instruction)
        time.sleep(0.05)
        return

def I2cLCDInit():
        LCD = mraa.I2c(0)
        LCD.address(0x3e)
        LCD.writeReg(0x80,0x38) #8Bit, 2lines, 5x7
        time.sleep(0.05)
        LCD.writeReg(0x80,0x08+0x07) #display on, cursor on, blink on
        time.sleep(0.05)
        LCD.writeReg(0x80,0x01) #clear display, cursor 1st line, 1st character
        return(LCD)

def I2cLCDLEDInit():
        LCDLED = mraa.I2c(0)
        LCDLED.address(0x62)
        LCDLED.writeReg(0,0)
        LCDLED.writeReg(1,0)
        LCDLED.writeReg(0x08,0xaa)
        return(LCDLED)

def LCDPrint(text):
        for letter in text:
                LCD.writeReg(0x40,ord(letter))
        return

def LEDColor(R,G,B):
        LCDLED.writeReg(4,R)
        LCDLED.writeReg(3,G)
        LCDLED.writeReg(2,B)
        return

LCD = I2cLCDInit()
LCDLED = I2cLCDLEDInit()

LEDColor(255,255,255)
LCDPrint("Jackson Heystek")
LCDInstruction(0x80+0x28) #Next Line, first character
LCDPrint("26/10/2016")
time.sleep(1)
LEDColor(0,255,255)
time.sleep(1)
LEDColor(255,0,255)
time.sleep(1)
LEDColor(255,255,0)
time.sleep(1)
LEDColor(255,0,0)
time.sleep(1)
LEDColor(255,255,255)

button = mraa.Aio(0)
button.dir(mraa.DIR_IN)
soilHumidity = mraa.Aio(1)
soilHumidity.dir(mraa.DIR_IN)
lightSensor = mraa.Aio(2)
lightSensor.dir(mraa.DIR_IN)
uvSensor = mraa.Aio(3)
uvSensor.dir(mraa.DIR_IN)

sensor = TH02()
temp = sensor.getTemperature()
humidity = sensor.getHumidity()
print temp
print humidity

Field1 = temp
Field2 = humidity
response = channel.update({1:Field1, 2:Field2})
