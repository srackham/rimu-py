# from rimu import macros, options
from rimu import options
from rimu.macros import defs, init, getValue, setValue, render


def test_parse():
    init()
    options.init()
    assert len(defs) == 2
    setValue('x', '1')
    assert len(defs) == 3
    assert getValue('x') == '1'
    assert getValue('y') == None
    assert render(r'\{x} = {x}') == '{x} = 1'
    assert render(r'{--=} foobar') == ' foobar'
    assert render(r'{--!} foobar') == ''
    setValue('x?', '2')
    assert getValue('x') == '1'
    setValue('y', r'$1 $2')
    assert render(r'{y|foo|bar}') == 'foo bar'
