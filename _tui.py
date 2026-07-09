from _structs import *
from _core import *
from _tools import *
from _menus import *
from textual.app import App


class NodeProbeTUI(App) :
	BINDINGS = [("t", "switch_theme", "Switch Theme")]
	CSS_PATH = "style.css"

	def on_mount(self) -> None :
		self.push_screen((MainMenu()))

	def on_button_pressed(self, event : Button.Pressed) -> None :
		match (event.button.id) :
			case "Scan" :
				ips = self.query_one("#RangeInput")
				if (not check_ip_format(ips.value)) :
					self.query_one("#RangeInputStatus").update("You must enter a valid IPv4 range")
					return
				self.probe = NodeProbe(
					# TODO
				)
				self.push_screen(MonitorMenu())
			case "ProbeAll" :
				...
			case "ProbeSelected" :
				...
			case "ClearLogs" :
				...
			case "BackMenu" :
				self.pop_screen()

	def action_switch_theme(self) -> None :
		self.theme = "textual-light" if self.theme == "textual-dark" else "textual-dark"


if __name__ == "__main__" :
	app = NodeProbeTUI();
	app.run()
