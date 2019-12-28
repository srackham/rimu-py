import io
import sys
import pytest
import rimuc


def test_basic(capsys, monkeypatch):
    # Inject stdin.
    monkeypatch.setattr('sys.stdin', io.StringIO('Hello\nWorld!'))
    rimuc.main()
    # Capture stdout, stderr.
    captured = capsys.readouterr()
    assert captured.out == '<p>Hello\nWorld!</p>'


def test_illegalLayout(capsys):
    with pytest.raises(SystemExit) as e:
        # Exits with exit code 2.
        rimuc.main(['--layout', 'foobar'])
    assert e.value.code == 2
    captured = capsys.readouterr()
    assert captured.err.startswith('illegal --layout: foobar')
