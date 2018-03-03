import pprint
import sublime

# for debug
pp = pprint.PrettyPrinter(indent=4)

class Base:

    def get_settings(self, attr):
        settings = sublime.load_settings('MarkdownTOC.sublime-settings')
        return settings.get(attr)

    def get_defaults(self):
        """return dict of settings"""
        return self.get_settings('defaults')

    def log(self, arg):
        if self.get_settings('logging') is True:
            arg = str(arg)
            sublime.status_message(arg)
            pp.pprint(arg)

    def error(self, arg):
        arg = str(arg)
        sublime.status_message(arg)
        pp.pprint(arg)
