# coding:utf-8
import os
import re
import sys
import sublime
from unittest import TestCase

VERSION = sublime.version()


class MarkdownTocTest(TestCase):

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
        toc_contents = re.sub(r'<!-- MarkdownTOC .*-->', '', toc_all)
        toc_contents = re.sub(r'<!-- /MarkdownTOC -->', '', toc_contents)
        toc_contents = toc_contents.rstrip()

        return toc_contents

    def commonSetup(self, filename, insert_position=3):
        # 1. load file
        file = os.path.join(os.path.dirname(__file__), 'samples/' + filename)
        text = open(file).read()
        self.setText(text)

        # 2. insert TOC
        # [NOTICE] Why insert_position=3 ?: Cannnot insert TOC when coursor position <= 2
        self.moveTo(insert_position)
        self.view.run_command('markdowntoc_insert')

        # 3. return TOC
        return self.getTOC_text()

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

    # =====

    def test_before_than_TOC_should_be_ignored(self):
        toc_txt = self.commonSetup('insert_position.md', 13)
        self.assert_NotIn('Heading 0', toc_txt)

    def test_after_than_TOC_should_be_included(self):
        toc_txt = self.commonSetup('insert_position.md', 13)
        self.assert_In('Heading 1', toc_txt)
        self.assert_In('Heading 2', toc_txt)
        self.assert_In('Heading 3', toc_txt)
        self.assert_In('Heading with anchor', toc_txt)

    def test_ignore_inside_codeblock(self):
        toc_txt = self.commonSetup('codeblock.md')
        self.assert_In('Outside1', toc_txt)
        self.assert_In('Outside2', toc_txt)
        self.assert_NotIn('Inside1', toc_txt)
        self.assert_NotIn('Inside2', toc_txt)
        self.assert_NotIn('Inside3', toc_txt)

    def test_escape_link(self):
        toc_txt = self.commonSetup('link.md')
        self.assert_In('This link is cool', toc_txt)

    def test_escape_square_bracket(self):
        toc_txt = self.commonSetup('square_bracket.md')
        self.assert_In('function(foo\[, bar\])', toc_txt)
