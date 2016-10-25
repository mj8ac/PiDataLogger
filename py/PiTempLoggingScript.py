#!/usr/bin/python

import 	sys
import 	cgi, cgitb
import 	time
import 	random
import 	json
import 	thread
from 	time 	import sleep
import csv
import os

cgitb.enable()

print "Content-type: text/html\n"
print " "

# testing branching

lastTemperature = [0,0,0,0,0,0,0,0]
jsonTempList = [[],[],[],[],[],[],[],[]]
jsonTempDict = [[],[],[],[],[],[],[],[]]
globalTempReadings = []

def getProbeAssignment():
	files = os.listdir("/sys/bus/w1/devices")
	files.remove("w1_bus_master1")
	probeList = {}
	for file in files:
		tmpFile = open("/sys/bus/w1/devices/"+file+"/w1_slave")
		probeNumber = tmpFile.read()
		tmpFile.close()
		probeNumber	= probeNumber.split("\n")[1].split(" ")[4]
		probeNumber = int(probeNumber[1])
		probeList[probeNumber]="/sys/bus/w1/devices/"+file+"/w1_slave"
		
	return probeList		

def getProbeTemperatures(probeList):
	tempReadings = []
	global lastTemperature
	
	
	for probe in probeList:
		tempReadingFile = open(probeList[probe])
		tempReading = tempReadingFile.read()
		tempReadingFile.close()
		tempReading = tempReading.split("\n")[1].split(" ")[9]
		tempReading = float(tempReading[2:])
		tempReading = tempReading / 1000
	
		if tempReading == 0:
			tempReading = lastTemperature[probe]
		if tempReading > 600:
			tempReading = 0
		else:
			lastTemperature[probe] = tempReading
			
		tempReadings.append(tempReading)
	
	return tempReadings		

def getTemperatures(probeList):
	global globalTempReadings
	
	while(True):
		globalTempReadings = getProbeTemperatures(probeList)
		createRealTimeChartFiles(globalTempReadings)
		print(globalTempReadings)

def createRealTimeChartFiles(tempReadings):
	for number in range(8):
	# create the real time chart files
		with open("/var/www/PizzaOven/t"+str(number+1)+"realTimeData.txt", "w") as datafile:
			datafile.seek(0)
			datafile.write(str(tempReadings[number]))
			datafile.truncate()	

		
def createChartFiles(tempReadings):
	global jsonTempList
	global jsonTempDict
	
	for number in range(8):
	
	# create the real time chart files
		# with open("/var/www/PizzaOven/t"+str(number+1)+"realTimeData.txt", "w") as datafile:
			# datafile.seek(0)
			# datafile.write(str(tempReadings[number]))
			# datafile.truncate()	
		
	# create the two minute chart files
		jsonTempList[number].append([(chartTime*1000), tempReadings[number]])
		jsonTempDict[number]={"label":"T" + str(number+1) , "data":jsonTempList[number]}
		with open("/var/www/PizzaOven/t"+str(number+1)+"LogChartData.json", "w") as LogChartFile:
			json.dump(jsonTempDict[number], LogChartFile)
	
def writeToSysLog():
	while (True):
		sys.stderr.write("Log from PizzaTempLogger thread")
		sleep(300)

logFile	= open("/var/www/debugLogFile.txt", "w")

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Create the new log files
LogDate = time.strftime("%Y-%m-%d_")

# Set the logging frequency in seconds
logFrequency = 120
logTime = 0

logFile.write("Creating new thread\n")
logFile.close()
thread.start_new_thread(writeToSysLog, ())


# get the probe ordering
probeList = getProbeAssignment()
thread.start_new_thread(getTemperatures, (probeList,))

sleep(10)

with open("/var/www/debugLogFile.txt", "a") as debugFile:
	debugFile.write("Threading has been started \n")

fileDate = time.strftime("%y-%m-%d_%H%M")

with open('/home/pi/TemperatureLogFiles/PiLoggerData_' + fileDate + '.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['Time', 'T1 [C]', 'T2 [C]', 'T3 [C]', 'T4 [C]', 'T5 [C]', 'T6 [C]', 'T7 [C]', 'T8 [C]'])
			
while True:
	
	logTime = time.strftime("%H%M")
	chartTime = time.time()
	
	# get the temperature data
	#tempReadings = getProbeTemperatures(probeList)
		
	#log data to csv file
	with open('/home/pi/TemperatureLogFiles/PiLoggerData_' + fileDate + '.csv', 'ab') as csvfile:
		writer = csv.writer(csvfile)		
		writer.writerow([logTime, globalTempReadings[0], globalTempReadings[1], globalTempReadings[2], globalTempReadings[3], 
		globalTempReadings[4], globalTempReadings[5], globalTempReadings[6], globalTempReadings[7]])
				
	createChartFiles(globalTempReadings)
			
	sleep(logFrequency)
	
	with open("/var/www/debugLogFile.txt", "a") as debugFile:
		debugFile.write("At the end of while loop \n\n")
		
thread.exit()
with open("/var/www/debugLogFile.txt", "a") as debugFile:
		debugFile.write("foodTemp > targetFoodTemp\n Leaving sys log thread\n")