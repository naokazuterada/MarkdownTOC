# coding:utf-8
from base import TestBase

class TestLowercaseOnlyAscii(TestBase):
    """Test for attributes 'lowercase_only_ascii'"""

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
        toc = self.init_update(self.lowercase_only_ascii_text.format(''))['toc']
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-example]', toc)

    def test_lowercase_only_ascii_true(self):
        toc = self.init_update(self.lowercase_only_ascii_text.format('lowercase_only_ascii=true'))['toc']
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-example]', toc)

    def test_lowercase_only_ascii_false(self):
        toc = self.init_update(self.lowercase_only_ascii_text.format('lowercase_only_ascii=false'))['toc']
        self.assert_In('- [ПРИМЕР EXAMPLE][пример-example]', toc)
