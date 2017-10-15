# coding:utf-8
from base import TestBase
import sublime
import sys

class TestLevels(TestBase):
    """Test of attributes 'levels'"""

    # for debug
    # def tearDown(self):
    #     pass

    levels_text = \
"""

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

    def appear_all_headings(self, toc_txt):
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_In('- heading 3', toc_txt)
        self.assert_In('- heading 4', toc_txt)
        self.assert_In('- heading 5', toc_txt)
        self.assert_In('- heading 6', toc_txt)
    def test_levels_default(self):
        """Default is no limit"""
        toc_txt = self.commonSetup(self.levels_text.format(''))
        self.appear_all_headings(toc_txt)

    def test_levels_1(self):
        """levels="1" shows h1 """
        toc_txt = self.commonSetup(self.levels_text.format('levels="1"'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_NotIn('- heading 2', toc_txt)
        self.assert_NotIn('- heading 3', toc_txt)
        self.assert_NotIn('- heading 4', toc_txt)
        self.assert_NotIn('- heading 5', toc_txt)
        self.assert_NotIn('- heading 6', toc_txt)

    def test_levels_1_2(self):
        """levels="1,2" shows h1,h2 """
        toc_txt = self.commonSetup(self.levels_text.format('levels="1,2"'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_NotIn('- heading 3', toc_txt)
        self.assert_NotIn('- heading 4', toc_txt)
        self.assert_NotIn('- heading 5', toc_txt)
        self.assert_NotIn('- heading 6', toc_txt)

    def test_levels_1_2_3(self):
        """levels="1,2,3" shows h1,h2,h3 """
        toc_txt = self.commonSetup(self.levels_text.format('levels="1,2,3"'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_In('- heading 3', toc_txt)
        self.assert_NotIn('- heading 4', toc_txt)
        self.assert_NotIn('- heading 5', toc_txt)
        self.assert_NotIn('- heading 6', toc_txt)

    def test_levels_1_2_3_4(self):
        """levels="1,2,3,4" shows h1,h2,h3,h4 """
        toc_txt = self.commonSetup(self.levels_text.format('levels="1,2,3,4"'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_In('- heading 3', toc_txt)
        self.assert_In('- heading 4', toc_txt)
        self.assert_NotIn('- heading 5', toc_txt)
        self.assert_NotIn('- heading 6', toc_txt)

    def test_levels_1_2_3_4_5(self):
        """levels="1,2,3,4,5" shows h1,h2,h3,h4,h5 """
        toc_txt = self.commonSetup(self.levels_text.format('levels="1,2,3,4,5"'))
        self.assert_In('- heading 1', toc_txt)
        self.assert_In('- heading 2', toc_txt)
        self.assert_In('- heading 3', toc_txt)
        self.assert_In('- heading 4', toc_txt)
        self.assert_In('- heading 5', toc_txt)
        self.assert_NotIn('- heading 6', toc_txt)

    def test_levels_1_2_3_4_5_6(self):
        """levels="1,2,3,4,5" shows h1,h2,h3,h4,h5 """
        toc_txt = self.commonSetup(self.levels_text.format('levels="1,2,3,4,5,6"'))
        self.appear_all_headings(toc_txt)
