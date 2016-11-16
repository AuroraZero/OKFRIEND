#Jackson Heystek
#Student ID 5847605
#Intel Edison Final Assessment

from I2cLCDRGBBacklight import I2CLCDDisplay #import the LCD Display commands
from TH02 import TH02 #import Temp and Humidity sensor commands
import mraa,time #import time, mraa for gpIO
import thingspeak #import thingspeak api for external data

channel_id = "175387"
write_key = "YUQJ29J2FZ8ZTLD7"
channel = thingspeak.Channel(id=channel_id,write_key=write_key)
LCDDisplay = I2CLCDDisplay() #Assign LCDDisplay as our display var

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

LCD = I2cLCDInit() #Initialize the Display
LCDLED = I2cLCDLEDInit() #Initialize the RGB Display backlight

LEDColor(255,255,255) #White
LCDPrint("Jackson Heystek")
LCDInstruction(0x80+0x28) #Next Line, first character
LCDPrint("2/11/2016")
time.sleep(1)
LEDColor(128,64,255)
time.sleep(4)

THSensor = TH02() #Use the imported TH02 library for the Temp and Humidity Sensor
index=1 #Button index value
while True: #Main loop
		button = mraa.Gpio(8) #button input on GPIO pin D8
		button.dir(mraa.DIR_IN)
		soilSensor = mraa.Aio(0) #Soil Sensor on Analogue input 0
		lightSensor = mraa.Aio(2) #Light Sensor on Analogue input 2
		uvSensor = mraa.Aio(1) #UV Sensor on Analogue input 1
		
        while(index==1):
                LEDColor(255,128,0)
                LCDDisplay.LCDInstruction(0x01) #Clear the display
                LCDDisplay.LCDPrint("UV Sensor:")
                LCDDisplay.LCDInstruction(0x80 + 0x28) #Next line
                LCDDisplay.LCDPrint(str(uvSensor.read()))
                time.sleep(1)
                if(button.read() == 1): #if the button is depressed, go to the next sensor
                        index+=1 

        while(index==2):
                LEDColor(128,255,128)
                LCDDisplay.LCDInstruction(0x01)
                LCDDisplay.LCDPrint("Light Sensor:")
                LCDDisplay.LCDInstruction(0x80 + 0x28)
                LCDDisplay.LCDPrint(str(lightSensor.read()))
                time.sleep(1)
                if(button.read() == 1):
                        index+=1

        while(index==3):
                LEDColor(0,128,255)
                LCDDisplay.LCDInstruction(0x01)
                LCDDisplay.LCDPrint("Soil Sensor:")
                LCDDisplay.LCDInstruction(0x80 + 0x28)
                LCDDisplay.LCDPrint(str(soilSensor.read()))
                time.sleep(1)
                if(button.read() == 1):
                        index+=1

        while(index==4):
               
				LEDColor(128,0,128)
                LCDDisplay.LCDInstruction(0x01)
                LCDDisplay.LCDPrint("Temp:  Humidity:")
                LCDDisplay.LCDInstruction(0x80 + 0x28)
                LCDDisplay.LCDPrint(temp)
                LCDDisplay.LCDPrint("  ")
                LCDDisplay.LCDPrint(humidity)
                time.sleep(1)
                if(button.read() == 1):
                        index+=1

        while(index==5):
                LEDColor(0,255,255)
                LCDDisplay.LCDInstruction(0x01) #Clear the display
                LCDDisplay.LCDPrint("Uploading...")
                time.sleep(1)
                Field1 = temp
                Field2 = humidity
                Field3 = uvSensor.read()
                Field4 = soilSensor.read()
                Field5 = lightSensor.read()
                channel.update({1:Field1,2:Field2,3:Field3,4:Field4,5:Field5}) #upload to thingspeak
                if(button.read() == 1):
                        index = 1
