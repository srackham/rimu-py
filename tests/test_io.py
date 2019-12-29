import re
from rimu import io


def test_Reader():
    reader = io.Reader('')
    assert reader.eof() == False
    assert len(reader.lines) == 1
    assert reader.cursor == ''
    reader.next()
    assert reader.eof() == True

    reader = io.Reader('Hello\nWorld!')
    assert len(reader.lines) == 2
    assert reader.cursor == 'Hello'
    reader.next()
    assert reader.cursor == 'World!'
    assert reader.eof() == False
    reader.next()
    assert reader.eof() == True

    reader = io.Reader('\n\nHello')
    assert len(reader.lines) == 3
    reader.skipBlankLines()
    assert reader.cursor == 'Hello'
    assert reader.eof() == False
    reader.next()
    assert reader.eof() == True

    reader = io.Reader('Hello\n*\nWorld!\nHello\n< Goodbye >')
    assert len(reader.lines) == 5
    lines = reader.readTo(re.compile(r'\*'))
    assert len(lines) == 1
    assert lines[0] == 'Hello'
    assert reader.eof() == False
    lines = reader.readTo(re.compile(r'^<(.*)>$'))
    assert len(lines) == 3
    assert lines[2] == ' Goodbye '
    assert reader.eof() == True

    reader = io.Reader('\n\nHello\nWorld!')
    assert len(reader.lines) == 4
    reader.skipBlankLines()
    lines = reader.readTo(re.compile(r'^$'))
    assert len(lines) == 2
    assert lines[1] == 'World!'
    assert reader.eof() == True


def test_Writer():
    writer = io.Writer()
    writer.write('Hello')
    assert writer.buffer[0] == 'Hello'
    writer.write('World!')
    assert writer.buffer[1] == 'World!'
    assert writer.toString() == 'HelloWorld!'
