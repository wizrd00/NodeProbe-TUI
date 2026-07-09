from _structs import *
from _exceptions import NodeProbeError
from ctypes import c_int, c_size_t
from psutil import net_if_addrs, net_if_stats
from socket import AF_INET, AF_PACKET, if_nametoindex
from re import match

def CHECK_STAT(stat : c_int, msg : str) :
	if (stat != status_t.SUCCESS) :
		raise NodeProbeError(msg, stat)

def get_ifindex(iface : str) -> c_int :
		return c_int(if_nametoindex(iface))

def get_timeout(timeout : int) -> c_int :
	return c_int(timeout)

def get_id(id : int) -> c_ushort :
	if (id not in range(0, 65536)) :
		raise ValueError(f"the \"id\" argument with value \"{id}\" must be a 16-bit number")
	return c_ushort(id)

def get_mac(mac : str) -> Mac :
	if (not match(r"^((?:[a-fA-F0-9]{2}[:]){5}[a-fA-F0-9]{2})$", mac)) :
		raise ValueError(f"the \"mac\" argument with value \"{mac}\" is invalid")
	return Mac(*[int(i, base = 16) for i in mac.split(":")])

def get_ip(ip : str) -> IPv4 :
	if (not match(r"^(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?!$)|$)){4}$", ip)) :
		raise ValueError(f"the \"ip\" argument with value \"{ip}\" is invalid")
	return IPv4(*[int(i) for i in ip.split(".")])

def get_port(port : int) -> c_ushort :
	if (port not in range(0, 65536)) :
		raise ValueError(f"the \"port\" argument with value \"{port}\" must be in (0, 65535) range")
	return c_ushort(port)

def get_mtu(iface : str) -> c_size_t :
	stats = net_if_stats()
	return c_size_t(stats[iface].mtu)

def get_src_mac(iface : str) -> str :
	addrs = net_if_addrs()[iface]
	for addr in addrs :
		if (addr.family == AF_PACKET) :
			return addr.address
	# there is no MAC address
	raise ValueError(f"there is no MAC address assocaited to \"{iface}\"!")


def get_src_ip(iface : str) -> str :
	addrs = net_if_addrs()[iface]
	for addr in addrs :
		if (addr.family == AF_INET) :
			return addr.address
	# there is no IP address
	raise ValueError(f"there is no IP address assocaited to \"{iface}\"")

def check_ip_format(ip : str) -> bool :
	return True
