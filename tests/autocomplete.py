# coding:utf-8
from base import TestBase
from MarkdownTOC.markdowntoc.autocomplete import AutoComplete


class TestAutoComplete(TestBase):
    """Test for completions in MarkdownTOC tag"""

    def completions_at(self, text, pt):
        """Return [trigger, contents] of completions at pt in text"""
        self.setText(text)
        self.moveTo(pt)
        result = AutoComplete().on_query_completions(self.view, "", [pt])
        if result is None:
            return None
        return [[c[0].split("\t")[0], c[1]] for c in result[0]]

    def complete(self, text):
        """Return triggers of completions at the end of text"""
        completions = self.completions_at(text, len(text))
        if completions is None:
            return None
        return [c[0] for c in completions]

    def close_contents(self, text, pt):
        """Return contents of '-->' completion at pt, or None"""
        for trigger, contents in self.completions_at(text, pt):
            if trigger == "-->":
                return contents
        return None

    def test_attribute_names(self):
        names = self.complete("<!-- MarkdownTOC ")
        self.assertIn("autolink", names)
        self.assertIn("levels", names)
        self.assertIn("bracket", names)

    def test_attribute_names_exclude_used(self):
        names = self.complete('<!-- MarkdownTOC autolink="true" ')
        self.assertNotIn("autolink", names)
        self.assertIn("levels", names)

    def test_attribute_names_in_closed_tag(self):
        names = self.complete_in_closed_tag()
        self.assertIn("autolink", names)

    def complete_in_closed_tag(self):
        text = "<!-- MarkdownTOC  -->\n"
        completions = self.completions_at(text, len("<!-- MarkdownTOC "))
        return [c[0] for c in completions]

    def test_close_with_end_tag(self):
        """Add the end tag too when it doesn't exist"""
        text = "<!-- MarkdownTOC "
        contents = self.close_contents(text, len(text))
        self.assertIn("-->", contents)
        self.assertIn("<!-- /MarkdownTOC -->", contents)

    def test_close_without_end_tag(self):
        """Add only '-->' when the end tag already exists"""
        text = "<!-- MarkdownTOC \n\n<!-- /MarkdownTOC -->\n"
        contents = self.close_contents(text, len("<!-- MarkdownTOC "))
        self.assertEqual(contents, "-->")

    def test_close_before_another_toc(self):
        """The end tag of the next TOC doesn't belong to this one"""
        text = "<!-- MarkdownTOC \n\n<!-- MarkdownTOC -->\n\n<!-- /MarkdownTOC -->\n"
        contents = self.close_contents(text, len("<!-- MarkdownTOC "))
        self.assertIn("<!-- /MarkdownTOC -->", contents)

    def test_no_close_in_closed_tag(self):
        self.assertNotIn("-->", self.complete_in_closed_tag())

    def test_bool_values(self):
        self.assertEqual(self.complete('<!-- MarkdownTOC autolink="'), ["true", "false"])
        self.assertEqual(self.complete("<!-- MarkdownTOC autoanchor="), ["true", "false"])

    def test_enum_values(self):
        self.assertEqual(self.complete('<!-- MarkdownTOC bracket="'), ["round", "square"])
        self.assertEqual(self.complete('<!-- MarkdownTOC style="'), ["ordered", "unordered"])

    def test_no_values_for_free_text(self):
        self.assertIsNone(self.complete('<!-- MarkdownTOC levels="'))

    def test_no_values_after_completed(self):
        self.assertIsNone(self.complete('<!-- MarkdownTOC autolink="true'))

    def test_outside_of_tag(self):
        self.assertIsNone(self.complete("# heading "))
        self.assertIsNone(self.complete("<!-- MarkdownTOC -->\n"))
        self.assertIsNone(self.complete("<!-- /MarkdownTOC "))
        self.assertIsNone(self.complete("<!-- MarkdownTOC:excluded "))
