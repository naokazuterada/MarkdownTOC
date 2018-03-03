from .markdowntoc_insert import MarkdowntocInsert

class MarkdowntocUpdate(MarkdowntocInsert):

    def run(self, edit):
        MarkdowntocInsert.find_tag_and_insert(self, edit)