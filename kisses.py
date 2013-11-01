import sublime, sublime_plugin
import Kisses.kisseslib

# previous type entries and how much to rememeber
getTypeHistory = []
getTypeHistoryLength = 10

def getSymbol(view):
	""" returns first selected word in active view """
	try:
		region = view.sel()[0]
		if region.begin() == region.end():
			word = view.word(region)
		else:
			word = region
		if not word.empty():
			symbol = view.substr(word) 
			return symbol
		else:
			return ""
	except Exception as e:
		print(repr(e))
		return ""
	

class GettypeCommand(sublime_plugin.TextCommand):
	""" Shows type of entity under the cursor """

	def run(self, edit):
		fileName = self.view.file_name()
		symbol = getSymbol(self.view)
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


class GettypehistoryCommand(sublime_plugin.TextCommand):
	""" Shows a box with previously requested type info """

	def run(self, edit):
		print("Showing a type search history.")
		print(getTypeHistory)
		sublime.active_window().show_quick_panel(getTypeHistory, on_select=None)


class HooglesearchCommand(sublime_plugin.TextCommand):
	""" asks hoogle about text at cursor, shows results in separate window """

	def run(self, edit):
		print("Searching in Hoogle")
		pass