# coding:utf-8
from base import TestBase
from MarkdownTOC.markdowntoc.autocomplete import AutoComplete


class TestAutoComplete(TestBase):
    """Test for completions in MarkdownTOC tag"""

    def complete(self, text):
        """Return triggers of completions at the end of text"""
        self.setText(text)
        pt = self.view.sel()[0].b
        result = AutoComplete().on_query_completions(self.view, "", [pt])
        if result is None:
            return None
        return [c[0].split("\t")[0] for c in result[0]]

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
        self.setText('<!-- MarkdownTOC  -->')
        pt = len("<!-- MarkdownTOC ")
        self.moveTo(pt)
        result = AutoComplete().on_query_completions(self.view, "", [pt])
        self.assertIsNotNone(result)

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
