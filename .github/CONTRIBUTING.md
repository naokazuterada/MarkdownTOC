# Contributing

These are the guidelines for contributing to this repository.

## Issues

Please use the template for your type of issue.

- [Bug Report](https://github.com/naokazuterada/MarkdownTOC/issues/new)
- [Feature Request](https://github.com/naokazuterada/MarkdownTOC/issues/new?template=feature.md)
- [Question](https://github.com/naokazuterada/MarkdownTOC/issues/new?template=question.md)

### Way of operation

1. The maintainers will `Close` the issue or PR
    1. Not accepted feature request
        - Add the `wontfix` label
    2. Not clear or unresponsive
        - Not clear: Problem is not obvious or not reproducible.
        - Unresponsive: the author does not respond to inquiries within 3 weeks.

## Gitter

If you want more general support or to ask questions, please use [Gitter](https://gitter.im/naokazuterada/MarkdownTOC) chat system.

## Patches

Patches for fixes, features, and improvements are accepted via pull requests.

Pull requests should be based on the master branch, unless you want to contribute to an active branch for a specific topic.

### Coding Style

You should use [Black](https://github.com/psf/black) for automatic code formatting.

```
pip install black
black .
```

### Test

You should use unit-tests for SublimeText by using [UnitTesting](https://github.com/randy3k/UnitTesting) plugin.

1. Install the UnitTesting plugin
2. Comment out or rename your own `MarkdownTOC.sublime-settings` so individual settings are not used during testing
3. [Run tests](https://github.com/randy3k/UnitTesting-example#running-tests)
4. Send Pull Request when tests pass

All contributions are welcome

## Useful Tools

- [Gyazo](https://gyazo.com/en): Tool for making animated GIFs from screen captures. Use it for showing how the function works.

## Licensing and copyright

Please note that accepted contributions are included in the repository and hence under the same license as the repository contributed to.
