import sublime, sublime_plugin, subprocess, shutil, os

class WranglerPromptRenameVariable(sublime_plugin.WindowCommand):
    def run(self):
        if self.window.active_view().is_dirty():
            sublime.status_message("Dirty File: Please save before refactoring")
            return

        self.window.show_input_panel("Specify New Variable Name:", "", self.on_done, None, None)
        pass

    def on_done(self, text):
        try:
            if self.window.active_view():
                self.window.active_view().run_command("wrangler_rename_variable", {"newName": text} )
        except ValueError:
            pass

class WranglerRenameVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit, newName):
        row = 0
        col = 0
        for region in self.view.sel():
            if not region.empty():
                (row,col) = self.view.rowcol(self.view.sel()[0].begin())
                if region.size() > 1:
                    row += 1
                    col += 1

        filename = self.view.file_name()
        searchPaths = "[]"
        tabWidth = 8
        #c = "wrangler_refacs add_to_export [\"{0}\", {{ {1}, {2} }}, [], emacs, {3}]".format(filename, funName, arity, 8)
        c = "wrangler_refacs rename_var [\"{0}\", {1}, {2}, \"{3}\", [], emacs, {5}]".format(filename, row, col, newName, searchPaths, tabWidth)
        cmd = ["erl_call","-sname","wrangler","-a", c]
        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (stdout, stderr) = p.communicate()
        print(stdout, stderr)
        if b'{ok, []}' == stdout: 
            sublime.status_message("Function already exported")
        elif b'{ok,' in stdout:
            shutil.copy2(filename + ".swp", filename)
            os.remove(filename + ".swp") 
        else:
            sublime.status_message((b'Error: Function export failed:' + stdout).decode("utf-8"))
        ##cmd = "erl_call -a \"api_wrangler rename_var [\\""" + "\"" + filename + "\\" + "\"" + "," + varName + "," + str(arity) + "," +  newName + ", [] ]\" -sname wrangler"
        #cmd = "erl_call -a \"api_wrangler rename_var [\" %s \", %s, %s ".format(filename, row, col, newName, searchPaths, context, tabWidth)
        # cmd = "erl_call -a \"wrangler_refacs rename_var [\\""\"{0}\\""\", {1}, {2}, \\""\"{3}\\""\", {4}, {5}, {6} ] \" -sname wrangler".format(filename, row + 1, col + 1, newName, searchPaths, context, tabWidth)
        # self.view.window().run_command("exec", {
        #       "cmd": cmd,
        #       "shell": True,
        #       "encoding": "cp850",
        #       "file_regex": "([^ ]*\.erl):?(\d*)"
        #       })
        #self.view.window().open_file(filename + ".swp")