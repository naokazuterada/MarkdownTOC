# coding=utf-8
import os,re,sys,sublime
from unittest import TestCase

VERSION = sublime.version()

def loadfile(filename):
    file = os.path.join(os.path.dirname(__file__), filename)
    return open(file).read()

# for testing internal function
# if VERSION < '3000':
#     # st2
#     MarkdownTOC = sys.modules["MarkdownTOC"]
# else:
#     # st3
#     MarkdownTOC = sys.modules["MarkdownTOC.MarkdownTOC"]

class test_markdownTOC(TestCase):

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

    def getTOC_text(self):
        toc_region = self.view.find(
            "<!-- MarkdownTOC .*-->(.|\n)+?<!-- /MarkdownTOC -->",
            sublime.IGNORECASE)
        return self.view.substr(toc_region)

    # ----------

    def test_headings_before_TOC_should_be_ignored(self):

        testdata = loadfile('sample.md')
        self.setText(testdata)

        # move to the next line of "heading 0"
        self.moveTo(13)

        self.view.run_command('markdowntoc_insert')

        toc_txt = self.getTOC_text()

        self.assertFalse('Heading 0' in toc_txt)


    def test_headings_after_TOC_should_be_included(self):

        testdata = loadfile('sample.md')
        self.setText(testdata)

        # move to the next line of "heading 0"
        self.moveTo(13)

        self.view.run_command('markdowntoc_insert')

        toc_txt = self.getTOC_text()

        self.assertTrue('Heading 1' in toc_txt)
        self.assertTrue('Heading 2' in toc_txt)
        self.assertTrue('Heading 3' in toc_txt)
        self.assertTrue('Heading with anchor' in toc_txt)


# class test_internal_functions(TestCase):

#     def test_foo(self):
#         x = MarkdownTOC.MarkdowntocInsert(1)
#         self.assertEqual(x, 2)
