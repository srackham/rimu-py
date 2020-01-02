import io
import sys
import pytest
import rimuc


def execRimuc(capsys, monkeypatch=None, args=[], input=''):
    sys.argv = ['rimuc', '--no-rimurc'] + args
    exitcode = 0
    if input != '':
        # Inject stdin.
        monkeypatch.setattr('sys.stdin', io.StringIO(input))
    try:
        rimuc.main()
    except SystemExit as e:
        exitcode = e.code
    return capsys.readouterr(), exitcode


def test_readResource(capsys):
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
    # TODO
    pass
