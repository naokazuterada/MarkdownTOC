# MarkdownTOC Plugin for Sublime Text

Sublime Text plugin for generating a Table of Contents (TOC) in a Markdown document.

| Linux & OSX | Windows     |
|:------------|:------------|
| [![Build Status](https://travis-ci.org/naokazuterada/MarkdownTOC.svg?branch=master)](https://travis-ci.org/naokazuterada/MarkdownTOC) | [![Build status](https://ci.appveyor.com/api/projects/status/vxj9jbihlrwfa6ui/branch/master?svg=true)](https://ci.appveyor.com/project/naokazuterada/markdowntoc/branch/master) |

![](./demo.gif)

## Table of Contents

<!-- MarkdownTOC bracket=round -->

- [Quick-start](#quick-start)
- [Features](#features)
  - [Insertion of TOC based on headings in document](#insertion-of-toc-based-on-headings-in-document)
  - [Automatic refresh of TOC when Markdown document is saved](#automatic-refresh-of-toc-when-markdown-document-is-saved)
  - [Auto anchor when heading has anchor defined](#auto-anchor-when-heading-has-anchor-defined)
  - [Auto linking](#auto-linking)
    - [Replacements for id characters](#replacements-for-id-characters)
  - [Control of depth listed in TOC](#control-of-depth-listed-in-toc)
  - [Ordered or unordered style for elements](#ordered-or-unordered-style-for-elements)
  - [Indentation prefix](#indentation-prefix)
- [Usage](#usage)
- [Attributes](#attributes)
- [Installation](#installation)
  - [Using Package Control](#using-package-control)
  - [From Git](#from-git)
    - [SublimeText 2 \(Mac\)](#sublimetext-2-mac)
    - [SublimeText 3 \(Mac\)](#sublimetext-3-mac)
  - [From downloadable file](#from-downloadable-file)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [References](#references)

<!-- /MarkdownTOC -->

## Quick-start

1. Open your [Markdown][markdowns] file
2. Place cursor to position where you want to insert the TOC
3. Press `<ctrl>` + `<shift>` + `p`
4. TOC is inserted in document
5. Save the document and you are done

## Features

- Insertion of TOC based on headings in document
- Automatic refresh of TOC when Markdown document is saved
- Auto link when heading has anchor defined
- Auto linking for _clickable_ TOC
- Control of depth listed in TOC
- Ordered or unordered style for elements
- Indentation prefix

### Insertion of TOC based on headings in document

When you have completed [installation](#installation) of the plugin, you can insert an automatically generated TOC based on you Markdown headings. See the [Usage](#usage) for details on how to get started.

For the following sample Markdown document:

```

# Heading 0

...

# Heading 1

...

## Heading 2

...

## Heading 3

...

# Heading with anchor [with-anchor]

...
```

The plugin will render:

```
# Heading 0

Headings before MarkdownTOC tags will be ignored.

TOC tag is able to having attributes.

<!-- MarkdownTOC autolink=true bracket=round -->

- [Heading 1](#heading-1)
  - [Heading 2](#heading-2)
  - [Heading 3](#heading-3)
- [Heading with anchor](#with-anchor)

<!-- /MarkdownTOC -->


# Heading 1

...

## Heading 2

...

## Heading 3

...

# Heading with anchor [with-anchor]

...
```

As you can read from the sample above:

1. Headings above the `MarkdownTOC` tag placement are ignored, only the rest of the document is considered in scope
2. TOC tags can overwrite default attributes using local settings (see: [Configuration](#configuration))
3. Heading can have anchors automatically linked (see: [auto anchor](#auto-anchor))

### Automatic refresh of TOC when Markdown document is saved

If we edit the Markdown document some more and add an additional heading:

```
## Heading 4
```

When we save the document, the TOC is automatically updated.

```
<!-- MarkdownTOC autolink=true bracket=round -->

- [Heading 1](#heading-1)
  - [Heading 2](#heading-2)
  - [Heading 3](#heading-3)
  - [Heading 4](#heading-4)  
- [Heading with anchor](#with-anchor)

<!-- /MarkdownTOC -->
```

### Auto anchor when heading has anchor defined

If you specify and anchor for your heading:

```
# Heading with anchor [with-anchor]
```

The TOC generation can be specified to respect this and a TOC element of the following format is generated:

```
- [Heading with anchor](#with-anchor)
```

Please note that the default for the attribute: [autoanchor](#autoanchor) is `false`.

You can add an HTML anchor (`<a name="xxx"></a>`) before the heading automaticaly.

```
<!-- MarkdownTOC autolink=true autoanchor=true bracket=round -->

- [Changelog](#changelog)
- [Glossary](#glossary)
- [API Specification](#api-specification)

<!-- /MarkdownTOC -->

<a name="changelog"></a>
# Changelog
Lorem ipsum...

<a name="glossary"></a>
# Glossary
Lorem ipsum...

<a name="api-specification"></a>
# API Specification
Lorem ipsum...
```

You can also set this in sublime-settings with key `default_autoanchor`.


### Auto linking

The plugin can be specified to auto link heading so you get a TOC with _clickable_ hyperlink elements.  

The following sample document:

```
# Heading 1

...

## Heading 2

...

## Heading 3
```

With `autolink` set to `true` will render the following:

```
<!-- MarkdownTOC autolink=true bracket=round -->

- [Heading 1](#heading-1)
  - [Heading 2](#heading-2)
  - [Heading 3](#heading-3)
  - [Heading 4](#heading-4)  
- [Heading with anchor](#with-anchor)

<!-- /MarkdownTOC -->
```

The auto link markup style can be one of:

- `square`, the default
- `round`, the style supported on Github

Please note that the default for the attribute: [autolink](#autolink) is `false`.

```
<!-- MarkdownTOC autolink=false -->

- MarkdownTOC Plugin for Sublime Text
  - Feature
  - Feature
  - Feature

<!-- /MarkdownTOC -->
```
```
<!-- MarkdownTOC autolink=true -->

- [MarkdownTOC Plugin for Sublime Text](#markdowntoc-plugin-for-sublime-text)
  - [Feature](#feature)
  - [Feature](#feature-1)
  - [Feature](#feature-2)

<!-- /MarkdownTOC -->
```

You can also set this in sublime-settings with key `default_autolink`.

**square**: according to ["Reference-style links"](http://daringfireball.net/projects/markdown/syntax#link).
```
<!-- MarkdownTOC bracket=square -->

- [Heading][heading]

<!-- /MarkdownTOC -->
```

**round**: according to Github style.
```
<!-- MarkdownTOC bracket=round -->

- [Heading](#heading)

<!-- /MarkdownTOC -->
```

You can also set this in sublime-settings with key `default_bracket`.

#### Replacements for id characters

You can also edit replacements when using 'Auto link' feature like following settings.

`MarkdownTOC.sublime-settings`

```json
{
  "id_replacements": {
    "-": " ",
    "" : ["!","#","$","&","'","(",")","*","+",",","/",":",";","=","?","@","[","]","`","\"", ".","<",">","{","}","™","®","©"]
  }
}
```

example:

```
# Super Product™
```

This heading changes to link with following id.

```
#super-product
```

- The value character(s) will be replaced to the key character.
- Replace sequence will execute from top to bottom.

### Control of depth listed in TOC

```
# Heading 1

...

## Heading 2

...

### Heading 3

...

#### Heading 2
```

With default depth:

```
<!-- MarkdownTOC -->

- [Heading 1]
  - [Heading 2]

<!-- /MarkdownTOC -->
```

With depth set to 4:

```
<!-- MarkdownTOC depth=4 -->

- [Heading 1]
  - [Heading 2]
    - [Heading 3]
      - [Heading 4]

<!-- /MarkdownTOC -->
```

Please note that the default for the attribute: [depth](#depth) is `2` and the maximum is `6` according to the [Markdown specification]. Specifying `0` means indefinite and means all heading sizes will be included.

You can also set this in sublime-settings with key `default_depth`.

### Ordered or unordered style for elements

The plugin supports two styles of TOC element listing: unordered and ordered.

```
# Heading 1

...

## Heading 2

...

## Heading 3
```

Unordered:

```
<!-- MarkdownTOC style=unordered -->

- foo
  - bar
    - qux
    - quux
  - buz
- qux

<!-- /MarkdownTOC -->
```

Ordered:

```
<!-- MarkdownTOC style=ordered -->

1. foo
  1. bar
    1. qux
    1. quux
  1. buz
1. qux

<!-- /MarkdownTOC -->
```

Please note that the default for the attribute: [style](#style) is `unordered`.

You can also set this in sublime-settings with key `default_style`.

### Indentation prefix

The indentation prefix is a specification of the string used to ident the TOC elements.

An _ugly_ but demonstrative example could be to use an emoji.

```
<!-- MarkdownTOC autolink=true bracket=round indent=:point_right: -->

- [Heading 1](#heading-1)
:point_right:- [Heading 2](#heading-2)
:point_right:- [Heading 3](#heading-3)
:point_right:- [Heading 4](#heading-4)  

<!-- /MarkdownTOC -->
```

Rendering as follows:

- [Heading 1](#heading-1)
:point_right:- [Heading 2](#heading-2)
:point_right:- [Heading 3](#heading-3)
:point_right:- [Heading 4](#heading-4)  

Please note that the default for the attribute: [indent](#indent) is `'\t'`.

You can set indent prefix.

```
4 spaces
<!-- MarkdownTOC indent="    " -->

- foo
    - bar
        - buz

<!-- /MarkdownTOC -->
```

You can also set this in sublime-settings with key `default_indent`.

## Usage

1. Open your Markdown file
2. Move cursor to position where you want to insert a TOC
3. Pick from menu: Tools > MarkdownTOC > Insert TOC
4. TOC is inserted in document
5. Update contents and save...
6. TOC has been updated.

***Don't remove the comment tags if you want to update every time saving.***

## Attributes

The following attributes can be used to control the generation of the TOC.

| attribute                | values                      | default      | key in settings     |
|:------------------------- |:--------------------------- |:------------- |:-------------------- |
| [autolink](#auto-link)    | `true`or`false`             | `false`       | `default_autolink`   |
| [bracket](#bracket)       | `square`or`round`           | `'square'`    | `default_bracket`    |
| [depth](#depth)           | uint (`0` means "no limit") | `2`           | `default_depth`      |
| [autoanchor](#autoanchor) | `true`or`false`             | `false`       | `default_autoanchor` |
| [style](#style)           | `ordered` or `unordered`    | `'unordered'` | `default_style`      |
| [indent](#indent)         | string                      | `'\t'`        | `default_indent`     |

You can define your own default values via package preferences, Sublime Texts way of letting user settings overwrite package defaults. Please see the [Section on Configuration](#Configuration).

## Installation

### Using Package Control

1. Run “Package Control: Install Package” command, find and install `MarkdownTOC` plugin.
2. Restart ST.

> [Package Control](http://wbond.net/sublime_packages/package_control)

### From Git

#### SublimeText 2 (Mac)

```sh
git clone git@github.com:naokazuterada/MarkdownTOC.git ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/MarkdownTOC
```

#### SublimeText 3 (Mac)

```sh
git clone git@github.com:naokazuterada/MarkdownTOC.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/MarkdownTOC
```

### From downloadable file

1. [Download zip](https://github.com/naokazuterada/MarkdownTOC/archive/master.zip) and expand it.
2. Open ST's "Packges" directory (Sublime Text > Preference > Browse Packages...).
3. Move "MarkdownTOC" directory into "Packages" directory.

## Configuration

You can set default values. Preference > Package Settings > MarkdownTOC > Settings - User

Pick: Sublime Text > Preferences > Package Settings > MarkdownTOC > Settings - User

Alternative you can create the file `~/Library/Application Support/Sublime Text 3/Packages/UserMarkdownTOC.sublime-settings`


`MarkdownTOC.sublime-settings`

```json
{
  "default_autolink": false,
  "default_bracket": "square",
  "default_depth": 2,
  "default_autoanchor": false,
  "default_style": "unordered",
  "default_indent": "\t"
}
```

```
<!-- MarkdownTOC depth=2 autolink=true bracket=round autoanchor=true style=ordered indent="    " -->
```

## Contributing

Contributions are most welcome, please see the [guidelines on contributing](https://github.com/naokazuterada/MarkdownTOC/blob/master/CONTRIBUTING.md).

## License

[MIT](https://github.com/naokazuterada/MarkdownTOC/blob/master/LICENSE-MIT)

## Author

[Naokazu Terada](https://github.com/naokazuterada)

## References

- [Daring Fireballs Markdown Syntax Specification](http://daringfireball.net/projects/markdown/syntax)
- [Sublime Text][sublimetext]
- [Sublime Text: Package Control][packagecontrol]
- [Emoji cheatsheet](http://www.emoji-cheat-sheet.com/)
- [Github flavoured markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/)

[markdown][http://daringfireball.net/projects/markdown/syntax]
[sublimetext][http://www.sublimetext.com/]
[packagecontrol][http://wbond.net/sublime_packages/package_control]
