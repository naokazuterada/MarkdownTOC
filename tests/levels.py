# coding:utf-8
from base import TestBase


class TestLevels(TestBase):
    """Test for attributes \'levels\'"""

    # for debug
    # def tearDown(self):
    #     pass

    text_1 = """

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# heading 1
## heading 2
### heading 3
#### heading 4
##### heading 5
###### heading 6
"""
    # TODO: test warning if depth is exists in settings

    def appear_all_headings(self, toc):
        self.assert_In("- heading 1", toc)
        self.assert_In("- heading 2", toc)
        self.assert_In("- heading 3", toc)
        self.assert_In("- heading 4", toc)
        self.assert_In("- heading 5", toc)
        self.assert_In("- heading 6", toc)

    def test_levels_default(self):
        """Default is no limit"""
        toc = self.init_update(self.text_1.format(""))["toc"]
        self.appear_all_headings(toc)

    def test_levels_1(self):
        """levels="1" shows h1 """
        toc = self.init_update(self.text_1.format('levels="1"'))["toc"]
        self.assert_In("- heading 1", toc)
        self.assert_NotIn("- heading 2", toc)
        self.assert_NotIn("- heading 3", toc)
        self.assert_NotIn("- heading 4", toc)
        self.assert_NotIn("- heading 5", toc)
        self.assert_NotIn("- heading 6", toc)

    def test_levels_1_2(self):
        """levels="1,2" shows h1,h2 """
        toc = self.init_update(self.text_1.format('levels="1,2"'))["toc"]
        self.assert_In("- heading 1", toc)
        self.assert_In("- heading 2", toc)
        self.assert_NotIn("- heading 3", toc)
        self.assert_NotIn("- heading 4", toc)
        self.assert_NotIn("- heading 5", toc)
        self.assert_NotIn("- heading 6", toc)

    def test_levels_1_2_3(self):
        """levels="1,2,3" shows h1,h2,h3 """
        toc = self.init_update(self.text_1.format('levels="1,2,3"'))["toc"]
        self.assert_In("- heading 1", toc)
        self.assert_In("- heading 2", toc)
        self.assert_In("- heading 3", toc)
        self.assert_NotIn("- heading 4", toc)
        self.assert_NotIn("- heading 5", toc)
        self.assert_NotIn("- heading 6", toc)

    def test_levels_1_2_3_4(self):
        """levels="1,2,3,4" shows h1,h2,h3,h4 """
        toc = self.init_update(self.text_1.format('levels="1,2,3,4"'))["toc"]
        self.assert_In("- heading 1", toc)
        self.assert_In("- heading 2", toc)
        self.assert_In("- heading 3", toc)
        self.assert_In("- heading 4", toc)
        self.assert_NotIn("- heading 5", toc)
        self.assert_NotIn("- heading 6", toc)

    def test_levels_1_2_3_4_5(self):
        """levels="1,2,3,4,5" shows h1,h2,h3,h4,h5 """
        toc = self.init_update(self.text_1.format('levels="1,2,3,4,5"'))["toc"]
        self.assert_In("- heading 1", toc)
        self.assert_In("- heading 2", toc)
        self.assert_In("- heading 3", toc)
        self.assert_In("- heading 4", toc)
        self.assert_In("- heading 5", toc)
        self.assert_NotIn("- heading 6", toc)

    def test_levels_1_2_3_4_5_6(self):
        """levels="1,2,3,4,5" shows h1,h2,h3,h4,h5 """
        toc = self.init_update(self.text_1.format('levels="1,2,3,4,5,6"'))["toc"]
        self.appear_all_headings(toc)

    text_2 = """

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

### heading 3
#### heading 4
# heading 1
## heading 2
##### heading 5
###### heading 6
"""

    def test_levels_specific_level(self):
        """Default is no limit"""
        toc = self.init_update(self.text_2.format('levels="3"'))["toc"]
        self.assert_In("- heading 3", toc)
        self.assert_NotIn("- heading 4", toc)
        self.assert_NotIn("- heading 1", toc)
        self.assert_NotIn("- heading 2", toc)
        self.assert_NotIn("- heading 5", toc)
        self.assert_NotIn("- heading 6", toc)

    def test_levels_specific_levels(self):
        """Default is no limit"""
        toc = self.init_update(self.text_2.format('levels="2,4,6"'))["toc"]
        self.assert_NotIn("- heading 3", toc)
        self.assert_In("- heading 4", toc)
        self.assert_NotIn("- heading 1", toc)
        self.assert_In("- heading 2", toc)
        self.assert_NotIn("- heading 5", toc)
        self.assert_In("- heading 6", toc)
