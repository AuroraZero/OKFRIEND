from I2cLCDRGBBacklight import I2CLCDDisplay #import the LCD Display commands
from TH02 import TH02 #import Temp and Humidity sensor commands
import mraa,time #import time, mraa for gpIO
import thingspeak #import thingspeak api for external data

channel_id = "175387"
write_key = "YUQJ29J2FZ8ZTLD7"
channel = thingspeak.Channel(id=channel_id,write_key=write_key)
LCDDisplay = I2CLCDDisplay()

LCDDisplay.LEDColor(255,255,255) #White
LCDDisplay.LCDPrint("NOW LOOK AT")
LCDDisplay.LCDInstruction(0x80+0x28) #Next Line, first character
LCDDisplay.LCDPrint("  THIS NET")
time.sleep(2)
LCDDisplay.LCDInstruction(0x01)
LCDDisplay.LCDPrint("  THAT I")
LCDDisplay.LCDInstruction(0x80+0x28) #Next Line, first character
LCDDisplay.LCDPrint("  JUST FOUND")
time.sleep(1)

THSensor = TH02()
button = mraa.Gpio(4) #button input on GPIO pin D8
button.dir(mraa.DIR_IN)
soilSensor = mraa.Aio(0) #Soil Sensor on Analogue input 0
lightSensor = mraa.Aio(2) #Light Sensor on Analogue input 2
uvSensor = mraa.Aio(1) #UV Sensor on Analogue input 1

index = 1
while True:
        while(index==1):
                LCDDisplay.LEDColor(128,64,255)
                LCDDisplay.LCDInstruction(0x01) #Clear the display
                LCDDisplay.LCDPrint("UV Sensor:")
                LCDDisplay.LCDInstruction(0x80 + 0x28) #Next line
                LCDDisplay.LCDPrint(str(uvSensor.read()))
                time.sleep(1)
                if(button.read() == 1):
                        index+=1

        while(index==2):
                LCDDisplay.LEDColor(64,128,128)
                LCDDisplay.LCDInstruction(0x01) #Clear the display
                LCDDisplay.LCDPrint("Light Sensor:")
                LCDDisplay.LCDInstruction(0x80 + 0x28) #Next line
                LCDDisplay.LCDPrint(str(lightSensor.read()))
                time.sleep(1)
                if(button.read() == 1):
                        index+=1

        while(index==3):
                LCDDisplay.LEDColor(128,64,192)
                LCDDisplay.LCDInstruction(0x01) #Clear the display
                LCDDisplay.LCDPrint("Soil Sensor:")
                LCDDisplay.LCDInstruction(0x80 + 0x28) #Next line
                LCDDisplay.LCDPrint(str(soilSensor.read()))
                time.sleep(1)
                if(button.read() == 1):
                        index+=1

        while(index==4):
                LCDDisplay.LEDColor(192,0,192)
                LCDDisplay.LCDInstruction(0x01) #Clear the display
                LCDDisplay.LCDPrint("Temp I2C:")
                LCDDisplay.LCDInstruction(0x80 + 0x28) #Next line
                LCDDisplay.LCDPrint(str(THSensor.getTemperature()))
                time.sleep(1)
                if(button.read() == 1):
                        index+=1

        while(index==5):
                LCDDisplay.LEDColor(0,192,64)
                LCDDisplay.LCDInstruction(0x01) #Clear the display
                LCDDisplay.LCDPrint("Humidity I2C:")
                LCDDisplay.LCDInstruction(0x80 + 0x28) #Next line
                LCDDisplay.LCDPrint(str(THSensor.getHumidity()))
                time.sleep(1)
                if(button.read() == 1):
                        index+=1

        while(index==6):
                LCDDisplay.LEDColor(0,255,255)
                LCDDisplay.LCDInstruction(0x01) #Clear the display
                LCDDisplay.LCDPrint("Now Recording...")
                LCDDisplay.LCDInstruction(0x80+0x28)
                LCDDisplay.LCDPrint("Thingspeak Upload....")
                Field1 = str(THSensor.getTemperature())
                Field2 = str(THSensor.getHumidity())
                Field3 = uvSensor.read()
                Field4 = soilSensor.read()
                Field5 = lightSensor.read()
                channel.update({1:Field1,2:Field2,3:Field3,4:Field4,5:Field5}) #upload to thingspeak
                time.sleep(1)

                if(button.read() == 1):
                        index = 1
