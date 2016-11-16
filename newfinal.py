from I2cLCDRGBBacklight import I2CLCDDisplay #import the LCD Display commands
from TH02 import TH02 #import Temp and Humidity sensor commands
import mraa,time #import time, mraa for gpIO
import thingspeak #import thingspeak api for external data

channel_id = "175387" #Thingspeak channel ID
write_key = "YUQJ29J2FZ8ZTLD7" #Thingspeak Write Key
channel = thingspeak.Channel(id=channel_id,write_key=write_key) #Channel update function

LEDColor(255,255,255) #White
LCDPrint("NOW LOOK AT")#Print text to Display
LCDInstruction(0x80+0x28) #Next Line, first character
LCDPrint("  THIS NET")
time.sleep(1)#Sleep for a sec
LCDInstruction(0x01)#Clear Display
LCDPrint("  THAT I")
LCDInstruction(0x80+0x28) #Next Line, first character
LCDPrint("  JUST FOUND")

THSensor = TH02() #Temperature & Humidity Sensor function from TH02.py
button = mraa.Gpio(8) #button input on GPIO pin D8
button.dir(mraa.DIR_IN) #gpIO direction as input
soilSensor = mraa.Aio(0) #Soil Sensor on Analogue input 0
lightSensor = mraa.Aio(2) #Light Sensor on Analogue input 2
uvSensor = mraa.Aio(1) #UV Sensor on Analogue input 1

index = 1 #initialise index variable as 1
while True: #main loop
	while(index==1): #first case, will be executed on first run and displays UV data
		LCDDisplay.LEDColor(128,64,255)
		LCDDisplay.LCDInstruction(0x01) #Clear the display
		LCDDisplay.LCDPrint("UV Sensor:")
		LCDDisplay.LCDInstruction(0x80 + 0x28) #Next line
		LCDDisplay.LCDPrint(str(uvSensor.read()))#We use string because the display may not accept integer varable types
		time.sleep(1)
		if(button.read() == 1):#If the button is depressed, increase the index value by 1, so that it gets kicked into the next loop
			index+=1
	
	while(index==2):#next case, will display Light sensor data
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
		LCDDisplay.LCDPrint(str(THSensor.getHumidity()))#Using strings again, just in case
		time.sleep(1)
		if(button.read() == 1):
			index+=1
	
	while(index==6):
		LEDColor(0,255,255)
		LCDDisplay.LCDInstruction(0x01) #Clear the display
		LCDDisplay.LCDPrint("Now Recording...")
		LCDDisplay.LCDInstruction(0x80+0x28)
		LCDDisplay.LCDPrint("Thingspeak Upload....")
		Field1 = str(THSensor.getTemperature())#update all the field values to send to thingspeak
		Field2 = str(THSensor.getHumidity())
		Field3 = uvSensor.read()
		Field4 = soilSensor.read()
		Field5 = lightSensor.read()
		channel.update({1:Field1,2:Field2,3:Field3,4:Field4,5:Field5}) #upload to thingspeak
		time.sleep(1)
		if(button.read() == 1):#reset to top of loop if button is depressed
			index = 1
