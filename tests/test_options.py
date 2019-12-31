from rimu import options
from rimu.options import RenderOptions


def test_init():
    assert options.safeMode == -1
    options.init()
    assert options.safeMode == 0
    assert options.htmlReplacement == '<mark>replaced HTML</mark>'
    assert options.callback == None


def test_isSafeModeNz():
    options.init()
    assert options.isSafeModeNz() == False
    options.safeMode = 1
    assert options.isSafeModeNz() == True


def test_skipMacroDefs():
    options.init()
    assert options.skipMacroDefs() == False
    options.safeMode = 1
    assert options.skipMacroDefs() == True
    options.safeMode = 1 + 8
    assert options.skipMacroDefs() == False


def test_skipBlockAttributes():
    options.init()
    assert options.skipBlockAttributes() == False
    options.safeMode = 1
    assert options.skipBlockAttributes() == False
    options.safeMode = 1 + 4
    assert options.skipBlockAttributes() == True


def test_updateFrom():
    options.init()
    options.updateFrom(RenderOptions(safeMode=1))
    assert options.safeMode == 1
    assert options.htmlReplacement == '<mark>replaced HTML</mark>'
    options.updateFrom(RenderOptions(htmlReplacement='foo'))
    assert options.safeMode == 1
    assert options.htmlReplacement == 'foo'


def test_setOption():
    options.init()
    # Illegal values do not update options.
    options.setOption('safeMode', 'ILLEGAL')
    assert options.safeMode == 0
    options.setOption('safeMode', '42')
    assert options.safeMode == 0
    options.setOption('safeMode', '1')
    options.setOption('reset', 'ILLEGAL')
    assert options.safeMode == 1
    # Reset clears options.
    options.setOption('reset', 'true')
    assert options.safeMode == 0


def test_htmlSafeModeFilter():
    options.init()
    assert options.htmlSafeModeFilter('foo') == 'foo'
    options.safeMode = 1
    assert options.htmlSafeModeFilter('foo') == ''
    options.safeMode = 2
    assert options.htmlSafeModeFilter('foo') == '<mark>replaced HTML</mark>'
    options.safeMode = 3
    assert options.htmlSafeModeFilter('<br>') == '&lt;br&gt;'
    options.safeMode = 0 + 4
    assert options.htmlSafeModeFilter('foo') == 'foo'
