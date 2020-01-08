from rimu import lists, api, io


def test_render():
    api.init()

    input = '- Item 1'
    reader = io.Reader(input)
    writer = io.Writer()
    lists.render(reader, writer)
    assert writer.toString() == r'<ul><li>Item 1</li></ul>'

    input = 'Term 1:: Item 1'
    reader = io.Reader(input)
    writer = io.Writer()
    lists.render(reader, writer)
    assert writer.toString() == r'<dl><dt>Term 1</dt><dd>Item 1</dd></dl>'

    input = r'''- Item 1
""
Quoted
""
- Item 2
 . Nested 1'''
    reader = io.Reader(input)
    writer = io.Writer()
    lists.render(reader, writer)
    assert writer.toString() == r'''<ul><li>Item 1<blockquote><p>Quoted</p></blockquote>
</li><li>Item 2<ol><li>Nested 1</li></ol></li></ul>'''
