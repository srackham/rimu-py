import re

from rimu import replacements


def test_init():
    replacements.init()
    assert len(replacements.defs) == len(replacements.DEFAULT_DEFS)
    assert replacements.defs is not replacements.DEFAULT_DEFS
    assert replacements.defs[0] is not replacements.DEFAULT_DEFS[0]
    assert replacements.defs[0].replacement == replacements.DEFAULT_DEFS[0].replacement


def test_getDefinition():
    replacements.init()
    assert len(replacements.defs) == len(replacements.DEFAULT_DEFS)
    assert replacements.getDefinition(r'\\?<image:([^\s|]+?)>') is not None
    assert replacements.getDefinition(r'X') is None


def test_setDefinition():
    replacements.init()
    replacements.setDefinition(r'\\?<image:([^\s|]+?)>', '', 'foo')
    assert len(replacements.defs) == len(replacements.DEFAULT_DEFS)
    d = replacements.getDefinition(r'\\?<image:([^\s|]+?)>')
    assert d.replacement == 'foo'
    assert d.match.flags & re.IGNORECASE == 0
    assert d.match.flags & re.MULTILINE == 0
    replacements.setDefinition(r'bar', 'mi', 'foo')
    assert len(replacements.defs) == len(replacements.DEFAULT_DEFS) + 1
    d = replacements.defs[-1]
    assert d.match.pattern == 'bar'
    assert d.replacement == 'foo'
    assert d.match.flags & re.IGNORECASE != 0
    assert d.match.flags & re.MULTILINE != 0
