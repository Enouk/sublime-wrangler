import sublime, sublime_plugin

class WranglerUndoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		cmd = "erl_call -a \"api_wrangler undo []\" -sname wrangler"
		self.view.window().run_command("exec", {
       		"cmd": cmd,
       		"shell": True,
       		"encoding": "cp850",
       		"file_regex": "([^ ]*\.erl):?(\d*)"
       		})
