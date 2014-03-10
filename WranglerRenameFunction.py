import sublime, sublime_plugin, os

class WranglerPromptRenameFunctionCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Wrangler New Function Name:", "", self.on_done, None, None)
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
    arity = 0
    for region in self.view.sel():
      if not region.empty():
        lc = self.view.line(region)
        line = self.view.substr(lc)
        funName = self.view.substr(region)
        if "()" in line:
            arity = 0
        else:
            ## Need a regexp here to get the real correct arity
            arity = line.count(',') + 1
            print(arity)

    filename = self.view.file_name()
    filepath = os.path.dirname(filename)
    cmd = "erl_call -a \"api_wrangler rename_fun [\\""\"{0}\\""\", {1}, {2}, {3}, [\\""\"{4}\\""\"] ]\" -sname wrangler".format(filename, funName, arity, newName, filepath)
    self.view.window().run_command("exec", {
          "cmd": cmd,
          "shell": True,
          "encoding": "cp850",
          "file_regex": "([^ ]*\.erl):?(\d*)"
          })