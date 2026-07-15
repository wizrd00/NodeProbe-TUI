from _structs import *
from _constants import *
from _globals import *
from _elements import *
from _core import *
from _tools import *
from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import VerticalGroup, HorizontalGroup, VerticalScroll
from textual.validation import Function
from textual.widgets import Header, Footer, Checkbox, Input, Label, Button, ListView, ListItem


class MainMenu(Screen) :
	selected = reactive(None, recompose = True)
	def compose(self) -> ComposeResult :
		global IFACE
		yield Header(icon = " ")
		with HorizontalGroup(id = "HorizontalGroup3") :
			if (self.selected in get_ifaces()) :
				IFACE = self.selected
				with VerticalScroll(id = "VerticalScroll1") :
					yield PortCheckbox("Ping", id = "PingCheckbox")
					ports_list = get_suggestion_ports()
					for port, trans, proto in ports_list :
						obj = PortCheckbox(f"\[{trans}] {port} {proto}")
						obj.port_value = (port, trans)
						yield obj
				with VerticalGroup(id = "VerticalGroup3") :
					yield Input(
						placeholder = get_input_placeholder(IFACE),
						type = "text",
						validators = [
							Function(check_ip_format, "Invalid IPv4 address range")
						],
						id = "RangeInput"
					)
					yield Label(
						"Valid IPv4 range formats :\n\t1. a.b.c.d/x (example: 192.168.1.1/24)\n\t2. a.b.c.x-y (example: 192.168.1.1-123)\n\t3. ip list (example: 192.168.1.1 192.168.1.22 192.168.2.56)",
						id = "ManualLabel"
					)
					yield Label("Enter a valid IPv4 range ▲", id = "RangeInputStatus")
					yield Button(label = "Scan", id = "Scan")
			else :
				iface_items = []
				for iface in get_ifaces() :
					item = ListItem(Label(iface))
					item.text = iface
					iface_items.append(item)
				with VerticalGroup() :
					yield Label("Select Network Interface ▼", id = "SelectLabel")
					yield ListView(*iface_items)

		yield Footer()

	def on_mount(self) -> None :
		self.title = TITLE

	def on_button_pressed(self, event : Button.Pressed) -> None :
		global IP_INPUT_VALUE
		if (event.button.id == "Scan") :
			if (not check_ip_format(IP_INPUT_VALUE)) :
				self.query_one("#RangeInputStatus").update("You must enter a valid IPv4 range ▲")
				return
			self.app.push_screen(MonitorMenu())
	def on_checkbox_changed(self, event : Checkbox.Changed) -> None :
		if (event.checkbox.id == "PingCheckbox") :
			PING = event.checkbox.value
		elif (event.checkbox.value) :
			PORTS.append(event.checkbox.port_value)
		else :
			PORTS.remove(event.checkbox.port_value) if (event.checkbox.port_value in PORTS) else ...

	def on_list_view_selected(self, event : ListView.Selected) -> None :
		self.selected = event.item.text

	@on(Input.Submitted)
	def check_submitted_range_input(self, event : Input.Submitted) -> None :
		global IP_INPUT_VALUE
		ip_input_stat = self.query_one("#RangeInputStatus")
		if not event.validation_result.is_valid :
			ip_input_stat.update("You must enter a valid IPv4 range ▲")
			IP_INPUT_VALUE = ""
		else :
			ip_input_stat.update("Press Scan ▼")
			ip_input = self.query_one("#RangeInput")
			IP_INPUT_VALUE = ip_input.value

	@on(Input.Changed)
	def check_changed_range_input(self, event : Input.Changed) -> None :
		global IP_INPUT_VALUE
		ip_input = self.query_one("#RangeInput")
		if (check_ip_format(ip_input.value)) :
			IP_INPUT_VALUE = ip_input.value


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

