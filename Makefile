PYTHON=python
MANAGE=${PYTHON} manage.py

run:
	${MANAGE} runserver 127.0.0.1:8000

backup:
	mkdir -p bak
	test ! -f ytenx/ytenx.sqlite || cp -f ytenx/ytenx.sqlite bak/ytenx-bak.`date +"%Y-%m-%d-%H-%M-%S"`.sqlite

sync: backup
	${PYTHON} scripts/build_sqlite.py --target ytenx/ytenx.sqlite --reset

rebuild-source-db: backup
	${MANAGE} rebuild_db --reset

golden-smoke:
	${PYTHON} scripts/golden_db_smoke.py

shell:
	${MANAGE} shell

import: backup
	${PYTHON} scripts/build_sqlite.py --target ytenx/ytenx.sqlite --reset
