#!/usr/bin/env python

import scapy.all as scapy
from optparse import OptionParser


def get_arguments():
	parser = OptionParser()
	parser.add_option("-t",  "--target", dest="target", help="Target IP / IP range")
	parser.add_option("-q", "--quiet", action="store_false", dest="verbose",
	default=True, help="don't print status message to stdout" )
	(options, args) = parser.parse_args()


def scan(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

	clients_list = []
	for element in answered_list:
		client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
		clients_list.append(client_dict)
	return clients_list


def print_result(results_list):
	print("IP\t\t\tMAC Address\n==============================")
	for client in results_list:
		print(client["ip"] + "\t\t" + client["mac"])


scan_result = scan("10.0.2.1/24")
print_result(scan_result)