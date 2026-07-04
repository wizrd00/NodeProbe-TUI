from ctypes import *
from nodeprobe_types import *
import os
import socket
import re

class Arpman :
	def __init__(self, iface : str, timeout : int, src_mac : str, out_mac : str, src_ip : str, dst_ip : str) :
		self.context = arpman_context_t(
			ifindex = self.__get_ifindex(iface),
			timeout = self.__get_timeout(timeout),
			src_mac = self.__get_mac(src_mac),
			out_mac = self.__get_mac(out_mac),
			src_ip = self.__get_ip(src_ip),
			dst_ip = self.__get_ip(dst_ip)
		)

	def __get_ifindex(self, iface : str) -> c_int :
		return c_int(socket.if_nametoindex(iface))

	def __get_timeout(self, timeout : int) -> c_int :
		return c_int(timeout)

	def __get_mac(self, mac : str) -> Mac :
		if (not re.match(r"^((?:[a-fA-F0-9]{2}[:]){5}[a-fA-F0-9]{2})$", mac)) :
			raise ValueError(f"the \"mac\" argument with value \"{mac}\" is invalid")
		return Mac(*[int(i, base = 16) for i in mac.split(":")])

	def __get_ip(self, ip : str) -> IPv4 :
		if (not re.match(r"^(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?!$)|$)){4}$", mac)) :
			raise ValueError(f"the \"ip\" argument with value \"{ip}\" is invalid")
		return IPv4(*[int(i) for i in ip.split(".")])

	def __del__(self) :
		os.close(self.context.sockfd.value)

class NodeProbeCore :
	def __init__(self, ip : str) :
		self.ip = ip


class NodeProbeIface :
	def __init__(self) :

	@staticmethod
	def check_input(value : str) -> bool :
		return True

