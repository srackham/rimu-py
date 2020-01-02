from rimu.expansion import ExpansionOptions


def test_expansionOptions():
    opts = ExpansionOptions(macros=True, specials=False)
    opts.merge(ExpansionOptions(macros=False, container=True))
    assert opts == ExpansionOptions(
        macros=False,
        container=True,
        specials=False)

    opts = ExpansionOptions(macros=True, specials=False)
    opts.parse('-macros +spans')
    assert opts == ExpansionOptions(
        macros=False,
        spans=True,
        specials=False)
