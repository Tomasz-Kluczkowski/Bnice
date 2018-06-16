from dashboard.templatetags.dashboard_tags import set_var, get_model_name


def test_set_var_tag():
    assert set_var('test_value') == 'test_value'


def test_get_model_name(smiley_custom_description):
    assert get_model_name(smiley_custom_description) == 'Smiley'
