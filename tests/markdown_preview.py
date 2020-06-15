# coding:utf-8
from base import TestBase


class TestMarkdownPreview(TestBase):
    """Test for attributes \'markdown_preview\'"""

    # for debug
    # def tearDown(self):
    #     pass

    markdown_preview_text = """

<!-- MarkdownTOC autolink=true uri_encoding=false {0} -->

<!-- /MarkdownTOC -->

# Hello 世界 World
# camión, último
# CAMIÓN, ÚLTIMO
# españa
# ESPAÑA
# пример russian
# ПРИМЕР RUSSIAN
"""
    # TODO: Check MarkdownPreview installed or not

    # common result (not test, call inside test)
    def common_markdown_preview(self, toc):
        self.assert_In("- [Hello 世界 World](#hello-世界-world)", toc)
        self.assert_In("- [camión, último](#camión-último)", toc)
        self.assert_In("- [CAMIÓN, ÚLTIMO](#camiÓn-Último)", toc)
        self.assert_In("- [españa](#españa)", toc)
        self.assert_In("- [ESPAÑA](#espaÑa)", toc)
        self.assert_In("- [пример russian](#пример-russian)", toc)
        self.assert_In("- [ПРИМЕР RUSSIAN](#ПРИМЕР-russian)", toc)

    # default
    def test_markdown_preview_default(self):
        toc = self.init_update(self.markdown_preview_text.format(""))["toc"]
        self.common_markdown_preview(toc)

    # markdown
    def test_markdown_preview_markdown(self):
        toc = self.init_update(
            self.markdown_preview_text.format("markdown_preview=markdown")
        )["toc"]
        self.assert_In("- [Hello 世界 World](#hello-world)", toc)
        self.assert_In("- [camión, último](#camion-ultimo)", toc)
        self.assert_In("- [CAMIÓN, ÚLTIMO](#camion-ultimo_1)", toc)
        self.assert_In("- [españa](#espana)", toc)
        self.assert_In("- [ESPAÑA](#espana_1)", toc)
        self.assert_In("- [пример russian](#russian)", toc)
        self.assert_In("- [ПРИМЕР RUSSIAN](#russian_1)", toc)

    # github
    def test_markdown_preview_github(self):
        toc = self.init_update(
            self.markdown_preview_text.format("markdown_preview=github")
        )["toc"]
        self.assert_In("- [Hello 世界 World](#hello-%E4%B8%96%E7%95%8C-world)", toc)
        self.assert_In("- [camión, último](#cami%C3%B3n-%C3%BAltimo)", toc)
        self.assert_In("- [CAMIÓN, ÚLTIMO](#cami%C3%B3n-%C3%BAltimo-1)", toc)
        self.assert_In("- [españa](#espa%C3%B1a)", toc)
        self.assert_In("- [ESPAÑA](#espa%C3%B1a-1)", toc)
        self.assert_In(
            "- [пример russian](#%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80-russian)", toc
        )
        self.assert_In(
            "- [ПРИМЕР RUSSIAN](#%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80-russian-1)", toc
        )

    # the other values...
    def test_markdown_preview_othervalues(self):
        toc = self.init_update(
            self.markdown_preview_text.format("markdown_preview=othervalues")
        )["toc"]
        self.common_markdown_preview(toc)

    # uniquify heading's id
    markdown_preview_uniquify_id_text = """

<!-- MarkdownTOC autolink=true uri_encoding=false {0} -->

<!-- /MarkdownTOC -->

# Heading
# Heading
# Heading
"""

    def test_markdown_preview_uniquify_id_markdown(self):
        toc = self.init_update(
            self.markdown_preview_uniquify_id_text.format("markdown_preview=markdown")
        )["toc"]
        self.assert_In("- [Heading](#heading)", toc)
        self.assert_In("- [Heading](#heading_1)", toc)
        self.assert_In("- [Heading](#heading_2)", toc)

    def test_markdown_preview_uniquify_id_github(self):
        toc = self.init_update(
            self.markdown_preview_uniquify_id_text.format("markdown_preview=github")
        )["toc"]
        self.assert_In("- [Heading](#heading)", toc)
        self.assert_In("- [Heading](#heading-1)", toc)
        self.assert_In("- [Heading](#heading-2)", toc)

    # no headings
    markdown_preview_no_heading_text = """

<!-- MarkdownTOC autolink=true uri_encoding=false {0} -->

<!-- /MarkdownTOC -->

"""

    def test_markdown_preview_no_heading_markdown(self):
        toc = self.init_update(
            self.markdown_preview_no_heading_text.format("markdown_preview=markdown")
        )["toc"]
        self.assert_NotIn("^- ", toc)

    def test_markdown_preview_no_heading_github(self):
        toc = self.init_update(
            self.markdown_preview_no_heading_text.format("markdown_preview=github")
        )["toc"]
        self.assert_NotIn("^- ", toc)
