import re
import unicodedata
from urllib.parse import quote

from .base import Base

class Id(Base):

    def __init__(self, id_replacements, markdown_preview, lowercase, lowercase_only_ascii):
        super().__init__()
        self.id_replacements = id_replacements
        self.markdown_preview = markdown_preview
        self.lowercase = lowercase
        self.lowercase_only_ascii = lowercase_only_ascii

    def heading_to_id(self, heading):
        if heading is None:
            return ''
        if self.markdown_preview == 'github':
            _h1 = self.postprocess_inject_header_id('<h1>%s</h1>' % heading)
            pattern = r'<h1 id="(.*)">.*</h1>'
            matchs = re.finditer(pattern, _h1)
            for match in matchs:
                return match.groups()[0]
        elif self.markdown_preview == 'markdown':
            return self.slugify(heading, '-')
        else:
            if not self.lowercase:
                _id = heading
            elif self.lowercase_only_ascii:
                # only ascii
                _id = ''.join(chr(ord(x) + ('A' <= x <= 'Z') * 32)
                              for x in heading)
            else:
                _id = heading.lower()
            return self.replace_strings_in_id(_id)

    def replace_strings_in_id(self, _str):
        for group in self.id_replacements:
            _str = re.sub(group['pattern'], group['replacement'], _str)
        return _str

    # from MarkdownPreview
    def slugify(self, value, separator):
        """ Slugify a string, to make it URL friendly. """
        value = unicodedata.normalize(
            'NFKD', value).encode(
            'ascii', 'ignore')
        value = re.sub(
            '[^\w\s-]',
            '',
            value.decode('ascii')).strip().lower()
        return re.sub('[%s\s]+' % separator, separator, value)

    # from MarkdownPreview
    def postprocess_inject_header_id(self, html):
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
            return m.group('open')[:-1] + (' id="%s">' %
                                           id) + m.group('text') + m.group('close')

        RE_TAGS = re.compile(r'''</?[^>]*>''')
        RE_WORD = re.compile(r'''[^\w\- ]''')
        RE_HEADER = re.compile(
            r'''(?P<open><h([1-6])>)(?P<text>.*?)(?P<close></h\2>)''', re.DOTALL)

        return RE_HEADER.sub(inject_id, html)