# coding:utf-8
from base import TestBase


class TestStyle(TestBase):
    """Test for attributes \'style\'"""

    # for debug
    # def tearDown(self):
    #     pass

    style_text = """

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# foo
## bar
## buz
# qux
"""

    def test_style_default(self):
        """Default Style is unordered"""
        toc = self.init_update(self.style_text.format(""))["toc"]
        self.assert_In("- foo", toc)
        self.assert_In("- bar", toc)
        self.assert_In("- buz", toc)
        self.assert_In("- qux", toc)

    def test_style_ordered(self):
        toc = self.init_update(self.style_text.format("style=ordered"))["toc"]
        self.assert_In("1. foo", toc)
        self.assert_In("1. bar", toc)
        self.assert_In("1. buz", toc)
        self.assert_In("1. qux", toc)

    def test_style_unordered(self):
        toc = self.init_update(self.style_text.format("style=unordered"))["toc"]
        self.assert_In("- foo", toc)
        self.assert_In("- bar", toc)
        self.assert_In("- buz", toc)
        self.assert_In("- qux", toc)
