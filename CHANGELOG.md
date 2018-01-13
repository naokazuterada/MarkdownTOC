Changes in MarkdownTOC
===========================

## 2.8.0

- Allow regular expressions in 'id_replacements' Ref: #113

## 2.7.1

- Drop BeautifulSoup dependency. Ref: #111
  Contribution by @ziembla

## 2.7.0

- Add `link_prefix` parameter. Ref: #54

## 2.6.0

- Add `remove_image` parameter. Ref: #43
- Add `lowercase` parameter. Ref: #40

## 2.5.0

- Add `Customizable list bullets` feature

## 2.4.1

- Fix problem that user's settings doesn't work. Ref: #100
- Fix problem that characters inside codeblock is also escaped. Ref: #64
  Contribution by Mathieu PATUREL ( @math2001 ). Ref: #101

## 2.4.0

- Support MarkdownPreview's anchoring

## 2.3.2

- Fix the way of import dependencies
- Add code coverage on redame

## 2.3.1

- Allow indentation of blockquates

## 2.3.0

- Add 'URI encoding' feature
- Change 'default_lowercase_only_ascii' default value ('false' to 'true') because it breaks link in Russian

## 2.2.1

- Improve heading detecting

## 2.2.0

- Add 'logging' option in 'Package Settings'

## 2.1.2

- Fix anchoring problem with '_'

## 2.1.1

- Improved ATX headings
    - Extra spaces processing in headings
    - Removing of closing sequence of # characters
- Allow not only chars but strings in id_replacement

## 2.1.0

- Add `lowercase_only_ascii` feature

## 2.0.0

- Enable HTML-like attribute style
- Remove compatibility to SublimeText2

## 1.8.0

- Enable to change indent prefix. ('Indent' feature)

## 1.7.1

- Fix issue about escaping brackets

## 1.7.0

- Add 'style' feature

## 1.6.1

- Fix issue about '===' or '---' headings


## 1.6.0

- Add 'Auto anchor' feature


## 1.5.0

- Add 'id_replacements' option in 'Package Settings'

## 1.4.0

- Change 'Auto link' syntax
- Implement defaults and override each TOCs
- Support MarkDown-Extra style to define ID
- Add 'Bracket' feature
- Bug fixes
  - Dealing with reference link in heading
  - Ignore links in heading
  - Ignore spaces in the end of heading

## 1.3.0

- Add 'Auto link' feature
- Bug fix: ignore headings and toc tags in codeblock
- Remove auto rewrite toc tag when 'depth' attr is not declared

## 1.2.2

- Ignore Horizontal Rules
- Support minor extentions

## 1.2.1

- Bug fixes

## 1.2.0

- Support '===' or '---' headings

## 1.1.0

- Add 'Controll Depth' feature

## 1.0.0

- Support for ST3.