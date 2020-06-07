# coding:utf-8
from base import TestBase


class TagVariation(TestBase):
    """Test for attributes \'style\'"""

    # for debug
    # def tearDown(self):
    #     pass

    def test_1(self):
        """Tag Variation 1"""
        text = """

<!-- MarkdownTOC autolink="true" bracket="square" style="ordered" -->

<!-- /MarkdownTOC -->

# foo
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("1. [foo][foo]", toc)

    def test_2(self):
        """Tag Variation 2"""
        text = """

<!-- MarkdownTOC
autolink="true" bracket="square" style="ordered" -->

<!-- /MarkdownTOC -->

# foo
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("1. [foo][foo]", toc)

    def test_3(self):
        """Tag Variation 3"""
        text = """

<!--
MarkdownTOC
autolink="true"
bracket="square"
style="ordered" -->

<!-- /MarkdownTOC -->

# foo
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("1. [foo][foo]", toc)

    def test_4(self):
        """Tag Variation 4"""
        text = """

<!--
MarkdownTOC
autolink="true"
bracket="square"
style="ordered"
-->

<!-- /MarkdownTOC -->

# foo
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("1. [foo][foo]", toc)

    def test_5(self):
        """Tag Variation 5"""
        text = """

<!--
MarkdownTOC
autolink="true"
bracket="square"
style="ordered"
-->

<!--
/MarkdownTOC
-->

# foo
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("1. [foo][foo]", toc)
