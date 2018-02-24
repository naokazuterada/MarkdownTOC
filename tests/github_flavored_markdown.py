# coding:utf-8
from base import TestBase

class TestAutolink(TestBase):
    """Test for GitHub Flavored Markdown"""

    # for debug
    # def tearDown(self):
    #     pass

    text = \
"""

<!-- MarkdownTOC autolink="true" bracket="round" -->

<!-- /MarkdownTOC -->

{0}
"""

    def test_escaped_square_brackets(self):
        """Escaped square brackets"""
        toc_txt = self.commonSetup(self.text.format('# variable \[required\]'))
        self.assert_In('- [variable \[required\]](#variable-required)', toc_txt)
