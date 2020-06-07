# coding:utf-8
from base import TestBase


class LinkPrefixBullets(TestBase):
    """Test for attributes \'link_prefix\'"""

    # for debug
    # def tearDown(self):
    #     pass

    link_prefix_text = """

<!-- MarkdownTOC autolink="true" {0} -->

<!-- /MarkdownTOC -->

# My Beatutiful Heading
"""

    def test_link_prefix_default(self):
        toc = self.init_update(self.link_prefix_text.format(""))["toc"]
        self.assert_In("- [My Beatutiful Heading](#my-beatutiful-heading)", toc)

    def test_link_prefix_1(self):
        toc = self.init_update(
            self.link_prefix_text.format('link_prefix="user-content-"')
        )["toc"]
        self.assert_In(
            "- [My Beatutiful Heading](#user-content-my-beatutiful-heading)", toc
        )
