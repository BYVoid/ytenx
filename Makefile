PYTHON=python
MANAGE=${PYTHON} manage.py

run:
	${MANAGE} runserver 127.0.0.1:8000

backup:
	mkdir -p bak
	cp -f ytenx/ytenx.sqlite bak/ytenx-bak.`date +"%Y-%m-%d-%H-%M-%S"`.sqlite

sync: backup
	${MANAGE} syncdb

shell:
	${MANAGE} shell

import: backup
	${MANAGE} shell < ytenx/sync/import.py
