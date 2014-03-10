import sublime, sublime_plugin, subprocess, shutil, os

class WranglerExportCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    funName = ""
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

    if funName == "":
        sublime.status_message("Error: Please select a funtion to export")
        return
    if self.view.is_dirty():
        sublime.status_message("Dirty File: Please save before refactoring")
        return

    filename = self.view.file_name()
    c = "wrangler_refacs add_to_export [\"{0}\", {{ {1}, {2} }}, [], emacs, {3}]".format(filename, funName, arity, 8)
    cmd = ["erl_call","-sname","wrangler","-a", c]
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
