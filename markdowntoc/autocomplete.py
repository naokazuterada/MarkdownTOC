import re
import sublime
import sublime_plugin

from .base import Base

# Unclosed "<!-- MarkdownTOC ..." right before the cursor
PT_OPEN_TAG = re.compile(r"<!--[\s\n]+MarkdownTOC(?P<attrs>(\s[^>]*)?)$", re.IGNORECASE)
# 'name="value' or 'name=value' right before the cursor
PT_VALUE = re.compile(r"\b(?P<name>\w+)=\"?(?P<value>[^\"\s]*)$")
# Attribute name being typed right before the cursor
PT_NAME = re.compile(r"\s\w*$")
PT_USED_NAME = re.compile(r"\b(\w+)=")
# First comment boundary after the cursor ("-->" means the tag is already closed)
PT_COMMENT_BOUNDARY = re.compile(r"-->|<!--")
# First MarkdownTOC open or close tag after the cursor
PT_NEXT_TAG = re.compile(r"<!--[\s\n]+(/?)MarkdownTOC\b", re.IGNORECASE)

CLOSE_TAG = "<!-- /MarkdownTOC -->"

# How far back/forward from the cursor to look for the tags
LOOKBEHIND = 1000
LOOKAHEAD = 10000

ENUM_VALUES = {
    "bracket": ["round", "square"],
    "lowercase": ["all", "only_ascii", "false"],
    "markdown_preview": ["github", "markdown"],
    "scope": ["document", "section"],
    "start": ["here", "top"],
    "style": ["ordered", "unordered"],
}


class AutoComplete(sublime_plugin.EventListener, Base):
    def on_query_completions(self, view, prefix, locations):
        pt = locations[0]
        attrs = self.attrs_before(view, pt)
        if attrs is None:
            return None
        completions = self.completions_for(attrs, self.text_after(view, pt))
        if not completions:
            return None
        return (
            completions,
            sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS,
        )

    def on_modified(self, view):
        # Markdown comments are excluded by the default auto_complete_selector,
        # so open the completion popup by ourselves while typing in the tag
        sels = view.sel()
        if len(sels) != 1 or not sels[0].empty():
            return
        pt = sels[0].b
        if pt == 0 or not re.match(r'[\w\s="]', view.substr(pt - 1)):
            return
        attrs = self.attrs_before(view, pt)
        if attrs is not None and self.completions_for(attrs, self.text_after(view, pt)):
            view.run_command(
                "auto_complete",
                {"disable_auto_insert": True, "next_completion_if_showing": False},
            )

    def attrs_before(self, view, pt):
        """Return the attributes text before pt if pt is in a MarkdownTOC open tag"""
        text = view.substr(sublime.Region(max(0, pt - LOOKBEHIND), pt))
        match = PT_OPEN_TAG.search(text)
        return match.group("attrs") if match else None

    def text_after(self, view, pt):
        return view.substr(sublime.Region(pt, min(view.size(), pt + LOOKAHEAD)))

    def close_completion(self, after):
        """Return the completion to close the open tag, or None if already closed"""
        boundary = PT_COMMENT_BOUNDARY.search(after)
        if boundary and boundary.group() == "-->":
            return None
        next_tag = PT_NEXT_TAG.search(after)
        if next_tag and next_tag.group(1) == "/":
            return ["-->\tclose tag", "-->"]
        # Add the close tag too as it doesn't exist yet
        return ["-->\tclose tag + end tag", "-->\n\n" + CLOSE_TAG + "\n$0"]

    def completions_for(self, attrs, after):
        defaults = self.defaults()

        match = PT_VALUE.search(attrs)
        if match:
            name = match.group("name")
            if name in ENUM_VALUES:
                values = ENUM_VALUES[name]
            elif type(defaults.get(name)) is bool:
                values = ["true", "false"]
            else:
                return None
            # Don't show again once a value is completed
            if match.group("value") in values:
                return None
            return [[value + "\t" + name, value] for value in values]

        if PT_NAME.search(attrs):
            used = PT_USED_NAME.findall(attrs)
            completions = [
                [name + "\tMarkdownTOC", name + '="$1"']
                for name in sorted(defaults)
                if name not in used
            ]
            close = self.close_completion(after)
            if close:
                completions.insert(0, close)
            return completions

        return None
