from rimu.expansion import Expand


def test_expansionOptions():
    opts = Expand(macros=True, specials=False)
    opts.merge(Expand(macros=False, container=True))
    assert opts == Expand(
        macros=False,
        container=True,
        specials=False)

    opts = Expand(macros=True, specials=False)
    opts.parse('-macros +spans')
    assert opts == Expand(
        macros=False,
        spans=True,
        specials=False)
