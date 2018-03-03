import re
from .base import Base

class Id(Base):

    def __init__(self, attrs):
        self.attrs = attrs

    def heading_to_id(self, heading):
        if heading is None:
            return ''
        if self.attrs['markdown_preview'] == 'github':
            _h1 = postprocess_inject_header_id('<h1>%s</h1>' % heading)
            pattern = r'<h1 id="(.*)">.*</h1>'
            matchs = re.finditer(pattern, _h1)
            for match in matchs:
                return match.groups()[0]
        elif self.attrs['markdown_preview'] == 'markdown':
            return slugify(heading, '-')
        else:
            if not self.attrs['lowercase']:
                _id = heading
            elif self.attrs['lowercase_only_ascii']:
                # only ascii
                _id = ''.join(chr(ord(x) + ('A' <= x <= 'Z') * 32)
                              for x in heading)
            else:
                _id = heading.lower()
            return self.replace_strings_in_id(_id)

    def replace_strings_in_id(self, _str):
        for group in self.get_settings('id_replacements'):
            _str = re.sub(group['pattern'], group['replacement'], _str)
        return _str
