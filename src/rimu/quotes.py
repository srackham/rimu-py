import re


class Def:

    def __init__(self, quote, openTag, closeTag, spans):
        self.quote = quote
        self.openTag = openTag
        self.closeTag = closeTag
        self.spans = spans

    @classmethod
    def copyFrom(cls, d):
        return Def(d.quote, d.openTag, d.closeTag, d.spans)


defs = []  # Mutable definitions initialized by DEFAULT_DEFS.

DEFAULT_DEFS = [
    Def(quote='**', openTag='<strong>', closeTag='</strong>', spans=True),
    Def(quote='*', openTag='<em>', closeTag='</em>', spans=True),
    Def(quote='__', openTag='<strong>', closeTag='</strong>', spans=True),
    Def(quote='_', openTag='<em>', closeTag='</em>', spans=True),
    Def(quote='``', openTag='<code>', closeTag='</code>', spans=False),
    Def(quote='`', openTag='<code>', closeTag='</code>', spans=False),
    Def(quote='~~', openTag='<del>', closeTag='</del>', spans=True),
]

quotesRe = None  # Searches for quoted text.
unescapeRe = None  # Searches for escaped quotes.


def init():
    '''Reset definitions to defaults.'''
    global defs
    # Make shallow copy of DEFAULT_DEFS (list and list objects).
    defs = list(map(lambda d: Def.copyFrom(d), DEFAULT_DEFS))
    initializeRegExps()


def initializeRegExps():
    '''Synthesise re's to find and unescape quotes.'''
    global quotesRe, unescapeRe
    quotes = list(map(lambda d: re.escape(d.quote), defs))
    # $1 is quote character(s), $2 is quoted text.
    # Quoted text cannot begin or end with whitespace.
    # Quoted can span multiple lines.
    # Quoted text cannot end with a backslash.
    quotesRe = re.compile(
        r'\\?(' + '|'.join(quotes) + r')([^\s\\]|\S[\s\S]*?[^\s\\])\1')
    # $1 is quote character(s).
    unescapeRe = re.compile(r'\\(' + '|'.join(quotes) + ')')


def getDefinition(quote):
    '''Return the quote definition corresponding to 'quote' character, return null if not found.'''
    found = list(filter(lambda d: d.quote == quote, defs))
    if len(found) == 0:
        return None
    else:
        return found[0]


def setDefinition(dfn):
    '''Update existing or add new quote definition.'''
    d = getDefinition(dfn.quote)
    if d != None:
        # Update existing definition.
        d.openTag = dfn.openTag
        d.closeTag = dfn.closeTag
        d.spans = dfn.spans
    else:
        # Double-quote definitions are prepended to the array so they are matched
        # before single-quote definitions(which are appended to the array).
        if len(dfn.quote) == 2:
            defs.insert(0, dfn)
        else:
            defs.append(dfn)
        initializeRegExps()


def unescape(s):
    '''Strip backslashes from quote characters.'''
    return unescapeRe.sub(lambda m: m[1], s)
