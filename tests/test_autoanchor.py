# coding:utf-8
from base import TestBase
import sublime
import sys

class TestAutoanchor(TestBase):
    """Test of attributes 'autoanchor'"""

    # for debug
    # def tearDown(self):
    #     pass

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
