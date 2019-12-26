import re


class Reader:
    #   List<String> self.lines
    #   int self.pos; # Line index of current line.

    def __init__(self, text):
        # Used internally by spans package.
        text = text.replace('\u0000', ' ')
        # Used internally by spans package.
        text = text.replace('\u0001', ' ')
        # Used internally by macros package.
        text = text.replace('\u0002', ' ')
        # Split self.lines on newline boundaries.
        # http:#stackoverflow.com/questions/1155678/javascript-string-newline-character
        # Split is broken on IE8 e.g. 'X\n\nX'.split(/\n/g).length) returns 2 but should return 3.
        self.lines = re.split(r'\r\n|\r|\n', text)
        self.pos = 0

    @property
    def cursor(self):
        assert not self.eof()
        return self.lines[self.pos]

    @cursor.setter
    def cursor(self, value):
        assert not self.eof()
        self.lines[self.pos] = value

    def eof(self):
        '''Return true if the cursor has advanced over all input self.lines.'''
        return self.pos >= len(self.lines)

    def next(self):
        '''Move cursor to next input line.'''
        if (not self.eof()):
            self.pos += 1

    def readTo(self, find):
        '''Read to the first line matching the re.

        Return the array of self.lines preceding the match plus a line containing
        the $1 match group (if it exists).
        Return null if an self.EOF is encountered.
        Exit with the reader pointing to the line following the match.'''
        result = []
        while (not self.eof()):
            match = find.search(self.cursor)
            if (match != None):
                if (find.groups > 0):
                    result.append(match[1])  # $1
                self.next()
                break
            result.append(self.cursor)
            self.next()
        # Blank line matches self.EOF.
        if (match != None or (find.pattern == r'^$' and self.eof())):
            return result
        else:
            return None

    def skipBlankLines(self):
        while (not self.eof() and self.cursor.strip() == ''):
            self.next()


class Writer:
    def __init__(self):
        self.buffer = []

    def write(self, s):
        self.buffer.append(s)

    def toString(self):
        return ''.join(self.buffer)
