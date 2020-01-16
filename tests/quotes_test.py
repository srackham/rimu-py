from rimu import quotes


def test_init():
    quotes.init()
    assert len(quotes.defs) == len(quotes.DEFAULT_DEFS)
    assert quotes.defs is not quotes.DEFAULT_DEFS
    assert quotes.defs[0] is not quotes.DEFAULT_DEFS[0]
    assert quotes.defs[0].quote == quotes.DEFAULT_DEFS[0].quote


def test_getDefinition():
    quotes.init()
    assert len(quotes.defs) == len(quotes.DEFAULT_DEFS)
    assert quotes.getDefinition('*') is not None
    assert quotes.getDefinition('X') is None


def test_setDefinition():
    quotes.init()

    quotes.setDefinition(quotes.Def(
        quote="*", openTag="<strong>", closeTag="</strong>", spans=True))
    assert len(quotes.defs) == len(quotes.DEFAULT_DEFS)
    d = quotes.getDefinition('*')
    assert d.openTag == '<strong>'

    quotes.setDefinition(
        quotes.Def(quote="x", openTag="<del>", closeTag="</del>", spans=True))
    assert len(quotes.defs) == len(quotes.DEFAULT_DEFS) + 1
    d = quotes.getDefinition('x')
    assert d.openTag == '<del>'
    assert quotes.defs[-1].openTag == '<del>'

    quotes.setDefinition(
        quotes.Def(quote="xx", openTag="<u>", closeTag="</u>", spans=True))
    assert len(quotes.defs) == len(quotes.DEFAULT_DEFS) + 2
    d = quotes.getDefinition('xx')
    assert d.openTag == '<u>'
    assert quotes.defs[0].openTag == '<u>'


def test_unescape():
    quotes.init()
    assert quotes.unescape(r'\* \~~ \x') == r'* ~~ \x'
