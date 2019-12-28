from rimu import api
from rimu import options


def render(source, opts=options.RenderOptions()):
    '''This is the exported render() API.'''
    # Implicit first-call API initialisation.
    if options.safeMode == None:
        api.init()
    options.updateOptions(opts)
    return api.render(source)
