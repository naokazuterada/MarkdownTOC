# coding:utf-8
from base import TestBase

class TestLowercase(TestBase):
    """Test for attributes 'lowercase'"""

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

    def common_only_ascii_true(self, toc):
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-example]', toc)
        self.assert_In('- [One Two Three][one-two-three]', toc)

    def test_lowercase_default_only_ascii_true(self):
        toc = self.init_update(self.text_lowercase_only_ascii_true.format(''))['toc']
        self.common_only_ascii_true(toc)

    def test_lowercase_true_only_ascii_true(self):
        toc = self.init_update(self.text_lowercase_only_ascii_true.format('lowercase=true'))['toc']
        self.common_only_ascii_true(toc)

    def test_lowercase_false_only_ascii_true(self):
        toc = self.init_update(self.text_lowercase_only_ascii_true.format('lowercase=false'))['toc']
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-EXAMPLE]', toc)
        self.assert_In('- [One Two Three][One-Two-Three]', toc)

    text_lowercase_only_ascii_false = \
"""

<!-- MarkdownTOC autolink=true uri_encoding=false lowercase_only_ascii=false {0} -->

<!-- /MarkdownTOC -->

# ПРИМЕР EXAMPLE
# One Two Three

"""

    def common_only_ascii_false(self, toc):
        self.assert_In('- [ПРИМЕР EXAMPLE][пример-example]', toc)
        self.assert_In('- [One Two Three][one-two-three]', toc)

    def test_lowercase_default_only_ascii_false(self):
        toc = self.init_update(self.text_lowercase_only_ascii_false.format(''))['toc']
        self.common_only_ascii_false(toc)

    def test_lowercase_true_only_ascii_false(self):
        toc = self.init_update(self.text_lowercase_only_ascii_false.format('lowercase=true'))['toc']
        self.common_only_ascii_false(toc)

    def test_lowercase_false_only_ascii_false(self):
        toc = self.init_update(self.text_lowercase_only_ascii_false.format('lowercase=false'))['toc']
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-EXAMPLE]', toc)
        self.assert_In('- [One Two Three][One-Two-Three]', toc)
