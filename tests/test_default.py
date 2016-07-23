# coding:utf-8
from base import TestBase

class TestDefault(TestBase):
    """Default tests"""

    # for debug
    # def tearDown(self):
    #     pass

    insert_position_text = \
"""
# Heading 0



# Heading 1

...


## Heading 2

...


## Heading 3

...


# Heading with anchor [with-anchor]

...
"""
    def test_before_than_TOC_should_be_ignored(self):
        toc_txt = self.commonSetup(self.insert_position_text, 13)
        self.assert_NotIn('Heading 0', toc_txt)

    def test_after_than_TOC_should_be_included(self):
        toc_txt = self.commonSetup(self.insert_position_text, 13)
        self.assert_In('Heading 1', toc_txt)
        self.assert_In('Heading 2', toc_txt)
        self.assert_In('Heading 3', toc_txt)
        self.assert_In('Heading with anchor', toc_txt)

    def test_ignore_inside_codeblock(self):
        text = \
"""


# Outside1

```
# Inseide
```

# Outside2

```

# Inseide2
# Inseide3

```
"""
        toc_txt = self.commonSetup(text)
        self.assert_In('Outside1', toc_txt)
        self.assert_In('Outside2', toc_txt)
        self.assert_NotIn('Inside1', toc_txt)
        self.assert_NotIn('Inside2', toc_txt)
        self.assert_NotIn('Inside3', toc_txt)

    def test_escape_link(self):
        text = \
"""


# This [link](http://sample.com/) is cool
"""
        toc_txt = self.commonSetup(text)
        self.assert_In('This link is cool', toc_txt)

    def test_escape_brackets(self):
        """Broken reference when header has square brackets
        https://github.com/naokazuterada/MarkdownTOC/issues/57
        """
        text = \
"""


# function(foo[, bar])
"""
        toc_txt = self.commonSetup(text)
        self.assert_In('function\(foo\[, bar\]\)', toc_txt)

    def test_spaces_in_atx_heading(self):
        text = \
"""


#Heading 0

#       Heading 1
"""
        toc_txt = self.commonSetup(text)
        self.assert_In('- Heading 0', toc_txt)
        self.assert_In('- Heading 1', toc_txt)

    def test_remove_atx_closing_seq(self):
        """ Remove closing sequence of # characters
        """
        text = \
"""


# Heading 0 #


## Heading 1       ###


# Heading 2 ##########


## Heading 3
"""
        toc_txt = self.commonSetup(text)
        self.assert_In('Heading 0\n', toc_txt)
        self.assert_In('Heading 1\n', toc_txt)
        self.assert_In('Heading 2\n', toc_txt)

    def test_id_replacement(self):
        """ Reoplace chars(or string) in id_replacements object in id string
        """
        text = \
"""

<!-- MarkdownTOC autolink=true -->

<!-- /MarkdownTOC -->

# Heading ! 0

# Heading # 1

# Heading !! 2

# Heading &and&and& 3

# &lt;element1>

# &#60;element2>
"""
        toc_txt = self.commonSetup(text)
        self.assert_In('- [Heading ! 0][heading--0]', toc_txt)
        self.assert_In('- [Heading # 1][heading--1]', toc_txt)
        self.assert_In('- [Heading !! 2][heading--2]', toc_txt)
        self.assert_In('- [Heading &and&and& 3][heading-andand-3]', toc_txt)
        self.assert_In('- [&lt;element1>][element1]', toc_txt)
        self.assert_In('- [&#60;element2>][element2]', toc_txt)