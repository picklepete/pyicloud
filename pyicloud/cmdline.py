#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
A Command Line Wrapper to allow easy use of pyicloud for
command line scripts, and related.
"""
import argparse
import pickle

import pyicloud


DEVICE_ERROR = (
    "Please use the --device switch to indicate which device to use."
)


def create_pickled_data(idevice, filename):
    """This helper will output the idevice to a pickled file named
    after the passed filename.

    This allows the data to be used without resorting to screen / pipe
    scrapping.  """
    data = {}
    for x in idevice.content:
        data[x] = idevice.content[x]
    location = filename
    pickle_file = open(location, 'wb')
    pickle.dump(data, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
    pickle_file.close()


def main():
    """		Main Function 	"""
    parser = argparse.ArgumentParser(
        description="Find My iPhone CommandLine Tool")

    parser.add_argument(
        "--username",
        action="store",
        dest="username",
        default="",
        help="Apple ID to Use"
    )
    parser.add_argument(
        "--password",
        action="store",
        dest="password",
        default="",
        help="Apple ID Password to Use",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list",
        default=False,
        help="Short Listings for Device(s) associated with account",
    )
    parser.add_argument(
        "--llist",
        action="store_true",
        dest="longlist",
        default=False,
        help="Detailed Listings for Device(s) associated with account",
    )
    parser.add_argument(
        "--locate",
        action="store_true",
        dest="locate",
        default=False,
        help="Retrieve Location for the iDevice (non-exclusive).",
    )

    #   Restrict actions to a specific devices UID / DID
    parser.add_argument(
        "--device",
        action="store",
        dest="device_id",
        default=False,
        help="Only effect this device",
    )

    #   Trigger Sound Alert
    parser.add_argument(
        "--sound",
        action="store_true",
        dest="sound",
        default=False,
        help="Play a sound on the device",
    )

    #   Trigger Message w/Sound Alert
    parser.add_argument(
        "--message",
        action="store",
        dest="message",
        default=False,
        help="Optional Text Message to display with a sound",
    )

    #   Trigger Message (without Sound) Alert
    parser.add_argument(
        "--silentmessage",
        action="store",
        dest="silentmessage",
        default=False,
        help="Optional Text Message to display with no sounds",
    )

    #   Lost Mode
    parser.add_argument(
        "--lostmode",
        action="store_true",
        dest="lostmode",
        default=False,
        help="Enable Lost mode for the device",
    )
    parser.add_argument(
        "--lostphone",
        action="store",
        dest="lost_phone",
        default=False,
        help="Phone Number allowed to call when lost mode is enabled",
    )
    parser.add_argument(
        "--lostpassword",
        action="store",
        dest="lost_password",
        default=False,
        help="Forcibly active this passcode on the idevice",
    )
    parser.add_argument(
        "--lostmessage",
        action="store",
        dest="lost_message",
        default="",
        help="Forcibly display this message when activating lost mode.",
    )

    #   Output device data to an pickle file
    parser.add_argument(
        "--outputfile",
        action="store_true",
        dest="output_to_file",
        default="",
        help="Save device data to a file in the current directory.",
    )

    command_line = parser.parse_args()
    if not command_line.username or not command_line.password:
        parser.error('No username or password supplied')

    from pyicloud import PyiCloudService
    try:
        api = PyiCloudService(
            command_line.username.strip(),
            command_line.password.strip()
        )
    except pyicloud.exceptions.PyiCloudFailedLoginException:
        raise RuntimeError('Bad username or password')

    for dev in api.devices:
        if (
            not command_line.device_id
            or (
                command_line.device_id.strip().lower()
                == dev.content["id"].strip().lower()
            )
        ):
            #   List device(s)
            if command_line.locate:
                dev.location()

            if command_line.output_to_file:
                create_pickled_data(
                    dev,
                    filename=(
                        dev.content["name"].strip().lower() + ".fmip_snapshot"
                    )
                )

            contents = dev.content
            if command_line.longlist:
                print "-"*30
                print contents["name"]
                for x in contents:
                    print "%20s - %s" % (x, contents[x])
            elif command_line.list:
#                print "\n"
                print "-"*30
                print "Name - %s" % contents["name"]
                print "Display Name  - %s" % contents["deviceDisplayName"]
                print "Location      - %s" % contents["location"]
                print "Battery Level - %s" % contents["batteryLevel"]
                print "Battery Status- %s" % contents["batteryStatus"]
                print "Device Class  - %s" % contents["deviceClass"]
                print "Device Model  - %s" % contents["deviceModel"]

            #   Play a Sound on a device
            if command_line.sound:
                if command_line.device_id:
                    dev.play_sound()
                else:
                    raise RuntimeError(
                        "\n\n\t\t%s %s\n\n" % (
                            "Sounds can only be played on a singular device.",
                            DEVICE_ERROR
                        )
                    )

            #   Display a Message on the device
            if command_line.message:
                if command_line.device_id:
                    dev.display_message(
                        subject='A Message',
                        message=command_line.message,
                        sounds=True
                    )
                else:
                    raise RuntimeError(
                        "%s %s" % (
                            "Messages can only be played "
                            "on a singular device.",
                            DEVICE_ERROR
                        )
                    )

            #   Display a Silent Message on the device
            if command_line.silentmessage:
                if command_line.device_id:
                    dev.display_message(
                        subject='A Silent Message',
                        message=command_line.silentmessage,
                        sounds=False
                    )
                else:
                    raise RuntimeError(
                        "%s %s" % (
                            "Silent Messages can only be played "
                            "on a singular device.",
                            DEVICE_ERROR
                        )
                    )

            #   Enable Lost mode
            if command_line.lostmode:
                if command_line.device_id:
                    dev.lost_device(
                        number=command_line.lost_phone.strip(),
                        text=command_line.lost_message.strip(),
                        newpasscode=command_line.lost_password.strip()
                    )
                else:
                    raise RuntimeError(
                        "%s %s" % (
                            "Lost Mode can only be activated "
                            "on a singular device.",
                            DEVICE_ERROR
                        )
                    )

if __name__ == '__main__':
    main()
