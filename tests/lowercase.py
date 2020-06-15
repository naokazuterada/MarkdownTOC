# coding:utf-8
from base import TestBase


class TestLowercase(TestBase):
    """Test for attributes \'lowercase\'"""

    # for debug
    # def tearDown(self):
    #     pass

    text = """

<!-- MarkdownTOC autolink=true uri_encoding=false {0} -->

<!-- /MarkdownTOC -->

# ПРИМЕР EXAMPLE
# One Two Three

"""

    def get_only_ascii(self, toc):
        self.assert_In("- [ПРИМЕР EXAMPLE](#ПРИМЕР-example)", toc)
        self.assert_In("- [One Two Three](#one-two-three)", toc)

    def get_all(self, toc):
        self.assert_In("- [ПРИМЕР EXAMPLE](#пример-example)", toc)
        self.assert_In("- [One Two Three](#one-two-three)", toc)

    def get_none(self, toc):
        self.assert_In("- [ПРИМЕР EXAMPLE](#ПРИМЕР-EXAMPLE)", toc)
        self.assert_In("- [One Two Three](#One-Two-Three)", toc)

    def test_default(self):
        toc = self.init_update(self.text.format(""))["toc"]
        self.get_only_ascii(toc)

    def test_false(self):
        toc = self.init_update(self.text.format('lowercase="false"'))["toc"]
        self.get_none(toc)

    def test_only_ascii(self):
        toc = self.init_update(self.text.format('lowercase="only_ascii"'))["toc"]
        self.get_only_ascii(toc)

    def test_all(self):
        toc = self.init_update(self.text.format('lowercase="all"'))["toc"]
        self.get_all(toc)

    def test_others(self):
        toc = self.init_update(self.text.format('lowercase="xxxxx"'))["toc"]
        self.get_all(toc)
