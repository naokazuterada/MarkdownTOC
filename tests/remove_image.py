# coding:utf-8
from base import TestBase
import sublime
import sys

class TestRemoveImage(TestBase):
    """Test of attributes 'remove_image'"""

    # for debug
    # def tearDown(self):
    #     pass

    remove_image_text = \
"""

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# ![icon](img/icon.png) In the beginning
# In the ![icon](img/icon.png) middle
# In the last ![icon](img/icon.png)
# [link](http://sample.com) In the beginning
# In the [link](http://sample.com) middle
# In the last [link](http://sample.com)
"""
    def common_remove_image_default(self, toc_txt):
        self.assert_In('- In the beginning', toc_txt)
        self.assert_In('- In the  middle', toc_txt)
        self.assert_In('- In the last', toc_txt)
        self.assert_In('- link In the beginning', toc_txt)
        self.assert_In('- In the link middle', toc_txt)
        self.assert_In('- In the last link', toc_txt)
    def test_remove_image_default(self):
        toc_txt = self.commonSetup(self.remove_image_text.format(''))
        self.common_remove_image_default(toc_txt)
    def test_remove_image_true(self):
        toc_txt = self.commonSetup(self.remove_image_text.format('remove_image="true"'))
        self.common_remove_image_default(toc_txt)
    def test_remove_image_false(self):
        toc_txt = self.commonSetup(self.remove_image_text.format('remove_image="false"'))
        self.assert_In('- ![icon](img/icon.png) In the beginning', toc_txt)
        self.assert_In('- In the ![icon](img/icon.png) middle', toc_txt)
        self.assert_In('- In the last ![icon](img/icon.png)', toc_txt)
        self.assert_In('- link In the beginning', toc_txt)
        self.assert_In('- In the link middle', toc_txt)
        self.assert_In('- In the last link', toc_txt)

    remove_image_codeblock_text = \
"""

<!-- MarkdownTOC {0} -->

<!-- /MarkdownTOC -->

# ![IMAGE](image.png) and [LINK](http://sample.com/) and [SQUARE] and (ROUND)
# hello![IMAGE](image.png) and [LINK](http://sample.com/) and [SQUARE] and (ROUND)
# `![IMAGE](image.png) and [LINK](http://sample.com/) and [SQUARE] and (ROUND)`
# hello`![IMAGE](image.png) and [LINK](http://sample.com/) and [SQUARE] and (ROUND)`
# `![IMAGE](image.png)` and `[LINK](http://sample.com/)` and `[SQUARE]` and `(ROUND)`
# hello`![IMAGE](image.png)` and `[LINK](http://sample.com/)` and `[SQUARE]` and `(ROUND)`
# `![IMAGE](image.png)`
# hello`![IMAGE](image.png)`
# `[LINK](http://sample.com/)`
# hello`[LINK](http://sample.com/)`
# [SQUARE] and (ROUND)
# `[SQUARE]` and `(ROUND)`
# `(ROUND)` and `[SQUARE]`
# hello[SQUARE] and (ROUND)
# hello`[SQUARE]` and `(ROUND)`
"""
    def common_remove_image_codeblock_default(self, toc_txt):
        self.assert_In('- and LINK and \[SQUARE\] and \(ROUND\)', toc_txt)
        self.assert_In('- hello and LINK and \[SQUARE\] and \(ROUND\)', toc_txt)
        self.assert_In('- `![IMAGE](image.png) and LINK and [SQUARE] and (ROUND)`', toc_txt)
        self.assert_In('- hello`![IMAGE](image.png) and LINK and [SQUARE] and (ROUND)`', toc_txt)
        self.assert_In('- `![IMAGE](image.png)` and `LINK` and `[SQUARE]` and `(ROUND)`', toc_txt)
        self.assert_In('- hello`![IMAGE](image.png)` and `LINK` and `[SQUARE]` and `(ROUND)`', toc_txt)
        self.assert_In('- `![IMAGE](image.png)`', toc_txt)
        self.assert_In('- hello`![IMAGE](image.png)`', toc_txt)
        self.assert_In('- `LINK`', toc_txt)
        self.assert_In('- hello`LINK`', toc_txt)
        self.assert_In('- \[SQUARE\] and \(ROUND\)', toc_txt)
        self.assert_In('- `[SQUARE]` and `(ROUND)`', toc_txt)
        self.assert_In('- `(ROUND)` and `[SQUARE]`', toc_txt)
        self.assert_In('- hello\[SQUARE\] and \(ROUND\)', toc_txt)
        self.assert_In('- hello`[SQUARE]` and `(ROUND)`', toc_txt)
    def test_remove_image_codeblock_default(self):
        toc_txt = self.commonSetup(self.remove_image_codeblock_text.format(''))
        self.common_remove_image_codeblock_default(toc_txt)
    def test_remove_image_codeblock_true(self):
        toc_txt = self.commonSetup(self.remove_image_codeblock_text.format('remove_image="true"'))
        self.common_remove_image_codeblock_default(toc_txt)
    def test_remove_image_codeblock_false(self):
        toc_txt = self.commonSetup(self.remove_image_codeblock_text.format('remove_image="false"'))
        self.assert_In('- ![IMAGE](image.png) and LINK and \[SQUARE\] and \(ROUND\)', toc_txt)
        self.assert_In('- hello![IMAGE](image.png) and LINK and \[SQUARE\] and \(ROUND\)', toc_txt)
        self.assert_In('- `![IMAGE](image.png) and LINK and [SQUARE] and (ROUND)`', toc_txt)
        self.assert_In('- hello`![IMAGE](image.png) and LINK and [SQUARE] and (ROUND)`', toc_txt)
        self.assert_In('- `![IMAGE](image.png)` and `LINK` and `[SQUARE]` and `(ROUND)`', toc_txt)
        self.assert_In('- hello`![IMAGE](image.png)` and `LINK` and `[SQUARE]` and `(ROUND)`', toc_txt)
        self.assert_In('- `![IMAGE](image.png)`', toc_txt)
        self.assert_In('- hello`![IMAGE](image.png)`', toc_txt)
        self.assert_In('- `LINK`', toc_txt)
        self.assert_In('- hello`LINK`', toc_txt)
        self.assert_In('- \[SQUARE\] and \(ROUND\)', toc_txt)
        self.assert_In('- `[SQUARE]` and `(ROUND)`', toc_txt)
        self.assert_In('- `(ROUND)` and `[SQUARE]`', toc_txt)
        self.assert_In('- hello\[SQUARE\] and \(ROUND\)', toc_txt)
        self.assert_In('- hello`[SQUARE]` and `(ROUND)`', toc_txt)