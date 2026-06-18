#!/usr/bin/env python3
import argparse
import os
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GOLDEN = ROOT / 'testdata' / 'golden' / 'ytenx.sqlite'

EXCLUDED_COUNT_TABLES = {
    'django_migrations',
    'django_session',
}

SAMPLE_TABLES = (
    'kyonh_sieuxyonh',
    'kyonh_dzih',
    'jihthex_dzih',
    'trngyan_dzih',
    'dciangxkox_dzih',
    'pyonh_dzih',
    'tcenghyonhtsen_dzih',
)

SMOKE_PAGES = (
    ('/', '韻典網'),
    ('/kyonh/', '廣韻'),
    ('/kyonh/sieux/1/', None),
    ('/kyonh/dzih/1/', None),
    ('/kyonh/yonhdo', '等韻圖'),
    ('/pyonh/', None),
    ('/trngyan/', None),
    ('/tcyts/', None),
    ('/zim?dzih=東&dzyen=1', '東'),
)


def main():
    parser = argparse.ArgumentParser(
        description='Rebuild a temporary SQLite DB and compare it with a golden DB.'
    )
    parser.add_argument('--golden', default=str(DEFAULT_GOLDEN))
    parser.add_argument('--keep-db', action='store_true')
    args = parser.parse_args()

    golden = Path(args.golden).resolve()
    if not golden.exists():
        raise SystemExit('golden DB does not exist: %s' % golden)

    with tempfile.TemporaryDirectory(prefix='ytenx-golden-') as tmpdir:
        target = Path(tmpdir) / 'ytenx.sqlite'
        rebuild_database(golden, target)
        compare_databases(golden, target)
        smoke_pages(target)
        print('Golden DB smoke passed: %s' % target)
        if args.keep_db:
            kept = ROOT / 'build' / 'golden-smoke.sqlite'
            kept.parent.mkdir(parents=True, exist_ok=True)
            kept.write_bytes(target.read_bytes())
            print('Kept rebuilt DB at %s' % kept)


def rebuild_database(golden, target):
    subprocess.run(
        [sys.executable, 'scripts/build_sqlite.py', '--target', str(target), '--reset'],
        cwd=str(ROOT),
        check=True,
    )


def compare_databases(golden, target):
    assert_no_foreign_key_violations(target)
    assert_equal('schema', schema(golden), schema(target))
    assert_equal('table counts', table_counts(golden), table_counts(target))
    for table in comparable_tables(golden):
        assert_equal('rows for %s' % table, table_rows(golden, table), table_rows(target, table))


def assert_no_foreign_key_violations(db_path):
    with sqlite3.connect(str(db_path)) as conn:
        violations = conn.execute('PRAGMA foreign_key_check;').fetchall()
    if violations:
        raise AssertionError('foreign_key_check failed: %r' % (violations,))


def schema(db_path):
    query = """
        SELECT type, name, tbl_name, sql
        FROM sqlite_master
        WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%'
        ORDER BY type, name;
    """
    with sqlite3.connect(str(db_path)) as conn:
        return conn.execute(query).fetchall()


def table_counts(db_path):
    counts = {}
    with sqlite3.connect(str(db_path)) as conn:
        tables = [
            row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
            )
        ]
        for table in tables:
            if table in EXCLUDED_COUNT_TABLES:
                continue
            counts[table] = conn.execute('SELECT COUNT(*) FROM "%s";' % table).fetchone()[0]
    return counts


def sample_rows(db_path, table):
    with sqlite3.connect(str(db_path)) as conn:
        order_by = primary_key_order(conn, table)
        query = 'SELECT * FROM "%s" ORDER BY %s LIMIT 10;' % (table, order_by)
        return conn.execute(query).fetchall()


def comparable_tables(db_path):
    with sqlite3.connect(str(db_path)) as conn:
        return [
            row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
            )
            if row[0] not in EXCLUDED_COUNT_TABLES
        ]


def table_rows(db_path, table):
    with sqlite3.connect(str(db_path)) as conn:
        columns = comparable_columns(conn, table)
        order_by = ', '.join('"%s"' % column for column in columns)
        select = ', '.join('"%s"' % column for column in columns)
        return conn.execute('SELECT %s FROM "%s" ORDER BY %s;' % (select, table, order_by)).fetchall()


def comparable_columns(conn, table):
    columns = conn.execute('PRAGMA table_info("%s");' % table).fetchall()
    names = [column[1] for column in columns]
    primary_keys = [column for column in columns if column[5]]
    if len(primary_keys) == 1 and primary_keys[0][1] == 'id':
        return [name for name in names if name != 'id']
    return names


def primary_key_order(conn, table):
    columns = conn.execute('PRAGMA table_info("%s");' % table).fetchall()
    primary_keys = [(column[5], column[1]) for column in columns if column[5]]
    if primary_keys:
        primary_keys.sort()
        return ', '.join('"%s"' % name for _, name in primary_keys)
    return 'rowid'


def smoke_pages(db_path):
    sys.path.insert(0, str(ROOT))
    os.environ['YTENX_DB_PATH'] = str(db_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ytenx.settings')

    import django
    from django.test import Client

    django.setup()
    client = Client()
    for path, expected in SMOKE_PAGES:
        response = client.get(path)
        if response.status_code != 200:
            raise AssertionError('%s returned HTTP %s' % (path, response.status_code))
        body = response.content.decode(response.charset or 'utf-8', errors='replace')
        if len(body.strip()) < 100:
            raise AssertionError('%s returned an unexpectedly small response' % path)
        if expected and expected not in body:
            raise AssertionError('%s did not contain %r' % (path, expected))


def assert_equal(label, expected, actual):
    if expected != actual:
        raise AssertionError('%s differ\nexpected: %r\nactual:   %r' % (label, expected, actual))


if __name__ == '__main__':
    main()
