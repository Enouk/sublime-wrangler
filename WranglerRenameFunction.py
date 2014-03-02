import sublime, sublime_plugin

class WranglerPromptRenameModuleCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel("Wrangler Rename Function:", "", self.on_done, None, None)
        pass

    def on_done(self, text):
        try:
            if self.window.active_view():
                self.window.active_view().run_command("wrangler_rename_function", {"newName": text} )
        except ValueError:
            pass

class WranglerRenameFunctionCommand(sublime_plugin.TextCommand):
	def run(self, edit, newName):
		funName = "myfun"
		arity = "0"
		for region in self.view.sel():
			if not region.empty():
				line = view.line(region)
				print(line)

		filename = self.view.file_name()
		cmd = "erl_call -a \"api_wrangler rename_fun [\\""" + "\"" + filename + "\\" + "\"" + "," + funName + "," + arity + "," +  newName + ", [] ]\" -sname wrangler"
		self.view.window().run_command("exec", {
       		"cmd": cmd,
       		"shell": True,
       		"encoding": "cp850",
       		"file_regex": "([^ ]*\.erl):?(\d*)"
       		})
