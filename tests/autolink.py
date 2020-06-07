# coding:utf-8
from base import TestBase


class TestAutolink(TestBase):
    """Test for attributes \'autolink\'"""

    # for debug
    # def tearDown(self):
    #     pass

    autolink_text = """

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# Foo Bar
"""

    def test_autolink_default(self):
        """Default Auto link is false"""
        toc = self.init_update(self.autolink_text.format(""))["toc"]
        self.assert_In("- Foo Bar", toc)

    def test_autolink_true(self):
        toc = self.init_update(self.autolink_text.format("autolink=true"))["toc"]
        self.assert_In("- [Foo Bar](#foo-bar)", toc)

    def test_autolink_false(self):
        toc = self.init_update(self.autolink_text.format("autolink=false"))["toc"]
        self.assert_In("- Foo Bar", toc)
