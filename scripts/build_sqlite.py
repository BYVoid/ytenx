#!/usr/bin/env python3
"""Build ytenx.sqlite from source data.

The romanized variable names are documented in docs/importer-glossary.md.
"""
import argparse
import re
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'scripts' / 'schema.sql'
DEFAULT_TARGET = ROOT / 'build' / 'ytenx.sqlite'

KNGIX_KEYS = (
    'kauPuonxHanh',
    'lixPyangKueh',
    'yangLik',
    'tciuPyapKau',
    'liukTcihYoi',
    'tungxDungGhua',
    'lixYeng',
    'dcjeuhYengPhyon',
    'drienghTriangDciangPyang',
    'phuanNgohYon',
    'boLipPuonx',
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


def main():
    parser = argparse.ArgumentParser(description='Build ytenx.sqlite from bundled source data without Django.')
    parser.add_argument('--target', default=str(DEFAULT_TARGET), help='SQLite output path.')
    parser.add_argument('--reset', action='store_true', help='Replace an existing target DB.')
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if target.exists() and not args.reset:
        raise SystemExit('target DB already exists, pass --reset: %s' % target)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.unlink()

    importer = Importer(target)
    importer.build()
    print('Built SQLite DB: %s' % target)


class Importer:
    def __init__(self, target):
        self.target = target
        self.conn = sqlite3.connect(str(target))
        self.conn.execute('PRAGMA foreign_keys = ON;')
        self.auto_ids = {}

    def build(self):
        self.create_schema()
        with self.conn:
            self.import_kyonh()
            self.import_jihthex()
            self.import_trngyan()
            self.import_dciangx()
            self.import_pyonh()
            self.import_tcengh()
            self.import_django_tables()
        self.check_foreign_keys()
        self.write_counts()
        self.conn.close()

    def create_schema(self):
        sql = []
        for line in SCHEMA.read_text(encoding='utf-8').splitlines():
            if line.startswith('CREATE TABLE sqlite_sequence'):
                continue
            sql.append(line)
        self.conn.executescript('\n'.join(sql))

    def rows(self, relpath, separator=' '):
        path = ROOT / relpath
        with path.open(encoding='utf-8') as handle:
            num = 0
            for raw in handle:
                if not raw or raw[0] == '#':
                    continue
                yield raw.rstrip('\n').split(separator), num
                num += 1

    def insert(self, table, **values):
        columns = list(values.keys())
        placeholders = ', '.join('?' for _ in columns)
        quoted = ', '.join('"%s"' % column for column in columns)
        self.conn.execute(
            'INSERT INTO "%s" (%s) VALUES (%s)' % (table, quoted, placeholders),
            [values[column] for column in columns],
        )

    def insert_ignore(self, table, **values):
        columns = list(values.keys())
        placeholders = ', '.join('?' for _ in columns)
        quoted = ', '.join('"%s"' % column for column in columns)
        self.conn.execute(
            'INSERT OR IGNORE INTO "%s" (%s) VALUES (%s)' % (table, quoted, placeholders),
            [values[column] for column in columns],
        )

    def m2m(self, table, **values):
        self.insert(table, id=self.next_id(table), **values)

    def m2m_ignore(self, table, **values):
        row = {'id': self.next_id(table)}
        row.update(values)
        columns = list(row.keys())
        placeholders = ', '.join('?' for _ in columns)
        quoted = ', '.join('"%s"' % column for column in columns)
        before = self.conn.total_changes
        self.conn.execute(
            'INSERT OR IGNORE INTO "%s" (%s) VALUES (%s)' % (table, quoted, placeholders),
            [row[column] for column in columns],
        )
        if self.conn.total_changes == before:
            self.auto_ids[table] -= 1

    def next_id(self, table):
        self.auto_ids[table] = self.auto_ids.get(table, 0) + 1
        return self.auto_ids[table]

    def check_foreign_keys(self):
        violations = self.conn.execute('PRAGMA foreign_key_check;').fetchall()
        if violations:
            raise SystemExit('foreign_key_check failed: %r' % (violations,))

    def write_counts(self):
        for table in COUNT_TABLES:
            count = self.conn.execute('SELECT COUNT(*) FROM %s;' % table).fetchone()[0]
            print('%s: %s' % (table, count))

    def import_django_tables(self):
        self.insert('django_migrations', id=1, app='sessions', name='0001_initial', applied='2026-01-01 00:00:00')

    def import_kyonh(self):
        cjeng_ngix = {}
        cjeng_preng = {}
        cjeng = {}
        gheh = {}
        yonh_ngix = {}
        yonh_preng = {}
        yonh = {}
        kuangx_tshiih = {}
        miuk = {}
        drak = {}
        cio = {}
        pyanx_dciangx = {}
        pyanx_ghrax = {}
        pyanx = {}
        preng = {}
        dauh = {}
        ngix = {}
        sieux = {}

        for line, _ in self.rows('ytenx/sync/kyonh/CjengMuxPrengQim.txt'):
            identifier = 'cjeng' + line[0]
            self.insert('kyonh_prengqim', identifier=identifier, baxter=line[1], polyhedron=line[2], tcengh=line[3], putonghua=line[4])
            cjeng_preng[line[0]] = identifier

        for line, _ in self.rows('ytenx/sync/kyonh/CjengMuxNgixQim.txt'):
            identifier = 'cjeng' + line[0]
            self.insert('kyonh_ngixqim', identifier=identifier, kauPuonxHanh=line[1], lixPyangKueh=line[2], yangLik=line[3], tciuPyapKau=line[4], liukTcihYoi=line[5], tungxDungGhua=line[6], lixYeng=line[7], dcjeuhYengPhyon=line[8], drienghTriangDciangPyang=line[9], phuanNgohYon=line[10], boLipPuonx=line[11])
            cjeng_ngix[line[0]] = identifier

        for line, _ in self.rows('ytenx/sync/kyonh/CjengMux.txt'):
            self.insert_ignore('kyonh_cjenglyih', mjeng=line[1], ziox=int(line[3]))
            self.insert('kyonh_cjengmux', dzih=line[0], lyih_id=line[1], ngix_id=cjeng_ngix[line[0]], preng_id=cjeng_preng[line[0]], ziox=int(line[2]))
            cjeng[line[0]] = {'dzih': line[0], 'ngix': cjeng_ngix[line[0]]}

        for line, _ in self.rows('ytenx/sync/kyonh/YonhGheh.txt'):
            self.insert_ignore('kyonh_yonhcjep', dzih=line[1])
            self.insert('kyonh_yonhgheh', dzih=line[0], cjep_id=line[1])
            gheh[line[0]] = line[0]

        for line, _ in self.rows('ytenx/sync/kyonh/YonhMuxPrengQim.txt'):
            identifier = 'yonh' + line[0]
            self.insert('kyonh_prengqim', identifier=identifier, baxter=line[1], polyhedron=line[2], tcengh=line[3], putonghua=line[4])
            yonh_preng[line[0]] = identifier

        for line, _ in self.rows('ytenx/sync/kyonh/YonhMuxNgixQim.txt'):
            identifier = 'yonh' + line[0]
            self.insert('kyonh_ngixqim', identifier=identifier, kauPuonxHanh=line[1], yangLik=line[2], lixYeng=line[3], dcjeuhYengPhyon=line[4], drienghTriangDciangPyang=line[5], phuanNgohYon=line[6], boLipPuonx=line[7])
            yonh_ngix[line[0]] = identifier

        pending_tuaih = {}
        for line, _ in self.rows('ytenx/sync/kyonh/YonhMux.txt'):
            ho = int(line[3] == '開')
            tshyuk = int(line[4] == '促')
            pending_tuaih[line[0]] = line[5] or None
            self.insert('kyonh_yonhmux', mjeng=line[0], gheh_id=line[1], tongx=int(line[2]), ho=ho, tshyuk=tshyuk, tuaih_id=None, ngix_id=yonh_ngix[line[0]], preng_id=yonh_preng[line[0]])
            yonh[line[0]] = {'mjeng': line[0], 'gheh': line[1], 'tshyuk': tshyuk, 'ngix': yonh_ngix[line[0]]}
        for key, tuaih in pending_tuaih.items():
            if tuaih:
                self.conn.execute('UPDATE kyonh_yonhmux SET tuaih_id = ? WHERE mjeng = ?', (tuaih, key))
                yonh[key]['tuaih'] = tuaih

        for line, _ in self.rows('ytenx/sync/kyonh/PrengQim.txt'):
            self.insert('kyonh_prengqim', identifier=line[0], polyhedron=line[1], hiovNivv=line[2], baxter=line[3])
            preng[line[0]] = line[0]
        for line, _ in self.rows('ytenx/sync/kyonh/Dauh.txt'):
            identifier = 'dauh' + line[0]
            self.insert('kyonh_prengqim', identifier=identifier, tcengh=line[1], putonghua=line[2])
            dauh[line[0]] = identifier

        for line, _ in self.rows('ytenx/sync/kyonh/SieuxYonh.txt'):
            identifier = line[0]
            c_ngix = self.row('kyonh_ngixqim', cjeng[line[2]]['ngix'])
            y_ngix = self.row('kyonh_ngixqim', yonh[line[3]]['ngix'])
            values = {'identifier': identifier}
            for key in KNGIX_KEYS:
                if c_ngix.get(key) and y_ngix.get(key):
                    values[key] = c_ngix[key] + y_ngix[key]
            self.insert('kyonh_ngixqim', **values)
            ngix[identifier] = identifier

        for line, _ in self.rows('ytenx/sync/kyonh/SieuxYonh.txt'):
            tshet = line[5]
            if not tshet:
                continue
            self.insert_ignore('kyonh_dciangxdzih', dzih=tshet[0])
            self.insert_ignore('kyonh_ghraxdzih', dzih=tshet[1])
            self.insert_ignore('kyonh_pyanxtshet', tshet=tshet, dciangx_id=tshet[0], ghrax_id=tshet[1])
            pyanx[tshet] = {'tshet': tshet, 'dciangx': tshet[0], 'ghrax': tshet[1]}
            pyanx_dciangx[tshet[0]] = tshet[0]
            pyanx_ghrax[tshet[1]] = tshet[1]

        for line, _ in self.rows('ytenx/sync/kyonh/KuangxYonhMiukTshiih.txt'):
            self.insert('kyonh_kuangxyonhmiuktshiih', dzih=line[0], kyenh=line[1], tshiih=int(line[2]))
            kuangx_tshiih[line[0]] = line[0]

        for line, _ in self.rows('ytenx/sync/kyonh/YonhMiuk.txt'):
            deuh = int(line[2])
            self.insert('kyonh_yonhmiuk', dzih=line[0], gheh_id=line[1], deuh=deuh, tshiih_id=line[3])
            miuk[line[0]] = {'dzih': line[0], 'gheh': line[1], 'deuh': deuh}
            for ym in yonh.values():
                if ym['gheh'] == line[1] and ym['tshyuk'] == 0:
                    self.m2m('kyonh_yonhmiuk_yonh', yonhmiuk_id=line[0], yonhmux_id=ym['mjeng'])

        for line, _ in self.rows('ytenx/sync/kyonh/YonhMiukDzip.txt'):
            self.insert('kyonh_yonhmiukdzip', id=self.next_id('kyonh_yonhmiukdzip'), bieng_id=line[0] or None, dciangx_id=line[1] or None, khioh_id=line[2] or None, njip_id=line[3] or None)

        for line, _ in self.rows('ytenx/sync/kyonh/DrakDzuonDang.txt'):
            identifier = line[0] + '_' + line[1]
            self.insert('kyonh_drakdzuondang', identifier=identifier, kyenh=int(line[0]), jep=int(line[1]), myon=line[2] if len(line) == 3 else '')
            self.insert('kyonh_cio', identifier=identifier, drakDzuonDang_id=identifier)
            drak[identifier] = identifier
            cio[identifier] = identifier

        for line, _ in self.rows('ytenx/sync/kyonh/SieuxYonh.txt'):
            ziox = int(line[0])
            self.insert('kyonh_sieuxyonh', ziox=ziox, taj=line[1], cjeng_id=line[2], yonh_id=line[3], yonhMiuk_id=line[4], pyanx_id=line[5] or None, ngix_id=line[0], preng_id=line[0], dauh_id='dauh' + line[0])
            sieux[line[0]] = {'ziox': ziox, 'cjeng': line[2], 'yonh': line[3], 'pyanx': line[5] or None}
            for c in line[6].split('/'):
                self.m2m('kyonh_sieuxyonh_cio', sieuxyonh_id=ziox, cio_id=c)

        last_dzih = ''
        last_ngieh = ''
        pattern = r'(^古文|^俗$|上同|^亦同|同上|^二同|^俗見上注|^俗本音.)'
        for line, num in self.rows('ytenx/sync/kyonh/Dzih.txt'):
            current_dzih = line[0]
            current_ngieh = re.sub(pattern, r'\1（' + last_dzih + '‧' + last_ngieh + '）', line[3], count=1)
            self.insert('kyonh_dzih', ziox=num + 1, dzih=current_dzih, sieuxYonh_id=int(line[1]), yih=int(line[2]), ngieh=current_ngieh)
            last_dzih = current_dzih
            last_ngieh = current_ngieh

        dciangx_cjeng = {}
        ghrax_yonh = {}
        for sy in sieux.values():
            if not sy['pyanx']:
                continue
            p = pyanx[sy['pyanx']]
            dciangx_cjeng.setdefault(p['dciangx'], {})[sy['cjeng']] = sy['cjeng']
            ghrax_yonh.setdefault(p['ghrax'], {})[sy['yonh']] = sy['yonh']
        for d, values in dciangx_cjeng.items():
            for c in values:
                self.m2m('kyonh_dciangxdzih_cjeng', dciangxdzih_id=d, cjengmux_id=c)
        for g, values in ghrax_yonh.items():
            for y in values:
                self.m2m('kyonh_ghraxdzih_yonh', ghraxdzih_id=g, yonhmux_id=y)

        self.kyonh_pyanx_by_tshet = pyanx
        self.kyonh_sieux_by_pyanx = {}
        for sy in sieux.values():
            if sy['pyanx']:
                self.kyonh_sieux_by_pyanx.setdefault(sy['pyanx'], []).append(sy['ziox'])

    def row(self, table, pk):
        cursor = self.conn.execute('SELECT * FROM "%s" WHERE 1=1 AND rowid IN (SELECT rowid FROM "%s" WHERE identifier = ?)' % (table, table), (pk,))
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        return dict(zip(columns, row)) if row else {}

    def import_jihthex(self):
        seen = set()

        def ensure(dzih):
            if dzih not in seen:
                self.insert('jihthex_dzih', dzih=dzih)
                seen.add(dzih)

        for line, _ in self.rows('ytenx/sync/jihthex/JihThex.csv', ','):
            ensure(line[0])
        for line, _ in self.rows('ytenx/sync/jihthex/ThaJihThex.csv', ','):
            ensure(line[0])
        for line, _ in self.rows('ytenx/sync/jihthex/JihThex.csv', ','):
            ensure(line[0])
            for table, text in (
                ('jihthex_dzih_dzyen_tongx', line[1]),
                ('jihthex_dzih_krau_dep', line[2]),
                ('jihthex_dzih_krenx', line[3]),
                ('jihthex_dzih_byan', line[4]),
            ):
                for c in text:
                    ensure(c)
                    self.m2m_ignore(table, from_dzih_id=line[0], to_dzih_id=c)
        for line, _ in self.rows('ytenx/sync/jihthex/ThaJihThex.csv', ','):
            ensure(line[0])
            for c in line[1]:
                ensure(c)
                self.m2m_ignore('jihthex_dzih_tha', from_dzih_id=line[0], to_dzih_id=c)

    def import_trngyan(self):
        cjeng = {}
        yonh = {}
        sieux = {}
        dzih_seen = {}
        for line, _ in self.rows('ytenx/sync/trngyan/CjengMuxNgixQim.txt'):
            self.insert('trngyan_ngixqim', identifier='c' + line[0], neng_keh_piuk=line[1])
        for line, _ in self.rows('ytenx/sync/trngyan/CjengMux.txt'):
            self.insert_ignore('trngyan_cjenglyih', mjeng=line[0])
            self.insert('trngyan_cjengmux', dzih=line[1], lyih_id=line[0], ngix_id='c' + line[1])
            cjeng[line[1]] = line[1]
        for line, _ in self.rows('ytenx/sync/trngyan/YonhMuxNgixQim.txt'):
            self.insert('trngyan_ngixqim', identifier='y' + line[0], neng_keh_piuk=line[1])
        for line, _ in self.rows('ytenx/sync/trngyan/YonhMux.txt'):
            box = line[0][0:2]
            ho = {'開': 1, '合': 2, '齊': 3, '撮': 4}[line[0][2]]
            self.insert_ignore('trngyan_yonhbox', mjeng=box)
            self.insert('trngyan_yonhmux', mjeng=line[0], yonh_box_id=box, ho=ho, ngix_id='y' + line[0])
            yonh[line[0]] = {'box': box, 'ho': ho}
        deuh_map = {'陰平': 1, '陽平': 2, '上': 3, '去': 4, '入平': 5, '入上': 6, '入去': 7}
        for line, _ in self.rows('ytenx/sync/trngyan/TriungNgyanQimYonh.txt'):
            y = yonh[line[5]]
            ziox = int(line[0])
            self.insert('trngyan_sieuxyonh', ziox=ziox, taj=line[1][0], cjeng_id=line[4], yonh_box_id=y['box'], yonh_id=line[5], deuh=deuh_map[line[2]], ho=y['ho'])
            sieux[line[0]] = ziox
        for vol, count in ((1, 94), (2, 118)):
            for i in range(1, count + 1):
                identifier = '%s_%s' % (vol, i)
                self.insert('trngyan_cio', identifier=identifier, kyenh=vol, jep=i)
        sieux_cio = {}
        for line, num in self.rows('ytenx/sync/trngyan/Dzih.txt'):
            dz = line[1]
            identifier = dz
            i = 1
            while identifier in dzih_seen:
                i += 1
                identifier = dz + str(i)
            dzih_seen[identifier] = True
            self.insert('trngyan_dzih', ziox=num + 1, id=identifier, dzih=dz, sieux_yonh_id=int(line[0]), tryoh=line[3])
            cio_id = '1_' + line[2]
            self.m2m('trngyan_dzih_cio', dzih_id=num + 1, cio_id=cio_id)
            sieux_cio.setdefault(int(line[0]), {})[cio_id] = cio_id
        for s, cios in sieux_cio.items():
            for c in cios:
                self.m2m('trngyan_sieuxyonh_cio', sieuxyonh_id=s, cio_id=c)

    def import_pyonh(self):
        yonh = {}
        sieux_cio = {}
        for line, _ in self.rows('ytenx/sync/pyonh/CjengMux.txt'):
            self.insert_ignore('pyonh_cjenglyih', mjeng=line[0])
            ngix = 'cjeng' + line[1]
            self.insert('pyonh_ngixqim', identifier=ngix)
            self.insert('pyonh_cjengmux', dzih=line[1], lyih_id=line[0], ngix_id=ngix)
        for line, _ in self.rows('ytenx/sync/pyonh/YonhBox.txt'):
            box = line[1]
            self.insert('pyonh_yonhbox', ziox=int(line[0]), mjeng=box)
            base = box[0]
            ngix = 'yonh' + base
            self.insert('pyonh_ngixqim', identifier=ngix)
            self.insert('pyonh_yonhmux', mjeng=base, yonh_box_id=int(line[0]), tshyuk=0, tuaih_id=None, ngix_id=ngix)
            yonh[base] = {'box': int(line[0]), 'tuaih': None}
            if len(box) == 4:
                tshyuk = box[3]
                t_ngix = 'yonh' + tshyuk
                self.insert('pyonh_ngixqim', identifier=t_ngix)
                self.insert('pyonh_yonhmux', mjeng=tshyuk, yonh_box_id=int(line[0]), tshyuk=1, tuaih_id=base, ngix_id=t_ngix)
                self.conn.execute('UPDATE pyonh_yonhmux SET tuaih_id = ? WHERE mjeng = ?', (tshyuk, base))
                yonh[base]['tuaih'] = tshyuk
                yonh[tshyuk] = {'box': int(line[0]), 'tuaih': base}
        deuh_map = {'平': 1, '上': 2, '去': 3, '入': 4}
        for line, _ in self.rows('ytenx/sync/pyonh/SieuxYonh.txt'):
            deuh = deuh_map[line[5]]
            ykey = line[3]
            if deuh == 4:
                ykey = yonh[ykey]['tuaih']
            self.insert('pyonh_sieuxyonh', ziox=int(line[0]), taj=line[1][0], cjeng_id=line[2], yonh_box_id=yonh[ykey]['box'], yonh_id=ykey, qim_jang=int(line[4] == '陽'), deuh=deuh)
        for vol, count in ((1, 105), (2, 97)):
            for i in range(1, count + 1):
                identifier = '%s_%s' % (vol, i)
                self.insert('pyonh_cio', identifier=identifier, kyenh=vol, jep=i)
        for line, _ in self.rows('ytenx/sync/pyonh/Dzih.txt'):
            ziox = int(line[0])
            self.insert('pyonh_dzih', ziox=ziox, dzih=line[2], sieux_yonh_id=int(line[1]), ngieh=line[6])
            vol = 1 if line[3] == '上冊' else 2
            for page in [line[4]] + ([line[5]] if line[5] else []):
                cio_id = '%s_%s' % (vol, page)
                self.m2m('pyonh_dzih_cio', dzih_id=ziox, cio_id=cio_id)
                sieux_cio.setdefault(int(line[1]), {})[cio_id] = cio_id
        for s, cios in sieux_cio.items():
            for c in cios:
                self.m2m('pyonh_sieuxyonh_cio', sieuxyonh_id=s, cio_id=c)

    def import_dciangx(self):
        cjeng = set()
        yonh = set()
        dzih_map = set()
        last = None
        myo = {'魚孟', '楚嫁', '阻買'}
        notes = []
        for line, num in self.rows('ytenx/sync/dciangx/DrienghTriang.txt'):
            dz = line[0]
            pyanx = line[7] + line[8]
            cj = line[9]
            yh = line[10]
            if cj not in cjeng:
                self.insert('dciangxkox_cjengbyo', mjeng=cj)
                cjeng.add(cj)
            if yh not in yonh:
                self.insert('dciangxkox_yonhbox', mjeng=yh)
                yonh.add(yh)
            identifier = dz
            i = 1
            while identifier in dzih_map:
                i += 1
                identifier = dz + str(i)
            dzih_map.add(identifier)
            ngix_1 = line[12]
            if line[13]:
                ngix_2, ngix_3 = line[13], line[14]
            else:
                ngix_2, ngix_3 = line[14], line[15]
            sieux_yonh = None
            matches = self.kyonh_sieux_by_pyanx.get(pyanx, [])
            if len(matches) == 1:
                sieux_yonh = matches[0]
            elif matches:
                sieux_yonh = matches[0]
            else:
                if last and last['ngix_1'] == ngix_1 and last['ngix_2'] == ngix_2 and last['ngix_3'] == ngix_3:
                    sieux_yonh = last['sieux_yonh_id']
                elif pyanx in myo:
                    sieux_yonh = None
                elif dz in ('拯', '氶'):
                    sieux_yonh = 1919
            row = {
                'ziox': num + 1,
                'id': identifier,
                'dzih': dz,
                'sieux_yonh_id': sieux_yonh,
                'cjeng_id': cj,
                'yonh_id': yh,
                'yonh_seh': int(line[11] or 0),
                'ngix_1': ngix_1,
                'ngix_2': ngix_2,
                'ngix_3': ngix_3,
                'tryoh': line[16],
            }
            self.insert('dciangxkox_dzih', **row)
            last = row

    def import_tcengh(self):
        miuk = {}
        dciangx = {}
        ghrax = {}
        pyanx = {}
        sieux = {}
        njip_ziox = 1
        cio_sieux_ziox = 1
        cio_dzih_ziox = 1
        for line, num in self.rows('ytenx/sync/tcenghyonhtsen/YonhMiuk.txt'):
            ziox = num + 1
            self.insert('tcenghyonhtsen_yonhbux', ziox=ziox, dzih=line[0][0])
            for i in range(1, 5):
                if not line[i]:
                    continue
                mziox = ziox
                if i == 4:
                    mziox = njip_ziox
                    njip_ziox += 1
                self.insert('tcenghyonhtsen_yonhmiuk', ziox=mziox, dzih=line[i], bux_id=ziox, deuh=i)
                miuk[line[i]] = {'dzih': line[i], 'deuh': i}

        def sync_pyanx(d, g):
            if not d or not g:
                return None
            if d not in dciangx:
                self.insert_ignore('tcenghyonhtsen_dciangxdzih', dzih=d)
                dciangx[d] = d
            if g not in ghrax:
                self.insert_ignore('tcenghyonhtsen_ghraxdzih', dzih=g)
                ghrax[g] = g
            tshet = d + g
            self.insert_ignore('tcenghyonhtsen_pyanxtshet', tshet=tshet, dciangx_id=d, ghrax_id=g)
            pyanx[tshet] = tshet
            return tshet

        for line, _ in self.rows('ytenx/sync/tcenghyonhtsen/SieuxYonh.txt'):
            p = sync_pyanx(line[3], line[4])
            self.insert('tcenghyonhtsen_sieuxyonh', ziox=int(line[0]), taj=line[1], yonhMiuk_id=line[2], pyanx_id=p, ipa=line[10], jamo=line[11], cioTriungZiox=cio_sieux_ziox)
            sieux[line[0]] = {'ziox': int(line[0]), 'deuh': miuk[line[2]]['deuh']}
            cio_sieux_ziox += 1

        def sy_or_none(value):
            return None if value in ('', '?') else int(value)

        for line, _ in self.rows('ytenx/sync/tcenghyonhtsen/QimBjin.txt'):
            self.insert('tcenghyonhtsen_qimbjin', ziox=int(line[0]), t1_id=sy_or_none(line[1]), t2_id=sy_or_none(line[2]), t3_id=sy_or_none(line[3]), t4_id=sy_or_none(line[4]), merge_t2_t3=int(line[5] != 'FALSE'), has_t4=int(line[4] != ''), filename=line[6], additional_id=sy_or_none(line[7]))

        sieux_cio = {}

        def ensure_cio(sy, jep):
            identifier = str(sy['deuh']) + jep
            self.insert_ignore('tcenghyonhtsen_cio', identifier=identifier, kyenh=sy['deuh'], jep=int(jep))
            return identifier

        for line, _ in self.rows('ytenx/sync/tcenghyonhtsen/Dzih.txt'):
            sy = sieux[line[2]]
            kwangx = int(line[5]) if len(line) > 5 and line[5] else None
            self.insert('tcenghyonhtsen_dzih', ziox=int(line[0]), dzih=line[1], sieux_id=sy['ziox'], ngieh=line[4], kwangx_id=kwangx, cioTriungZiox=cio_dzih_ziox)
            cio_dzih_ziox += 1
            for jep in line[3].split('/'):
                cid = ensure_cio(sy, jep)
                self.m2m_ignore('tcenghyonhtsen_dzih_cio', dzih_id=int(line[0]), cio_id=cid)
                sieux_cio.setdefault(sy['ziox'], {})[cid] = cid

        for table, m2m_table, key, filename in (
            ('tcenghyonhtsen_koxqim', 'tcenghyonhtsen_koxqim_cio', 'koxqim_id', 'KoxQim.txt'),
            ('tcenghyonhtsen_jitdzih', 'tcenghyonhtsen_jitdzih_cio', 'jitdzih_id', 'JitDzih.txt'),
        ):
            for line, _ in self.rows('ytenx/sync/tcenghyonhtsen/' + filename):
                sy = sieux[line[2]]
                if table.endswith('jitdzih'):
                    kwangx = int(line[5]) if len(line) > 5 and line[5] else None
                    self.insert(table, ziox=int(line[0]), dzih=line[1], sieux_id=sy['ziox'], ngieh=line[4], kwangx_id=kwangx)
                else:
                    self.insert(table, ziox=int(line[0]), dzih=line[1], sieux_id=sy['ziox'])
                for jep in line[3].split('/'):
                    cid = ensure_cio(sy, jep)
                    self.m2m_ignore(m2m_table, **{key: int(line[0]), 'cio_id': cid})
                    sieux_cio.setdefault(sy['ziox'], {})[cid] = cid

        for s, cios in sieux_cio.items():
            for c in cios:
                self.m2m('tcenghyonhtsen_sieuxyonh_cio', sieuxyonh_id=s, cio_id=c)

        for line, _ in self.rows('ytenx/sync/tcenghyonhtsen/GhiunhTranscription.txt', '\t'):
            self.insert('tcenghyonhtsen_ghiunhtranscription', ziox=int(line[0]), ghiunhBox=line[1], shioJiekHiunh=line[2], shioIpa=line[3], njipJiekHiunh=line[4], njipIpa=line[5])
        for line, _ in self.rows('ytenx/sync/tcenghyonhtsen/ShiengTranscription.txt', '\t'):
            self.insert('tcenghyonhtsen_shiengtranscription', ziox=int(line[0]), shiengLwih=line[1], jiekHiunh=line[2], ipa=line[3], memo=line[4])
        for line, _ in self.rows('ytenx/sync/tcenghyonhtsen/DewhTranscription.txt', '\t'):
            self.insert('tcenghyonhtsen_dewhtranscription', ziox=int(line[0]), dewhLwih=line[1], jiekHiunh=line[2], ipa=line[3], memo=line[4])


if __name__ == '__main__':
    main()
