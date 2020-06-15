# coding:utf-8
from base import TestBase


class TestBracket(TestBase):
    """Test for attributes \'bracket\'"""

    # for debug
    # def tearDown(self):
    #     pass

    # TODO: How can we remove 'autolink=true' only in these tests below ?

    bracket_text = """

<!-- MarkdownTOC autolink=true {0} -->

<!-- /MarkdownTOC -->

# foo bar
"""

    def test_bracket_default(self):
        """Default Bracket is round"""
        toc = self.init_update(self.bracket_text.format(""))["toc"]
        self.assert_In("- [foo bar](#foo-bar)", toc)

    def test_bracket_square(self):
        toc = self.init_update(self.bracket_text.format("bracket=square"))["toc"]
        self.assert_In("- [foo bar][foo-bar]", toc)

    def test_bracket_round(self):
        toc = self.init_update(self.bracket_text.format("bracket=round"))["toc"]
        self.assert_In("- [foo bar](#foo-bar)", toc)
