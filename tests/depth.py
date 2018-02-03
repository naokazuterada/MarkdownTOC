# coding:utf-8
from base import TestBase
import sublime
import sys

class TestDepth(TestBase):
    """Test of attributes 'depth'"""

    # for debug
    # def tearDown(self):
    #     pass

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
