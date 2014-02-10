import sublime, sublime_plugin, re, os.path

pattern_anchor = re.compile(r'\[.*?\]')
pattern_endspace = re.compile(r' *?\z')

TOCTAG_START = "<!-- MarkdownTOC -->"
TOCTAG_END   = "<!-- /MarkdownTOC -->"

class MarkdowntocInsert(sublime_plugin.TextCommand):

  def run(self, edit):

    if not self.find_tag_and_insert(edit):
      sels = self.view.sel()
      for sel in sels:
        # add TOCTAG
        toc  = TOCTAG_START+"\n"
        toc += "\n"
        toc += self.get_TOC(sel.end())
        toc += "\n"
        toc += TOCTAG_END+"\n"

        self.view.insert(edit, sel.begin(), toc)


  # Search MarkdownTOC comments in document
  def find_tag_and_insert(self,edit):
    sublime.status_message('fint TOC tags and refresh its content')
    
    extractions = []
    toc_starts = self.view.find_all("^<!-- MarkdownTOC( | depth=([0-9]+) )-->\n",sublime.IGNORECASE,'$2',extractions)
    depth = 0
    if 0 < len(extractions) and str(extractions[0])!='':
      depth = int(extractions[0])

    for toc_start in toc_starts:
      if 0 < len(toc_start):
        toc_end = self.view.find("^"+TOCTAG_END+"\n",toc_start.end())
        if toc_end:
          toc = self.get_TOC(depth, toc_end.end())
          tocRegion = sublime.Region(toc_start.end(),toc_end.begin())

          self.view.replace(edit, tocRegion, "\n"+toc+"\n")
          sublime.status_message('find TOC-tags and refresh')
          return True
    # self.view.status_message('no TOC-tags')
    return False

  # TODO: add "end" parameter
  def get_TOC(self, depth=0, begin=0):

    # Search headings in docment
    if depth==0:
      headings = self.view.find_all("^#+? ")
    else:
      headings = self.view.find_all("^#{1,"+str(depth)+"}? ")

    items = [] # [[headingNum,text],...]
    for heading in headings:
      if begin < heading.end():
        heading_text = self.view.substr(sublime.Region(heading.end(),self.view.line(heading).end()))
        heading_num = heading.size()-1
        items.append([heading_num,heading_text])



    # Shape TOC  ------------------
    items = format(items)


    # Create TOC  ------------------
    toc = ''
    for item in items:
      heading_num = item[0] - 1
      heading_text = item[1].rstrip()

      # add indent by heading_num
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

def format(items):
  headings = []
  for item in items:
    headings.append(item[0])
  # ----------

  # set root to 1
  min_heading = min(headings)
  if 1<min_heading:
    for i,item in enumerate(headings):
      headings[i] -= min_heading-1
  headings[0] = 1 # first item must be 1

  # minimize "jump width"
  for i,item in enumerate(headings):
    if 0<i and 1<item-headings[i-1]:
      before = headings[i]
      after = headings[i-1]+1
      headings[i] = after
      for n in range(i+1,len(headings)):
        if(headings[n]==before):
          headings[n] = after
        else:
          break

  # ----------
  for i,item in enumerate(items):
    item[0] = headings[i]
  return items

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
