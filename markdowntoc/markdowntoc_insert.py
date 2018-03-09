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
PT_REF_LINK = re.compile(r'(?<!\\)\[.+?(?<!\\)\]\s*$')

# ![alt](path/to/image.png)
PT_IMAGE = re.compile(r'!\[([^\]]+)\]\([^\)]+\)')
# [Heading]{#my-id}
PT_EX_ID = re.compile(r'\{#.+?\}$')
PT_TAG = re.compile(r'<.*?>')
PT_ANCHOR = re.compile(r'<a\s+id="[^"]+"\s*>\s*</a>')

class MarkdowntocInsert(sublime_plugin.TextCommand, Base):

    def run(self, edit):
        if not self.find_tag_and_insert(edit):
            sels = self.view.sel()
            for sel in sels:
                attrs = self.defaults()

                # add TOCTAG
                toc = "<!-- MarkdownTOC -->\n"
                toc += "\n"
                toc += self.get_toc(attrs, sel.end(), edit)
                toc += "\n"
                toc += "<!-- /MarkdownTOC -->\n"

                self.view.insert(edit, sel.begin(), toc)
                self.log('inserted TOC')

        # TODO: process to add another toc when tag exists

    def get_toc_open_tag(self):
        search_results = self.view.find_all(
            "^<!-- MarkdownTOC .*-->\n",
            sublime.IGNORECASE)
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

    def get_toc_close_tag(self, start):
        close_tags = self.view.find_all("^<!-- /MarkdownTOC -->\n")
        close_tags = self.remove_items_in_codeblock(close_tags)
        for close_tag in close_tags:
            if start < close_tag.begin():
                return close_tag

    def find_tag_and_insert(self, edit):
        """Search MarkdownTOC comments in document"""
        toc_starts = self.get_toc_open_tag()
        for dic in toc_starts:

            toc_start = dic["region"]
            if 0 < len(toc_start):

                toc_close = self.get_toc_close_tag(toc_start.end())

                if toc_close:
                    toc = self.get_toc(dic, toc_close.end(), edit)
                    tocRegion = sublime.Region(
                        toc_start.end(), toc_close.begin())
                    if toc:
                        self.view.replace(edit, tocRegion, "\n" + toc + "\n")
                        self.log('refresh TOC content')
                        return True
                    else:
                        self.view.replace(edit, tocRegion, "\n")
                        self.log('TOC is empty')
                        return False
        self.log('cannot find TOC tags')
        return False

    def escape_brackets(self, _text):
        # Escape brackets which not in image and codeblock

        def do_escape(_text, _pattern, _open, _close):
            images = []
            brackets = []
            codes = []
            for m in re.compile(r'`[^`]*`').finditer(_text):
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

        _text = do_escape(_text, re.compile(r'(?<!\\)\[([^\]]*)(?<!\\)\]'), '\[', '\]')
        _text = do_escape(_text, re.compile(r'(?<!\\)\(([^\)]*)(?<!\\)\)'), '\(', '\)')

        return _text

    # TODO: add "end" parameter
    def get_toc(self, attrs, begin, edit):

        # Search headings in docment
        pattern_hash = "^#+?[^#]"
        pattern_h1_h2_equal_dash = "^.*?(?:(?:\r\n)|\n|\r)(?:-+|=+)$"
        pattern_heading = "%s|%s" % (pattern_h1_h2_equal_dash, pattern_hash)
        headings = self.view.find_all(pattern_heading)

        headings = self.remove_items_in_codeblock(headings)

        if len(headings) < 1:
            return ''

        items = []  # [[headingNum,text,position,anchor_id],...]
        for heading in headings:
            if begin < heading.end():
                lines = self.view.lines(heading)
                if len(lines) == 1:
                    # handle hash headings, ### chapter 1
                    r = sublime.Region(
                        heading.end() - 1, self.view.line(heading).end())
                    text = self.view.substr(r).strip().rstrip('#')
                    indent = heading.size() - 1
                    items.append([indent, text, heading.begin()])
                elif len(lines) == 2:
                    # handle = or - headings
                    # Title 1
                    # ====
                    # section1
                    # ----
                    text = self.view.substr(lines[0])
                    if text.strip():
                        indent = 1 if (
                            self.view.substr(lines[1])[0] == '=') else 2
                        items.append([indent, text, heading.begin()])

        if len(items) < 1:
            return ''

        # Shape TOC  ------------------
        items = Util.format(items)

        # TODO: Remove this block in the future release version
        # Depth limit  ------------------
        if hasattr(attrs, 'depth'):
            # WARNING
            url = 'https://github.com/naokazuterada/MarkdownTOC/releases/tag/3.0.0'
            message = '[MarkdownTOC] <b>OBSOLETE</b> <br>Don\'t use \'depth\' any more, use \'levels\' instead.'

            def open_link(v):
                webbrowser.open_new(url)
            self.view.show_popup(
                message + '<br><a href>Instruction</a>', on_navigate=open_link)
            self.error(PT_TAG.sub('', message) + ' Instruction > ' + url)

        # Filtering by heading level  ------------------
        accepted_levels = list(
            map(lambda i: int(i), attrs['levels']))
        items = list(filter((lambda j: j[0] in accepted_levels), items))

        # Create TOC  ------------------
        toc = ''
        _ids = []
        level_counters = [0]
        remove_image = attrs['remove_image']
        link_prefix = attrs['link_prefix']
        bullets = attrs['bullets']

        for item in items:
            _id = None
            _indent = item[0] - 1
            _text = item[1]
            if remove_image:
                # Remove markdown image which not in codeblock
                images = []
                codes = []
                for m in re.compile(r'`[^`]*`').finditer(_text):
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
                        return ''
                    else:
                        return m.group(0)
                _text = re.sub(PT_IMAGE, _replace, _text)

            _list_bullet = bullets[_indent % len(bullets)]
            _text = PT_TAG.sub('', _text)  # remove html tags
            _text = _text.strip()  # remove start and end spaces

            # Ignore links: e.g. '[link](http://sample.com/)' -> 'link'
            # this is [link](http://www.sample.com/)
            link = re.compile(r'([^!])\[([^\]]+)\]\([^\)]+\)')
            _text = link.sub('\\1\\2', _text)
            # [link](http://www.sample.com/) link in the beginning of line
            beginning_link = re.compile(r'^\[([^\]]+)\]\([^\)]+\)')
            _text = beginning_link.sub('\\1', _text)

            # Add indent
            for i in range(_indent):
                _prefix = attrs['indent']
                # Support escaped characters like '\t'
                _prefix = _prefix.encode().decode('unicode-escape')
                toc += _prefix

            # -----------------
            # Reference-style links: e.g. '# heading [my-anchor]'
            ref_links = list(PT_REF_LINK.finditer(_text))

            def filtering(ref_links, text):
                images = []
                codes = []
                valids = []
                for m in re.compile(r'`[^`]*`').finditer(text):
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
                _text = _text[0:match.start()].replace(
                    '[', '').replace(']', '').rstrip()
                _id = match.group().replace('[', '').replace(']', '')
            elif match_ex_id:
                _text = _text[0:match_ex_id.start()].rstrip()
                _id = match_ex_id.group().replace('{#', '').replace('}', '')
            elif attrs['autolink']:
                _id = Id(
                        self.settings('id_replacements'),
                        attrs['markdown_preview'],
                        attrs['lowercase']
                    ).heading_to_id(_text)
                if attrs['uri_encoding']:
                    _id = quote(_id)

                _ids.append(_id)
                n = _ids.count(_id)
                if 1 < n:
                    _id += '-' + str(n - 1)

            if attrs['style'] == 'unordered':
                list_prefix = _list_bullet + ' '
            elif attrs['style'] == 'ordered':
                list_prefix = '1. '

            # escape brackets
            _text = self.escape_brackets(_text)

            if link_prefix:
                _id = link_prefix + _id

            if _id is None:
                toc += list_prefix + _text + '\n'
            elif attrs['bracket'] == 'round':
                toc += list_prefix + '[' + _text + '](#' + _id + ')\n'
            else:
                toc += list_prefix + '[' + _text + '][' + _id + ']\n'

            item.append(_id)

        self.update_anchors(edit, items, attrs['autoanchor'])

        return toc

    def update_anchors(self, edit, items, autoanchor):
        """Inserts, updates or deletes a link anchor in the line before each header."""
        v = self.view
        # Iterate in reverse so that inserts don't affect the position
        for item in reversed(items):
            anchor_region = v.line(item[2] - 1)  # -1 to get to previous line
            is_update = PT_ANCHOR.match(v.substr(anchor_region))
            if autoanchor:
                # if autolink=false then item[3] will be None,
                # so use raw heading valie(replaced whitespaces) then
                _id = item[3] or re.sub(r'\s+', '-', item[1])
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
                        sublime.Region(
                            anchor_region.begin(),
                            anchor_region.end() + 1))

    def get_attributes_from(self, tag_str):
        """return dict of settings from tag_str"""
        pattern = re.compile(
            r'\b(?P<name>\w+)=((?P<empty>)|(\'(?P<quoted>[^\']+)\')|("(?P<dquoted>[^"]+)")|(?P<simple>\S+))\s')
        attrs = dict(
            (m.group('name'),
                m.group('simple') or
                m.group('dquoted') or
                m.group('quoted') or
                m.group('empty'))
            for m in pattern.finditer(tag_str)
        )

        # parse values according to type of values in settings file
        defaults = self.defaults()
        for key in attrs:
            if type(defaults[key]) is list:
                attrs[key] = attrs[key].split(',')
            elif type(defaults[key]) is bool:
                attrs[key] = Util.strtobool(attrs[key])

        return attrs

    def remove_items_in_codeblock(self, items):

        codeblocks = self.view.find_all("^\s*`{3,}[^`]*$")
        codeblockAreas = []  # [[area_begin, area_end], ..]
        i = 0
        while i < len(codeblocks) - 1:
            area_begin = codeblocks[i].begin()
            area_end = codeblocks[i + 1].begin()
            if area_begin and area_end:
                codeblockAreas.append([area_begin, area_end])
            i += 2

        items = [
            h for h in items if Util.is_out_of_areas(
                h.begin(),
                codeblockAreas)]
        return items
