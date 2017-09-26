# coding:utf-8
from base import TestBase
import sublime
import sys

class TestStyle(TestBase):
    """Test of attributes 'style'"""

    # for debug
    # def tearDown(self):
    #     pass

    style_text = \
"""

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# foo
## bar
## buz
# qux
"""
    def test_style_default(self):
        """Default Style is unordered"""
        toc_txt = self.commonSetup(self.style_text.format(''))
        self.assert_In('- foo', toc_txt)
        self.assert_In('- bar', toc_txt)
        self.assert_In('- buz', toc_txt)
        self.assert_In('- qux', toc_txt)

    def test_style_ordered(self):
        toc_txt = self.commonSetup(self.style_text.format('style=ordered'))
        self.assert_In('1. foo', toc_txt)
        self.assert_In('1. bar', toc_txt)
        self.assert_In('1. buz', toc_txt)
        self.assert_In('1. qux', toc_txt)

    def test_style_unordered(self):
        toc_txt = self.commonSetup(self.style_text.format('style=unordered'))
        self.assert_In('- foo', toc_txt)
        self.assert_In('- bar', toc_txt)
        self.assert_In('- buz', toc_txt)
        self.assert_In('- qux', toc_txt)
