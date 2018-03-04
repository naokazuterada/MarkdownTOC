import pprint
import sublime

# for debug
pp = pprint.PrettyPrinter(indent=4)

class Base(object):

    def settings(self, attr):
        settings = sublime.load_settings('MarkdownTOC.sublime-settings')
        return settings.get(attr)

    def defaults(self):
        """return dict of settings"""
        return self.settings('defaults')

    def log(self, arg):
        if self.settings('logging') is True:
            arg = str(arg)
            sublime.status_message(arg)
            pp.pprint(arg)

    def error(self, arg):
        arg = str(arg)
        sublime.status_message(arg)
        pp.pprint(arg)
