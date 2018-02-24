# coding:utf-8
from base import TestBase

class TestAutolink(TestBase):
    """Test of attributes 'autolink'"""

    # for debug
    # def tearDown(self):
    #     pass

    autolink_text = \
"""

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# Foo Bar
"""

    def test_autolink_default(self):
        """Default Auto link is false"""
        toc_txt = self.commonSetup(self.autolink_text.format(''))
        self.assert_In('- Foo Bar', toc_txt)

    def test_autolink_true(self):
        toc_txt = self.commonSetup(self.autolink_text.format('autolink=true'))
        self.assert_In('- [Foo Bar][foo-bar]', toc_txt)

    def test_autolink_false(self):
        toc_txt = self.commonSetup(self.autolink_text.format('autolink=false'))
        self.assert_In('- Foo Bar', toc_txt)
