# MarkdownTOC Plugin for Sublime Text

This plugin search headings in document and insert TOC(Table Of Contents) to it.

![](./demo.gif)

## Installing

With Package Control:


1. Run “Package Control: Install Package” command, find and install `MarkdownTOC` plugin.
2. Restart ST.

> [Package Control](http://wbond.net/sublime_packages/package_control)


With Git:

for SublimeText 2 (Mac)
```sh
git clone git@github.com:naokazuterada/MarkdownTOC.git ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/MarkdownTOC
```

for SublimeText 3 (Mac)
```sh
git clone git@github.com:naokazuterada/MarkdownTOC.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/MarkdownTOC
```

Without any dependencies:

1. [Download zip](https://github.com/naokazuterada/MarkdownTOC/archive/master.zip) and expand it.
2. Open ST's "Packges" directory (Sublime Text > Preference > Browse Packages...).
3. Move "MarkdownTOC" directory into "Packages" directory.


## Sample

```md

# Heading 0

Headings before MarkdownTOC tags will be ignored.

<!-- MarkdownTOC depth=0 -->

- Heading 1
  - Heading 2
    - Heading 3
- [Heading with anchor](#with-anchor)

<!-- /MarkdownTOC -->


# Heading 1

...

## Heading 2

...

### Heading 3

...

# Heading with anchor [with-anchor]

...
```
## Using

1. Open Markdown files.
2. Move cursor to position where you want to insert TOC.
3. Tools > MarkdownTOC > Insert TOC
4. TOC has inserted into document!
5. Update contents and save...
6. TOC has been updated.

***Don't remove the comment tags if you want to update every time saving.***

## Feature

- Insert Table of Contents depending on headings in document
- TOC reflects contents from below its position or cursor (when you select "Insert TOC" menu)
- Auto linking when heading has anchor
- Refresh contents when file is saving
- Depth control


### Depth control

You can control TOC depth in its comment tags.

```
<!-- MarkdownTOC depth=2 -->

- foo
  - bar
  - buz
- qux

<!-- /MarkdownTOC -->
```
```
<!-- MarkdownTOC depth=3 -->

- foo
  - bar
    - qux
    - quux
  - buz
- qux

<!-- /MarkdownTOC -->
```

You can also set default depth in Settings.

Preference > Package Settings > MarkdownTOC > Settings - User

```
{
  "default_depth": 0
}
```

`depth=0` means no limit
