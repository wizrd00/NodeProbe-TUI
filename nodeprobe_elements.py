from nodeprobe_types import *
from rich.text import Text
from textual.widgets import Label, Input, Button, DataTable, Log, Collapsible


class ManualLabel(Label) :
	...


class RangeInput(Input) :
	...


class Scan(Button) :
	...


class ProbeAll(Button) :
	...

class ProbeSelected(Button) :
	...


class ClearLogs(Button) :
	...


class BackMenu(Button) :
	...


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



