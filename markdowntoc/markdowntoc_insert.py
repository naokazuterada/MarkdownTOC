import pprint
import re
import sublime
import sublime_plugin
import sys
import webbrowser

from urllib.parse import quote

from .autorunner import AutoRunner
from .base import Base
from .util import Util
from .id import Id

# for debug
pp = pprint.PrettyPrinter(indent=4)

# [Heading][my-id]
# Negative lookbehind
PT_REF_LINK = re.compile(r"(?<!\\)\[.+?(?<!\\)\]\s*$")

# ![alt](path/to/image.png)
PT_IMAGE = re.compile(r"!\[([^\]]+)\]\([^\)]+\)")
# [Heading]{#my-id}
PT_EX_ID = re.compile(r"\{#.+?\}$")
PT_TAG = re.compile(r"<.*?>")
PT_ANCHOR = re.compile(r'<a\s+id="[^"]+"\s*>\s*</a>')
# name="value" in the TOC tag
PT_ATTRIBUTE = re.compile(
    r'\b(?P<name>\w+)=((?P<empty>)|(\'(?P<quoted>[^\']+)\')|("(?P<dquoted>[^"]+)")|(?P<simple>\S+))\s'
)
# Attributes not inherited by a new TOC as they depend on the position
RANGE_ATTRIBUTES = ["levels", "start", "scope"]


# <!-- MarkdownTOC:excluded  -->
PT_EXCLUDE = re.compile(r"^<!--.*(MarkdownTOC:excluded).*-->", re.IGNORECASE)


class MarkdowntocInsert(sublime_plugin.TextCommand, Base):
    def run(self, edit):
        """Insert a new TOC at the cursor, then refresh all of the TOCs"""
        tocs = self.get_tocs()
        headings = self.get_headings()

        # Decide all of the tags before inserting as inserts change the positions
        inserts = []
        for sel in self.view.sel():
            pt = sel.begin()
            # Don't insert in an existing TOC
            if any(o["region"].begin() <= pt < c.end() for o, c in tocs):
                continue
            # The tag must be at the beginning of a line, so insert it below
            # the line not to split the line
            before = after = ""
            line = self.view.line(pt)
            if line.begin() != pt:
                pt = line.end()
                before = "\n"
                # Use the line break after the line if exists
                after = "" if pt < self.view.size() else "\n"
            else:
                after = "\n"
            attrs = self.get_new_toc_attributes(tocs, headings, pt)
            tag = "<!-- MarkdownTOC%s -->\n\n<!-- /MarkdownTOC -->" % attrs
            inserts.append([pt, before + tag + after])

        # Insert from the bottom so that inserts don't affect the other positions
        for pt, tag in sorted(inserts, key=lambda i: i[0], reverse=True):
            self.view.insert(edit, pt, tag)
            self.log("inserted TOC")

        self.find_tag_and_insert(edit)

    def get_new_toc_attributes(self, tocs, headings, pt):
        """Return the attributes text for a new TOC inserted at pt.

        When a TOC already exists, the new TOC inherits the attributes of the
        first TOC except for the range ones, and gets scope="section" when it is
        in a section which ends before the end of the document.
        """
        if not tocs:
            return ""
        tag_str = self.view.substr(tocs[0][0]["region"])
        attrs = [
            m.group(0).strip()
            for m in PT_ATTRIBUTE.finditer(tag_str)
            if m.group("name") not in RANGE_ATTRIBUTES
        ]
        parent, section_end = self.get_section(headings, pt, pt)
        if parent and section_end is not None:
            attrs.append('scope="section"')
        return "".join(" " + attr for attr in attrs)

    def get_toc_open_tag(self):
        search_results = self.view.find_all(
            r"^<!--[\s\n]+MarkdownTOC[\s\n]+[^>]*-->\n", sublime.IGNORECASE
        )
        search_results = self.remove_items_in_codeblock(search_results)

        toc_open_tags = []
        for toc_open in search_results:
            if 0 < len(toc_open):

                toc_open_tag = {"region": toc_open}

                # settings in user settings
                settings_user = self.defaults()

                # settings in tag
                tag_str = self.view.substr(toc_open)
                settings_tag = self.get_attributes_from(tag_str)

                # merge
                toc_open_tag.update(settings_user)
                toc_open_tag.update(settings_tag)

                toc_open_tags.append(toc_open_tag)

        return toc_open_tags

    def get_toc_close_tags(self):
        close_tags = self.view.find_all(r"<!--[\s\n]+/MarkdownTOC[\s\n]+-->\n")
        return self.remove_items_in_codeblock(close_tags)

    def get_tocs(self):
        """Return pairs of open tag (with attributes) and close tag"""
        open_tags = self.get_toc_open_tag()
        close_tags = self.get_toc_close_tags()
        tocs = []
        for i, open_tag in enumerate(open_tags):
            start = open_tag["region"].end()
            if i + 1 < len(open_tags):
                next_start = open_tags[i + 1]["region"].begin()
            else:
                next_start = self.view.size()
            for close_tag in close_tags:
                if start < close_tag.begin():
                    # Ignore the open tag without its own close tag
                    if close_tag.begin() < next_start:
                        tocs.append([open_tag, close_tag])
                    break
        return tocs

    def find_tag_and_insert(self, edit):
        """Search MarkdownTOC comments in document and refresh all of the TOCs"""
        tocs = self.get_tocs()
        if not tocs:
            self.log("cannot find TOC tags")
            return False

        headings = self.get_headings()
        edits = []  # [[position, "toc" or "anchor", args], ...]
        anchors = {}  # {heading position: [item, autoanchor]}
        has_content = False
        for open_tag, close_tag in tocs:
            items = self.select_headings(
                headings, open_tag, open_tag["region"].begin(), close_tag.end()
            )
            toc = self.build_toc(open_tag, items, headings)
            region = sublime.Region(open_tag["region"].end(), close_tag.begin())
            content = "\n" + toc + "\n" if toc else "\n"
            edits.append([region.begin(), "toc", [region, content]])
            has_content = has_content or bool(toc)

            # When a heading is listed in multiple TOCs, the upper TOC decides
            # its anchor, but autoanchor=true has priority over false
            for item in items:
                current = anchors.get(item[2])
                if current is None or (open_tag["autoanchor"] and not current[1]):
                    anchors[item[2]] = [item, open_tag["autoanchor"]]

        for position, (item, autoanchor) in anchors.items():
            edits.append([position, "anchor", [item, autoanchor]])

        # Edit from the bottom so that edits don't affect the other positions
        for position, kind, args in sorted(edits, key=lambda e: e[0], reverse=True):
            if kind == "toc":
                self.view.replace(edit, *args)
            else:
                self.update_anchor(edit, *args)

        self.log("refresh TOC content" if has_content else "TOC is empty")
        return has_content

    def escape_brackets(self, _text):
        # Escape brackets which not in image and codeblock

        def do_escape(_text, _pattern, _open, _close):
            images = []
            brackets = []
            codes = []
            for m in re.compile(r"`[^`]*`").finditer(_text):
                codes.append([m.start(), m.end()])

            def not_in_codeblock(target):
                return not Util.within_ranges(target, codes)

            def not_in_image(target):
                return not Util.within_ranges(target, images)

            # Collect images not in codeblock
            for m in PT_IMAGE.finditer(_text):
                images.append([m.start(), m.end()])
            images = list(filter(not_in_codeblock, images))
            # Collect brackets not in image tags
            for m in _pattern.finditer(_text):
                brackets.append([m.start(), m.end()])
            brackets = list(filter(not_in_image, brackets))
            brackets = list(filter(not_in_codeblock, brackets))
            brackets = list(map((lambda x: x[0]), brackets))
            # Escape brackets

            def replace_brackets(m):
                if m.start() in brackets:
                    return _open + m.group(1) + _close
                else:
                    return m.group(0)

            return re.sub(_pattern, replace_brackets, _text)

        _text = do_escape(_text, re.compile(r"(?<!\\)\[([^\]]*)(?<!\\)\]"), r"\[", r"\]")
        _text = do_escape(_text, re.compile(r"(?<!\\)\(([^\)]*)(?<!\\)\)"), r"\(", r"\)")

        return _text

    def get_headings(self):
        """Return all headings in document: [[region, level, text, excluded], ...]"""

        # Search headings in docment
        pattern_hash = "^#+?[^#]"
        pattern_h1_h2_equal_dash = "^.*?(?:(?:\r\n)|\n|\r)(?:-+|=+)$"
        pattern_heading = "%s|%s" % (pattern_h1_h2_equal_dash, pattern_hash)
        headings = self.view.find_all(pattern_heading)

        headings = self.remove_items_in_codeblock(headings)

        results = []
        for heading in headings:
            lines = self.view.lines(heading)
            previous_line = self.view.substr(self.view.line(lines[0].a - 1))
            excluded = bool(PT_EXCLUDE.match(previous_line))

            if len(lines) == 1:
                # handle hash headings, ### chapter 1
                r = sublime.Region(heading.end() - 1, self.view.line(heading).end())
                text = self.view.substr(r).strip().rstrip("#")
                indent = heading.size() - 1
                results.append([heading, indent, text, excluded])
            elif len(lines) == 2:
                # handle = or - headings
                # Title 1
                # ====
                # section1
                # ----
                text = self.view.substr(lines[0])
                if text.strip():
                    heading_type = self.view.substr(lines[1])[0]
                    indent = 1 if heading_type == "=" else 2
                    results.append([heading, indent, text, excluded])
        return results

    def get_section(self, headings, toc_begin, toc_end):
        """Return [parent heading, end position] of the section which the TOC
        placed from toc_begin to toc_end is in.

        The TOC is in the same section as the heading right after it, so the
        parent is the nearest heading before the TOC whose level is upper than
        that heading. parent is None when the TOC is in the root (document), and
        end position is None when the section continues to the end of document.
        """
        nexts = [h for h in headings if toc_end <= h[0].begin()]
        if nexts:
            parents = [
                h for h in headings if h[0].end() <= toc_begin and h[1] < nexts[0][1]
            ]
            if parents:
                parent = parents[-1]
                for h in nexts:
                    if h[1] <= parent[1]:
                        return [parent, h[0].begin()]
                return [parent, None]
        return [None, None]

    def select_headings(self, headings, attrs, toc_begin, toc_end):
        """Return items of headings listed in the TOC placed from toc_begin to toc_end:
        [[headingNum, text, position], ...]"""

        # scope="section" lists the headings in the section which the TOC is in
        scope_begin = 0
        scope_end = self.view.size()
        if attrs["scope"] == "section":
            parent, section_end = self.get_section(headings, toc_begin, toc_end)
            if parent:
                scope_begin = parent[0].end()
            if section_end is not None:
                scope_end = section_end

        # start="top" lists the headings from the top of the scope,
        # including the ones before the TOC
        begin = scope_begin if attrs["start"] == "top" else toc_end
        end = scope_end

        items = [
            [h[1], h[2], h[0].begin()]
            for h in headings
            if begin < h[0].end() and h[0].begin() < end and not h[3]
        ]

        # Filtering by heading level  ------------------
        accepted_levels = list(map(lambda i: int(i), attrs["levels"]))
        items = list(filter((lambda j: j[0] in accepted_levels), items))

        # Shape TOC  ------------------
        return Util.format(items)

    def build_toc(self, attrs, items, headings):
        """Return TOC text of items, and append the anchor id to each item"""
        if len(items) < 1:
            return ""

        # TODO: Remove this block in the future release version
        # Depth limit  ------------------
        if hasattr(attrs, "depth"):
            # WARNING
            url = "https://github.com/naokazuterada/MarkdownTOC/releases/tag/3.0.0"
            message = "[MarkdownTOC] <b>OBSOLETE</b> <br>Don't use 'depth' any more, use 'levels' instead."

            def open_link(v):
                webbrowser.open_new(url)

            self.view.show_popup(
                message + "<br><a href>Instruction</a>", on_navigate=open_link
            )
            self.error(PT_TAG.sub("", message) + " Instruction > " + url)

        # Create TOC  ------------------
        toc = ""
        texts_and_ids = self.get_texts_and_ids(attrs, headings)
        link_prefix = attrs["link_prefix"]
        bullets = attrs["bullets"]

        for item in items:
            _indent = item[0] - 1
            _text, _id = texts_and_ids[item[2]]

            _list_bullet = bullets[_indent % len(bullets)]

            # Add indent
            for i in range(_indent):
                _prefix = attrs["indent"]
                # Support escaped characters like '\t'
                _prefix = _prefix.encode().decode("unicode-escape")
                toc += _prefix

            if attrs["style"] == "unordered":
                list_prefix = _list_bullet + " "
            elif attrs["style"] == "ordered":
                list_prefix = "1. "

            # escape brackets
            _text = self.escape_brackets(_text)

            if link_prefix:
                _id = link_prefix + _id

            if _id is None:
                toc += list_prefix + _text + "\n"
            elif attrs["bracket"] == "round":
                toc += list_prefix + "[" + _text + "](#" + _id + ")\n"
            else:
                toc += list_prefix + "[" + _text + "][" + _id + "]\n"

            item.append(_id)

        return toc

    def get_texts_and_ids(self, attrs, headings):
        """Return text and id of all headings for TOC: {position: [text, id]}

        Duplicate auto link ids are numbered over the whole document like GitHub
        does, including headings out of the TOC (other levels, excluded, before
        the TOC)
        """
        texts_and_ids = {}
        counts = {}
        delimiter = "_" if attrs["markdown_preview"] == "markdown" else "-"
        # Load the setting only once as it is used for all of the headings
        id_replacements = self.settings("id_replacements")
        for heading in headings:
            _text, _id, is_auto_id = self.get_text_and_id(
                attrs, heading[2], id_replacements
            )
            if is_auto_id:
                n = counts.get(_id, 0)
                counts[_id] = n + 1
                if 0 < n:
                    _id += delimiter + str(n)
            texts_and_ids[heading[0].begin()] = [_text, _id]
        return texts_and_ids

    def get_text_and_id(self, attrs, _text, id_replacements):
        """Return [text, id, is_auto_id] of the heading text for TOC.
        id is None when autolink=false and the heading has no own id"""
        _id = None
        is_auto_id = False
        if attrs["remove_image"]:
            # Remove markdown image which not in codeblock
            images = []
            codes = []
            for m in re.compile(r"`[^`]*`").finditer(_text):
                codes.append([m.start(), m.end()])

            def not_in_codeblock(_target):
                return not Util.within_ranges(_target, codes)

            # Collect images not in codeblock
            for m in PT_IMAGE.finditer(_text):
                images.append([m.start(), m.end()])
            images = list(filter(not_in_codeblock, images))
            images = list(map((lambda x: x[0]), images))

            def _replace(m):
                if m.start() in images:
                    return ""
                else:
                    return m.group(0)

            _text = re.sub(PT_IMAGE, _replace, _text)

        _text = PT_TAG.sub("", _text)  # remove html tags
        _text = _text.strip()  # remove start and end spaces

        # Ignore links: e.g. '[link](http://sample.com/)' -> 'link'
        # this is [link](http://www.sample.com/)
        link = re.compile(r"([^!])\[([^\]]+)\]\([^\)]+\)")
        _text = link.sub("\\1\\2", _text)
        # [link](http://www.sample.com/) link in the beginning of line
        beginning_link = re.compile(r"^\[([^\]]+)\]\([^\)]+\)")
        _text = beginning_link.sub("\\1", _text)

        # -----------------
        # Reference-style links: e.g. '# heading [my-anchor]'
        ref_links = list(PT_REF_LINK.finditer(_text))

        def filtering(ref_links, text):
            images = []
            codes = []
            valids = []
            for m in re.compile(r"`[^`]*`").finditer(text):
                codes.append([m.start(), m.end()])

            def not_in_codeblock(target):
                return not Util.within_ranges(target, codes)

            def not_in_image(target):
                return not Util.within_ranges(target, images)

            # Collect images not in codeblock
            for m in PT_IMAGE.finditer(text):
                images.append([m.start(), m.end()])
            images = list(filter(not_in_codeblock, images))
            # # Collect valids not in image tags
            for m in ref_links:
                valids.append([m.start(), m.end()])
            valids = list(filter(not_in_image, valids))
            valids = list(filter(not_in_codeblock, valids))
            valids = list(map((lambda x: x[0]), valids))
            return list(filter(lambda x: x.start() in valids, ref_links))

        ref_links = filtering(ref_links, _text)

        # -----------------

        # Markdown-Extra special attribute style:
        # e.g. '# heading {#my-anchor}'
        match_ex_id = PT_EX_ID.search(_text)

        if len(ref_links):
            match = ref_links[-1]
            _text = _text[0 : match.start()].replace("[", "").replace("]", "").rstrip()
            _id = match.group().replace("[", "").replace("]", "")
        elif match_ex_id:
            _text = _text[0 : match_ex_id.start()].rstrip()
            _id = match_ex_id.group().replace("{#", "").replace("}", "")
        elif attrs["autolink"]:
            _id = Id(
                id_replacements,
                attrs["markdown_preview"],
                str(attrs["lowercase"]).lower(),
            ).heading_to_id(_text)
            if attrs["uri_encoding"]:
                _id = quote(_id)
            is_auto_id = True

        return [_text, _id, is_auto_id]

    def update_anchor(self, edit, item, autoanchor):
        """Inserts, updates or deletes a link anchor in the line before the header."""
        v = self.view
        anchor_region = v.line(item[2] - 1)  # -1 to get to previous line
        is_update = PT_ANCHOR.match(v.substr(anchor_region))
        if autoanchor:
            # if autolink=false then item[3] will be None,
            # so use raw heading valie(replaced whitespaces) then
            _id = item[3] or re.sub(r"\s+", "-", item[1])
            if is_update:
                new_anchor = '<a id="{0}"></a>'.format(_id)
                v.replace(edit, anchor_region, new_anchor)
            else:
                new_anchor = '\n<a id="{0}"></a>'.format(_id)
                v.insert(edit, anchor_region.end(), new_anchor)

        else:
            if is_update:
                v.erase(
                    edit,
                    sublime.Region(anchor_region.begin(), anchor_region.end() + 1),
                )

    def get_attributes_from(self, tag_str):
        """return dict of settings from tag_str"""
        pattern = PT_ATTRIBUTE
        attrs = dict(
            (
                m.group("name"),
                m.group("simple")
                or m.group("dquoted")
                or m.group("quoted")
                or m.group("empty"),
            )
            for m in pattern.finditer(tag_str)
        )

        # parse values according to type of values in settings file
        return self.parse_values(attrs)

    def remove_items_in_codeblock(self, items):

        codeblocks = self.view.find_all(r"^(\s|[-*])*(`{3,}|~{3,})\S*")
        codeblockAreas = []  # [[area_begin, area_end], ..]
        i = 0
        while i < len(codeblocks) - 1:
            area_begin = codeblocks[i].begin()
            area_end = codeblocks[i + 1].begin()
            if area_begin and area_end:
                codeblockAreas.append([area_begin, area_end])
            i += 2

        items = [h for h in items if Util.is_out_of_areas(h.begin(), codeblockAreas)]
        return items
