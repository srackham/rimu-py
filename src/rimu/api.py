from rimu import options, quotes, replacements


def init():
    options.init()
    quotes.init()
    replacements.init()


def render(source):
    # TODO
    return '<p>'+source+'</p>'
