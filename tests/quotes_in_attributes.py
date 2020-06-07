# coding:utf-8
from base import TestBase


class TestQuotesInAttributes(TestBase):
    """Test for quotes in attributes"""

    # for debug
    # def tearDown(self):
    #     pass

    text = """

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# foo
## bar
"""

    def test_no_quote(self):
        """Allow no quotes in attribute"""
        toc = self.init_update(self.text.format("levels=1"))["toc"]
        self.assert_In("- foo", toc)
        self.assert_NotIn("- bar", toc)

    def test_single(self):
        """Allow single quotes in attribute"""
        toc = self.init_update(self.text.format("levels='1'"))["toc"]
        self.assert_In("- foo", toc)
        self.assert_NotIn("- bar", toc)

    def test_double(self):
        """Allow single quotes in attribute"""
        toc = self.init_update(self.text.format('levels="1"'))["toc"]
        self.assert_In("- foo", toc)
        self.assert_NotIn("- bar", toc)
