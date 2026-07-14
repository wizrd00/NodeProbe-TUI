from _structs import *
from rich.text import Text
from textual.widgets import DataTable, Log, Collapsible, Checkbox


class HostList(DataTable) :
	def compose(self) -> ComposeResult :
		yield DataTable()

	def on_mount(self) -> None :
		self.add_columns(*TABLE_KEYS)
		self.add_row(*(Text("192.168.43.81"), Text("E7:AB:CD:EF:12:45"), 123))
		self.add_row(*(Text("192.168.43.221"), Text("E7:AB:CD:EF:12:45"), 123))
		self.fixed_row = 4
		self.cursor_type = "row"


class LogList(Log) :
	def compose(self) -> ComposeResult :
		yield Log()

	def on_mount(self) -> None :
		pass


class HostInfo(Collapsible) :
	def compose(self) -> ComposeResult :
		yield Collapsible()


class PortCheckbox(Checkbox) :
	BUTTON_INNER = "+"
