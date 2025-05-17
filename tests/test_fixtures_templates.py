
def test_template_context(template_context, user_create):
    assert template_context({'somevar': 'someval'})

    context = template_context({'a': 'b'}, user='aname')
    assert context.get('user').username == 'aname'

    auser = user_create(attributes={'username': 'xx'})
    context = template_context({'a': 'b'}, user=auser)
    assert context.get('user').username == 'xx'


def test_template_render_tag(template_render_tag):
    rendered = template_render_tag('static', 'static "some.jpg"')
    assert rendered == '/static/some.jpg'


def test_this_template_strip_tags(template_strip_tags):
    stripped = template_strip_tags('<b>some</b>')
    assert stripped == 'some'
