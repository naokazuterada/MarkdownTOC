import pprint
import sublime
from .util import Util

# for debug
pp = pprint.PrettyPrinter(indent=4)

DEFAULT = "Packages/MarkdownTOC/MarkdownTOC.sublime-settings"


class Base(object):
    def settings(self, attr):
        files = sublime.find_resources("MarkdownTOC.sublime-settings")
        files.remove(DEFAULT)

        settings = self.decode_value(DEFAULT)
        for f in files:
            user_settings = self.decode_value(f)
            if user_settings != None:
                Util.dict_merge(settings, user_settings)
        return settings[attr]

    def defaults(self):
        return self.parse_values(self.settings("defaults"))

    def parse_values(self, values):
        """Convert string values to the types used in the default settings,
        e.g. "1,2" -> ["1", "2"] for levels, "true" -> True for autolink"""
        types = self.decode_value(DEFAULT)["defaults"]
        for key, value in values.items():
            if key not in types or not isinstance(value, str):
                continue
            if type(types[key]) is list:
                values[key] = value.split(",")
            elif type(types[key]) is bool:
                values[key] = Util.strtobool(value)
        return values

    def decode_value(self, file):
        # Check json syntax
        try:
            return sublime.decode_value(sublime.load_resource(file))
        except ValueError as e:
            self.error("Invalid json in %s: %s" % (file, e))

    def log(self, arg):
        if self.settings("logging") is True:
            arg = str(arg)
            sublime.status_message(arg)
            pp.pprint(arg)

    def error(self, arg):
        arg = "MarkdownTOC Error: " + arg
        arg = str(arg)
        sublime.status_message(arg)
        pp.pprint(arg)
