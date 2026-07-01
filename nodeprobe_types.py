from ctypes import *

TITLE = "NodeProbe-TUI"

MAN = """
Manual

1.Specify an IP range
...
"""

TABLE_KEYS = ("IP", "MAC", "RTT")

class arpman_context_t(Structure) :
	_fields_ = [
		("sockfd", c_int),
		("ifindex", c_int),
		("timeout", c_int),
		("src_mac", c_ubyte * 6),
		("out_mac", c_ubyte * 6),
		("src_ip", c_ubyte * 4),
		("dst_ip", c_ubyte * 4)
	]

class icmpman_context_t(Structure) :
	_fields_ = [
		("sockfd", c_int),
		("ifindex", c_int),
		("timeout", c_int),
		("id", c_ushort),
		("mtu_size", c_size_t),
		("src_mac", c_ubyte * 6),
		("dst_mac", c_ubyte * 6),
		("src_ip", c_ubyte * 4),
		("dst_ip", c_ubyte * 4)
	]

class tcpman_context_t(Structure) :
	_fields_ = [
		("sockfd", c_int),
		("ifindex", c_int),
		("timeout", c_int),
		("mtu_size", c_size_t),
		("src_mac", c_ubyte * 6),
		("dst_mac", c_ubyte * 6),
		("src_ip", c_ubyte * 4),
		("dst_ip", c_ubyte * 4),
		("src_port", c_ushort),
		("dst_port", c_ushort)
	]

class udpman_context_t(Structure) :
	_fields_ = [
		("sockfd", c_int),
		("ifindex", c_int),
		("timeout", c_int),
		("mtu_size", c_size_t),
		("src_mac", c_ubyte * 6),
		("dst_mac", c_ubyte * 6),
		("src_ip", c_ubyte * 4),
		("dst_ip", c_ubyte * 4),
		("src_port", c_ushort),
		("dst_port", c_ushort)
	]
