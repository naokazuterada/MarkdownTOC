# coding:utf-8
from base import TestBase


class TestExcludeHeading(TestBase):
    """Ignore exclude heading"""

    # for debug
    # def tearDown(self):
    #     pass

    text_1 = """

<!-- MarkdownTOC -->

<!-- /MarkdownTOC -->

# heading 1

<!-- MarkdownTOC:excluded  -->
# heading 2

# heading 3

"""

    def test_exclude_heading(self):
        """Default is no limit"""
        toc = self.init_update(self.text_1)["toc"]
        self.assert_In("- heading 1", toc)
        self.assert_NotIn("- heading 2", toc)
        self.assert_In("- heading 3", toc)

    text_2 = """

<!-- MarkdownTOC indent="  " -->

<!-- /MarkdownTOC -->

# level 1
<!-- MarkdownTOC:excluded  -->
## level 2
### level 3
<!-- MarkdownTOC:excluded  -->
#### level 4
<!-- MarkdownTOC:excluded  -->
##### level 5
###### level 6

"""

    def test_exclude_heading_level(self):
        """Existence and level is correct"""
        toc = self.init_update(self.text_2)["toc"]
        # existence
        self.assert_NotIn("- level 2", toc)
        self.assert_NotIn("- level 4", toc)
        self.assert_NotIn("- level 5", toc)
        # level
        self.assert_In(
            """- level 1
  - level 3
    - level 6""",
            toc,
        )
