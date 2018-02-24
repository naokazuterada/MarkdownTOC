# coding:utf-8
from base import TestBase
import sublime
import sys

class TestListBullets(TestBase):
    """Test of attributes 'list_bullets'"""

    # for debug
    # def tearDown(self):
    #     pass

    list_bullets_text = \
"""

<!-- MarkdownTOC levels="1,2,3,4,5,6" {0} -->

<!-- /MarkdownTOC -->

# Heading1
## Heading2
## Heading2-2
### Heading3
### Heading3-2
#### Heading4
#### Heading4-2
##### Heading5
###### Heading6
"""
    def test_list_bullets_default(self):
        toc_txt = self.commonSetup(self.list_bullets_text.format(''))
        self.assert_In('- Heading1', toc_txt)
        self.assert_In('- Heading2', toc_txt)
        self.assert_In('- Heading2-2', toc_txt)
        self.assert_In('- Heading3', toc_txt)
        self.assert_In('- Heading3-2', toc_txt)
        self.assert_In('- Heading4', toc_txt)
        self.assert_In('- Heading4-2', toc_txt)
        self.assert_In('- Heading5', toc_txt)
        self.assert_In('- Heading6', toc_txt)
    def test_list_bullets_2values(self):
        toc_txt = self.commonSetup(self.list_bullets_text.format('list_bullets="+,-"'))
        self.assert_In('+ Heading1', toc_txt)
        self.assert_In('- Heading2', toc_txt)
        self.assert_In('- Heading2-2', toc_txt)
        self.assert_In('+ Heading3', toc_txt)
        self.assert_In('+ Heading3-2', toc_txt)
        self.assert_In('- Heading4', toc_txt)
        self.assert_In('- Heading4-2', toc_txt)
        self.assert_In('+ Heading5', toc_txt)
        self.assert_In('- Heading6', toc_txt)
    def test_list_bullets_3values(self):
        toc_txt = self.commonSetup(self.list_bullets_text.format('list_bullets="-,+,*"'))
        self.assert_In('- Heading1', toc_txt)
        self.assert_In('+ Heading2', toc_txt)
        self.assert_In('+ Heading2-2', toc_txt)
        self.assert_In('* Heading3', toc_txt)
        self.assert_In('* Heading3-2', toc_txt)
        self.assert_In('- Heading4', toc_txt)
        self.assert_In('- Heading4-2', toc_txt)
        self.assert_In('+ Heading5', toc_txt)
        self.assert_In('* Heading6', toc_txt)
    def test_list_bullets_4values(self):
        toc_txt = self.commonSetup(self.list_bullets_text.format('list_bullets="-,+,-,*"'))
        self.assert_In('- Heading1', toc_txt)
        self.assert_In('+ Heading2', toc_txt)
        self.assert_In('+ Heading2-2', toc_txt)
        self.assert_In('- Heading3', toc_txt)
        self.assert_In('- Heading3-2', toc_txt)
        self.assert_In('* Heading4', toc_txt)
        self.assert_In('* Heading4-2', toc_txt)
        self.assert_In('- Heading5', toc_txt)
        self.assert_In('+ Heading6', toc_txt)