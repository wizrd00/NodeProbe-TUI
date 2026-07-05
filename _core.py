from ctypes import *
from _types import *
from _constants import *
from _tools import *
import os
import socket
import re

# Creating this interface according to NodeProbe Documentation at link https://github.com/wizrd00/NodeProbe/blob/main/assets/doc.md

class arpman :
	def __init__(self, iface : str, timeout : int, src_addr : tuple[str, str], dst_addr : tuple[str, str]) :
		self.context = arpman_context_t(
			ifindex = get_ifindex(iface),
			timeout = get_timeout(timeout),
			src_mac = get_mac(src_addr[0]),
			out_mac = get_mac(dst_addr[0]), # it must be the gateway MAC address
			src_ip = get_ip(src_addr[1]),
			dst_ip = get_ip(dst_addr[1])
		)
		CHECK_STAT(lib.arpman_create_context(pointer(self.context)), "lib.arpman_create_context()")

	def arpman_mac_request(self) -> Mac | None :
		mac = Mac()
		stat = lib.arpman_mac_request(pointer(self.context), pointer(mac))
		match (stat) :
			case status_t.SUCCESS :
				return mac
			case status_t.TIMEOUT :
				return None
			case _ :
				CHECK_STAT(stat, "lib.arpman_mac_request() failed")

	def __del__(self) :
		lib.arpman_delete_context(pointer(self.context))


class icmpman :
	def __init__(self, iface : str, timeout : int, src_addr : tuple[str, str], dst_addr : tuple[str, str]) :
		self.context = icmpman_context_t(
			ifindex = get_ifindex(iface),
			timeout = get_timeout(timeout),
			src_mac = get_mac(src_addr[0]),
			dst_mac = get_mac(dst_addr[0]),
			src_ip = get_ip(src_addr[1]),
			dst_ip = get_ip(dst_addr[1])
		)
		CHECK_STAT(lib.icmpman_create_context(pointer(self.context)), "lib.icmpman_create_context()")

	def icmpman_echo_request(self) -> bool | None :
		stat = lib.icmpman_echo_request(pointer(self.context))
		match (stat) :
			case status_t.SUCCESS :
				return True
			case status_t.TIMEOUT :
				return False
			case _ :
				CHECK_STAT(stat, "lib.icmpman_echo_request() failed")

	def __del__(self) :
		lib.icmpman_delete_context(pointer(self.context))


class tcpman :
	def __init__(self, iface : str, timeout : int, src_addr : tuple[str, str, int], dst_addr : tuple[str, str, int]) :
		self.context = tcpman_context_t(
			ifindex = get_ifindex(iface),
			timeout = get_timeout(timeout),
			mtu_size = get_mtu(iface),
			src_mac = get_mac(src_addr[0]),
			out_mac = get_mac(dst_addr[0]),
			src_ip = get_ip(src_addr[1]),
			dst_ip = get_ip(dst_addr[1]),
			src_port = get_port(src_addr[2])
			dst_port = get_port(dst_addr[2])
		)
		CHECK_STAT(lib.tcpman_create_context(pointer(self.context)), "lib.tcpman_create_context()")

	def tcpman_sync_request(self) -> bool | None :
		stat = lib.tcpman_echo_request(pointer(self.context))
		match (stat) :
			case status_t.SUCCESS :
				return True
			case status_t.FAILURE :
				return False
			case _ :
				CHECK_STAT(stat, "lib.tcpman_sync_request() failed")

	def __del__(self) :
		lib.tcpman_delete_context(pointer(self.context))


class udpman :
	def __init__(self, iface : str, timeout : int, src_addr : tuple[str, str, int], dst_addr : tuple[str, str, int]) :
		self.context = udpman_context_t(
			ifindex = get_ifindex(iface),
			timeout = get_timeout(timeout),
			mtu_size = get_mtu(iface),
			src_mac = get_mac(src_addr[0]),
			out_mac = get_mac(dst_addr[0]),
			src_ip = get_ip(src_addr[1]),
			dst_ip = get_ip(dst_addr[1]),
			src_port = get_port(src_addr[2])
			dst_port = get_port(dst_addr[2])
		)
		CHECK_STAT(lib.udpman_create_context(pointer(self.context)), "lib.udpman_create_context()")

	def udpman_udp_request(self) -> bool | None :
		stat = lib.udpman_echo_request(pointer(self.context))
		match (stat) :
			case status_t.SUCCESS :
				return True
			case status_t.FAILURE :
				return False
			case _ :
				CHECK_STAT(stat, "lib.udpman_udp_request() failed")

	def __del__(self) :
		lib.udpman_delete_context(pointer(self.context))


class NodeProbeTask :
	def __init__(self, iface : str, gateway_mac : str, ip : str, tcp_ports : Iterator[int], udp_ports[int], ping : bool) :
		self.iface = iface
		self.out_mac = gateway_mac
		self.ip = ip
		self.tcp_ports = tcp_ports
		self.udp_ports = udp_ports
		self.ping = ping
		self.arpman = arpman(iface, ARPMAN_TIMEOUT, (get_src_mac(iface), get_src_ip(iface)), (gateway_mac, ip))
		// TODO

class NodeProbe :
	def __init__(self, iface : str, gateway_mac : str, ips : Iterator[str], tcp_ports : Iterator[int], udp_ports : Iterator[int]) :
		self.iface = iface
		self.out_mac = gateway_mac
		self.ips = ips
		self.tcp_ports = tcp_ports
		self.udp_ports = udp_ports
