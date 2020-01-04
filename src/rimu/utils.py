import re
from typing import Match

from rimu import options, spans
from rimu.expansion import ExpansionOptions


def replaceSpecialChars(s: str) -> str:
    return s.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')


def replaceMatch(match: Match, replacement: str, expansionOptions: ExpansionOptions = None) -> str:
    '''Replace pattern '$1' or '$$1', '$2' or '$$2'... in `replacement` with corresponding match groups
       from `match`. If pattern starts with one '$' character add specials to `expansionOptions`,
       if it starts with two '$' characters add spans to `expansionOptions`.'''
    if expansionOptions is None:
        expansionOptions = ExpansionOptions()

    def repl(m):
        # Replace $1, $2 ... with corresponding match groups.
        if m[1] == '$$':
            expansionOptions.spans = True
        else:
            expansionOptions.specials = True
        i = int(m[2])
        # match group number.
        if i > match.re.groups:
            options.errorCallback('undefined replacement group: ' + m[0])
            return ''
        result = match[i]
        # match group text.
        return replaceInline(result, expansionOptions)
    return re.sub(r'(\${1,2})(\d)', repl, replacement)


def replaceInline(text: str, expansionOptions: ExpansionOptions) -> str:
    '''Replace the inline elements specified in options in text and return the result.'''
    result = text
    if expansionOptions.macros:
        # TODO: result = macros.render(result)
        pass
    # Spans also expand special characters.
    if expansionOptions.spans:
        result = spans.render(result)
    elif expansionOptions.specials:
        result = replaceSpecialChars(result)
    return result
