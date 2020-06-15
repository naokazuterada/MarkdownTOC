# coding:utf-8
from base import TestBase


class TestItalic(TestBase):
    """Test for attributes \'bracket\'"""

    # for debug
    # def tearDown(self):
    #     pass

    # TODO: How can we remove 'autolink=true' only in these tests below ?

    bracket_text = """

<!-- MarkdownTOC autolink=true -->

<!-- /MarkdownTOC -->

# this is _italic_
# _this is italic_
# _this is not italic __
# this _is italic_
# _ this is not italic _
# 2 _ this is not italic _
# _this is not italic with markdown error _
# 2 _this is not italic with markdown error _
# `_should ignore underscores in codeblocks_`
# `_should ignore underscores in codeblocks 2_ `
# this is ` _more complex_ ` exmaple
# this_is_not_italic
# t_h_i_s__i_s__n_o_t__i_t_a_l_i_c
# _t_h_i_s__i_s__i_t_a_l_i_c_
"""

    def test_italic_in_inheading1(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In("- [this is _italic_](#this-is-italic)", toc)

    def test_italic_in_inheading2(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In("- [_this is italic_](#this-is-italic-1)", toc)

    def test_italic_in_inheading3(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In("- [_this is not italic __](#_this-is-not-italic-__)", toc)

    def test_italic_in_inheading4(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In("- [this _is italic_](#this-is-italic-2)", toc)

    def test_italic_in_inheading5(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In("- [_ this is not italic _](#_-this-is-not-italic-_)", toc)

    def test_italic_in_inheading6(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In("- [2 _ this is not italic _](#2-_-this-is-not-italic-_)", toc)

    def test_italic_in_inheading7(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In(
            "- [_this is not italic with markdown error _](#_this-is-not-italic-with-markdown-error-_)",
            toc,
        )

    def test_italic_in_inheading8(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In(
            "- [2 _this is not italic with markdown error _](#2-_this-is-not-italic-with-markdown-error-_)",
            toc,
        )

    def test_italic_in_inheading9(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In(
            "- [`_should ignore underscores in codeblocks_`](#_should-ignore-underscores-in-codeblocks_)",
            toc,
        )

    def test_italic_in_inheading10(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In(
            "- [`_should ignore underscores in codeblocks 2_ `](#_should-ignore-underscores-in-codeblocks-2_-)",
            toc,
        )

    def test_italic_in_inheading11(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In(
            "- [this is ` _more complex_ ` exmaple](#this-is-_more-complex_-exmaple)",
            toc,
        )

    def test_italic_in_inheading12(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In("- [this_is_not_italic](#this_is_not_italic)", toc)

    def test_italic_in_inheading13(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In(
            "- [t_h_i_s__i_s__n_o_t__i_t_a_l_i_c](#t_h_i_s__i_s__n_o_t__i_t_a_l_i_c)",
            toc,
        )

    def test_italic_in_inheading14(self):
        toc = self.init_update(self.bracket_text)["toc"]
        self.assert_In(
            "- [_t_h_i_s__i_s__i_t_a_l_i_c_](#t_h_i_s__i_s__i_t_a_l_i_c)", toc
        )
