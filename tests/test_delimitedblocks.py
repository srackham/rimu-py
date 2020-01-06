from rimu import blockattributes, io, quotes, replacements
from rimu import delimitedblocks as b


def test_getDefinition():
    b.init()
    d = b.getDefinition('paragraph')
    assert d.openTag == '<p>'
    d = b.getDefinition('foo')
    assert d is None


def test_setDefinition():
    b.init()
    b.setDefinition('indented', '<foo>|</foo>')
    d = b.getDefinition('indented')
    assert d.openTag == '<foo>'
    assert d.closeTag == '</foo>'


def test_render():
    blockattributes.init()
    quotes.init()
    replacements.init()
    b.init()
    input = 'Test'
    reader = io.Reader(input)
    writer = io.Writer()

    b.render(reader, writer)
    assert writer.toString() == '<p>Test</p>'

    input = '  Indented'
    reader = io.Reader(input)
    writer = io.Writer()
    b.render(reader, writer)
    assert writer.toString() == '<pre><code>Indented</code></pre>'
