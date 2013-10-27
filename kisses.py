import sublime, sublime_plugin
import Kisses.kisseslib

# previous type entries and how much to rememeber
getTypeHistory = []
getTypeHistoryLength = 10

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")


class GettypeCommand(sublime_plugin.TextCommand):
	""" Shows type of entity under the cursor """

	def run(self, edit):
		for region in self.view.sel():
			if region.begin() == region.end():
				word = self.view.word(region)
			else:
				word = region
			if not word.empty():
				symbol = self.view.substr(word) 
				fileName = self.view.file_name()
				print("Checking symbol " + symbol +" in filename : "+fileName)
				h = Kisses.kisseslib.Hugs()
				response = h.runHugs(fileName, ':t '+symbol+'\n')
				result = h.processResponse(response, Kisses.kisseslib.TypeParser(symbol))
				gotMessage = False
				for item in result:
					if type(item) is Kisses.kisseslib.HugsError:
						# todo: show errors
						pass
					if type(item) is Kisses.kisseslib.HugsMessage:
						# todo: show results
						if not item.message in getTypeHistory:
							getTypeHistory.append(item.message)
							if len(getTypeHistory) > getTypeHistoryLength:
								getTypeHistory.pop()
						# show popup
						sublime.active_window().show_quick_panel(getTypeHistory, on_select=None)
						gotMessage = True
						pass
				if not gotMessage:
					# show default message, e.g. "symbol not found"
					sublime.status_message('GetType: no info on '+symbol)
					pass

