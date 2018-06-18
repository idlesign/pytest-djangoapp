from django.core.management.base import BaseCommand

from .compat import options_getter, CommandOption

get_options = options_getter((
    CommandOption('--two', action='store'),
))


class Command(BaseCommand):

    help = 'Sends scheduled messages (both in pending and error statuses).'

    option_list = get_options()

    def add_arguments(self, parser):
        parser.add_argument('one')
        get_options(parser.add_argument)

    def handle(self, one, **options):
        self.stdout.write('bingo')
        self.stderr.write('bongo')

        two = options.get('two', None)

        return '%s|%s' % (one, two)
