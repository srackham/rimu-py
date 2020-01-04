from rimu import options, quotes, replacements


def init() -> None:
    options.init()
    quotes.init()
    replacements.init()


def render(source: str) -> str:
    # TODO
    return '<p>'+source+'</p>'
