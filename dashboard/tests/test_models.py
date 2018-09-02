def test_smiley_reverse(smiley_custom_description):
    """Confirm correct reverse url."""
    smiley = smiley_custom_description
    assert smiley.get_absolute_url() == '/dashboard/child/1/'


def test_oopsy_reverse(oopsy_custom_description):
    """Confirm correct reverse url."""
    oopsy = oopsy_custom_description
    assert oopsy.get_absolute_url() == '/dashboard/child/detail/tom_k/nat_k/1'


def test_smiley_str(smiley_custom_description):
    smiley = smiley_custom_description
    assert smiley.__str__() == 'Removed rubbish'


def test_oopsy_str(oopsy_custom_description):
    oopsy = oopsy_custom_description
    assert oopsy.__str__() == 'Was rude'
