#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
#
#	A Command Line Wrapper to allow easy use of pyicloud for command line scripts, and related.
#


################################################################################
# Python imports

from optparse import OptionParser
import pyicloud
import sys

################################################################################
# Globals
################################################################################

parser = OptionParser(usage="usage: %prog [options] filename",
					  version="%prog 1.0")

#
#	Username
#
parser.add_option("-u", "--username",
				  action="store",
				  dest="username",
				  default="",
				  help="Apple ID to Use")

#
#	Password
#
parser.add_option("-p", "--password",
				  action="store", 
				  dest="password",
				  default="",
				  help="Apple ID Password to Use",)

#
#	List devices
#
parser.add_option("", "--list",
				  action="store_true", 
				  dest="list_devices",
				  default=False,
				  help="List Device(s) associated with account",)

#
#	Restrict actions to a specific devices UID / DID
#
parser.add_option("", "--device",
				  action="store", 
				  dest="device_id",
				  default=False,
				  help="Only effect this device",)

#
#	Trigger Sound Alert
#
parser.add_option("--sound",
				  action="store_true", 
				  dest="sound",
				  default=False,
				  help="Play a sound on the device",)

#
#	Trigger Message w/Sound Alert
#
parser.add_option("--message",
				  action="store", 
				  dest="message",
				  default=False,
				  help="Optional Text Message to display with a sound",)

#
#	Trigger Message (without Sound) Alert
#
parser.add_option("--silentmessage",
				  action="store", 
				  dest="silentmessage",
				  default=False,
				  help="Optional Text Message to display with no sounds",)

#
#	Lost Mode 
#
parser.add_option("--lostmode",
				  action="store_true", 
				  dest="lostmode",
				  default=False,
				  help="Enable Lost mode for the device",)

parser.add_option("--lostphone",
				  action="store", 
				  dest="lost_phone",
				  default=False,
				  help="Phone Number to allow the user to call when lost mode is enabled",)

parser.add_option("--lostpassword",
				  action="store", 
				  dest="lost_password",
				  default=False,
				  help="Forcibly active this passcode on the idevice",)

parser.add_option("--lostmessage",
				  action="store", 
				  dest="lost_message",
				  default="",
				  help="Forcibly display this message when activating lost mode.",)



(options, args) = parser.parse_args()
print options

if options.username == "" or options.password == "":
	print "No Username or password supplied."
	sys.exit(1)
	
from pyicloud import PyiCloudService
try:
	api = PyiCloudService(options.username.strip(), options.password.strip() )
except PyiCloudFailedLoginException:
	print ("Bad Username or Password")
	sys.exit(1)

for dev in api.devices:
	if options.device_id == False or options.device_id.strip().lower() == dev.content["id"].strip().lower():
		#
		#	List device(s)
		#
		if options.list_devices:
			print "\n"
			print "-"*30
			contents = dev.content
			print contents["name"]
			for x in contents:
				print "%20s - %s" % (x, contents[x])

		#
		#	Play a Sound on a device
		#
		print options.sound
		if options.sound == True:
			if options.device_id <> False:
				dev.play_sound ( )
			else:
				print "\n\n\t\tSounds can only be played on a singular device.  Please use the --device switch to indicate which device to play the sound on.\n\n"
				sys.exit(1)

		#
		#	Display a Message on the device
		#
		if options.message <> False:
			if options.device_id <> False:
				dev.display_message( subject='A Message', message=options.message, sounds=True)
			else:
				print "\n\n\t\tMessages can only be played on a singular device.  Please use the --device switch to indicate which device to play the sound on.\n\n"
				sys.exit(1)

		#
		#	Display a Silent Message on the device
		#
		if options.silentmessage <> False:
			if options.device_id <> False:
				dev.display_message( subject='A Silent Message', message=options.silentmessage, sounds=False)
			else:
				print "\n\n\t\tSilent Messages can only be played on a singular device.  Please use the --device switch to indicate which device to play the sound on.\n\n"
				sys.exit(1)


		#
		#	Enable Lost mode
		#
		if options.lostmode <> False:
			if options.device_id <> False:
				dev.lost_device( number = options.lost_phone.strip(),  text=options.lost_message.strip(), newpasscode = options.lost_password.strip() )
			else:
				print "\n\n\t\tLost Mode can only be activated on a singular device.  Please use the --device switch to indicate which device to play the sound on.\n\n"
				sys.exit(1)

		 