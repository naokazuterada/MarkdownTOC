# coding:utf-8
from base import TestBase

class TestAttribute(TestBase):
    """Test of attributes"""

    # for debug
    # def tearDown(self):
    #     pass

    # -----------------
    # Auto link

    autolink_text = \
"""

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# Foo Bar
"""

    def test_autolink_default(self):
        """Default Auto link is false"""
        toc_txt = self.commonSetup(self.autolink_text.format(''))
        self.assert_In('- Foo Bar', toc_txt)

    def test_autolink_true(self):
        toc_txt = self.commonSetup(self.autolink_text.format('autolink=true'))
        self.assert_In('- [Foo Bar][foo-bar]', toc_txt)

    def test_autolink_false(self):
        toc_txt = self.commonSetup(self.autolink_text.format('autolink=false'))
        self.assert_In('- Foo Bar', toc_txt)


    # -----------------
    # Bracket

    # TODO: How can we remove "autolink=true" only in these tests below ?

    bracket_text = \
"""

<!-- MarkdownTOC autolink=true {0} -->

<!-- /MarkdownTOC -->

# foo bar
"""
    def test_bracket_default(self):
        """Default Bracket is square"""
        toc_txt = self.commonSetup(self.bracket_text.format(''))
        self.assert_In('- [foo bar][foo-bar]', toc_txt)

    def test_bracket_square(self):
        toc_txt = self.commonSetup(self.bracket_text.format('bracket=square'))
        self.assert_In('- [foo bar][foo-bar]', toc_txt)

    def test_bracket_round(self):
        toc_txt = self.commonSetup(self.bracket_text.format('bracket=round'))
        self.assert_In('- [foo bar](#foo-bar)', toc_txt)

    # -----------------
    # Depth

    depth_text = \
"""

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# heading 1
## heading 2
### heading 3
#### heading 4
##### heading 5
"""
    def test_depth_default(self):
        """Default Depth is 2"""
        toc_txt = self.commonSetup(self.depth_text.format(''))
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_NotIn('- heading 3', toc_txt)
        self.assert_NotIn('- heading 4', toc_txt)
        self.assert_NotIn('- heading 5', toc_txt)

    def test_depth_0(self):
        """Depth 0 means no limit"""
        toc_txt = self.commonSetup(self.depth_text.format('depth=0'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_In('- heading 3', toc_txt)
        self.assert_In('- heading 4', toc_txt)
        self.assert_In('- heading 5', toc_txt)

    def test_depth_1(self):
        toc_txt = self.commonSetup(self.depth_text.format('depth=1'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_NotIn('- heading 2', toc_txt)
        self.assert_NotIn('- heading 3', toc_txt)
        self.assert_NotIn('- heading 4', toc_txt)
        self.assert_NotIn('- heading 5', toc_txt)

    def test_depth_2(self):
        toc_txt = self.commonSetup(self.depth_text.format('depth=2'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_NotIn('- heading 3', toc_txt)
        self.assert_NotIn('- heading 4', toc_txt)
        self.assert_NotIn('- heading 5', toc_txt)

    def test_depth_3(self):
        toc_txt = self.commonSetup(self.depth_text.format('depth=3'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_In('- heading 3', toc_txt)
        self.assert_NotIn('- heading 4', toc_txt)
        self.assert_NotIn('- heading 5', toc_txt)

    def test_depth_4(self):
        toc_txt = self.commonSetup(self.depth_text.format('depth=4'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_In('- heading 3', toc_txt)
        self.assert_In('- heading 4', toc_txt)
        self.assert_NotIn('- heading 5', toc_txt)

    def test_depth_5(self):
        toc_txt = self.commonSetup(self.depth_text.format('depth=5'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_In('- heading 3', toc_txt)
        self.assert_In('- heading 4', toc_txt)
        self.assert_In('- heading 5', toc_txt)

    # -----------------
    # Auto anchor

    autoanchor_text = \
"""

<!-- MarkdownTOC autolink=true {0} -->

<!-- /MarkdownTOC -->

# Changelog
# Glossary
# API Specification
"""
    def test_autoanchor_false(self):
        """Default Auto Anchor is false"""
        body_txt = self.commonSetupAndUpdateGetBody(self.autoanchor_text.format(''))
        self.assert_NotIn('<a name="changelog"></a>', body_txt)
        self.assert_NotIn('<a name="glossary"></a>', body_txt)
        self.assert_NotIn('<a name="api-specification"></a>', body_txt)

    def test_autoanchor_true(self):
        body_txt = self.commonSetupAndUpdateGetBody(self.autoanchor_text.format('autoanchor=true'))
        self.assert_In('<a name="changelog"></a>\n# Changelog', body_txt)
        self.assert_In('<a name="glossary"></a>\n# Glossary', body_txt)
        self.assert_In('<a name="api-specification"></a>\n# API Specification', body_txt)

    def test_autoanchor_false(self):
        body_txt = self.commonSetupAndUpdateGetBody(self.autoanchor_text.format('autoanchor=false'))
        self.assert_NotIn('<a name="changelog"></a>', body_txt)
        self.assert_NotIn('<a name="glossary"></a>', body_txt)
        self.assert_NotIn('<a name="api-specification"></a>', body_txt)


    # -----------------
    # Style

    style_text = \
"""

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# foo
## bar
## buz
# qux
"""
    def test_style_default(self):
        """Default Style is unordered"""
        toc_txt = self.commonSetup(self.style_text.format(''))
        self.assert_In('- foo', toc_txt)
        self.assert_In('- bar', toc_txt)
        self.assert_In('- buz', toc_txt)
        self.assert_In('- qux', toc_txt)

    def test_style_ordered(self):
        toc_txt = self.commonSetup(self.style_text.format('style=ordered'))
        self.assert_In('1. foo', toc_txt)
        self.assert_In('1. bar', toc_txt)
        self.assert_In('1. buz', toc_txt)
        self.assert_In('1. qux', toc_txt)

    def test_style_unordered(self):
        toc_txt = self.commonSetup(self.style_text.format('style=unordered'))
        self.assert_In('- foo', toc_txt)
        self.assert_In('- bar', toc_txt)
        self.assert_In('- buz', toc_txt)
        self.assert_In('- qux', toc_txt)

    # -----------------
    # Indent

    indent_text = \
"""

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# foo
## bar
### buz
#### qux
"""
    # TODO: This test cannot be passed when tab(\t) is convert to space by sublime's other feature
    # def test_indent_default(self):
    #     """Default indent is 1tab"""
    #     toc_txt = self.commonSetup(self.indent_text.format('depth=0'))
    #     self.assert_In('- foo', toc_txt)
    #     self.assert_In('\t- bar', toc_txt)
    #     self.assert_In('\t\t- buz', toc_txt)
    #     self.assert_In('\t\t\t- qux', toc_txt)

    def test_indent_2spaces(self):
        toc_txt = self.commonSetup(self.indent_text.format('depth=0 indent="  "'))
        self.assert_In('- foo', toc_txt)
        self.assert_In('  - bar', toc_txt)
        self.assert_In('    - buz', toc_txt)
        self.assert_In('      - qux', toc_txt)

    def test_indent_4spaces(self):
        toc_txt = self.commonSetup(self.indent_text.format('depth=0 indent="    "'))
        self.assert_In('- foo', toc_txt)
        self.assert_In('    - bar', toc_txt)
        self.assert_In('        - buz', toc_txt)
        self.assert_In('            - qux', toc_txt)

    # -----------------
    # Lowercase only ascii

    lowercase_only_ascii_text = \
"""

<!-- MarkdownTOC uri_encoding=false {0} -->

<!-- /MarkdownTOC -->

# ПРИМЕР EXAMPLE
"""

    def test_lowercase_only_ascii_default(self):
        toc_txt = self.commonSetup(self.lowercase_only_ascii_text.format('autolink=true'))
        self.assert_In('- [ПРИМЕР EXAMPLE][пример-example]', toc_txt)

    def test_lowercase_only_ascii_true(self):
        toc_txt = self.commonSetup(self.lowercase_only_ascii_text.format('autolink=true lowercase_only_ascii=true'))
        self.assert_In('- [ПРИМЕР EXAMPLE][ПРИМЕР-example]', toc_txt)

    def test_lowercase_only_ascii_false(self):
        toc_txt = self.commonSetup(self.lowercase_only_ascii_text.format('autolink=true lowercase_only_ascii=false'))
        self.assert_In('- [ПРИМЕР EXAMPLE][пример-example]', toc_txt)

    # -----------------
    # URI encode

    uri_encoding_text = \
"""

<!-- MarkdownTOC autolink=true lowercase_only_ascii=true {0} -->

<!-- /MarkdownTOC -->

# Camión, último
# España
# こんにちわ 世界
# Пример Example
# 一个标题
"""

    def test_uri_encoding_default(self):
        toc_txt = self.commonSetup(self.uri_encoding_text.format(''))
        self.assert_In('- [Camión, último][cami%C3%B3n-%C3%BAltimo]', toc_txt)
        self.assert_In('- [España][espa%C3%B1a]', toc_txt)
        self.assert_In('- [こんにちわ 世界][%E3%81%93%E3%82%93%E3%81%AB%E3%81%A1%E3%82%8F-%E4%B8%96%E7%95%8C]', toc_txt)
        self.assert_In('- [Пример Example][%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80-example]', toc_txt)
        self.assert_In('- [一个标题][%E4%B8%80%E4%B8%AA%E6%A0%87%E9%A2%98]', toc_txt)

    def test_uri_encoding_true(self):
        toc_txt = self.commonSetup(self.uri_encoding_text.format('uri_encoding=true'))
        self.assert_In('- [Camión, último][cami%C3%B3n-%C3%BAltimo]', toc_txt)
        self.assert_In('- [España][espa%C3%B1a]', toc_txt)
        self.assert_In('- [こんにちわ 世界][%E3%81%93%E3%82%93%E3%81%AB%E3%81%A1%E3%82%8F-%E4%B8%96%E7%95%8C]', toc_txt)
        self.assert_In('- [Пример Example][%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80-example]', toc_txt)
        self.assert_In('- [一个标题][%E4%B8%80%E4%B8%AA%E6%A0%87%E9%A2%98]', toc_txt)

    def test_uri_encoding_false(self):
        toc_txt = self.commonSetup(self.uri_encoding_text.format('uri_encoding=false'))
        self.assert_In('- [Camión, último][camión-último]', toc_txt)
        self.assert_In('- [España][españa]', toc_txt)
        self.assert_In('- [こんにちわ 世界][こんにちわ-世界]', toc_txt)
        self.assert_In('- [Пример Example][Пример-example]', toc_txt)
        self.assert_In('- [一个标题][一个标题]', toc_txt)