# Import the neccessary libraries
import RPI.GPIO as GPIO 
import time 
import datetime
import csv 
from aws import get_AWS_client, upload_to_AWS

# Perform the GPIO callback to check moisture levels
def callback(channel):  
	s3 = get_AWS_client()
	if GPIO.input(channel):
		print "LED off"
		name = write_CSV(False)
		upload_to_AWS(s3, name, 'soil_monitoring-bucket', name)
	else:
		print "LED on"
		name = write_CSV(True)
		upload_to_AWS(s3, name, 'soil_monitoring-bucket', name)

def write_CSV(water_boolean):
	if water_boolean:
		needs_water = 'False'
	else:
		needs_water = 'True'
	now = datetime.datetime.now()
	name = "data/" + now.strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
	try:
		with open(name, 'w', newline='') as file:
			writer = csx.writer(file)
			writer.writerow(["timestamp", "needs_water"])
			writer.writerow([now.strftime('%Y-%m-%d_%H-%M-%S'), needs_water])
	except:
		print('Error with writing CSV file')
	return name

def main():
	# Set our GPIO numbering to BCM
	GPIO.setmode(GPIO.BCM)
	# Define the GPIO pin that we have our digital output from our sensor connected to
	channel = 17
	# Set the GPIO pin to an input
	GPIO.setup(channel, GPIO.IN)
	# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
	GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
	# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
	GPIO.add_event_callback(channel, callback)

	while True:
		time.sleep(600)


if __name__ == '__main__':
	main()
