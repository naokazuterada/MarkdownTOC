import sublime, sublime_plugin, re

pattern_anchor = re.compile(r'\[.*?\]')
pattern_endspace = re.compile(r' *?\z')

class MarkdowntocCommand(sublime_plugin.TextCommand):

  def run(self, edit):

  	# Search headings in docment
    headings = self.view.find_all("^#*? ")
    
    items = [] # [headingNum,text]
    for heading in headings:
    	text = self.view.substr(sublime.Region(heading.end(),self.view.line(heading).end()))
    	heading_num = heading.size()-1
    	items.append([heading_num,text])

    # Create TOC
    toc = ''
    for item in items:
    	heading_num = item[0]
    	heading_text = item[1].rstrip()

    	# indent by heading_num
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

    # Insert TOC to selection
    sels = self.view.sel()
    for sel in sels:
    	self.view.insert(edit, sel.begin(), toc) 
