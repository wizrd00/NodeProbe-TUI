from ctypes import *
from subprocess import getoutput

TITLE = "NodeProbe-TUI"

MAN = """
Manual

1.Specify an IP range
...
"""

TABLE_KEYS = ("IP", "MAC", "RTT")

Mac = c_ubyte * 6
IPv4 = c_ubyte * 4

class arpman_context_t(Structure) :
	_fields_ = [
		("sockfd", c_int),
		("ifindex", c_int),
		("timeout", c_int),
		("src_mac", Mac),
		("out_mac", Mac),
		("src_ip", IPv4),
		("dst_ip", IPv4)
	]

class icmpman_context_t(Structure) :
	_fields_ = [
		("sockfd", c_int),
		("ifindex", c_int),
		("timeout", c_int),
		("id", c_ushort),
		("mtu_size", c_size_t),
		("src_mac", Mac),
		("dst_mac", Mac),
		("src_ip", IPv4),
		("dst_ip", IPv4)
	]

class tcpman_context_t(Structure) :
	_fields_ = [
		("sockfd", c_int),
		("ifindex", c_int),
		("timeout", c_int),
		("mtu_size", c_size_t),
		("src_mac", Mac),
		("dst_mac", Mac),
		("src_ip", IPv4),
		("dst_ip", IPv4),
		("src_port", c_ushort),
		("dst_port", c_ushort)
	]

class udpman_context_t(Structure) :
	_fields_ = [
		("sockfd", c_int),
		("ifindex", c_int),
		("timeout", c_int),
		("mtu_size", c_size_t),
		("src_mac", Mac),
		("dst_mac", Mac),
		("src_ip", IPv4),
		("dst_ip", IPv4),
		("src_port", c_ushort),
		("dst_port", c_ushort)
	]


nodeprobe = cdll.LoadLibrary(f"library/libnodeprobe-{getoutput("ldd --version 2>&1 | grep -qi musl && echo musl || echo glibc")}.so")
