#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    # creating an instance
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        #code to handle error
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        #code to handle error
        parser.error("[-] Please specify a MAC address, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    # moreSECURE- cannot access more information using more commands like eth0;ls
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    #subprocess.call(" ifconfig " + interface + " down ", shell=True)
    #subprocess.call(" ifconfig " + interface + " hw ether " + new_mac, shell=True)
    #subprocess.call(" ifconfig " + interface + " up ", shell=True)

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("[-] No address found")

options = get_arguments()
cur_mac = get_current_mac(options.interface)
print("CURRENT MAC: " + str(cur_mac))
change_mac(options.interface, options.new_mac)
cur_mac = get_current_mac(options.interface)

if cur_mac == options.new_mac:
    print("[+] MAC address is successfully changed to " + cur_mac)
else:
    print("[-] MAC address did not change.")

