# coding:utf-8
from base import TestBase


class TestAutoanchor(TestBase):
    """Test for attributes \'autoanchor\'"""

    # for debug
    # def tearDown(self):
    #     pass

    text = """
<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# Changelog
# Glossary
# API Specification
"""

    def test_autoanchor_default(self):
        """autoanchor is 'false' in default"""
        body_txt = self.init_update(self.text_with_autolink_true.format(""))["body"]
        self.assert_NotIn('<a id="changelog"></a>\n# Changelog', body_txt)
        self.assert_NotIn('<a id="glossary"></a>\n# Glossary', body_txt)
        self.assert_NotIn('<a id="api-specification"></a>', body_txt)

    def test_autoanchor_true(self):
        """If autoanchor is 'true' then added anchor"""
        body_txt = self.init_update(self.text.format("autoanchor=true"))["body"]
        self.assert_In('<a id="Changelog"></a>\n# Changelog', body_txt)
        self.assert_In('<a id="Glossary"></a>\n# Glossary', body_txt)
        self.assert_In('<a id="API-Specification"></a>\n# API Specification', body_txt)

    def test_autoanchor_false(self):
        """If autoanchor is 'false' then it doesn't added anchor"""
        body_txt = self.init_update(self.text.format("autoanchor=false"))["body"]
        self.assert_NotIn('<a id="changelog"></a>', body_txt)
        self.assert_NotIn('<a id="glossary"></a>', body_txt)
        self.assert_NotIn('<a id="api-specification"></a>', body_txt)

    text_with_autolink_true = """

<!-- MarkdownTOC autolink=true {0} -->

<!-- /MarkdownTOC -->

# Changelog
# Glossary
# API Specification
"""

    def test_with_autolink_autoanchor_default(self):
        """With autolink: autoanchor is 'false' in default"""
        body_txt = self.init_update(self.text_with_autolink_true.format(""))["body"]
        self.assert_NotIn('<a id="changelog"></a>\n# Changelog', body_txt)
        self.assert_NotIn('<a id="glossary"></a>\n# Glossary', body_txt)
        self.assert_NotIn('<a id="api-specification"></a>', body_txt)

    def test_with_autolink_autoanchor_true(self):
        """With autolink: If autoanchor is 'true' then it adds anchor"""
        body_txt = self.init_update(
            self.text_with_autolink_true.format("autoanchor=true")
        )["body"]
        self.assert_In('<a id="changelog"></a>\n# Changelog', body_txt)
        self.assert_In('<a id="glossary"></a>\n# Glossary', body_txt)
        self.assert_In('<a id="api-specification"></a>\n# API Specification', body_txt)

    def test_with_autolink_autoanchor_false(self):
        """With autolink: If autoanchor is 'false' then it doesn't added anchor"""
        body_txt = self.init_update(
            self.text_with_autolink_true.format("autoanchor=false")
        )["body"]
        self.assert_NotIn('<a id="changelog"></a>\n# Changelog', body_txt)
        self.assert_NotIn('<a id="glossary"></a>\n# Glossary', body_txt)
        self.assert_NotIn('<a id="api-specification"></a>', body_txt)
