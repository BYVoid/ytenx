import importlib
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, connections


SYNC_MODULES = (
    'ytenx.sync.kyonh',
    'ytenx.sync.jihthex',
    'ytenx.sync.trngyan',
    'ytenx.sync.dciangx',
    'ytenx.sync.pyonh',
    'ytenx.sync.tcenghyonhtsen',
)

COUNT_TABLES = (
    'kyonh_sieuxyonh',
    'kyonh_dzih',
    'jihthex_dzih',
    'trngyan_dzih',
    'dciangxkox_dzih',
    'pyonh_dzih',
    'tcenghyonhtsen_dzih',
)


class Command(BaseCommand):
    help = 'Rebuild the SQLite database and import the bundled ytenx data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete the configured SQLite database before rebuilding it.',
        )
        parser.add_argument(
            '--skip-check',
            action='store_true',
            help='Skip PRAGMA foreign_key_check after import.',
        )

    def handle(self, *args, **options):
        db_name = settings.DATABASES['default']['NAME']
        if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
            raise CommandError('rebuild_db only supports the SQLite backend.')

        db_path = Path(db_name)
        if options['reset']:
            connections.close_all()
            if db_path.exists():
                db_path.unlink()
                self.stdout.write('Removed %s' % db_path)
        elif db_path.exists():
            raise CommandError('%s already exists; use --reset to rebuild it.' % db_path)

        db_path.parent.mkdir(parents=True, exist_ok=True)

        call_command('migrate', run_syncdb=True, verbosity=options['verbosity'])

        for module_name in SYNC_MODULES:
            module = importlib.import_module(module_name)
            module.sync()

        if not options['skip_check']:
            violations = self._foreign_key_violations()
            if violations:
                raise CommandError('foreign_key_check failed: %r' % (violations,))

        self._write_counts()
        self.stdout.write(self.style.SUCCESS('Database rebuilt: %s' % db_path))

    def _foreign_key_violations(self):
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_key_check;')
            return cursor.fetchall()

    def _write_counts(self):
        with connection.cursor() as cursor:
            for table in COUNT_TABLES:
                cursor.execute('SELECT COUNT(*) FROM %s;' % table)
                count = cursor.fetchone()[0]
                self.stdout.write('%s: %s' % (table, count))
