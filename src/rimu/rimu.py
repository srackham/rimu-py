from rimu import api
from rimu import options
from rimu.options import RenderOptions


def render(source: str, opts: RenderOptions = RenderOptions()) -> str:
    '''Exported render() API.'''
    # Implicit first-call API initialisation.
    if options.safeMode == -1:
        api.init()
    options.updateOptions(opts)
    return api.render(source)
