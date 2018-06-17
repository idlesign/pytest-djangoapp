
def test_template_context(template_context):
    assert template_context({'somevar': 'someval'})


def test_template_render_tag(template_render_tag):
    rendered = template_render_tag('static', 'static "some.jpg"')
    assert rendered == '/static/some.jpg'


def test_this_template_strip_tags(template_strip_tags):
    stripped = template_strip_tags('<b>some</b>')
    assert stripped == 'some'
