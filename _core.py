from ctypes import *
from _structs import *
from _constants import *
from _tools import *
from _nodeprobe import *
import os
import time
import threading # dispite of GIL existanse, most of libnodeprobe operations are I/O-bound. So threading library will be a good choice
import random


def task_runner(tasks : NodeProbeTaskList, results : NodeProbeResultList) :
	while (True) :
		task = tasks.get_task()
		if (not task) :
			break
		results.add_result(task.run())


class NodeProbeTask :
	def __init__(self, iface : str, out_mac : str, ip : str, tcp_ports : Iterator[int], udp_ports : Iterator[int], ping : bool) :
		self.iface = iface
		self.out_mac = out_mac
		self.ip = ip
		self.tcp_ports = tcp_ports
		self.udp_ports = udp_ports
		self.ping = ping

	def run(self) -> tuple[NodeProbeResult, NodeProbeError] :
		result = NodeProbeResult(self.ip)
		src_mac = get_src_mac(self.iface)
		dst_mac = self.out_mac
		src_ip = get_src_ip(self.iface)
		dst_ip = self.ip
		src_port = 0
		dst_port = 0
		try :
			mod = arpman(self.iface, ARPMAN_TIMEOUT, (src_mac, src_ip), (dst_mac, dst_ip))
			print(mod)
			start = time.time()
			result.host_mac = mod.arpman_mac_request()
			result.arpman_time = time.time() - start
			if (not result.host_mac) :
				return (result, None)
			dst_mac = ":".join([f"{i:02X}" for i in result.host_mac])
			del mod
		except NodeProbeError as error :
			return (result, error)
		if (self.ping) :
			try :
				mod = icmpman(self.iface, ICMPMAN_TIMEOUT, random.randint(0, 65535), (src_mac, src_ip), (dst_mac, dst_ip))
				print(mod)
				start = time.time()
				result.pingable = mod.icmpman_echo_request()
				result.icmpman_time = time.time() - start
				del mod
			except NodeProbeError as error :
				return (result, error)
		try :
			mod = tcpman(self.iface, TCPMAN_TIMEOUT, (src_mac, src_ip, src_port), (dst_mac, dst_ip, dst_port))
			print(mod)
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
			mod = udpman(self.iface, UDPMAN_TIMEOUT, (src_mac, src_ip, src_port), (dst_mac, dst_ip, dst_port))
			print(mod)
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
	def __init__(self, iface : str, out_mac : str, ips : Iterator[str], tcp_ports : Iterator[int], udp_ports : Iterator[int], ping : bool) :
		self.iface = iface
		self.out_mac = out_mac
		self.ips = ips
		self.tcp_ports = tcp_ports
		self.udp_ports = udp_ports
		self.ping = ping
		self.cpus = os.process_cpu_count()
		self.tasks = NodeProbeTaskList()
		self.results = NodeProbeResultList()
		self.threads = []

	def is_done(self) :
		return threading.active_count() - 1 == 0

	def run(self) :
		for ip in self.ips :
			self.tasks.add_task(
				NodeProbeTask(
					iface = self.iface,
					out_mac = self.out_mac,
					ip = ip,
					tcp_ports = self.tcp_ports,
					udp_ports = self.udp_ports,
					ping = self.ping
				)
			)
		available_cpus = self.cpus - 1 if (self.cpus > 1) else self.cpus
		for cpu in range(available_cpus) :
			self.threads.append(
				threading.Thread(
					target = task_runner,
					args = (self.tasks, self.results)

				)
			)
		for thread in self.threads :
			thread.start()

probe = NodeProbe(
	iface = "wlo1",
	out_mac = "ff:ff:ff:ff:ff:ff",
	ips = ["10.28.42.66", "10.28.42.195"],
	tcp_ports = [21, 22, 80, 2121, 8080],
	udp_ports = [53, 67, 123],
	ping = True
)
print("exec probe.run()")
probe.run()
while (not probe.is_done()) :
	print("alive threads count %d" % threading.active_count())
	print("not done yet")
	time.sleep(0.5)

while (True) :
	output = probe.results.get_result()
	if (not output) :
		break
	result, error = output
	breakpoint()
