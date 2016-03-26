# coding:utf-8
import os
import re
import sys
import sublime
from unittest import TestCase

VERSION = sublime.version()


class TestBase(TestCase):
    """Super class includes common settings and functions. This class doesn't include any tests."""

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

    # -----

    def setText(self, string):
        self.view.run_command("insert", {"characters": string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def moveTo(self, pos):
        """Move cursor to pos."""
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pos))

    def getTOC_text(self):
        """Find TOC in the document, and return the list texts in it."""
        toc_region = self.view.find(
            "<!-- MarkdownTOC .*-->(.|\n)+?<!-- /MarkdownTOC -->",
            sublime.IGNORECASE)
        toc_all = self.view.substr(toc_region)

        # pick toc contents
        toc_contents = re.sub(r'<!-- MarkdownTOC .* -->', '', toc_all)
        toc_contents = re.sub(r'<!-- /MarkdownTOC -->', '', toc_contents)
        toc_contents = toc_contents.rstrip()

        return toc_contents

    def commonSetup(self, text, insert_position=3):
        # 1. load text
        self.setText(text)

        # 2. insert TOC
        # [NOTICE] Why insert_position=3 ?: Cannnot insert TOC when coursor position <= 2
        self.moveTo(insert_position)
        self.view.run_command('markdowntoc_insert')

        # 3. return TOC
        return self.getTOC_text()

    # def commonSetupFile(self, filename, insert_position=3):
    #     # 1. load file
    #     file = os.path.join(os.path.dirname(__file__), 'samples/' + filename)
    #     text = open(file).read()
    #
    #     return self.commonSetup(text, insert_position)

    def commonSetupAndUpdate(self, text, insert_position=3):
        # 1. load text
        self.setText(text)

        # 2. update TOC
        self.view.run_command('markdowntoc_update')

        # 3. return TOC
        return self.getTOC_text()

    def commonSetupAndUpdateGetBody(self, text, insert_position=3):
        # 1. load text
        self.setText(text)

        # 2. update TOC
        self.view.run_command('markdowntoc_update')

        # 3. return Body Text
        return self.view.substr(sublime.Region(0, self.view.size()))

    # -----

    def assert_NotIn(self, txt, toc_txt):
        """Adapt assertNotIn to SublimeText2."""
        if VERSION < '3000':
            self.assertFalse(txt in toc_txt)
        else:
            self.assertNotIn(txt, toc_txt)

    def assert_In(self, txt, toc_txt):
        """Adapt assertIn to SublimeText2."""
        if VERSION < '3000':
            self.assertTrue(txt in toc_txt)
        else:
            self.assertIn(txt, toc_txt)
