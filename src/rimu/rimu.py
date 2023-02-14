from rimu import document, options
from rimu.options import RenderOptions
from typing import Optional


def render(source: str, opts: Optional[RenderOptions] = None) -> str:
    '''Exported render() API.'''
    if opts is None:
        opts = RenderOptions()
    # Implicit first-call API initialisation.
    if options.safeMode == -1:
        document.init()
    options.updateFrom(opts)
    return document.render(source)
