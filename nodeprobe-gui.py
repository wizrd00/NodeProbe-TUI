from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class NodeProbe(App) :
	BINDINGS = [("t", "switch_theme", "Switch Theme")]

	def compose(self) -> ComposeResult :
		yield Header()
		yield Footer()

	def action_switch_theme(self) -> None :
		self.theme = "textual-light" if self.theme == "textual-dark" else "textual-dark"


if __name__ == "__main__" :
	app = NodeProbe();
	app.run()
