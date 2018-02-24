# coding:utf-8
from base import TestBase

class TestLowercase(TestBase):
    """Test of attributes 'lowercase'"""

    # for debug
    # def tearDown(self):
    #     pass

    text_lowercase_only_ascii_true = \
"""

<!-- MarkdownTOC autolink=true uri_encoding=false lowercase_only_ascii=true {0} -->

<!-- /MarkdownTOC -->

# ПРИМЕР EXAMPLE
# One Two Three

"""
    def common_only_ascii_true(self, toc_txt):
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-example]', toc_txt)
        self.assert_In('- [One Two Three][one-two-three]', toc_txt)

    def test_lowercase_default_only_ascii_true(self):
        toc_txt = self.commonSetup(self.text_lowercase_only_ascii_true.format(''))
        self.common_only_ascii_true(toc_txt)

    def test_lowercase_true_only_ascii_true(self):
        toc_txt = self.commonSetup(self.text_lowercase_only_ascii_true.format('lowercase=true'))
        self.common_only_ascii_true(toc_txt)

    def test_lowercase_false_only_ascii_true(self):
        toc_txt = self.commonSetup(self.text_lowercase_only_ascii_true.format('lowercase=false'))
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-EXAMPLE]', toc_txt)
        self.assert_In('- [One Two Three][One-Two-Three]', toc_txt)

    text_lowercase_only_ascii_false = \
"""

<!-- MarkdownTOC autolink=true uri_encoding=false lowercase_only_ascii=false {0} -->

<!-- /MarkdownTOC -->

# ПРИМЕР EXAMPLE
# One Two Three

"""
    def common_only_ascii_false(self, toc_txt):
        self.assert_In('- [ПРИМЕР EXAMPLE][пример-example]', toc_txt)
        self.assert_In('- [One Two Three][one-two-three]', toc_txt)

    def test_lowercase_default_only_ascii_false(self):
        toc_txt = self.commonSetup(self.text_lowercase_only_ascii_false.format(''))
        self.common_only_ascii_false(toc_txt)

    def test_lowercase_true_only_ascii_false(self):
        toc_txt = self.commonSetup(self.text_lowercase_only_ascii_false.format('lowercase=true'))
        self.common_only_ascii_false(toc_txt)

    def test_lowercase_false_only_ascii_false(self):
        toc_txt = self.commonSetup(self.text_lowercase_only_ascii_false.format('lowercase=false'))
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-EXAMPLE]', toc_txt)
        self.assert_In('- [One Two Three][One-Two-Three]', toc_txt)
