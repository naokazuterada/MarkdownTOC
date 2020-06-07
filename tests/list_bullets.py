# coding:utf-8
from base import TestBase


class TestListBullets(TestBase):
    """Test for attributes \'bullets\'"""

    # for debug
    # def tearDown(self):
    #     pass

    bullets_text = """

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

    def test_bullets_default(self):
        toc = self.init_update(self.bullets_text.format(""))["toc"]
        self.assert_In("- Heading1", toc)
        self.assert_In("- Heading2", toc)
        self.assert_In("- Heading2-2", toc)
        self.assert_In("- Heading3", toc)
        self.assert_In("- Heading3-2", toc)
        self.assert_In("- Heading4", toc)
        self.assert_In("- Heading4-2", toc)
        self.assert_In("- Heading5", toc)
        self.assert_In("- Heading6", toc)

    def test_bullets_2values(self):
        toc = self.init_update(self.bullets_text.format('bullets="+,-"'))["toc"]
        self.assert_In("+ Heading1", toc)
        self.assert_In("- Heading2", toc)
        self.assert_In("- Heading2-2", toc)
        self.assert_In("+ Heading3", toc)
        self.assert_In("+ Heading3-2", toc)
        self.assert_In("- Heading4", toc)
        self.assert_In("- Heading4-2", toc)
        self.assert_In("+ Heading5", toc)
        self.assert_In("- Heading6", toc)

    def test_bullets_3values(self):
        toc = self.init_update(self.bullets_text.format('bullets="-,+,*"'))["toc"]
        self.assert_In("- Heading1", toc)
        self.assert_In("+ Heading2", toc)
        self.assert_In("+ Heading2-2", toc)
        self.assert_In("* Heading3", toc)
        self.assert_In("* Heading3-2", toc)
        self.assert_In("- Heading4", toc)
        self.assert_In("- Heading4-2", toc)
        self.assert_In("+ Heading5", toc)
        self.assert_In("* Heading6", toc)

    def test_bullets_4values(self):
        toc = self.init_update(self.bullets_text.format('bullets="-,+,-,*"'))["toc"]
        self.assert_In("- Heading1", toc)
        self.assert_In("+ Heading2", toc)
        self.assert_In("+ Heading2-2", toc)
        self.assert_In("- Heading3", toc)
        self.assert_In("- Heading3-2", toc)
        self.assert_In("* Heading4", toc)
        self.assert_In("* Heading4-2", toc)
        self.assert_In("- Heading5", toc)
        self.assert_In("+ Heading6", toc)
