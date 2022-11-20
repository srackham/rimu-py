from typing import Dict

from rimu import document, io, lineblocks


def test_render():
    tests: Dict[str, str] = {
        r'# foo': r'<h1>foo</h1>',
        r'// foo': r'',
        r'<image:foo|bar>': r'<img src="foo" alt="bar">',
        r'<<#foo>>': r'<div id="foo"></div>',
        r'.class #id "css"': r'',
        r".safeMode='0'": r'',
        r"|code|='<code>|</code>'": r'',
        r"^='<sup>|</sup>'": r'',
        r"/\.{3}/i = '&hellip;'": r'',
        r"{foo}='bar'": r'',
    }
    document.init()
    for k, v in tests.items():
        reader = io.Reader(k)
        writer = io.Writer()
        lineblocks.render(reader, writer)
        got = writer.toString()
        assert got == v
