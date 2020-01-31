'''Basic rendering tests (full syntax tested in rimu_test.py).'''

import re

from rimu import options, quotes, replacements
from rimu.spans import Fragment, defrag, fragQuote, fragReplacements, render


def test_spans():
    options.init()
    quotes.init()
    replacements.init()

    input = 'Hello *Cruel* World!'
    frags = fragQuote(Fragment(text=input, done=False))
    assert len(frags) == 5
    output = defrag(frags)
    assert output == 'Hello <em>Cruel</em> World!'
    assert render(input) == output

    input = 'Hello **Cruel** World!'
    frags = fragQuote(Fragment(text=input, done=False))
    assert len(frags) == 5
    output = defrag(frags)
    assert output == 'Hello <strong>Cruel</strong> World!'
    assert render(input) == output

    input = '[Link](http://example.com)'
    frags = fragReplacements([Fragment(text=input, done=False)])
    assert len(frags) == 3
    output = defrag(frags)
    assert output == '<a href="http://example.com">Link</a>'
    assert render(input) == output

    input = '**[Link](http://example.com)**'
    output = render(input)
    assert output == '<strong><a href="http://example.com">Link</a></strong>'

    input = '<br>'
    output = render(input)
    assert output == '<br>'
