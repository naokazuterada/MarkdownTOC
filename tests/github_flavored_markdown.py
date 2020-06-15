# coding:utf-8
from base import TestBase


class TestAutolink(TestBase):
    """Test for GitHub Flavored Markdown"""

    # for debug
    # def tearDown(self):
    #     pass

    def test_escaped_square_brackets(self):
        """Escaped square brackets"""
        toc_txt = self.init_update(
            """

<!-- MarkdownTOC autolink="true" bracket="round" -->

<!-- /MarkdownTOC -->

# variable \[required\]
"""
        )["toc"]
        self.assert_In("- [variable \[required\]](#variable-required)", toc_txt)

    def test_underscores_asterisks_head(self):
        """Underscores and Asterisks in the head of line`"""
        toc_txt = self.init_update(
            """

<!-- MarkdownTOC autolink="true" bracket="round" -->

<!-- /MarkdownTOC -->

# _x test 1
# _x_ test 2
# *x* test 3
# _x _ test 4
# *x * test 5
# _ x_ test 6
# * x* test 7
# __x__ test 8
# **x** test 9
# __x __ test 10
# **x ** test 11
# __ x__ test 12
# ** x** test 13
# _x test 14
# x_ test 15
"""
        )["toc"]
        self.assert_In("- [_x test 1](#_x-test-1)", toc_txt)
        self.assert_In("- [_x_ test 2](#x-test-2)", toc_txt)
        self.assert_In("- [*x* test 3](#x-test-3)", toc_txt)
        self.assert_In("- [_x _ test 4](#_x-_-test-4)", toc_txt)
        self.assert_In("- [*x * test 5](#x--test-5)", toc_txt)
        self.assert_In("- [_ x_ test 6](#_-x_-test-6)", toc_txt)
        self.assert_In("- [* x* test 7](#-x-test-7)", toc_txt)
        self.assert_In("- [__x__ test 8](#x-test-8)", toc_txt)
        self.assert_In("- [**x** test 9](#x-test-9)", toc_txt)
        self.assert_In("- [__x __ test 10](#__x-__-test-10)", toc_txt)
        self.assert_In("- [**x ** test 11](#x--test-11)", toc_txt)
        self.assert_In("- [__ x__ test 12](#__-x__-test-12)", toc_txt)
        self.assert_In("- [** x** test 13](#-x-test-13)", toc_txt)
        self.assert_In("- [_x test 14](#_x-test-14)", toc_txt)
        self.assert_In("- [x_ test 15](#x_-test-15)", toc_txt)

    def test_underscores_asterisks_tail(self):
        """Underscores and Asterisks in the end of line"""
        toc_txt = self.init_update(
            """

<!-- MarkdownTOC autolink="true" bracket="round" -->

<!-- /MarkdownTOC -->

# 1 test_x
# 2 test _x_
# 3 test *x*
# 4 test _x _
# 5 test *x *
# 6 test _ x_
# 7 test * x*
# 8 test __x__
# 9 test **x**
# 10 test __x __
# 11 test **x **
# 12 test __ x__
# 13 test ** x**
# 14 test _x
# 15 test x_
"""
        )["toc"]
        self.assert_In("- [1 test_x](#1-test_x)", toc_txt)
        self.assert_In("- [2 test _x_](#2-test-x)", toc_txt)
        self.assert_In("- [3 test *x*](#3-test-x)", toc_txt)
        self.assert_In("- [4 test _x _](#4-test-_x-_)", toc_txt)
        self.assert_In("- [5 test *x *](#5-test-x-)", toc_txt)
        self.assert_In("- [6 test _ x_](#6-test-_-x_)", toc_txt)
        self.assert_In("- [7 test * x*](#7-test--x)", toc_txt)
        self.assert_In("- [8 test __x__](#8-test-x)", toc_txt)
        self.assert_In("- [9 test **x**](#9-test-x)", toc_txt)
        self.assert_In("- [10 test __x __](#10-test-__x-__)", toc_txt)
        self.assert_In("- [11 test **x **](#11-test-x-)", toc_txt)
        self.assert_In("- [12 test __ x__](#12-test-__-x__)", toc_txt)
        self.assert_In("- [13 test ** x**](#13-test--x)", toc_txt)
        self.assert_In("- [14 test _x](#14-test-_x)", toc_txt)
        self.assert_In("- [15 test x_](#15-test-x_)", toc_txt)

    def test_underscores_asterisks_middle(self):
        """Underscores and Asterisks in the middle of line"""
        toc_txt = self.init_update(
            """

<!-- MarkdownTOC autolink="true" bracket="round" -->

<!-- /MarkdownTOC -->

# 1_x test
# 2 _x_ test
# 3 *x* test
# 4 _x _ test
# 5 *x * test
# 6 _ x_ test
# 7 * x* test
# 8 __x__ test
# 9 **x** test
# 10 __x __ test
# 11 **x ** test
# 12 __ x__ test
# 13 ** x** test
# 14 _x test
# 15 x_ test
"""
        )["toc"]
        self.assert_In("- [1_x test](#1_x-test)", toc_txt)
        self.assert_In("- [2 _x_ test](#2-x-test)", toc_txt)
        self.assert_In("- [3 *x* test](#3-x-test)", toc_txt)
        self.assert_In("- [4 _x _ test](#4-_x-_-test)", toc_txt)
        self.assert_In("- [5 *x * test](#5-x--test)", toc_txt)
        self.assert_In("- [6 _ x_ test](#6-_-x_-test)", toc_txt)
        self.assert_In("- [7 * x* test](#7--x-test)", toc_txt)
        self.assert_In("- [8 __x__ test](#8-x-test)", toc_txt)
        self.assert_In("- [9 **x** test](#9-x-test)", toc_txt)
        self.assert_In("- [10 __x __ test](#10-__x-__-test)", toc_txt)
        self.assert_In("- [11 **x ** test](#11-x--test)", toc_txt)
        self.assert_In("- [12 __ x__ test](#12-__-x__-test)", toc_txt)
        self.assert_In("- [13 ** x** test](#13--x-test)", toc_txt)
        self.assert_In("- [14 _x test](#14-_x-test)", toc_txt)
        self.assert_In("- [15 x_ test](#15-x_-test)", toc_txt)
