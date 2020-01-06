import re
from typing import Any

from rimu import options


class ExpansionOptions:
    '''Processing priority(highest to lowest): container, skip, spans and specials.
       If spans is true then both spans and specials are processed.
       They are assumed false if they are not explicitly defined.
       If a custom filter is specified their use depends on the filter.'''
    macros: bool
    container: bool
    skip: bool
    spans: bool
    # Span substitution also expands special characters.
    specials: bool

    def __init__(self,
                 macros: bool = None,
                 container: bool = None,
                 skip: bool = None,
                 spans: bool = None,
                 specials: bool = None,
                 ):
        self.macros = macros
        self.container = container
        self.skip = skip
        self.spans = spans
        self.specials = specials

    def __eq__(self, obj: Any) -> bool:
        return (isinstance(obj, ExpansionOptions) and
                self.macros == obj.macros and
                self.container == obj.container and
                self.skip == obj.skip and
                self.spans == obj.spans and
                self.specials == obj.specials)

    @classmethod
    def copyFrom(cls, other: 'ExpansionOptions') -> 'ExpansionOptions':
        return ExpansionOptions(
            other.macros,
            other.container,
            other.skip,
            other.spans,
            other.specials,
        )

    def merge(self, other: 'ExpansionOptions') -> None:
        if other is None:
            return
        if other.macros is not None:
            self.macros = other.macros
        if other.container is not None:
            self.container = other.container
        if other.skip is not None:
            self.skip = other.skip
        if other.spans is not None:
            self.spans = other.spans
        if other.specials is not None:
            self.specials = other.specials

    def parse(self, opts: str) -> None:
        '''Parse block-options string into blockOptions.'''
        if opts != '':
            for opt in re.split(r'\s+', opts.strip()):
                if options.isSafeModeNz() and opt == '-specials':
                    options.errorCallback('-specials block option not valid in safeMode')
                    continue
                if re.match(r'^[+-](macros|spans|specials|container|skip)$', opt) is not None:
                    value = opt[0] == '+'
                    if opt[1:] == 'macros':
                        self.macros = value
                    elif opt[1:] == 'spans':
                        self.spans = value
                    elif opt[1:] == 'specials':
                        self.specials = value
                    elif opt[1:] == 'container':
                        self.container = value
                    elif opt[1:] == 'skip':
                        self.skip = value
                else:
                    options.errorCallback('illegal block option: ' + opt)
