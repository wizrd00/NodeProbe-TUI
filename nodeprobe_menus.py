from nodeprobe_types import *
from nodeprobe_elements import *
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import VerticalGroup, HorizontalGroup, VerticalScroll
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
					yield ProbeAll(label = "Probe All", id = "ProbeAll")
					yield ProbeSelected(label = "Probe Selected", id = "ProbeSelected")
					yield ClearLogs(label = "Clear Logs", id = "ClearLogs")
					yield BackMenu(label = "Back Menu", id = "BackMenu")
		yield Footer()

	def on_mount(self) -> None :
		self.title = TITLE

	def on_data_table_cell_selected(self, event : DataTable.CellSelected) -> None :
		...


class MainMenu(Screen) :
	def compose(self) -> ComposeResult :
		yield Header(icon = " ")
		with HorizontalGroup(id = "HorizontalGroup3") :
			yield ManualLabel(MAN, id = "ManualLabel")
			with VerticalScroll(id = "VerticalScroll1") :
				for _ in range(20) :
					yield Checkbox("hello")
			with VerticalGroup(id = "VerticalGroup3") :
				yield RangeInput(placeholder = "192.168.1.1/24", id = "RangeInput")
				yield Scan(label = "Scan", id = "Scan")

		yield Footer()

	def on_mount(self) -> None :
		self.title = TITLE

	def on_checkbox_changed(self, event : Checkbox.Changed) -> None :
		...


