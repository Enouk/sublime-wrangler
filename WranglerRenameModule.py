import sublime, sublime_plugin

class WranglerPromptRenameModuleCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel("Wrangler Rename Module:", "", self.on_done, None, None)
        pass

    def on_done(self, text):
        try:
            if self.window.active_view():
                self.window.active_view().run_command("wrangler_rename_module", {"newName": text} )
        except ValueError:
            pass

class WranglerRenameModuleCommand(sublime_plugin.TextCommand):
	def run(self, edit, newName):
		filename = self.view.file_name()
		cmd = "erl_call -a \"api_wrangler rename_mod [\\""" + "\"" + filename + "\\" + "\"" + ","+  newName + ", [] ]\" -sname wrangler"
		self.view.window().run_command("exec", {
       		"cmd": cmd,
       		"shell": True,
       		"encoding": "cp850",
       		"file_regex": "([^ ]*\.erl):?(\d*)"
       		})