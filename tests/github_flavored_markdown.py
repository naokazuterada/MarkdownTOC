# coding:utf-8
from base import TestBase

class TestAutolink(TestBase):
    """Test for GitHub Flavored Markdown"""

    # for debug
    # def tearDown(self):
    #     pass

#     def test_escaped_square_brackets(self):
#         """Escaped square brackets"""
#         toc_txt = self.commonSetup(\
# """

# <!-- MarkdownTOC autolink="true" bracket="round" -->

# <!-- /MarkdownTOC -->

# # variable \[required\]
# """)
#         self.assert_In('- [variable \[required\]](#variable-required)', toc_txt)

#     def test_underscores(self):
#         """Underscores"""
#         toc_txt = self.commonSetup(\
# """

# <!-- MarkdownTOC autolink="true" bracket="round" -->

# <!-- /MarkdownTOC -->

# # 1 test_x
# # 2 test _x_
# # 3 test _x
# # 4 test x_
# """)
#         self.assert_In('- [1 test_x](#1-test_x)', toc_txt)
#         self.assert_In('- [2 test _x_](#2-test-x)', toc_txt)
#         self.assert_In('- [3 test _x](#3-test-_x)', toc_txt)
#         self.assert_In('- [4 test x_](#4-test-x_)', toc_txt)
