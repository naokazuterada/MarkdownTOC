# coding:utf-8
from superclass import MarkdownTocTest

class MarkdownTocTestAttribute(MarkdownTocTest):
    """ Test about attributes"""

    # for debug
    # def tearDown(self):
    #     pass

    # -----------------
    # bracket

    def test_attribute_bracket_default(self):
        text = \
"""


# foo bar
"""
        toc_txt = self.commonSetup(text)
        self.assert_In('- [foo bar][foo-bar]', toc_txt)

    def test_attribute_bracket_square(self):
        text = \
"""

<!-- MarkdownTOC bracket=square -->

<!-- /MarkdownTOC -->

# foo bar
"""
        toc_txt = self.commonSetup(text)
        self.assert_In('- [foo bar][foo-bar]', toc_txt)

    def test_attribute_bracket_round(self):
        text = \
"""

<!-- MarkdownTOC bracket=round -->

<!-- /MarkdownTOC -->

# foo bar
"""
        toc_txt = self.commonSetupAndUpdate(text)
        self.assert_In('- [foo bar](#foo-bar)', toc_txt)
