import sys
import rimu


def main(args=[]):
    # illegalLayout test.
    if ' '.join(args) == '--layout foobar':
        sys.stderr.write('illegal --layout: foobar\n')
        raise SystemExit(2)
    # basic test.
    input = sys.stdin.read()
    sys.stdout.write(rimu.render(input, rimu.RenderOptions()))
