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
		CHECK_STAT(nodeprobe.arpman_create_context(pointer(self.context)), "calling arpman_create_context() failed")

	def arpman_mac_request(self) -> Mac :
		mac = Mac()
		CHECK_STAT(nodeprobe.arpman_mac_request(pointer(self.context), pointer(mac)), "calling arpman_mac_request_failed() failed")
		return mac

	def __get_ifindex(self, iface : str) -> c_int :
		return c_int(socket.if_nametoindex(iface))

	def __get_timeout(self, timeout : int) -> c_int :
		return c_int(timeout)

	def __get_mac(self, mac : str) -> Mac :
		if (not re.match(r"^((?:[a-fA-F0-9]{2}[:]){5}[a-fA-F0-9]{2})$", mac)) :
			raise ValueError(f"the \"mac\" argument with value \"{mac}\" is invalid")
		return Mac(*[int(i, base = 16) for i in mac.split(":")])

	def __get_ip(self, ip : str) -> IPv4 :
		if (not re.match(r"^(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})(?:\.(?!$)|$)){4}$", ip)) :
			raise ValueError(f"the \"ip\" argument with value \"{ip}\" is invalid")
		return IPv4(*[int(i) for i in ip.split(".")])

	def __del__(self) :
		os.close(self.context.sockfd)

class NodeProbeCore :
	def __init__(self, ip : str) :
		self.ip = ip


class NodeProbeIface :
	def __init__(self) :
		...

	@staticmethod
	def check_input(value : str) -> bool :
		return True

a = Arpman("wlo1", 1000, "cc:47:40:fc:7b:05", "5e:79:e0:4e:10:86", "10.28.42.207", "10.28.42.66")
mac = a.arpman_mac_request()
print(":".join([f"{i:x}" for i in mac]))
