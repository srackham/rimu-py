def replaceSpecialChars(s):
    return s.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')


class ExpansionOptions:
    # TODO
    pass


def replaceMatch(match, replacement, expansionOptions=ExpansionOptions()):
    '''Replace pattern '$1' or '$$1', '$2' or '$$2'... in `replacement` with corresponding match groups
       from `match`. If pattern starts with one '$' character add specials to `expansionOptions`,
       if it starts with two '$' characters add spans to `expansionOptions`.'''
    # TODO
    return 'MOCK'
