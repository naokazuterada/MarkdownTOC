# coding:utf-8
from base import TestBase

class TestMarkdownPreview(TestBase):
    """Test of attributes 'markdown_preview'"""

    # for debug
    # def tearDown(self):
    #     pass

    markdown_preview_text = \
"""

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
    def common_markdown_preview(self, toc_txt):
        self.assert_In('- [Hello 世界 World][hello-世界-world]', toc_txt)
        self.assert_In('- [camión, último][camión-último]', toc_txt)
        self.assert_In('- [CAMIÓN, ÚLTIMO][camiÓn-Último]', toc_txt)
        self.assert_In('- [españa][españa]', toc_txt)
        self.assert_In('- [ESPAÑA][espaÑa]', toc_txt)
        self.assert_In('- [пример russian][пример-russian]', toc_txt)
        self.assert_In('- [ПРИМЕР RUSSIAN][ПРИМЕР-russian]', toc_txt)

    # default
    def test_markdown_preview_default(self):
        toc_txt = self.commonSetup(self.markdown_preview_text.format(''))
        self.common_markdown_preview(toc_txt)

    # markdown
    def test_markdown_preview_markdown(self):
        toc_txt = self.commonSetup(self.markdown_preview_text.format('markdown_preview=markdown'))
        self.assert_In('- [Hello 世界 World][hello-world]', toc_txt)
        self.assert_In('- [camión, último][camion-ultimo]', toc_txt)
        self.assert_In('- [CAMIÓN, ÚLTIMO][camion-ultimo-1]', toc_txt)
        self.assert_In('- [españa][espana]', toc_txt)
        self.assert_In('- [ESPAÑA][espana-1]', toc_txt)
        self.assert_In('- [пример russian][russian]', toc_txt)
        self.assert_In('- [ПРИМЕР RUSSIAN][russian-1]', toc_txt)

    # github
    def test_markdown_preview_github(self):
        toc_txt = self.commonSetup(self.markdown_preview_text.format('markdown_preview=github'))
        self.assert_In('- [Hello 世界 World][hello-%E4%B8%96%E7%95%8C-world]', toc_txt)
        self.assert_In('- [camión, último][cami%C3%B3n-%C3%BAltimo]', toc_txt)
        self.assert_In('- [CAMIÓN, ÚLTIMO][cami%C3%B3n-%C3%BAltimo-1]', toc_txt)
        self.assert_In('- [españa][espa%C3%B1a]', toc_txt)
        self.assert_In('- [ESPAÑA][espa%C3%B1a-1]', toc_txt)
        self.assert_In('- [пример russian][%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80-russian]', toc_txt)
        self.assert_In('- [ПРИМЕР RUSSIAN][%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80-russian-1]', toc_txt)

    # the other values...
    def test_markdown_preview_othervalues(self):
        toc_txt = self.commonSetup(self.markdown_preview_text.format('markdown_preview=othervalues'))
        self.common_markdown_preview(toc_txt)

    # uniquify heading's id
    markdown_preview_uniquify_id_text = \
"""

<!-- MarkdownTOC autolink=true uri_encoding=false {0} -->

<!-- /MarkdownTOC -->

# Heading
# Heading
# Heading
"""
    def test_markdown_preview_uniquify_id_markdown(self):
        toc_txt = self.commonSetup(self.markdown_preview_uniquify_id_text.format('markdown_preview=markdown'))
        self.assert_In('- [Heading][heading]', toc_txt)
        self.assert_In('- [Heading][heading-1]', toc_txt)
        self.assert_In('- [Heading][heading-2]', toc_txt)
    def test_markdown_preview_uniquify_id_github(self):
        toc_txt = self.commonSetup(self.markdown_preview_uniquify_id_text.format('markdown_preview=github'))
        self.assert_In('- [Heading][heading]', toc_txt)
        self.assert_In('- [Heading][heading-1]', toc_txt)
        self.assert_In('- [Heading][heading-2]', toc_txt)

    # no headings
    markdown_preview_no_heading_text = \
"""

<!-- MarkdownTOC autolink=true uri_encoding=false {0} -->

<!-- /MarkdownTOC -->

"""
    def test_markdown_preview_no_heading_markdown(self):
        toc_txt = self.commonSetup(self.markdown_preview_no_heading_text.format('markdown_preview=markdown'))
        self.assert_NotIn('^- ', toc_txt)
    def test_markdown_preview_no_heading_github(self):
        toc_txt = self.commonSetup(self.markdown_preview_no_heading_text.format('markdown_preview=github'))
        self.assert_NotIn('^- ', toc_txt)