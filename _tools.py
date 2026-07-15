from _structs import *
from _exceptions import NodeProbeError
from ctypes import c_int, c_size_t
from psutil import net_if_addrs, net_if_stats
from socket import AF_INET, AF_PACKET, if_nametoindex, inet_pton
from re import match
from json import load

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
	pat = [
		r"^((1\d{2}|2[0-4]\d|25[0-5]|[1-9]?\d)(\.(?=\d)|(?!\d))){4}(/([12]?\d|3[0-2]))?$",
		r"^((1\d{2}|2[0-4]\d|25[0-5]|[1-9]?\d)(\.(?=\d))){3}((1\d{2}|2[0-4]\d|25[0-5]|[1-9]?\d)-(1\d{2}|2[0-4]\d|25[0-5]|[1-9]?\d))?$",
		r"^(((1\d{2}|2[0-4]\d|25[0-5]|[1-9]?\d)(\.(?=\d)|(?!\d))){4}(\ |$)){1,}$"
	]
	return True if (match(pat[0], ip) or match(pat[1], ip) or match(pat[2], ip)) else False

def get_input_placeholder(iface : str) -> str :
	for addr in net_if_addrs()[iface] :
		if (addr.family != AF_INET) :
			continue
		a = inet_pton(AF_INET, addr.address)
		b = inet_pton(AF_INET, addr.netmask)
		c = int.from_bytes(b)
		net_sec = ".".join([str(a[i] & b[i]) for i in range(4)])
		count = 0
		for i in range(32) :
			count += 1 if ((1 << i) & c != 0) else 0
		return f"{net_sec}/{count}"
	return "192.168.1.1/24"

def get_suggestion_ports() -> list[tuple[int, str, str]] :
	ports = []
	with open("ports.json", "r") as file :
		tmp = load(file)
	for k, v in tmp.items() :
		for i in v :
			ports.append((i["port"], k, i["service"]))
	return ports

def get_ifaces() -> dict_keys[str] :
	return net_if_addrs().keys()
