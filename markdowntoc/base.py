import pprint
import sublime
import json
from .util import Util

# for debug
pp = pprint.PrettyPrinter(indent=4)

class Base(object):

    def settings(self, attr):
        settings = json.loads(sublime.load_resource('Packages/MarkdownTOC/MarkdownTOC.sublime-settings'))
        user_settings = json.loads(sublime.load_resource('Packages/User/MarkdownTOC.sublime-settings'))
        Util.dict_merge(settings, user_settings)
        return settings[attr]

    def defaults(self):
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
