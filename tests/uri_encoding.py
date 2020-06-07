# coding:utf-8
from base import TestBase


class TestUriEncoding(TestBase):
    """Test for attributes \'uri_encoding\'"""

    # for debug
    # def tearDown(self):
    #     pass

    uri_encoding_text = """

<!-- MarkdownTOC autolink="true" lowercase="only_ascii" {0} -->

<!-- /MarkdownTOC -->

# Camión, último
# España
# こんにちわ 世界
# Пример Example
# 一个标题
"""
    # default: uri_encoding=true
    def test_uri_encoding_default(self):
        toc = self.init_update(self.uri_encoding_text.format(""))["toc"]
        self.assert_In("- [Camión, último](#cami%C3%B3n-%C3%BAltimo)", toc)
        self.assert_In("- [España](#espa%C3%B1a)", toc)
        self.assert_In(
            "- [こんにちわ 世界](#%E3%81%93%E3%82%93%E3%81%AB%E3%81%A1%E3%82%8F-%E4%B8%96%E7%95%8C)",
            toc,
        )
        self.assert_In(
            "- [Пример Example](#%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80-example)", toc
        )
        self.assert_In("- [一个标题](#%E4%B8%80%E4%B8%AA%E6%A0%87%E9%A2%98)", toc)

    def test_uri_encoding_true(self):
        toc = self.init_update(self.uri_encoding_text.format("uri_encoding=true"))[
            "toc"
        ]
        self.assert_In("- [Camión, último](#cami%C3%B3n-%C3%BAltimo)", toc)
        self.assert_In("- [España](#espa%C3%B1a)", toc)
        self.assert_In(
            "- [こんにちわ 世界](#%E3%81%93%E3%82%93%E3%81%AB%E3%81%A1%E3%82%8F-%E4%B8%96%E7%95%8C)",
            toc,
        )
        self.assert_In(
            "- [Пример Example](#%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80-example)", toc
        )
        self.assert_In("- [一个标题](#%E4%B8%80%E4%B8%AA%E6%A0%87%E9%A2%98)", toc)

    def test_uri_encoding_false(self):
        toc = self.init_update(self.uri_encoding_text.format("uri_encoding=false"))[
            "toc"
        ]
        self.assert_In("- [Camión, último](#camión-último)", toc)
        self.assert_In("- [España](#españa)", toc)
        self.assert_In("- [こんにちわ 世界](#こんにちわ-世界)", toc)
        self.assert_In("- [Пример Example](#Пример-example)", toc)
        self.assert_In("- [一个标题](#一个标题)", toc)
