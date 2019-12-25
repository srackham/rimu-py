import rimu.api as api
import rimu.utils as utils

# Global option values.
safeMode = None
htmlReplacement = None
callback = None


class RenderOptions:
    def __init__(self, safeMode=None, htmlReplacement=None, reset=None, callback=None):
        self.safeMode = safeMode
        self.htmlReplacement = htmlReplacement
        self.reset = reset
        self.callback = callback


class CallbackMessage:
    def __init__(self, type, text):
        self.type = type
        self.text = text


def init():
    '''Initialize globals.'''
    global safeMode, htmlReplacement, callback
    safeMode = 0
    htmlReplacement = '<mark>replaced HTML</mark>'
    callback = None


def isSafeModeNz():
    '''Return true if safeMode is non-zero.'''
    return safeMode != 0


def getSafeMode():
    return safeMode


def skipMacroDefs():
    '''Return true if Macro Definitions are ignored.'''
    return safeMode != 0 and (safeMode & 0x8) == 0


def skipBlockAttributes():
    '''Return true if Block Attribute elements are ignored.'''
    return (safeMode & 0x4) != 0


def updateOptions(options):
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


def setOption(name, value):
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
        htmlReplacement = value
    else:
        errorCallback('illegal API option name: ' + name)


def htmlSafeModeFilter(html):
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


def errorCallback(message):
    if callback != None:
        callback(CallbackMessage('error', message))


def panic(message):
    '''Called when an unexpected program error occurs.'''
    msg = 'panic: ' + message
    print(msg)
    errorCallback(msg)
