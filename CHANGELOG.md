This log contains Python specific changes, the [full change
log](https://srackham.github.io/rimu/changelog.html) is on the Rimu website.

## 11.4.2
- Updated the build environment from Python 3.8 to Python 3.10 (the rimu-py package itself remains compatible with Python 3.8 and up).

## 11.4.1
- Moved the development environment from a Docker container to a Conda virtual environment (this eliminates the need for Docker and having to develop remotely in a Docker container).

## 11.4.0
- Added GFM (GitHub Flavored Markdown) multiline blockquote delimited block syntax.

## 11.3.0
- Added `^[caption](url)` link syntax which opens the link in a new browser tab.
- Added [`important`, `note`, `tip` and `warning`]({tips}#important-note-tip-and-warning-styles)
  admonition classes to [rimuc]({reference}#rimuc-command) styled outputs.

## 11.1.8
- Updates ported from [Rimu
7 JavaScript 11.1.8](https://srackham.github.io/rimu/changelog.html).

## 11.1.7
- Updates ported from [Rimu
7 JavaScript 11.1.7](https://srackham.github.io/rimu/changelog.html).

## 11.1.6
- Initial release of the Rimu Python port.