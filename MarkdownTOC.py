import sublime
import sublime_plugin
import re
import os.path
import pprint
import sys
from urllib.parse import quote
from bs4 import BeautifulSoup
import unicodedata

# for dbug
pp = pprint.PrettyPrinter(indent=4)

pattern_reference_link = re.compile(r'\[.+?\]$') # [Heading][my-id]
pattern_link = re.compile(r'([^!])\[(.+?)\]\(.+?\)')  # [link](http://www.sample.com/)
pattern_image = re.compile(r'!\[[^\]]+\]\([^)]+\)') # ![alt](path/to/image.png)
pattern_ex_id = re.compile(r'\{#.+?\}$')         # [Heading]{#my-id}
pattern_tag = re.compile(r'<.*?>')
pattern_anchor = re.compile(r'<a\s+name="[^"]+"\s*>\s*</a>')
pattern_toc_tag_start = re.compile(r'<!-- *')
pattern_toc_tag_end = re.compile(r'-->')

pattern_h1_h2_equal_dash = "^.*?(?:(?:\r\n)|\n|\r)(?:-+|=+)$"

TOCTAG_START = "<!-- MarkdownTOC -->"
TOCTAG_END = "<!-- /MarkdownTOC -->"

class MarkdowntocInsert(sublime_plugin.TextCommand):

    def run(self, edit):

        if not self.find_tag_and_insert(edit):
            sels = self.view.sel()
            for sel in sels:
                attrs = self.get_settings()

                # add TOCTAG
                toc = TOCTAG_START + "\n"
                toc += "\n"
                toc += self.get_toc(attrs, sel.end(), edit)
                toc += "\n"
                toc += TOCTAG_END + "\n"

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
                settings_user = self.get_settings()

                # settings in tag
                tag_str = self.view.substr(toc_open)
                settings_tag = self.get_attibutes_from(tag_str)

                # merge
                toc_open_tag.update(settings_user)
                toc_open_tag.update(settings_tag)

                toc_open_tags.append(toc_open_tag)

        return toc_open_tags

    def get_toc_close_tag(self, start):
        close_tags = self.view.find_all("^" + TOCTAG_END + "\n")
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
        # TODO ここでpattern_image以外の部分のみを対象にする
        # Get indexes of images
        # ![image](path/to.png)
        images = [] # [[start,end],...]
        for m in pattern_image.finditer(_text):
            images.append([m.start(), m.end()])

        # Get indexes of backquotes
        # `foo`
        backquotes = [] # [[start,end],...]
        stock = None
        for m in re.compile(r'`').finditer(_text):
            if stock == None:
                stock = m.start()
            else:
                backquotes.append([stock, m.start()])
                stock = None

        # Get indexes of square brackets
        pattern_square_brackets = re.compile(r'\[([^\]]*)\]') # [foo]
        square_brackets = [] # [[start,end],...]
        stock = None
        for m in pattern_square_brackets.finditer(_text):
            square_brackets.append([m.start(), m.end()])

        # Get indexes of round brackets
        pattern_round_brackets = re.compile(r'\(([^\)]*)\)') # (foo)
        round_brackets = [] # [[start,end],...]
        stock = None
        for m in pattern_round_brackets.finditer(_text):
            round_brackets.append([m.start(), m.end()])

        def within_ranges(target, ranges):
            tb = target[0]
            te = target[1]
            for _range in ranges:
                rb = _range[0]
                re = _range[1]
                if (rb <= tb and tb <= re) and (rb <= tb and tb <= re):
                    return True
            return False

        def not_in_image(target):
            return not within_ranges(target, images)

        def not_in_codeblock(target):
            return not within_ranges(target, backquotes)

        images = list(filter(not_in_codeblock, images))

        # Filtering by effectiveness
        square_brackets = list(filter(not_in_image, square_brackets))
        square_brackets = list(filter(not_in_codeblock, square_brackets))
        square_brackets = list(map((lambda x: x[0]), square_brackets))

        round_brackets = list(filter(not_in_image, round_brackets))
        round_brackets = list(filter(not_in_codeblock, round_brackets))
        round_brackets = list(map((lambda x: x[0]), round_brackets))


        # Replace

        def replace_square_brackets(m):
            if m.start() in square_brackets:
                return '\['+m.group(1)+'\]'
            else:
                return m.group(0)
        _text = re.sub(pattern_square_brackets, replace_square_brackets, _text)

        def replace_round_brackets(m):
            if m.start() in round_brackets:
                return '\('+m.group(1)+'\)'
            else:
                return m.group(0)
        _text = re.sub(pattern_round_brackets, replace_round_brackets, _text)

        return _text

    # TODO: add "end" parameter
    def get_toc(self, attrs, begin, edit):

        # from MarkdownPreview
        def slugify(value, separator):
            """ Slugify a string, to make it URL friendly. """
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
            value = re.sub('[^\w\s-]', '', value.decode('ascii')).strip().lower()
            return re.sub('[%s\s]+' % separator, separator, value)

        # from MarkdownPreview
        def postprocess_inject_header_id(html):
            """ Insert header ids when no anchors are present """
            unique = {}

            def header_to_id(text):
                if text is None:
                    return ''
                # Strip html tags and lower
                id = RE_TAGS.sub('', text).lower()
                # Remove non word characters or non spaces and dashes
                # Then convert spaces to dashes
                id = RE_WORD.sub('', id).replace(' ', '-')
                # Encode anything that needs to be
                return quote(id)

            def inject_id(m):
                id = header_to_id(m.group('text'))
                if id == '':
                    return m.group(0)
                # Append a dash and number for uniqueness if needed
                value = unique.get(id, None)
                if value is None:
                    unique[id] = 1
                else:
                    unique[id] += 1
                    id += "-%d" % value
                return m.group('open')[:-1] + (' id="%s">' % id) + m.group('text') + m.group('close')

            RE_TAGS = re.compile(r'''</?[^>]*>''')
            RE_WORD = re.compile(r'''[^\w\- ]''')
            RE_HEADER = re.compile(r'''(?P<open><h([1-6])>)(?P<text>.*?)(?P<close></h\2>)''', re.DOTALL)

            return RE_HEADER.sub(inject_id, html)

        def heading_to_id(heading):
            if heading is None:
                return ''
            if attrs['markdown_preview'] == 'github':
                _h1 = postprocess_inject_header_id('<h1>%s</h1>' % heading)
                pattern = r'<h1 id="(.*)">.*</h1>'
                matchs = re.finditer(pattern, _h1)
                for match in matchs:
                    return match.groups()[0]
            elif attrs['markdown_preview'] == 'markdown':
                return slugify(heading, '-')
            else:
                if strtobool(attrs['lowercase_only_ascii']):
                    # only ascii
                    _id = ''.join(chr(ord(x)+('A'<=x<='Z')*32) for x in heading)
                else:
                    _id = heading.lower()
                return replace_strings_in_id(_id)

        def replace_strings_in_id(_str):
            replacements = self.get_setting('id_replacements')
            for _key in replacements:
                _substitute = _key
                _targets = replacements[_key]
                for _target in _targets:
                    _str = _str.replace(_target, _substitute)
            return _str


        # Search headings in docment
        pattern_hash = "^#+?[^#]"
        headings = self.view.find_all(
            "%s|%s" % (pattern_h1_h2_equal_dash, pattern_hash))

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
        items = format(items)

        # Depth limit  ------------------
        _depth = int(attrs['depth'])
        if 0 < _depth:
            items = list(filter((lambda i: i[0] <= _depth), items))

        # Create TOC  ------------------
        toc = ''
        _ids = []
        level_counters = [0]
        ignore_image = strtobool(attrs['ignore_image'])
        list_bullets = attrs['list_bullets']

        for item in items:
            _id = None
            _indent = item[0] - 1
            _text = item[1]
            if ignore_image:
                _text = pattern_image.sub('', _text) # remove markdown image
            _list_bullet = list_bullets[_indent%len(list_bullets)]
            _text = pattern_tag.sub('', _text) # remove html tags
            _text = _text.strip() # remove start and end spaces
            # Ignore links: e.g. '[link](http://sample.com/)' -> 'link'
            self.log('+++')
            self.log(_text)
            # _text = pattern_link.sub('\\1\\2', _text)
            self.log(_text)
            # Add indent
            for i in range(_indent):
                _prefix = attrs['indent']
                # Support escaped characters like '\t'
                _prefix = _prefix.encode().decode('unicode-escape')
                toc += _prefix

            # Reference-style links: e.g. '# heading [my-anchor]'
            list_reference_link = list(pattern_reference_link.finditer(_text))

            # Markdown-Extra special attribute style: e.g. '# heading {#my-anchor}'
            match_ex_id = pattern_ex_id.search(_text)

            if len(list_reference_link):
                self.log('@1')
                match = list_reference_link[-1]
                _text = _text[0:match.start()].replace('[','').replace(']','').rstrip()
                _id = match.group().replace('[','').replace(']','')
            elif match_ex_id:
                self.log('@2')
                _text = _text[0:match_ex_id.start()].rstrip()
                _id = match_ex_id.group().replace('{#','').replace('}','')
            elif strtobool(attrs['autolink']):
                self.log('@3')
                _id = heading_to_id(_text)
                if strtobool(attrs['uri_encoding']):
                    _id = quote(_id)

                _ids.append(_id)
                n = _ids.count(_id)
                if 1 < n:
                    _id += '-' + str(n-1)

            if attrs['style'] == 'unordered':
                list_prefix = _list_bullet+' '
            elif attrs['style'] == 'ordered':
                list_prefix = '1. '

            # escape brackets
            _text = self.escape_brackets(_text)

            if _id == None:
                toc += list_prefix + _text + '\n'
            elif attrs['bracket'] == 'round':
                toc += list_prefix + '[' + _text + '](#' + _id + ')\n'
            else:
                toc += list_prefix + '[' + _text + '][' + _id + ']\n'

            item.append(_id)

        self.update_anchors(edit, items, strtobool(attrs['autoanchor']))

        return toc

    def update_anchors(self, edit, items, autoanchor):
        """Inserts, updates or deletes a link anchor in the line before each header."""
        v = self.view
        # Iterate in reverse so that inserts don't affect the position
        for item in reversed(items):
            anchor_region = v.line(item[2] - 1)  # -1 to get to previous line
            is_update = pattern_anchor.match(v.substr(anchor_region))
            if autoanchor:
                if is_update:
                    new_anchor = '<a name="{0}"></a>'.format(item[3])
                    v.replace(edit, anchor_region, new_anchor)
                else:
                    new_anchor = '\n<a name="{0}"></a>'.format(item[3])
                    v.insert(edit, anchor_region.end(), new_anchor)

            else:
                if is_update:
                    v.erase(edit, sublime.Region(anchor_region.begin(), anchor_region.end() + 1))

    def get_setting(self, attr):
        settings = sublime.load_settings('MarkdownTOC.sublime-settings')
        return settings.get(attr)

    def get_settings(self):
        """return dict of settings"""
        return {
            "autoanchor":           self.get_setting('default_autoanchor'),
            "autolink":             self.get_setting('default_autolink'),
            "bracket":              self.get_setting('default_bracket'),
            "depth":                self.get_setting('default_depth'),
            "ignore_image":         self.get_setting('default_ignore_image'),
            "indent":               self.get_setting('default_indent'),
            "list_bullets":         self.get_setting('default_list_bullets'),
            "lowercase_only_ascii": self.get_setting('default_lowercase_only_ascii'),
            "style":                self.get_setting('default_style'),
            "uri_encoding":         self.get_setting('default_uri_encoding'),
            "markdown_preview":     self.get_setting('default_markdown_preview')
        }

    def get_attibutes_from(self, tag_str):
        """return dict of settings from tag_str"""

        tag_str_html = pattern_toc_tag_start.sub("<", tag_str)
        tag_str_html = pattern_toc_tag_start.sub(">", tag_str_html)

        soup = BeautifulSoup(tag_str_html, "html.parser")

        return soup.find('markdowntoc').attrs

    def remove_items_in_codeblock(self, items):

        codeblocks = self.view.find_all("^\s*`{3,}[^`]*$")
        codeblockAreas = [] # [[area_begin, area_end], ..]
        i = 0
        while i < len(codeblocks)-1:
            area_begin = codeblocks[i].begin()
            area_end   = codeblocks[i+1].begin()
            if area_begin and area_end:
                codeblockAreas.append([area_begin, area_end])
            i += 2

        items = [h for h in items if is_out_of_areas(h.begin(), codeblockAreas)]
        return items

    def log(self, arg):
        if self.get_setting('logging') == True:
            arg = str(arg)
            sublime.status_message(arg)
            pp.pprint(arg)
    def error(self, arg):
        arg = str(arg)
        sublime.status_message(arg)
        pp.pprint(arg)

def is_out_of_areas(num, areas):
    for area in areas:
        if area[0] < num and num < area[1]:
            return False
    return True

def format(items):
    headings = []
    for item in items:
        headings.append(item[0])
    # --------------------------

    # minimize diff between headings -----
    _depths = list(set(headings)) # sort and unique
    # replace with depth rank
    for i, item in enumerate(headings):
        headings[i] = _depths.index(headings[i])+1
    # ----- /minimize diff between headings

    # --------------------------
    for i, item in enumerate(items):
        item[0] = headings[i]
    return items

def strtobool(val):
    """pick out from 'distutils.util' module"""
    if isinstance(val, str):
        val = val.lower()
        if val in ('y', 'yes', 't', 'true', 'on', '1'):
            return 1
        elif val in ('n', 'no', 'f', 'false', 'off', '0'):
            return 0
        else:
            raise ValueError("invalid truth value %r" % (val,))
    else:
        return bool(val)


# Search and refresh if it's exist


class MarkdowntocUpdate(MarkdowntocInsert):

    def run(self, edit):
        MarkdowntocInsert.find_tag_and_insert(self, edit)


class AutoRunner(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        # limit scope
        root, ext = os.path.splitext(view.file_name())
        ext = ext.lower()
        if ext in [".md", ".markdown", ".mdown", ".mdwn", ".mkdn", ".mkd", ".mark"]:
            view.run_command('markdowntoc_update')
