# MarkdownTOC Plugin for Sublime Text 2

This plugin search headings in document and insert TOC(Table Of Contents) to it.

## Feature

- Insert Table of Contents depending on headings in document
- TOC reflects contents from below its position or cursor (when you select "Insert TOC" menu)
- Auto linking when heading has anchor
- Refresh contents when file is saving

## Installing

With Package Control:


1. Run “Package Control: Install Package” command, find and install `MarkdownTOC` plugin.
2. Restart SublimeText.

> [Package Control](http://wbond.net/sublime_packages/package_control)


Use Git:

```sh
git clone git@github.com:naokazuterada/MarkdownTOC.git ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/MarkdownTOC
```

Don't use Git:

1. [Download zip](https://github.com/naokazuterada/MarkdownTOC/archive/master.zip)
2. Expand zip (appear "MarkdownTOC" folder)
3. Open "Packges" directory (Sublime Text 2 > Preference > Browse Packages...)
4. Move "MarkdownTOC" directory into "Packages" directory.


## Using

1. Open Markdown files.
2. Move cursor to position where you want to insert TOC.
3. Tools > MarkdownTOC > Insert TOC
4. TOC has inserted into document!
5. Update contents and save...
6. TOC has been updated.

***Don't remove the comment tags if you want to update every time saving.***
