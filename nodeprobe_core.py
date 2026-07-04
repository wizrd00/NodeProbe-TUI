from nodeprobe_types import *


class NodeProbeCore :
	def __init__(self) :
		pass


class NodeProbeIface(NodeProbeCore) :
	def __init__(self) :
		super()

	@staticmethod
	def check_input(value : str) -> bool :
		return "i" in value

