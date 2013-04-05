import sublime, sublime_plugin, re, os.path

pattern_anchor = re.compile(r'\[.*?\]')
pattern_endspace = re.compile(r' *?\z')

TOCTAG_START = "<!-- MarkdownTOC -->"
TOCTAG_END   = "<!-- /MarkdownTOC -->"

class MarkdowntocInsert(sublime_plugin.TextCommand):

  def run(self, edit):

    if not find_tag_and_insert(self,edit):

      # add TOCTAG
      toc = self.get_TOC()
      toc = TOCTAG_START+"\n"+toc
      toc = toc+TOCTAG_END+"\n"

      sels = self.view.sel()
      for sel in sels:
          self.view.insert(edit, sel.begin(), toc) 


  # Search MarkdownTOC comments in document
  def find_tag_and_insert(self,edit):
    toc = self.get_TOC()
    sublime.status_message('fint TOC tags and refresh its content')
    toc_starts = self.view.find_all("^"+TOCTAG_START+"\n")
    for toc_start in toc_starts:
      if 0 < len(toc_start):
        toc_end = self.view.find("^"+TOCTAG_END+"\n",toc_start.end())
        if toc_end:
          tocRegion = sublime.Region(toc_start.end(),toc_end.begin())
          self.view.replace(edit, tocRegion, toc) 
          sublime.status_message('fint TOC tags and refresh its content')
          return True
    # self.view.status_message('no TOC tags')
    return False

  def get_TOC(self):
    headings = self.view.find_all("^#*? ")
    
    # Search headings in docment ---
    items = [] # [headingNum,text]
    for heading in headings:
      text = self.view.substr(sublime.Region(heading.end(),self.view.line(heading).end()))
      heading_num = heading.size()-1
      items.append([heading_num,text])

    # Create TOC  ------------------
    toc = ''
    for item in items:
      heading_num = item[0]
      heading_text = item[1].rstrip()

      # add indent by heading_num
      heading_num -= 1
      for i in range(heading_num):
        toc += '\t'

      # Handling anchors
      matchObj = pattern_anchor.search(heading_text)
      if matchObj:
        only_text = heading_text[0:matchObj.start()]
        only_text = only_text.rstrip()
        toc += '- ['+only_text+']'+matchObj.group()+'\n'
      else:
        toc += '- '+heading_text+'\n'
    return toc


# Search and refresh if it's exist
class MarkdowntocUpdate(MarkdowntocInsert):
  def run(self, edit):
    MarkdowntocInsert.find_tag_and_insert(self,edit)


class AutoRunner(sublime_plugin.EventListener):
  def on_pre_save(self, view):
    # limit scope
    root, ext = os.path.splitext(view.file_name())
    if ext == ".md" or ext == ".markdown":
      view.run_command('markdowntoc_update')
