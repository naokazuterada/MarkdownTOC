# coding=utf-8
import os,re,sys,sublime
from unittest import TestCase

VERSION = sublime.version()

def loadfile(filename):
    file = os.path.join(os.path.dirname(__file__), filename)
    return open(file).read()

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

    def assert_NotIn(self, txt, toc_txt):
        if VERSION < '3000':
            self.assertFalse(txt in toc_txt)
        else:
            self.assertNotIn(txt, toc_txt)

    def assert_In(self, txt, toc_txt):
        if VERSION < '3000':
            self.assertTrue(txt in toc_txt)
        else:
            self.assertIn(txt, toc_txt)

    # ----------

    def test_headings_before_TOC_should_be_ignored(self):

        text = loadfile('sample.md')
        self.setText(text)

        # move to the next line of "heading 0"
        self.moveTo(13)

        self.view.run_command('markdowntoc_insert')

        toc_txt = self.getTOC_text()

        self.assert_NotIn('Heading 0', toc_txt)


    def test_headings_after_TOC_should_be_included(self):

        text = loadfile('sample.md')
        self.setText(text)

        # move to the next line of "heading 0"
        self.moveTo(13)

        self.view.run_command('markdowntoc_insert')

        toc_txt = self.getTOC_text()

        self.assert_In('Heading 1', toc_txt)
        self.assert_In('Heading 2', toc_txt)
        self.assert_In('Heading 3', toc_txt)
        self.assert_In('Heading with anchor', toc_txt)
