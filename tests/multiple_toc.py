# coding:utf-8
import re

from base import TestBase


class TestMultipleToc(TestBase):
    """Test for multiple TOCs and attributes 'start', 'scope'"""

    def tocs(self, body):
        """Return the contents of all TOCs in body"""
        return re.findall(
            r"<!-- MarkdownTOC[^>]*-->\n(.*?)<!-- /MarkdownTOC -->", body, re.DOTALL
        )

    text_sections = """
<!-- MarkdownTOC autolink="true" levels="1" -->

<!-- /MarkdownTOC -->

# macOS

<!-- MarkdownTOC autolink="true" {0} -->

<!-- /MarkdownTOC -->

## Installation
## Usage

# Windows
## Installation

# Index

<!-- MarkdownTOC autolink="true" {1} -->

<!-- /MarkdownTOC -->
"""

    def test_all_tocs_are_updated(self):
        body = self.init_update(self.text_sections.format("", ""))["body"]
        tocs = self.tocs(body)
        self.assertEqual(len(tocs), 3)
        # levels="1"
        self.assert_In("- [macOS](#macos)", tocs[0])
        self.assert_NotIn("Installation", tocs[0])
        # start="here", scope="document" by default
        self.assert_NotIn("macOS", tocs[1])
        self.assert_In("- [Installation](#installation)", tocs[1])
        self.assert_In("- [Windows](#windows)", tocs[1])
        # no headings after the last TOC
        self.assertEqual(tocs[2].strip(), "")

    def test_scope_section(self):
        body = self.init_update(self.text_sections.format('scope="section"', ""))["body"]
        toc = self.tocs(body)[1]
        self.assert_In("- [Installation](#installation)", toc)
        self.assert_In("- [Usage](#usage)", toc)
        self.assert_NotIn("Windows", toc)
        self.assert_NotIn("installation-1", toc)

    def test_scope_section_ids(self):
        """Duplicate ids are numbered over the whole document in a section TOC"""
        text = """
# macOS
## Installation

# Windows

<!-- MarkdownTOC autolink="true" scope="section" -->

<!-- /MarkdownTOC -->

## Installation
"""
        toc = self.init_update(text)["toc"]
        self.assertEqual(toc.strip(), "- [Installation](#installation-1)")

    def test_scope_section_without_parent(self):
        """The TOC before any heading lists all of the headings after it"""
        text = """

<!-- MarkdownTOC scope="section" -->

<!-- /MarkdownTOC -->

# heading 1
# heading 2
"""
        toc = self.init_update(text)["toc"]
        self.assert_In("- heading 1", toc)
        self.assert_In("- heading 2", toc)

    def test_start_top(self):
        body = self.init_update(self.text_sections.format("", 'start="top"'))["body"]
        toc = self.tocs(body)[2]
        self.assert_In("- [macOS](#macos)", toc)
        self.assert_In("\t- [Installation](#installation)", toc)
        self.assert_In("\t- [Installation](#installation-1)", toc)
        self.assert_In("- [Index](#index)", toc)

    def test_start_top_scope_section(self):
        """start="top" doesn't list the headings out of the section"""
        text = """
# Hello World!
## Overview

# API

<!-- MarkdownTOC autolink="true" start="top" scope="section" -->

<!-- /MarkdownTOC -->

## foo()
## bar()

# Index
"""
        toc = self.tocs(self.init_update(text)["body"])[0]
        self.assertEqual(toc.strip(), "- [foo\\(\\)](#foo)\n- [bar\\(\\)](#bar)")

    def test_scope_section_before_heading(self):
        """The TOC is in the same section as the heading right after it"""
        text = """
# Hello World!
## Foo
### Bar

<!-- MarkdownTOC autolink="true" scope="section" -->

<!-- /MarkdownTOC -->

# Hello World!4
## 2
### 3
"""
        toc = self.tocs(self.init_update(text)["body"])[0]
        self.assert_In("- [Hello World!4](#hello-world4)", toc)
        self.assert_In("\t- [2](#2)", toc)
        self.assert_In("\t\t- [3](#3)", toc)
        self.assert_NotIn("Bar", toc)

    def test_scope_section_in_middle(self):
        """start="top" lists the headings of the section before the TOC too"""
        text = """
# Overview

# API
## foo()

<!-- MarkdownTOC autolink="true" scope="section" {0} -->

<!-- /MarkdownTOC -->

## bar()

# Index
"""
        toc = self.tocs(self.init_update(text.format(""))["body"])[0]
        self.assertEqual(toc.strip(), "- [bar\\(\\)](#bar)")

        self.tearDown()
        self.setUp()
        toc = self.tocs(self.init_update(text.format('start="top"'))["body"])[0]
        self.assertEqual(toc.strip(), "- [foo\\(\\)](#foo)\n- [bar\\(\\)](#bar)")

    def test_start_top_with_autoanchor(self):
        """Anchors inserted before the TOC don't break the TOC"""
        text = """
# heading 1
# heading 2

<!-- MarkdownTOC autolink="true" autoanchor="true" start="top" -->

<!-- /MarkdownTOC -->
"""
        body = self.init_update(text)["body"]
        self.assert_In('<a id="heading-1"></a>\n# heading 1', body)
        self.assert_In('<a id="heading-2"></a>\n# heading 2', body)
        toc = self.tocs(body)[0]
        self.assert_In("- [heading 1](#heading-1)", toc)
        self.assert_In("- [heading 2](#heading-2)", toc)

    def test_update_twice(self):
        """Updating again doesn't change the document"""
        text = self.text_sections.format('scope="section" autoanchor="true"', 'start="top"')
        self.setText(text)
        self.view.run_command("markdowntoc_update")
        first = self.view.substr(self.view.find(r"(.|\n)*", 0))
        self.view.run_command("markdowntoc_update")
        second = self.view.substr(self.view.find(r"(.|\n)*", 0))
        self.assertEqual(first, second)

    def test_autoanchor_true_has_priority(self):
        """A TOC with autoanchor=false doesn't remove anchors of another TOC"""
        text = """
<!-- MarkdownTOC autolink="true" -->

<!-- /MarkdownTOC -->

# Section

<!-- MarkdownTOC autolink="true" autoanchor="true" scope="section" -->

<!-- /MarkdownTOC -->

## heading
"""
        body = self.init_update(text)["body"]
        self.assert_In('<a id="heading"></a>\n## heading', body)
        self.assert_NotIn('<a id="section"></a>', body)

    def test_open_tag_without_close_tag(self):
        """The open tag without its own close tag is ignored"""
        text = """
<!-- MarkdownTOC -->

<!-- MarkdownTOC -->

<!-- /MarkdownTOC -->

# heading
"""
        body = self.init_update(text)["body"]
        self.assert_In("<!-- MarkdownTOC -->\n\n<!-- MarkdownTOC -->\n\n- heading\n\n<!-- /MarkdownTOC -->", body)

    text_insert = """

<!-- MarkdownTOC -->

<!-- /MarkdownTOC -->

# heading 1

# heading 2
## heading 2-1
"""

    def insert_at(self, pt):
        self.setText(self.text_insert)
        self.moveTo(pt)
        self.view.run_command("markdowntoc_insert")
        return self.view.substr(self.view.find(r"(.|\n)*", 0))

    def test_insert_another_toc(self):
        """Insert TOC adds a new TOC even when a TOC exists"""
        pt = self.text_insert.index("## heading 2-1")
        body = self.insert_at(pt)
        tocs = self.tocs(body)
        self.assertEqual(len(tocs), 2)
        self.assert_In("- heading 1", tocs[0])
        self.assertEqual(tocs[1].strip(), "- heading 2-1")
        self.assert_In("<!-- /MarkdownTOC -->\n## heading 2-1", body)

    def test_insert_in_toc(self):
        """Insert TOC in an existing TOC only refreshes it"""
        pt = self.text_insert.index("<!-- /MarkdownTOC -->")
        body = self.insert_at(pt)
        tocs = self.tocs(body)
        self.assertEqual(len(tocs), 1)
        self.assert_In("- heading 1", tocs[0])

    def test_insert_in_middle_of_line(self):
        """The new TOC is inserted below the line not to split the line"""
        pt = self.text_insert.index("heading 2\n") + len("heading")
        body = self.insert_at(pt)
        self.assert_In(
            "# heading 2\n<!-- MarkdownTOC -->\n\n- heading 2-1\n\n<!-- /MarkdownTOC -->\n## heading 2-1",
            body,
        )

    def test_insert_in_middle_of_last_line(self):
        """The new TOC is inserted below the last line without line break"""
        self.setText("\n\n# heading 1")
        self.moveTo(len("\n\n# head"))
        self.view.run_command("markdowntoc_insert")
        body = self.view.substr(self.view.find(r"(.|\n)*", 0))
        self.assertEqual(body, "\n\n# heading 1\n<!-- MarkdownTOC -->\n\n<!-- /MarkdownTOC -->\n")

    text_inherit = """

<!-- MarkdownTOC autolink="true" bracket=square levels="1" -->

<!-- /MarkdownTOC -->

# Usage

# API
{0}
## foo()
## bar()
{1}
"""

    def insert_marker(self, text):
        """Insert TOC at '|' in text"""
        pt = text.index("|")
        self.setText(text.replace("|", ""))
        self.moveTo(pt)
        self.view.run_command("markdowntoc_insert")
        return self.view.substr(self.view.find(r"(.|\n)*", 0))

    def test_insert_inherits_attributes(self):
        """The new TOC inherits the attributes of the first TOC except levels"""
        body = self.insert_marker(self.text_inherit.format("|", "# Index"))
        self.assert_In(
            '# API\n<!-- MarkdownTOC autolink="true" bracket=square scope="section" -->\n\n'
            "- [foo\\(\\)][foo]\n- [bar\\(\\)][bar]\n",
            body,
        )

    def test_insert_no_scope_at_end_of_document(self):
        """scope="section" is not added when the section continues to the end"""
        body = self.insert_marker(self.text_inherit.format("|", ""))
        self.assert_In('# API\n<!-- MarkdownTOC autolink="true" bracket=square -->\n', body)

    def test_insert_no_scope_in_root(self):
        """scope="section" is not added when the TOC is not in a section"""
        body = self.insert_marker(self.text_inherit.format("", "|\n# Index"))
        self.assert_In('<!-- MarkdownTOC autolink="true" bracket=square -->\n\n- [Index][index]\n', body)

    def test_insert_first_toc(self):
        """The first TOC has no attributes"""
        text = "\n\n# API\n|\n## foo()\n\n# Index\n"
        body = self.insert_marker(text)
        self.assert_In("# API\n<!-- MarkdownTOC -->\n\n- foo\\(\\)\n- Index\n", body)
