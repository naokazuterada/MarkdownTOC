# coding:utf-8
from base import TestBase


class TestDuplicateIds(TestBase):
    """Duplicate ids are numbered over the whole document like GitHub does"""

    def test_same_as_before(self):
        """Ids don't change when all of duplicates are in the TOC"""
        text = """

<!-- MarkdownTOC autolink="true" -->

<!-- /MarkdownTOC -->

# macOS
## Installation
# Windows
## Installation
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- [Installation](#installation)\n", toc)
        self.assert_In("- [Installation](#installation-1)", toc)

    def test_other_levels(self):
        """Count headings excluded by levels"""
        text = """

<!-- MarkdownTOC autolink="true" levels="1,2" -->

<!-- /MarkdownTOC -->

# API
### Options
## Options
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- [Options](#options-1)", toc)
        self.assert_NotIn("(#options)", toc)

    def test_before_toc(self):
        """Count headings before the TOC"""
        text = """
# Example

<!-- MarkdownTOC autolink="true" -->

<!-- /MarkdownTOC -->

## Example
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- [Example](#example-1)", toc)

    def test_excluded_heading(self):
        """Count headings excluded by MarkdownTOC:excluded"""
        text = """

<!-- MarkdownTOC autolink="true" -->

<!-- /MarkdownTOC -->

<!-- MarkdownTOC:excluded -->
## Notes
## Notes
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- [Notes](#notes-1)", toc)
        self.assert_NotIn("(#notes)", toc)

    def test_markdown_preview_delimiter(self):
        text = """
# Example

<!-- MarkdownTOC autolink="true" markdown_preview="markdown" -->

<!-- /MarkdownTOC -->

# Example
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- [Example](#example_1)", toc)

    def test_autoanchor(self):
        """Inserted anchors use the same ids"""
        text = """
# Example

<!-- MarkdownTOC autolink="true" autoanchor="true" -->

<!-- /MarkdownTOC -->

# Example
"""
        body = self.init_update(text)["body"]
        self.assert_In('<a id="example-1"></a>\n# Example', body)

    def test_numbered_id_used_by_another_heading(self):
        """Number again when the numbered id is used by another heading like GitHub"""
        text = """

<!-- MarkdownTOC autolink="true" -->

<!-- /MarkdownTOC -->

# Foo
# Foo
# foo-1
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- [Foo](#foo)\n- [Foo](#foo-1)\n- [foo-1](#foo-1-1)", toc)
