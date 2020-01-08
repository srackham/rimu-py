from rimu import (blockattributes, delimitedblocks, macros, options, quotes,
                  replacements)


def init() -> None:
    blockattributes.init()
    options.init()
    delimitedblocks.init()
    macros.init()
    quotes.init()
    replacements.init()


def render(source: str) -> str:
    # TODO
    return '<p>'+source+'</p>'
