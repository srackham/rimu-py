from rimu import options
from rimu import quotes
from rimu import replacements


def init():
    options.init()
    quotes.init()
    replacements.init()


def render(source):
    # TODO
    return '<p>'+source+'</p>'
