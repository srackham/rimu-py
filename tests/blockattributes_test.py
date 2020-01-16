from rimu import blockattributes as b
from rimu import options


def test_parse():
    options.init()
    b.init()
    success = b.parse('.foo bar #id "font-size: 16px;" [title="Hello!"]')
    assert success == True
    assert b.classes == 'foo bar'
    assert b.id == 'id'
    assert b.css == 'font-size: 16px;'
    assert b.attributes == 'title="Hello!"'


def test_injectHtmlAttributes():
    b.init()
    b.classes = 'foo bar'
    b.id = 'ID'
    b.css = 'font-size: 16px;'
    b.attributes = 'title="Hello!"'
    result = b.injectHtmlAttributes('<p class="do">')
    assert result == '<p id="id" style="font-size: 16px;" title="Hello!" class="foo bar do">'
    assert b.classes == ''
    assert b.css == ''
    assert b.attributes == ''


def test_slugify():
    b.init()
    assert b.slugify('-Foo bar  ') == 'foo-bar'
    b.ids.insert(0, 'foo-bar')
    assert b.slugify('Foo bar') == 'foo-bar-2'
