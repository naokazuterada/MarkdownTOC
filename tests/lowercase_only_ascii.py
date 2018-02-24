# coding:utf-8
from base import TestBase

class TestLowercaseOnlyAscii(TestBase):
    """Test of attributes 'lowercase_only_ascii'"""

    # for debug
    # def tearDown(self):
    #     pass

    lowercase_only_ascii_text = \
"""

<!-- MarkdownTOC autolink=true uri_encoding=false {0} -->

<!-- /MarkdownTOC -->

# ПРИМЕР EXAMPLE
"""
    def test_lowercase_only_ascii_default(self):
        toc_txt = self.commonSetup(self.lowercase_only_ascii_text.format(''))
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-example]', toc_txt)

    def test_lowercase_only_ascii_true(self):
        toc_txt = self.commonSetup(self.lowercase_only_ascii_text.format('lowercase_only_ascii=true'))
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-example]', toc_txt)

    def test_lowercase_only_ascii_false(self):
        toc_txt = self.commonSetup(self.lowercase_only_ascii_text.format('lowercase_only_ascii=false'))
        self.assert_In('- [ПРИМЕР EXAMPLE][пример-example]', toc_txt)
