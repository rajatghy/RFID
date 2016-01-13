import multiprocessing
import RPi.GPIO as GPIO
import MFRC522
import signal
import util
import time
import datetime

continue_reading = True #Boolean that changes to false when sigint is captured.

#Capture SIGINT for cleanup when the script is aborted.
def end_read(signal,frame):
	global continue_reading
	print "Ctrl+C captured, ending read."
	continue_reading = False
	GPIO.cleanup()

#Wait For RFID Card and push UID into a queue
def waitForCard(iq):
	# Hook the SIGINT
	signal.signal(signal.SIGINT, end_read)

	# Create an object of the class MFRC522
	MIFAREReader = MFRC522.MFRC522()

	# Welcome message
	print "Welcome to the MFRC522 RFID System"
	print "Press Ctrl-C to stop."

	# This loop keeps checking for chips. If one is near it will get the UID and authenticate
	while continue_reading:

		# Scan for cards    
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

		# If a card is found
		#if status == MIFAREReader.MI_OK:
			#print "Card detected"

		# Get the UID of the card
		(status,uid) = MIFAREReader.MFRC522_Anticoll()

		# If we have the UID, continue
		if status == MIFAREReader.MI_OK:
			#Push the UID into a queue
			rfid = util.uid_to_rfid(uid); 
			temp = [];
			temp.append(rfid);
			temp.append(datetime.datetime.now());
			iq.put(temp);
			#If we put a card in the queue, wait for 5 seconds.
			#This is to avoid sending the same card several times.
			time.sleep(5);

			# #TEST CODE
			# print "Card detected.";