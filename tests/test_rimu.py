import rimu


def test_render():
    assert rimu.render('Hello World!') == '<p>Hello World!</p>'
