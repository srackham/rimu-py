import json

import rimu
from rimu import options


def unexpectedError(message: options.CallbackMessage) -> None:
    raise Exception(f'unexpected callback: {message}')


def test_render():
    assert rimu.render('Hello World!') == '<p>Hello World!</p>'


def test_jsonTests():
    with open('./tests/rimu-tests.json') as f:
        data = json.load(f)
    for spec in data:
        description = spec['description']
        unsupported = 'py' in spec.get('unsupported', '')
        if unsupported:
            print(f'skipped unsupported: {description}')
            continue
        print(description)
        renderOptions = rimu.RenderOptions()
        renderOptions.safeMode = spec['options'].get('safeMode')
        renderOptions.htmlReplacement = spec['options'].get('htmlReplacement')
        renderOptions.reset = spec['options'].get('reset')
        msg = ''

        def callback(message: rimu.CallbackMessage):
            nonlocal msg
            msg += f'{message.type}: {message.text}\n'
        # Captured callback message.
        if spec['expectedCallback'] or unsupported:
            renderOptions.callback = callback
        else:
            # Callback should not occur, this will throw an error.
            renderOptions.callback = unexpectedError
        input = spec['input']
        result = rimu.render(input, renderOptions)
        assert result == spec['expectedOutput'], description
        if spec['expectedCallback']:
            assert msg.strip() == spec['expectedCallback']
