#!/usr/bin/env python

import os
import scapy.all as scapy
import requests
import commands
from uuid import getnode as get_mac

def check_root():
    uid = os.getuid()
    if str(uid) != '0':
        print("[*] Run az root")
        exit()

def get_range_ip():
	local_ip = commands.getoutput('hostname -I')
	local_ip = local_ip.split('.')
	local_ip.remove(local_ip[-1])
	local_ip.append('0/24')
	local_ip = '.'.join(local_ip)
	return local_ip

def get_vendor(mac):
	api_url = 'http://macvendors.co/api/%s'
	json_result = requests.get(api_url % mac)
	dict_result = json_result.json()
	company = dict_result[u'result'][u'company']
	return company

def scan(ip):
	arp_request = scapy.ARP(pdst=ip)
	brodcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_brodcast = brodcast/arp_request
	answered_list = scapy.srp(arp_request_brodcast, timeout=0.5, verbose=False)[0]
	clients_list = []
	for elements in answered_list:
		clients_dict = {"ip":elements[1].psrc, "mac":elements[1].hwsrc, "vendor":get_vendor(elements[1].hwsrc)}
		clients_list.append(clients_dict)
	return clients_list

def main():
	check_root()
	result = scan(get_range_ip())
	print "IP\t\t\tAt MAC Address\t\t\tVendor/Company"
	print "-----------------------------------------------------------------------------------------"
	for i in result:
		print i["ip"] + "\t\t" + (i["mac"]).upper() + "\t\t" + i["vendor"]

if __name__ == "__main__":
	main()
