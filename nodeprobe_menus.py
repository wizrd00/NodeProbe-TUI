from nodeprobe_types import *
from nodeprobe_elements import *
from nodeprobe_core import *
from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import VerticalGroup, HorizontalGroup, VerticalScroll
from textual.validation import Function
from textual.widgets import Header, Footer, Checkbox

class MonitorMenu(Screen) :
	def compose(self) -> ComposeResult :
		yield Header(icon = " ")
		with VerticalGroup(id = "VerticalGroup1") :
			with HorizontalGroup(id = "HorizontalGroup1") :
				yield HostList(id = "HostList")
				yield LogList(id = "LogList")
			with HorizontalGroup(id = "HorizontalGroup2") :
				yield HostInfo(id = "HostInfo")
				with VerticalGroup(id = "VerticalGroup2") :
					yield Button(label = "Probe All", id = "ProbeAll")
					yield Button(label = "Probe Selected", id = "ProbeSelected")
					yield Button(label = "Clear Logs", id = "ClearLogs")
					yield Button(label = "Back Menu", id = "BackMenu")
		yield Footer()

	def on_mount(self) -> None :
		self.title = TITLE

	def on_data_table_cell_selected(self, event : DataTable.CellSelected) -> None :
		...


class MainMenu(Screen) :
	def compose(self) -> ComposeResult :
		yield Header(icon = " ")
		with HorizontalGroup(id = "HorizontalGroup3") :
			yield Label(MAN, id = "ManualLabel")
			with VerticalScroll(id = "VerticalScroll1") :
				for _ in range(20) :
					yield Checkbox("hello")
			with VerticalGroup(id = "VerticalGroup3") :
				yield Input(
					placeholder = "192.168.1.1/24",
					type = "text",
					validators = [
						Function(NodeProbeIface.check_input, "Invalid IPv4 address range")
					],
					id = "RangeInput"
				)
				yield Label("Enter a valid IPv4 range", id = "RangeInputStatus")
				yield Button(label = "Scan", id = "Scan")

		yield Footer()

	def on_mount(self) -> None :
		self.title = TITLE

	def on_checkbox_changed(self, event : Checkbox.Changed) -> None :
		...

	@on(Input.Submitted)
	def check_range_input(self, event : Input.Submitted) -> None :
		if not event.validation_result.is_valid :
			self.query_one("#RangeInputStatus").update("You must enter a valid IPv4 range")
		else :
			self.query_one("#RangeInputStatus").update("Press Scan")
