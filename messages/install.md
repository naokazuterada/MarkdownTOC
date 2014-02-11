# MarkdownTOC

This plugin search headings in document and insert TOC(Table Of Contents) to it.

## Feature

- Insert Table of Contents depending on headings in document
- TOC reflects contents from below its position or cursor (when you select "Insert TOC" menu)
- Auto linking when heading has anchor
- Refresh contents when file is saving
- [Control TOC depth in its comment tags][depth-control]

## Using

1. Open Markdown files.
2. Move cursor to position where you want to insert TOC.
3. Tools > MarkdownTOC > Insert TOC
4. TOC has inserted into document!
5. Update contents and save...
6. TOC has been updated.

***Don't remove the comment tags if you want to update every time saving.***


## Depth control [depth-control]

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
