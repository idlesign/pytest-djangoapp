
def test_template_context(template_context):
    assert template_context({'somevar': 'someval'})


def test_template_render_tag(template_render_tag):
    assert template_render_tag('static', 'static "some.jpg"')
