from _structs import *
from _constants import *
from _globals import *
from _core import *
from _tools import *
from _menus import *
from textual.app import App

THEME_INDEX = 0

class NodeProbeTUI(App) :
	BINDINGS = [("t", "switch_theme", "Switch Theme")]
	CSS_PATH = "style.css"

	def on_mount(self) -> None :
		self.theme = "nord"
		self.push_screen((MainMenu()))
		self.themes = [
			"nord",
			"gruvbox",
			"tokyo-night",
			"textual-dark",
			"solarized-light",
			"atom-one-dark",
			"atom-one-light"
		]

	def action_switch_theme(self) -> None :
		global THEME_INDEX
		THEME_INDEX = 0 if (THEME_INDEX == len(self.themes)) else THEME_INDEX
		self.theme = self.themes[THEME_INDEX]
		THEME_INDEX += 1


if __name__ == "__main__" :
	app = NodeProbeTUI();
	app.run()
