# coding:utf-8
from base import TestBase


class TestIndent(TestBase):
    """Test for attributes \'indent\'"""

    # for debug
    # def tearDown(self):
    #     pass

    indent_text = """

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# foo
## bar
### buz
#### qux
"""
    # TODO: This test cannot be passed when tab(\t) is convert to space by sublime's other feature
    # def test_indent_default(self):
    #     '''Default indent is 1tab'''
    #     toc = self.init_update(self.indent_text.format('levels="1,2,3,4,5,6"'))['toc']
    #     self.assert_In('- foo', toc)
    #     self.assert_In('\t- bar', toc)
    #     self.assert_In('\t\t- buz', toc)
    #     self.assert_In('\t\t\t- qux', toc)

    def test_indent_2spaces(self):
        toc = self.init_update(
            self.indent_text.format('levels="1,2,3,4,5,6" indent="  "')
        )["toc"]
        self.assert_In("- foo", toc)
        self.assert_In("  - bar", toc)
        self.assert_In("    - buz", toc)
        self.assert_In("      - qux", toc)

    def test_indent_4spaces(self):
        toc = self.init_update(
            self.indent_text.format('levels="1,2,3,4,5,6" indent="    "')
        )["toc"]
        self.assert_In("- foo", toc)
        self.assert_In("    - bar", toc)
        self.assert_In("        - buz", toc)
        self.assert_In("            - qux", toc)
