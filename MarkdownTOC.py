import sublime, sublime_plugin

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
    	heading_text = item[1]

    	# indent by heading_num
    	heading_num -= 1
    	for i in range(heading_num):
    		toc += '	'

    	toc += '- '+item[1]+'\n'

    # Insert TOC to selection
    sels = self.view.sel()
    for sel in sels:
    	self.view.insert(edit, sel.begin(), toc) 
