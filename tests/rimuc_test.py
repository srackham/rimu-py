import io
import json
import sys
from typing import Union

import pytest

import rimuc
from rimu import document


def execRimuc(capsys, monkeypatch=None, args=[], input=''):
    document.init()
    sys.argv = ['rimuc', '--no-rimurc'] + args
    exitcode: Union[str, int, None] = 0
    if input != '':
        # Inject stdin.
        assert monkeypatch is not None
        monkeypatch.setattr('sys.stdin', io.StringIO(input))
    try:
        rimuc.main()
    except SystemExit as e:
        exitcode = e.code
    return capsys.readouterr(), exitcode


def test_readResource():
    # Throws exception if there is a missing resource file.
    for style in ['classic', 'flex', 'plain', 'sequel', 'v8']:
        rimuc.readResource(f'{style}-header.rmu')
        rimuc.readResource(f'{style}-footer.rmu')
    rimuc.readResource('manpage.txt')


def test_helpCommand(capsys):
    captured, exitcode = execRimuc(capsys, args=['-h'])
    assert exitcode == 0
    assert captured.out.startswith('\nNAME')


def test_basic(capsys, monkeypatch):
    captured, exitcode = execRimuc(capsys, monkeypatch, input='Hello\nWorld!')
    assert exitcode == 0
    assert captured.out == '<p>Hello\nWorld!</p>'


def test_illegalLayout(capsys):
    captured, exitcode = execRimuc(capsys, args=['--layout', 'foobar'])
    assert exitcode == 1
    assert captured.err.startswith('illegal --layout: foobar')


def test_jsonTests(capsys, monkeypatch):
    with open('./tests/rimuc-tests.json') as f:
        data = json.load(f)
    for spec in data:
        description = spec['description']
        for layout in ['', 'classic', 'flex', 'sequel']:
            # Skip if not a layouts test and we have a layout, or if it is a layouts test but no layout is specified.
            if not spec.get('layouts', False) and layout or spec.get('layouts', False) and not layout:
                continue
            # Massage project-specific paths.
            argstr = spec['args'].replace('./examples/example-rimurc.rmu', './tests/fixtures/example-rimurc.rmu')
            argstr = argstr.replace('./test/fixtures/', './tests/fixtures/')
            spec['expectedOutput'] = spec['expectedOutput'].replace('./test/fixtures/', './tests/fixtures/')
            # Parse arguments string to arguments array.
            args = []
            if argstr:
                for arg in argstr.split(' '):
                    arg = arg.strip()
                    if arg.startswith('"'):
                        arg = arg[1:-1]  # Strip enclosing double-quotes.
                    args.append(arg)
            if layout:
                args[0:0] = ['--layout', layout]
            input = spec['input']
            predicate = spec['predicate']
            expectedOutput = spec['expectedOutput']
            captured, exitcode = execRimuc(capsys, monkeypatch, args=args, input=input)
            output = f'{captured.err}{captured.out}'
            assert exitcode == spec.get('exitCode', 0)
            if predicate == "equals":
                assert output == expectedOutput
            elif predicate == '!equals':
                assert output != expectedOutput
            elif predicate == 'contains':
                assert expectedOutput in output
            elif predicate == '!contains':
                assert expectedOutput not in output
            elif predicate == 'startsWith':
                assert output.startswith(expectedOutput)
            else:
                raise Exception(description + ': illegal predicate: ' + predicate)
