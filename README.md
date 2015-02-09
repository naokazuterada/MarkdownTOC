# MarkdownTOC Plugin for Sublime Text

This plugin search headings in document and insert TOC(Table Of Contents) to it.

![](./demo.gif)

## Feature

- Insert TOC depending on headings in document
- TOC reflects contents from below its position or cursor (when you select "Insert TOC" menu)
- Auto linking when heading has anchor
- Refresh contents when file is saving
- Depth control
- Auto link (useful on Github etc.)

## Sample

```
# Heading 0

Headings before MarkdownTOC tags will be ignored.

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

## Using

1. Open Markdown files.
2. Move cursor to position where you want to insert TOC.
3. Tools > MarkdownTOC > Insert TOC
4. TOC has inserted into document!
5. Update contents and save...
6. TOC has been updated.

***Don't remove the comment tags if you want to update every time saving.***

## Attributes

| attributes             | values                      | defaults    | keys in settings    |
|:---------------------- |:--------------------------- |:----------- |:------------------- |
| [autolink](#auto-link) | `true`or`false`             | `false`     | `default_autolink`  |
| [bracket](#bracket)    | `square`or`round`           | `square`    | `default_bracket`   |
| [depth](#depth)        | uint (`0` means "no limit") | `2`         | `default_depth`     |

You can set default values. Preference > Package Settings > MarkdownTOC > Settings - User

`MarkdownTOC.sublime-settings`

```json
{
  "default_autolink": false,
  "default_bracket": "square",
  "default_depth": 2
}
```

All attributes can be overridden in each TOC open tags like...

```
<!-- MarkdownTOC depth=2 autolink=true bracket=round  -->
```



### Auto link

This will be useful on Github.

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

#### Replecements for id charactors

You can also edit replecements when using 'Auto link' feature like following settings.

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

- The value charactor(s) will be replaced to the key charactor.
- Replece sequence will execute from top to bottom.


### Bracket

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


### Depth

You can control TOC depth.

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
