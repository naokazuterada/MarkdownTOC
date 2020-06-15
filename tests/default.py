# coding:utf-8
from base import TestBase


class TestDefault(TestBase):
    """Default tests"""

    # for debug
    # def tearDown(self):
    #     pass

    insert_position_text = """
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
        toc = self.init_insert(self.insert_position_text, 13)
        self.assert_NotIn("Heading 0", toc)

    def test_after_than_TOC_should_be_included(self):
        toc = self.init_insert(self.insert_position_text, 13)
        self.assert_In("Heading 1", toc)
        self.assert_In("Heading 2", toc)
        self.assert_In("Heading 3", toc)
        self.assert_In("Heading with anchor", toc)

    def test_ignore_inside_codeblock(self):
        text = """


# heading1

```
# heading2
```

```markdown
# heading3
```

```

# heading4
# heading5

```
"""
        toc = self.init_insert(text)
        self.assert_In("heading1", toc)
        self.assert_NotIn("heading3", toc)
        self.assert_NotIn("heading2", toc)
        self.assert_NotIn("heading4", toc)
        self.assert_NotIn("heading5", toc)

    def test_ignore_inside_codeblock_alt(self):
        text = """


# heading1

~~~
# heading2
~~~

~~~markdown
# heading3
~~~

~~~

# heading4
# heading5

~~~
"""
        toc = self.init_insert(text)
        self.assert_In("heading1", toc)
        self.assert_NotIn("heading3", toc)
        self.assert_NotIn("heading2", toc)
        self.assert_NotIn("heading4", toc)
        self.assert_NotIn("heading5", toc)

    def test_escape_link(self):
        text = """


# This [link](http://sample.com/) is cool
"""
        toc = self.init_insert(text)
        self.assert_In("This link is cool", toc)

    def test_escape_brackets(self):
        """Broken reference when header has square brackets
        https://github.com/naokazuterada/MarkdownTOC/issues/57
        """
        text = """


# function(foo[, bar])
"""
        toc = self.init_insert(text)
        self.assert_In("function\(foo\[, bar\]\)", toc)

    def test_spaces_in_atx_heading(self):
        text = """


#Heading 0

#       Heading 1
"""
        toc = self.init_insert(text)
        self.assert_In("- Heading 0", toc)
        self.assert_In("- Heading 1", toc)

    def test_remove_atx_closing_seq(self):
        """ Remove closing sequence of # characters"""
        text = """


# Heading 0 #


## Heading 1       ###


# Heading 2 ##########


## Heading 3
"""
        toc = self.init_insert(text)
        self.assert_In("Heading 0\n", toc)
        self.assert_In("Heading 1\n", toc)
        self.assert_In("Heading 2\n", toc)

    def test_id_replacement(self):
        """ Reoplace chars(or string) in id_replacements object in id string"""
        text = """

<!-- MarkdownTOC autolink=true -->

<!-- /MarkdownTOC -->

# Heading ! 0

# Heading # 1

# Heading !! 2

# Heading &and&and& 3

# &lt;element1>

# &#60;element2>
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- [Heading ! 0](#heading--0)", toc)
        self.assert_In("- [Heading # 1](#heading--1)", toc)
        self.assert_In("- [Heading !! 2](#heading--2)", toc)
        self.assert_In("- [Heading &and&and& 3](#heading-andand-3)", toc)
        self.assert_In("- [&lt;element1>](#element1)", toc)
        self.assert_In("- [&#60;element2>](#element2)", toc)

    def test_no_escape_in_code(self):
        """ No escape in codeblock"""
        text = """

<!-- MarkdownTOC -->

<!-- /MarkdownTOC -->

# `function(param, [optional])`
# (a static function) `greet([name])` (original, right?)
# `add(keys, command[, args][, context])`
# `get_context(key[, operator][, operand][, match_all])`
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- `function(param, [optional])`", toc)
        self.assert_In(
            "- \\(a static function\\) `greet([name])` \\(original, right?\\)", toc
        )
        self.assert_In("- `add(keys, command[, args][, context])`", toc)
        self.assert_In("- `get_context(key[, operator][, operand][, match_all])`", toc)

    def test_no_escape_in_code_with_link(self):
        """ No escape in codeblock (with link)"""
        text = """

<!-- MarkdownTOC autolink=true -->

<!-- /MarkdownTOC -->

# `function(param, [optional])`
# (a static function) `greet([name])` (original, right?)
# `add(keys, command[, args][, context])`
# `get_context(key[, operator][, operand][, match_all])`
"""
        toc = self.init_update(text)["toc"]
        self.assert_In(
            "- [`function(param, [optional])`](#functionparam-optional)", toc
        )
        self.assert_In(
            "- [\\(a static function\\) `greet([name])` \\(original, right?\\)](#a-static-function-greetname-original-right)",
            toc,
        )
        self.assert_In(
            "- [`add(keys, command[, args][, context])`](#addkeys-command-args-context)",
            toc,
        )
        self.assert_In(
            "- [`get_context(key[, operator][, operand][, match_all])`](#get_contextkey-operator-operand-match_all)",
            toc,
        )

    def test_no_headings(self):
        """ No headings there"""
        text = """

<!-- MarkdownTOC autolink=true -->

<!-- /MarkdownTOC -->

# `function(param, [optional])`
# (a static function) `greet([name])` (original, right?)
# `add(keys, command[, args][, context])`
# `get_context(key[, operator][, operand][, match_all])`
"""
        toc = self.init_update(text)["toc"]
        self.assert_NotIn("^- ", toc)

    def test_uniquify_id_1(self):
        """ uniquify id if there are same text headings"""
        text = """

<!-- MarkdownTOC autolink=true -->

<!-- /MarkdownTOC -->

# Heading
# Heading
# Heading
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- [Heading](#heading)", toc)
        self.assert_In("- [Heading](#heading-1)", toc)
        self.assert_In("- [Heading](#heading-2)", toc)

    def test_uniquify_id_2(self):
        """ handle = or - headings"""
        text = """

<!-- MarkdownTOC autolink=true indent="  " -->

<!-- /MarkdownTOC -->

Heading 1
=======

Heading 2
-------
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- [Heading 1](#heading-1)", toc)
        self.assert_In("  - [Heading 2](#heading-2)", toc)

    def test_whitespace_in_begining(self):
        """Ignore images in heading"""
        text = """

<!-- MarkdownTOC -->

<!-- /MarkdownTOC -->

# Heading
#  Heading
#   Heading
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- Heading", toc)
        self.assert_NotIn("-  Heading", toc)
        self.assert_NotIn("-   Heading", toc)

    def test_image_in_heading(self):
        """Ignore images in heading"""
        text = """

<!-- MarkdownTOC -->

<!-- /MarkdownTOC -->

# ![icon](images/icon.png) Heading
# Image in ![icon](images/icon.png)sentence
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- Heading", toc)
        self.assert_In("- Image in sentence", toc)
