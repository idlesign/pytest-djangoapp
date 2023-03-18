from django import VERSION


def test_command_run(command_run, capsys):

    result = command_run('my_command', args=['one'], options={'two': 'three'})
    out, err = capsys.readouterr()

    assert 'bingo' in out
    assert 'bongo' in err

    if VERSION >= (1, 10):
        assert result == 'one|three'


def test_command_migration(command_makemigrations, capsys):

    result = command_makemigrations()
    out, err = capsys.readouterr()

    assert result is None

    assert 'No changes' in out
    assert err == ''
