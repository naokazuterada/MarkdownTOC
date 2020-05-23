import pprint
import sublime
from .util import Util

# for debug
pp = pprint.PrettyPrinter(indent=4)


class Base(object):

    def settings(self, attr):
        DEFAULT = 'Packages/MarkdownTOC/MarkdownTOC.sublime-settings'
        files = sublime.find_resources('MarkdownTOC.sublime-settings')
        files.remove(DEFAULT)

        settings = self.decode_value(DEFAULT)
        for f in files:
            user_settings = self.decode_value(f)
            if user_settings != None:
                Util.dict_merge(settings, user_settings)
        return settings[attr]

    def defaults(self):
        return self.settings('defaults')

    def decode_value(self, file):
        # Check json syntax
        try:
            return sublime.decode_value(sublime.load_resource(file))
        except ValueError as e:
            self.error('Invalid json in %s: %s' % (file, e))

    def log(self, arg):
        if self.settings('logging') is True:
            arg = str(arg)
            sublime.status_message(arg)
            pp.pprint(arg)

    def error(self, arg):
        arg = 'MarkdownTOC Error: '+arg
        arg = str(arg)
        sublime.status_message(arg)
        pp.pprint(arg)
