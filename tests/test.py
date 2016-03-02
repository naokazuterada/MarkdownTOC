# coding=utf-8
import os,re,sys,sublime
from unittest import TestCase

VERSION = sublime.version()
SAMPLE_TEXT = os.path.join(os.path.dirname(__file__), 'sample.md')

# for testing internal function
# if VERSION < '3000':
#     # st2
#     MarkdownTOC = sys.modules["MarkdownTOC"]
# else:
#     # st3
#     MarkdownTOC = sys.modules["MarkdownTOC.MarkdownTOC"]

class test_helloworld_command(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            # close file
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    # move cursor to
    def moveTo(self, pos):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pos))

    # ----------

    def test_headings_before_TOC_will_be_ignored(self):

        testdata = open(SAMPLE_TEXT).read()
        self.setText(testdata)

        self.moveTo(13)

        self.view.run_command('markdowntoc_insert')

        toc_start = self.view.find(
            "^<!-- MarkdownTOC .*-->$",
            sublime.IGNORECASE)
        toc_end = self.view.find(
            "^<!-- /MarkdownTOC -->$",
            sublime.IGNORECASE)

        toc_txt = self.view.substr(sublime.Region(toc_start.begin(), toc_end.end()))

        # TODO 上の２つの正規表現を１つにできないか
        # pattern_toc = re.compile(r'<!-- MarkdownTOC .*-->.*<!-- /MarkdownTOC -->') # [Heading][my-id]
        toc = self.view.find("^<!-- MarkdownTOC .*-->$(.\n)*^<!-- /MarkdownTOC -->$", sublime.IGNORECASE)
        toc_txt2 = self.view.substr(toc)
        self.moveTo(0)
        self.setText(len(toc_txt2))

        self.assertFalse('Heading 0' in toc_txt)


# class test_internal_functions(TestCase):

#     def test_foo(self):
#         x = MarkdownTOC.MarkdowntocInsert(1)
#         self.assertEqual(x, 2)
