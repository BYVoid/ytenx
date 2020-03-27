# 韻典網

韻典網是一個綜合的韻書查詢工具，包含《廣韻》、《中原音韻》、《洪武正韻牋》、《分韻撮要》和《上古音系》。該網站發軔於「廣韻查詢系統」，收集了互聯網上以及出版物中許多資源，加以整理後向公衆開放。正如韻典網其名，它的目的是建立一個集合了的中國古代各大韻書的查詢工具，爲音韻、方言、古詩詞專業人士和愛好者提供服務。

更多介紹見 http://ytenx.org/about

## Set environment

    sudo pip install virtualenv
    virtualenv ENV
    source ENV/bin/activate
    pip install -r requirements.txt

## Create database

    ./manage.py migrate --run-syncdb
    ./manage.py shell < ytenx/sync/import.py

## Run

    ./manage.py runserver
