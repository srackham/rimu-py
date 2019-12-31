from rimu import api
from rimu import utils
from typing import Any, Callable, Optional

Callback = Optional[Callable[[str, str], None]]

# Global option values.
safeMode: int = -1  # Trigger API initialization.
htmlReplacement: str
callback: Callback = None


class RenderOptions:
    '''Rimu render API options.'''
    safeMode: Optional[int]
    htmlReplacement: Optional[str]
    reset: Optional[bool]
    callback: Callback

    def __init__(self, safeMode: int = None, htmlReplacement: str = None, reset: Any = None, callback: Callback = None):
        self.safeMode = safeMode
        self.htmlReplacement = htmlReplacement
        self.reset = reset
        self.callback = callback


def init() -> None:
    '''Initialize API render options.'''
    global safeMode, htmlReplacement, callback
    safeMode = 0
    htmlReplacement = '<mark>replaced HTML</mark>'
    callback = None


def isSafeModeNz() -> bool:
    '''Return true if safeMode is non-zero.'''
    return safeMode != 0


def getSafeMode() -> int:
    return safeMode


def skipMacroDefs() -> bool:
    '''Return true if Macro Definitions are ignored.'''
    return safeMode != 0 and (safeMode & 0x8) == 0


def skipBlockAttributes() -> bool:
    '''Return true if Block Attribute elements are ignored.'''
    return (safeMode & 0x4) != 0


def updateFrom(options: RenderOptions) -> None:
    ''' Update specified (non-null) options.'''
    global safeMode, htmlReplacement, callback
    # Install callback first to ensure option errors are logged.
    if callback != None:
        callback = options.callback
    setOption('reset', options.reset)  # Reset takes priority.
    # Install callback again in case it has been reset.
    if options.callback != None:
        callback = options.callback
    if options.safeMode != None:
        setOption('safeMode', str(options.safeMode))
    if options.htmlReplacement != None:
        setOption('htmlReplacement', options.htmlReplacement)


def setOption(name: str, value: Any) -> None:
    '''Set named option value.'''
    global safeMode, htmlReplacement, callback
    if name == 'safeMode':
        n = 0
        try:
            n = int(value)
        except:
            errorCallback('illegal safeMode API option value: ' + str(value))
        if n < 0 or n > 15:
            errorCallback('illegal safeMode API option value: ' + str(value))
        else:
            safeMode = n
    elif name == 'reset':
        if value == False or value == 'false':
            return
        elif value == True or value == 'true':
            api.init()
        else:
            errorCallback('illegal reset API option value: ' + str(value))
    if name == 'htmlReplacement':
        htmlReplacement = str(value)
    else:
        errorCallback('illegal API option name: ' + name)


def htmlSafeModeFilter(html: str) -> str:
    '''Filter HTML based on current safeMode.'''
    n = safeMode & 0x3
    if n == 0:    # Raw HTML (default behavior).
        return html
    elif n == 1:  # Drop HTML.
        return ''
    elif n == 2:  # Replace HTML with 'htmlReplacement' option string.
        return htmlReplacement
    elif n == 3:  # Render HTML as text.
        return utils.replaceSpecialChars(html)
    else:
        return ''


def errorCallback(message: str) -> None:
    if callback != None:
        callback('error', message)


def panic(message: str) -> None:
    '''Called when an unexpected program error occurs.'''
    msg = 'panic: ' + message
    print(msg)
    errorCallback(msg)
