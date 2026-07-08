from ctypes import *
from _types import *
from _constants import *
from _tools import *
from _nodeprobe import *
import time
import threading


def task_runner(tasks : NodeProbeTaskList, results : NodeProbeResultList) :
	while ((task = tasks.get_task())) :
		results.add_result(task.run())


class NodeProbeTask :
	def __init__(self, iface : str, gateway_mac : str, ip : str, tcp_ports : Iterator[int], udp_ports : Iterator[int], ping : bool) :
		self.iface = iface
		self.out_mac = gateway_mac
		self.ip = ip
		self.tcp_ports = tcp_ports
		self.udp_ports = udp_ports
		self.ping = ping

	def run(self) -> tuple[NodeProbeResult, NodeProbeError] :
		result = NodeProbeResult()
		src_addr = (get_src_mac(self.iface), get_src_ip(self.iface), 0)
		dst_addr = (self.out_mac, self.ip, 0)
		try :
			mod = arpman(self.iface, ARPMAN_TIMEOUT, src_addr[:2], dst_addr[:2])
			start = time.time()
			result.host_mac = mod.arpman_mac_request()
			result.arpman_time = time.time() - start
			dst_addr[0] = ":".join([f"{i:02X}" for i in result.host_mac])
			del mod
		except NodeProbeError as error :
			return (result, error)
		if (self.ping) :
			try :
				mod = icmpman(self.iface, ICMPMAN_TIMEOUT, src_addr[:2], dst_addr[:2])
				start = time.time()
				result.pingable = mod.icmpman_echo_request()
				result.icmpman_time = time.time() - start
				del mod
			except NodeProbeError as error :
				return (result, error)
		try :
			mod = tcpman(self.iface, TCPMAN_TIMEOUT, src_addr, dst_addr)
			start = time.time()
			for port in self.tcp_ports :
				mod.set_src_port(random.randint(1, 65535))
				mod.set_dst_port(port)
				if (mod.tcpman_sync_request()) :
					result.open_tcp_ports.append(port)
			result.tcpman_time = time.time() - start
			del mod
		except NodeProbeError as error :
			return (result, error)
		try :
			mod = udpman(self.iface, UDPMAN_TIMEOUT, src_addr, dst_addr)
			start = time.time()
			for port in self.udp_ports :
				mod.set_src_port(random.randint(1, 65535))
				mod.set_dst_port(port)
				if (mod.udpman_udp_request()) :
					result.open_udp_ports.append(port)
			result.udpman_time = time.time() - start
			del mod
		except NodeProbeError as error :
			return (result, error)
		return (result, None)


class NodeProbeResultList :
	def __init__(self) :
		self.results = []
		self.mutex = threading.Semaphore(value = 1)

	def add_result(self, result : tuple[NodeProbeResult, NodeProbeError]) -> None :
		self.mutex.acquire()
		self.results.append(result)
		self.mutex.release()

	def get_result(self) -> tuple[NodeProbeResult, NodeProbeError] | None :
		self.mutex.acquire()
		result = self.results.pop() if (len(self.results) > 0) else None
		self.mutex.release()
		return result


class NodeProbeTaskList :
	def __init__(self) :
		self.tasks = []
		self.mutex = threading.Semaphore(value = 1)

	def add_task(self, task : NodeProbeTask) -> None :
		self.tasks.append(task)

	def get_task(self) -> NodeProbeTask | None :
		self.mutex.acquire()
		task = self.tasks.pop() if (len(self.tasks) > 0) else None
		self.mutex.release()
		return task


class NodeProbe :
	def __init__(self, iface : str, gateway_mac : str, ips : Iterator[str], tcp_ports : Iterator[int], udp_ports : Iterator[int]) :
		self.iface = iface
		self.out_mac = gateway_mac
		self.ips = ips
		self.tcp_ports = tcp_ports
		self.udp_ports = udp_ports
		self.tasks = NodeProbeTaskList()
		self.results = NodeProbeResultList()
