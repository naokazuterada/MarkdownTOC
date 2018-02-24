# coding:utf-8
from base import TestBase

class TestBracket(TestBase):
    """Test for attributes 'bracket'"""

    # for debug
    # def tearDown(self):
    #     pass

    # TODO: How can we remove "autolink=true" only in these tests below ?

    bracket_text = \
"""

<!-- MarkdownTOC autolink=true {0} -->

<!-- /MarkdownTOC -->

# foo bar
"""
    def test_bracket_default(self):
        """Default Bracket is square"""
        toc_txt = self.commonSetup(self.bracket_text.format(''))
        self.assert_In('- [foo bar][foo-bar]', toc_txt)

    def test_bracket_square(self):
        toc_txt = self.commonSetup(self.bracket_text.format('bracket=square'))
        self.assert_In('- [foo bar][foo-bar]', toc_txt)

    def test_bracket_round(self):
        toc_txt = self.commonSetup(self.bracket_text.format('bracket=round'))
        self.assert_In('- [foo bar](#foo-bar)', toc_txt)
